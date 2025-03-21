# -*- coding: utf-8 -*-
"""Hiveコンポーネントベースモジュール

このモジュールはSpeeDBeeSynapseのコンポーネントをPythonで実装する場合にインポートするモジュールです。

"""

from __future__ import annotations
from contextlib import contextmanager, closing
from enum import IntEnum
import io
import json
import os
import pathlib
import threading
import time
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Iterator

_DELTA_BASE_TIME = 50000000


class HiveApiError(Exception):
    def __init__(self, code:int, system_errno:int=0, db_errno:int=0, message:str="", *args):
        super().__init__(code, system_errno, db_errno, message, *args)
        self.code = code
        self.system_errno = system_errno
        self.db_errno = db_errno
        self.message = message
    def __str__(self):
        className = self.__class__.__name__
        c = self.code
        args_str = ",".join([str(x) for x in self.args[1:]])
        return f"{className}(0x{c:08x},{args_str})"

class HiveComponentBase:
    """コンポーネント用基底クラス

    すべてのコンポーネントはこのクラスを継承して定義する必要があります。

    Attributes:
        in_portX (HiveInPort): 入力ポートX番を表すインスタンス変数。実際にはin_port1, in_port2のように、`X`には数字が入ります。
        out_portX (HiveOutPort): 出力ポートX番を表すインスタンス変数。実際にはout_port1, out_port2のように、`X`には数字が入ります。

    """

    def __new__(cls, api=None):
        instance = super().__new__(cls)
        if not api:
            api = _DummyApi()
        instance.__api = api
        instance.__cv = threading.Condition()
        instance.log = HiveLog(instance.__api)
        for i in range(cls._hive_outports+1):
            setattr(instance, f'out_port{i}', HiveOutPort(instance.__api, i))
        for i in range(cls._hive_inports+1):
            setattr(instance, f'in_port{i}', HiveInPort(instance.__api, i))
        return instance
    @property
    def instance_id(self):
        return self.__api.get_instance_id()
    def set_runnable(self, r):
        if callable(self.__api.set_runnable):
            self.__api.set_runnable(r)
    def premain(self, param: str | dict) -> typing.Optional[ErrorInfoBase]:
        """コンポーネントメイン処理直前に呼ばれる関数

        コンポーネントの開始時、メイン処理の直前に呼ばれます。
        ここでパラメータを読み取ってカラムの作成や独自の初期化処理等を行うことが可能です。

        ただし、この関数における処理は全コンポーネント内で排他制御が掛けられますので長時間処理に時間がかかると、その間、他のコンポーネントのpremainが動作できないことに留意してください。その代わり、ここでカラムを作成する場合はメイン処理で作成する場合に比べて高速に動作します。

        正常に初期化処理等が終了した場合は、何も返さず本メソッドを終了してください。その後`main`メソッドがコールされます。

        何らかの理由により、コンポーネントの実行を継続できない場合は、ErrorInfoBaseを継承したクラスのインスタンスを返却してください。それにより画面上にもエラーの内容が表示され、コンポーネントは停止します。（`main`,`postmain`メソッドは呼ばれません）

        このメソッドの定義は必須ではありません。

        Args:
            param (str | dict): コンポーネントへのパラメータ

        Returns:
            None: 正常に終了した
            ErrorInfoBase: なんらかの理由でコンポーネントを開始できない場合、ErrorInfoBaseを継承したエラーオブジェクトを返す

        """
        pass
    def main(self, param: str | dict):
        """コンポーネントメイン処理関数

        コンポーネントのメイン処理を実装するためのメソッドです。
        HiveComponentBaseを継承したクラスではこのメソッドを必ずオーバーライドして、実装してください。

        この関数の終了は、コンポーネントの処理が完了したことを意味します。正常に終了する際は何も返す必要はありません。
        エラーにより終了する場合は、ErrorInfoBaseを継承したクラスのインスタンスを返してください。返されたインスタンスの情報は画面上に停止理由として表示されます。

        このメソッドの外に例外が送出された場合、不明なエラーとしてコンポーネントは停止します。その挙動が望ましくない場合は、例外をキャッチして処理を継続するか、ErrorInfoBaseを継承したクラスのインスタンスを返して本メソッドを終了してください。

        Args:
            param (str | dict): コンポーネントへのパラメータ

        Returns:
            None: 正常に終了した
            ErrorInfoBase: なんらかの理由でコンポーネントを開始できない場合、ErrorInfoBaseを継承したエラーオブジェクトを返す

        """
        raise Exception("`main` method not defined")
    def postmain(self, param: str | dict):
        """コンポーネントメイン処理直後に呼ばれる関数

        コンポーネントの停止時など、メイン処理関数が終了した直後に呼ばれます。<br>
        メイン処理がエラー等で終了した場合も必ず呼ばれるため、使用したリソースの解放等を行うことを想定しています。<br>
        このメソッドの定義は必須ではありません。

        Args:
            param (str | dict): コンポーネントへのパラメータ

        """
        pass
    def is_runnable(self):
        """コンポーネントの実行継続可否判定

        このコンポーネントのメイン処理を継続してよいかを判定します。
        コンポーネントは定期的（少なくとも5秒以内）にこの関数をコールし、メインの処理を継続してよいか確認する必要があります。
        この関数がTrueを返すときはそのままメイン処理を継続することができますが、
        Falseを返すときは、速やかにメイン処理を終了する必要があります。

        Returns:
            Trueなら継続可能、Flaseならコンポーネントの停止要求が出ている

        """
        return self.__api.is_runnable()
    def get_timestamp(self) -> int:
        """現在時刻の取得

        ナノ秒単位のUNIXタイムで表現された現在時刻を取得します。

        Returns:
            現在時刻のタイムスタンプ。

        """
        return self.__api.get_timestamp()
    def notify_stop(self):
        """コンポーネントの停止要求通知

        このコンポーネントがシステムから停止要求を受けた場合にコールされます。<br>
        HiveComponentBaseを継承したクラスでは必要に応じてこのメソッドをオーバーライドしてください。<br>
        メソッドがコールされた場合には、速やかにコンポーネントのメイン処理を停止させる必要があります。

        メイン処理内で`is_runnable()`を定期的にコールして継続可否をチェックするのであれば、この関数を実装する必要はありません。

        """
        pass
    def register_status(self, status:RunningStatus):
        """ステータス情報の登録

        エラー情報が追加されたステータスを登録します

        Args:
            status: エラー情報が登録されたステータスオブジェクト
        """
        statusInt = self.__api.status_alloc()
        for error in status.errors:
            self.__api.status_add_error(statusInt, error)
        self.__api.status_add_emission_received(statusInt,
            status.total_emission_count,
            status.total_emission_bytes,
            status.total_received_count,
            status.total_received_bytes)

        self.__api.status_register(statusInt)
        self.__api.status_free(statusInt)
    def _get_error_index(self, error: ErrorInfoBase) -> int:
        error_id = error.get_error_id()
        index = self._hive_error_id_map.get(error_id, -1)
        if len(self._hive_error_types) <= index:
            return -1
        return index
    def Status(self):  # noqa: N802
        """ステータス情報の生成

        エラー情報を登録するためのステータスオブジェクトを生成します。
        """
        return RunningStatus()

    def interval_iteration(self, interval, base_time=0):
        """定期処理用イテレータ

        コンポーネントにて一定時間間隔で何らかの処理をするためのイテレータです。<br>
        指定された基準時刻より、指定した定期処理間隔でイテレータから値がyieldされます。ただし実際に処理が開始されるタイミングは厳密に予定時刻と一致するわけではなく、OSやデバイスの負荷やクロック精度に影響されます。

        また、ユーザーが実装する定期的な処理の実行に、定期処理間隔より長い時間を要した場合、次の定期処理がスキップされることがあります。この場合、スキップされた定期処理の回数がyieldの第二要素として受け取れます。

        本関数はコンポーネントの停止要求を受けた場合にはイテレーションを終了します。

        Args:
            interval: 定期処理間隔（単位：ナノ秒）
            base_time: イテレーション開始基準時刻を表すUNIXタイム（単位：ナノ秒）

        Yields:
            [0]: その時のイテレーションが実行される予定だった時刻を表すUNIXタイム（単位：ナノ秒）
            [1]: 直前のイテレーションのスキップ数

        Examples:
            以下のようにfor文でイテレータとして使用できます。
            ```python
            for [ts, skip] in self.interval_iteration(1000000000):
                #
                # 定期的に実行したい処理
                #
            ```
            この場合は1秒間隔で「定期的に実行したい処理」の部分が実行されます。
        """
        now = self.__api.get_timestamp()
        if now < base_time - _DELTA_BASE_TIME:
            # 基準時刻に達してない場合はその時刻まで待ち
            if not self.__sleep_until(base_time - _DELTA_BASE_TIME):
                return
        else:
            elapsed_time = now - base_time + _DELTA_BASE_TIME
            base_time += ((elapsed_time//interval)+1) * interval
            # 基準時刻をintervalの倍数で最も近い時刻に補正

        prev_counter = 0
        counter = 1
        while self.__api.is_runnable():
            # 次のyieldタイミングを算出
            next_time = base_time + (counter-1)*interval

            if next_time + interval < self.__api.get_timestamp():
                # その次のタイミングも過ぎているなら今回はスキップ
                counter += 1
                continue

            if not self.__sleep_until(next_time):
                return

            yield [next_time, counter - prev_counter - 1]
            prev_counter = counter
            counter += 1

    def __sleep_until(self, until):
        sleep_time = until - self.__api.get_timestamp()
        if 0 < sleep_time:
            with self.__cv:
                return not self.__cv.wait(sleep_time / 1000000000)
        return True
    def _hive_notify_stop(self):
        if callable(self.notify_stop):
            self.notify_stop()
        with self.__cv:
            self.__cv.notify_all()
    def save_running_info(self, key:str, data:bytes):
        """任意の情報を保存する

        任意のバイト列をシステムに記録します。<br>
        保存されたデータは、同一のコンポーネントであればシステムの再起動後もload_running_info()で参照する事ができます。また、指定されたkeyにより異なるデータとして保存されるため、複数保存したい場合はそれぞれkeyを分けてください。

        Args:
            key (str): 保存する情報を識別するためのキー
            data (bytes): bytes型の保存したい情報

        Raises:
            HiveApiError: Hiveフレームワークの各種エラー
        """
        self.__api.save_running_info(key, data)
    def load_running_info(self, key:str) -> typing.Optional[bytes]:
        """任意の情報を読み込む

        Args:
            key (str): 読み込みたい情報を識別するためのキー

        Raises:
            HiveApiError: Hiveフレームワークの各種エラー

        Returns:
            data: byte型の読み込んだデータ
            None: データがない
        """
        return self.__api.load_running_info(key)

class DataType(IntEnum):
    """データ型定義Enumクラス

    データ型を示すEnumクラスです。カラム作成時に指定するDataTypeとして、このアトリビュートを使用してください。

    Attributes:
        NONE(0): どの型にも一致しない未定義の型
        BOOLEAN(1): 真偽値型
        INT8(2): 8bit符号あり整数型
        INT16(3): 16bit符号あり整数型
        INT32(4): 32bit符号あり整数型
        INT64(5): 64bit符号あり整数型
        UINT8(6): 8bit符号なし整数型
        UINT16(7): 16bit符号なし整数型
        UINT32(8): 32bit符号なし整数型
        UINT64(9): 64bit符号なし整数型
        FLOAT(10): 32bit浮動小数点型
        DOUBLE(11): 64bit浮動小数点型
        TIMESTAMP(12): タイムスタンプ型
        STRING(13): 文字列
        BINARY(14): バイナリ
        COMPLEXDOUBLE(15): 複素数
        FILE(16): ファイル
        JSON(17): JSON
        BSON(18): BSON
        MESSAGEPACK(19): MessagePack
        COMPONENTSTATUS(20): コンポーネントステータス

    """
    NONE            = 0
    BOOLEAN         = 1
    INT8            = 2
    INT16           = 3
    INT32           = 4
    INT64           = 5
    UINT8           = 6
    UINT16          = 7
    UINT32          = 8
    UINT64          = 9
    FLOAT           = 10
    DOUBLE          = 11
    TIMESTAMP       = 12
    STRING          = 13
    BINARY          = 14
    COMPLEXDOUBLE   = 15
    FILE            = 16
    JSON            = 17
    BSON            = 18
    MESSAGEPACK     = 19
    COMPONENTSTATUS = 20
    BOOL            = 1
    I8              = 2
    I16             = 3
    I32             = 4
    I64             = 5
    U8              = 6
    U16             = 7
    U32             = 8
    U64             = 9
    FLT             = 10
    DBL             = 11

    @staticmethod
    def from_string(type_str:str):
        upper = type_str.upper()
        return getattr(DataType, upper, DataType.NONE)


class ColumnType(IntEnum):
    LOW            = 0
    MIDDLE         = 1
    HIGH            = 2

class ColumnOption:
    """カラムオプション

    出力ポートのカラムに対するオプション設定

    Attributes:
        column_type (ColumnType): カラムタイプ(LOW、MIDDLE、HIGH)
        samplingrate (float): サンプリングレート
        compression_unit (int): 圧縮単位
        fixedsize_binary (int): カラムデータサイズ
        max_binarysize (int): LO可変長タイプのデータ最大長

    """

    def __init__(self, column_type:ColumnType=ColumnType.LOW, samplingrate:float=0, compression_unit:int=0, fixedsize_binary:int=0, max_binarysize:int=0):
        self.column_type = column_type.value
        self.samplingrate = samplingrate
        self.compression_unit = compression_unit
        self.fixedsize_binary = fixedsize_binary
        self.max_binarysize = max_binarysize

class _DummyApi:
    def __init__(self):
        self.runnable = False
    def set_runnable(self, r):
        self.runnable = r
    def is_runnable(self):
        return self.runnable
    def get_timestamp(self):
        return time.time_ns()
    def create_column(self, port:int, name:str, data_type:int, data_array:int, opt):
        #self.__api.create_column(port_no, name, data_type.value, data_array, opt)
        return {}
    def insert_single_value(self, column, value, ts:int):
        #self.__api.insert_single_value(self.__port_no, self.name, value, ts)
        print(f'DATA INSERT: {value}')  # noqa: T201
    def make_temp_file_name(self):
        return 'tempfile'
    def register_file(self, port:int, name:str, filepath:str, ts:int):
        pass
    def get_inport_columns(self, port:int):
        return []
    def get_inport_columns_updated_at(self, port:int):
        return time.time_ns()
    def get_current_log_level(self):
        return HiveLogLevel.TRACE
    def put_log(self, lv:HiveLogLevel, msg:str):
        print('LOG:', msg)  # noqa: T201
    def save_running_info(self, key:str, data:bytes):
        pass
    def load_running_info(self, key:str) -> typing.Optional[bytes]:
        return None

class FileTypeMetaInfo(typing.TypedDict, total=False):
    """ファイル型データメタ情報

    ファイル型カラムに登録するファイルのメタ情報をもつクラスです。
    いずれのメンバも省略可能です。

    Attributes:
        media_type (ColumnType): メディアタイプ(application/jsonやtext/csvなどを設定できる)
        filename (float): ファイル名のヒント（ファイルエミッタに繋いだ場合にこのファイル名が使われる）
        begin_timestamp (int): このファイルに収められたデータの時間範囲の先頭時刻（UNIXタイム、単位：ナノ秒）
        end_timestamp (int): このファイルに収められたデータの時間範囲の末尾時刻（UNIXタイム、単位：ナノ秒）

    """

    media_type: str
    filename: str
    begin_timestamp: int
    end_timestamp: int

class OutColumn:
    """出力ポートのカラム

    出力ポートのカラムに対するデータの登録等はこのクラスのインスタンスを介して行います

    Attributes:
        name (str): 作成時に指定したカラム名
        data_type (DataType): 作成時に指定したカラムのデータ型
        data_array (int): 作成時に指定したカラムの要素数
            スカラ型の場合は0となります
        options (ColumnOption): 作成時に指定したカラムのオプション

    """

    def __init__(self, api, port_no:int, name:str, data_type:DataType, data_array:int, opt:typing.Optional[ColumnOption]):
        self.__api = api
        self.__port_no = port_no
        self.name = name
        self.data_type = data_type
        self.data_array = data_array
        self.options = opt
        self.column = self.__api.create_column(port_no, name, data_type.value, data_array, opt)
    def insert(self, *args) -> None:
        """カラムへの値登録

        このカラムに指定したタイムスタンプ`ts`の値を登録します。<br>
        タイムスタンプを省略した場合は現在時刻として扱われます。<br>
        dataには、このカラム作成時のデータ型と一致するデータを渡してください。異なるデータを渡した場合、暗黙に変換可能なものは変換されますが、そうでない場合はエラーとなります。

        Args:
            data: 登録する値
            ts: この値を登録するタイムスタンプ

        Raises:
            TypeError: このカラムのデータ型に一致しない、不正なデータが渡された
            InvalidTimestamp: タイムスタンプが現在時刻と著しく離れている、もしくは前に登録したタイムスタンプより過去になっている

        """
        self.insert_single_value(*args)
    def insert_single_value(self, value:typing.Any, ts:int=0) -> None:
        self.__api.insert_single_value(self.column, value, ts)
    def insert_multiple_values(self, values:[typing.Any], ts:int=0) -> None:
        self.__api.insert_multiple_values(self.column, values, ts)
    @contextmanager
    def open_file(self):
        """新規ファイルの作成

        ファイル型として作成されたカラムに登録する新規のファイルをオープンし、そのファイルオブジェクトを返します。

        Returns:
            FileObject: オープンされたファイルオブジェクト

        Raises:
            TypeError: FILE型でないカラムに対してこのメソッドが呼ばれた
            HiveApiError: Hiveフレームワークの各種エラー
            OSError: ファイルオープンに関連する各種エラー

        Examples:
            以下のようにwith句で使用できます。
            ```python
            file_column = self.out_port1.Column("clmfile", DataType.FILE)
            with file_column.open_file() as fo:
                fo.write("filedata - line 1\\n".encode('utf-8))
                fo.write("filedata - line 2\\n".encode('utf-8))
                fo.write("filedata - line 3\\n".encode('utf-8))

                file_column.insert_file(fo, ts)
            ```
        """
        if self.data_type != DataType.FILE:
            raise TypeError(f"column {self.name} is not DataType.FILE")

        filepath = self.__api.make_temp_file_name()
        fo = open(filepath, mode='wb')
        fo._filepath = filepath
        try:
            yield fo
        finally:
            fo.close()
    def insert_file(self, fo:typing.IO[typing.AnyStr], ts:int=0, meta:typing.Optional[FileTypeMetaInfo]=None) -> None:
        """ファイルのDB登録

        ファイルをファイル型のカラムへ登録します。

        Args:
            file: オープンされたファイルオブジェクト
            ts: この値を登録するタイムスタンプ
            meta: 登録するファイルのメタ情報

        Raises:
            ValueError: 登録しようとしたファイルがすでにクローズされている
            HiveApiError: Hiveフレームワークの各種エラー
            OSError: ファイル操作に関連する各種エラー

        """
        if fo.closed:
            raise ValueError("invalid operation closed file inserted")

        fo.seek(0, io.SEEK_END)
        filesize = fo.tell()
        fo.close()

        if meta is None:
            meta = {}

        media_type = meta.get('media_type', '')
        filename = meta.get('filename', '')
        begin = meta.get('begin_timestamp', 0)
        end = meta.get('end_timestamp', 0)

        new_filepath = self.__api.register_file(self.__port_no, self.name, fo._filepath, False, ts)
        self.__api.insert_file(
                self.column,
                new_filepath,
                filesize,
                media_type,
                filename,
                begin,
                end,
                ts)

    def insert_file_move(self, pathlike, ts:int=0, meta:typing.Optional[FileTypeMetaInfo]=None) -> None:
        """既存ファイルのDB登録（移動）

        すでに作成済みのファイルをファイル型のカラムへ登録します。
        指定されたファイルは、DBの管理ディレクトリに移動されます。引数で指定したパスにはファイルが残らないことに注意してください。
        ディレクトリは登録できません。

        Args:
            pathlike: 登録対象のファイルのパスを表すpath-likeオブジェクト
            ts: この値を登録するタイムスタンプ
            meta: 登録するファイルのメタ情報

        Raises:
            ValueError: 指定したパス
            HiveApiError: Hiveフレームワークの各種エラー
            OSError: ファイル操作に関連する各種エラー
        """
        file = pathlib.Path(pathlike)
        filesize = file.stat().st_size

        if meta is None:
            meta = {}

        media_type = meta.get('media_type', '')
        filename = meta.get('filename', '')
        begin = meta.get('begin_timestamp', 0)
        end = meta.get('end_timestamp', 0)

        new_filepath = self.__api.register_file(self.__port_no, self.name, str(file), False, ts)
        self.__api.insert_file(
                self.column,
                new_filepath,
                filesize,
                media_type,
                filename,
                begin,
                end,
                ts)

    def insert_file_copy(self, pathlike, ts:int=0, meta:typing.Optional[FileTypeMetaInfo]=None) -> None:
        """既存ファイルのDB登録（コピー）

        すでに作成済みのファイルをファイル型のカラムへ登録します。
        指定されたファイルはDBの管理ディレクトリにコピーされ、そのコピー先のファイルがカラムに登録されます。
        以降、引数で指定した元ファイルのパスは参照されません。
        ディレクトリは登録できません。

        Args:
            pathlike: 登録対象のファイルのパスを表すpath-likeオブジェクト
            ts: この値を登録するタイムスタンプ
            meta: 登録するファイルのメタ情報

        Raises:
            ValueError: 指定したパス
            HiveApiError: Hiveフレームワークの各種エラー
            OSError: ファイル操作に関連する各種エラー
        """
        file = pathlib.Path(pathlike)
        filesize = file.stat().st_size

        if meta is None:
            meta = {}

        media_type = meta.get('media_type', '')
        filename = meta.get('filename', '')
        begin = meta.get('begin_timestamp', 0)
        end = meta.get('end_timestamp', 0)

        new_filepath = self.__api.register_file(self.__port_no, self.name, str(file), True, ts)
        self.__api.insert_file(
                self.column,
                new_filepath,
                filesize,
                media_type,
                filename,
                begin,
                end,
                ts)

    def insert_file_ref(self, pathlike, ts:int=0, meta:typing.Optional[FileTypeMetaInfo]=None) -> None:
        """既存ファイルのDB登録（参照）

        すでに作成済みのファイルをファイル型のカラムへ登録します。
        指定されたファイルは、そのパスのままカラムに登録されます。
        そのためファイルを削除してしまうと、このカラムの情報を他のコンポーネントが参照する際にもファイルを参照できなくなります。
        ディレクトリは登録できません。

        Args:
            pathlike: 登録対象のファイルのパスを表すpath-likeオブジェクト
            ts: この値を登録するタイムスタンプ
            meta: 登録するファイルのメタ情報

        Raises:
            ValueError: 指定したパス
            HiveApiError: Hiveフレームワークの各種エラー
            OSError: ファイル操作に関連する各種エラー
        """
        file = pathlib.Path(pathlike).absolute()
        filesize = file.stat().st_size

        if meta is None:
            meta = {}

        media_type = meta.get('media_type', '')
        filename = meta.get('filename', '')
        begin = meta.get('begin_timestamp', 0)
        end = meta.get('end_timestamp', 0)

        self.__api.insert_file(
                self.column,
                str(file),
                filesize,
                media_type,
                filename,
                begin,
                end,
                ts)

class AggregationType(IntEnum):
    """集約種別定義Enumクラス

    入力ポートから取得するカラムデータの集約種別を表します

    Attributes:
        NONE(0): なし
        OLDER(1): 最古値
        NEWER(2): 最新値
        COUNT(3): 件数
        SUM(4): 総和
        SUMSQ(5): 2乗和
        SUMSQD(6): 偏差平方和
        MIN(7): 最小
        MAX(8): 最大
        RANGE(9): 範囲
        MEAN(10): 算術平均値
        VAR(11): 分散
        STDEV(12): 標準偏差
        UVAR(13): 不偏分散
        USTDEV(14): 標本不偏標準偏差
        STDER(15): 標準誤差
        CV(16): 変動係数
        MEDIAN(17): 中央値
        QUARTMIN(18): 四分位数
        QUART1(19): 四分位数
        QUART2(20): 四分位数
        QUART3(21): 四分位数
        QUARTMAX(22): 四分位数
        MODE(23): 最頻値
        MODECOUNT(24): 最頻値個数
        MDEV(25): 平均偏差
        HMEAN(26): 調和平均
        GMEAN(27): 幾何平均
        KURT(28): 尖度
        SKEW(29): 歪度

    """
    NONE         = 0
    OLDER        = 1
    NEWER        = 2
    COUNT        = 3
    SUM          = 4
    SUMSQ        = 5
    SUMSQD       = 6
    MIN          = 7
    MAX          = 8
    RANGE        = 9
    MEAN         = 10
    VAR          = 11
    STDEV        = 12
    UVAR         = 13
    USTDEV       = 14
    STDER        = 15
    CV           = 16
    MEDIAN       = 17
    QUARTMIN     = 18
    QUART1       = 19
    QUART2       = 20
    QUART3       = 21
    QUARTMAX     = 22
    MODE         = 23
    MODECOUNT    = 24
    MDEV         = 25
    HMEAN        = 26
    GMEAN        = 27
    KURT         = 28
    SKEW         = 29
    END          = 30

class AggregationTypeSet():
    """入力ポートのカラムからデータ取得する際に有効になっている統計情報を示すフラグのセット。

    `AggregationType`の属性を`test()`メソッドに渡すことでこの統計情報が有効になっているかを確認できます。
    また、イテレーターを使って有効になっている統計情報のリストを取得することも可能です。

    Examples:
        `AggregationType`の属性を`test()`メソッドに渡すことでこの統計情報が有効になっているかを確認できます。
        ```python
        if a_type_set.test(AggregationType.MAX):
          pring(max: ON")
        else:
          pring(max: OFF")
        ```

        また、イテレーターを使って有効になっている統計情報のリストを取得することも可能です。
        ```python
        for a_type in aggregation_type_set:
            print(a_type.name)
        ```
    """
    def __init__(self, bitset):
        self.bitset = bitset
    def test(self, type:AggregationType) -> bool:
        b = 1 << (type.value - 1)
        return (self.bitset & b) != 0
    def set(self, type:AggregationType):
        b = 1 << (type.value - 1)
        self.bitset = self.bitset | b
    def unset(self, type:AggregationType):
        b = ~(1 << (type.value - 1))
        self.bitset = self.bitset & b
    def __iter__(self):
        for i in range(AggregationType.END-1):
            flag = (1 << i)
            if self.bitset & flag != 0:
                yield AggregationType(i+1)


class InColumn:
    """入力ポートのカラム

    このクラスからは情報を取得するのみです。カラムに対してデータを登録するなどの操作はできません。

    Attributes:
        source_name (str): カラムを生成したコンポーネントの名前
        data_name (str): カラムの名前
        data_type (DataType): カラムの型情報
        array_size (int): カラムの配列要素数（スカラの場合は0）
        raw_data (bool): カラムからのデータ取得時に未加工のデータが含まれるか否かを示す真偽値
        stat_type_set (AggregationTypeSet): カラムからのデータ取得時に有効となっている統計情報を示すフラグセット
        output_name (str): カラムの出力名。指定がない場合はNone
    """

    def __init__(self,
                 api,
                 column,
                 source_name:str,
                 data_name:str,
                 data_type:int,
                 array_size:int,
                 raw_data:bool,
                 stat_type_set:int,
                 output_name:typing.Optional[str]=None,
                 capsule=None):
        self.__api = api
        self.__column = column
        self.__source_name = source_name
        self.__data_name = data_name
        self.__data_type = DataType(data_type)
        self.__array_size = array_size
        self.__raw_data = raw_data
        self.__stat_type_set = AggregationTypeSet(stat_type_set)
        self.__output_name = output_name
        self._capsule = capsule

    @property
    def source_name(self) -> str:
        return self.__source_name
    @property
    def data_name(self) -> str:
        return self.__data_name
    @property
    def data_type(self) -> DataType:
        return self.__data_type
    @property
    def array_size(self) -> int:
        return self.__array_size
    @property
    def raw_data(self) -> bool:
        return self.__raw_data
    @property
    def stat_type_set(self) -> AggregationTypeSet:
        return self.__stat_type_set
    @property
    def output_name(self) -> str:
        return self.__output_name

    def get_latest_value(self, use_storage:bool = False) -> (int,typing.Any):
        """カラムの最新値取得

        カラムに登録されている最新のデータを読み込み、そのタイムスタンプと値のタプルを返します。

        Args:
            use_storage (bool): ※現時点では未サポート<br>
                ストレージに永続化されたデータからの読み込みを行う場合にTrueを指定してください。<br>
                Falseの場合、メモリ上からのみ読み込みを行うため、永続化されたデータが有ってもデータなしを返す可能性があります。<br>
                Trueの場合でも、メモリ上に最新データがあればストレージのアクセスは行いません。<br>

        Returns:
            * `(0, None)`: カラムから読み込める値がない場合
            * `(>0, !=None)`: 読み込まれたタイムスタンプと値

        Raises:
            HiveApiError: Hiveフレームワークの各種エラー
        """
        return self.__api.get_latest_value(self.__column)

    def __str__(self):
        if self.__array_size > 0:
            type = f"({self.__data_type.name}[{self.__array_size}])"
        else:
            type = f"({self.__data_type.name})"

        name = f"{self.__source_name}:{self.__data_name}"
        if self.__output_name:
            name = f"{self.__source_name}:{self.__data_name}:{self.__output_name}"
        else:
            name = f"{self.__source_name}:{self.__data_name}"

        return f"{name} {type}"

class InPortReader:
    """入力ポートリーダー

    入力ポートのカラムから、データを読み込むクラスです。<br>
    このクラスは直接インスタンス化せず、`self.in_portX.ContinuousReader()`、もしくは、`self.in_portX.TimeRangeReader()`関数を使用してください。
    """

    def __init__(self, api, port_no, retry_once:bool, begin:int, end:int=0, column:typing.Optional[InColumn]=None):
        self.__api = api
        self.__port_no = port_no
        self.__retry_once = retry_once
        self.__begin = begin
        self.__end = end
        self.__target_column = column
        self.__reader = None
    def __del__(self):
        self.close();
    def __enter__(self):
        self.open()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    def __iter__(self) -> Iterator[typing.Optional[HiveWindowData]]:
        if self.__end == 0:
            raise RuntimeError("ContinuationReader could not iterate reading")
        while data := self.read():
            yield data

    def open(self):
        if not self.__reader:
            self.__reader = self.__api.open_in_port_reader(self.__port_no, self.__begin)
    def close(self):
        if self.__reader:
            self.__api.close_in_port_reader(self.__reader)
            self.__reader = None

    def read(self) -> typing.Optional[HiveWindowData]:
        """カラムデータ読み込み

        入力ポートからカラムデータを読み込みます。

        Returns:
            HiveWindowData: 読み込んだウィンドウデータを返します。
            None: 現時点で読み込みできない場合はNoneが返されます。

        Raises:
            HiveApiError: Hiveフレームワークの各種エラー

        """
        window_data = self.__api.read_from_in_port_reader(self.__reader, self.__end)
        if window_data:
            return window_data
        if not self.__retry_once:
            return None

        time.sleep(0.5)
        window_data = self.__api.read_from_in_port_reader(self.__reader, self.__end)
        return window_data

class HiveOutPort:
    """出力ポートを表すクラス

    出力ポートに対するカラムの作成等はこのクラスのインスタンスを介して行います。<br>
    このクラスのインスタンスを直接生成することはできません。コンポーネントの開始時に、アトリビュート`self.out_port1`のように最初からアクセスできますのでこれを使ってください。
    """
    def __init__(self, api, no):
        self.__api = api
        self.__no = no

    def Column(self, name:str, data_type:DataType, data_array:int=0, opt:typing.Optional[ColumnOption]=None) -> OutColumn:  # noqa: N802
        """カラム生成

        この出力ポート内に、指定された名称のカラムを生成します。

        Args:
            name: 作成するカラム名
            data_type: 作成するカラムのデータ型
            data_array: 作成するカラムの要素数(スカラ型の場合は0を指定)
            opt: カラムオプション

        Returns:
            OutColumn

        Raises:
            HiveApiError: Hiveフレームワークの各種エラー

        """
        return OutColumn(self.__api, self.__no, name, data_type, data_array, opt)

    def register_confirmed_time(self, ts:int=0) -> None:
        """出力ポートへの確定時刻登録

        この出力ポートのカラムへのデータ登録が、指定した時刻`ts`までは確定したことを通知します。この登録により、指定した時刻`ts`より前の時刻のデータは読み込むことができることを、フローリンクを通して繋がっている別のコンポーネントが知ることができます。

        ※このAPIの呼び出しは必須ではありません。

        Args:
            ts: 出力ポートのカラムへのデータ登録が確定している時刻
                省略した場合は現在時刻になります
        """
        self.__api.register_confirmed_time(self.__no, ts)


class HiveInPort:
    """入力ポートを表すクラス

    入力ポートからデータを取得するような処理はこのクラスのインスタンスを介して行います

    """

    def __init__(self, api, no):
        self.__api = api
        self.__no = no

    def get_columns(self) -> list[InColumn]:
        """カラムリストの取得

        この入力ポートに接続されている全カラムの情報を取得します

        Returns:
            list[InColumn]
        """
        return self.__api.get_inport_columns(self.__no)

    @property
    def columns_updated_at(self) -> int:
        return self.__api.get_inport_columns_updated_at(self.__no)

    def ContinuousReader(self, start:int) -> InPortReader:  # noqa: N802
        """継続カラムリーダーの生成

        この入力ポートに接続されているカラムから、継続的にデータを読み込むContinuousReaderを生成します

        Args:
            start: 入力ポートからの読み込みを開始する時刻（UNIXタイム、単位：ナノ秒）

        Returns:
            ContinuousReader

        Examples:
            以下のようにwith句でreaderを取得して使用できます。
            ```python
            with self.in_port1.ContinuousReader(start=self.get_timestamp()) as reader:
                while self.is_runnable():
                    window_data = reader.read()
                    if not window_data:
                        continue
                        :
            ```

        """
        return InPortReader(self.__api, self.__no, True, start)

    def TimeRangeReader(self, start:int, end:int) -> InPortReader:  # noqa: N802
        """時間範囲データリーダーの生成

        指定したカラム、もしくは入力ポートに接続されている全カラムから、指定した時間範囲のデータを読み込むTimeRangeReaderを生成します

        Args:
            start: 入力ポートからの読み込みを開始する時刻（UNIXタイム、単位：ナノ秒）
            end: 入力ポートからの読み込みを終了する時刻（UNIXタイム、単位：ナノ秒）
            column: データを取得するカラム(指定がない場合には入力ポートの全カラム)

        Returns:
            data

        Examples:
            以下のようにwith句でreaderを取得して使用できます。
            ```python
            with self.in_port1.ContinuousReader(start=self.get_timestamp()) as reader:
                for window_data in reader:
                    :
            ```


        """
        return InPortReader(self.__api, self.__no, False, start, end)

class RunningStatus:
    def __init__(self):
        self.errors :list[ErrorInfoBase] = []
        self.total_emission_count :typing.Optional[int] = None
        self.total_emission_bytes :typing.Optional[int] = None
        self.total_received_count :typing.Optional[int] = None
        self.total_received_bytes :typing.Optional[int] = None
    def add_error(self, err:ErrorInfoBase):
        """エラー情報登録

        ステータスオブジェクトにエラー情報を登録します。
        このオブジェクトに登録しただけでは保存されません。最終的にはHiveComponentBase.register_statusを呼び出してシステムに登録してください。

        Args:
            err: エラー情報
        """
        self.errors.append(err)

def ErrorType(error_id:str, *param_names:str):  # noqa: N802
    """エラー情報クラス生成

    エラー情報を管理するクラスを生成します。
    実際のエラー情報は、この関数で生成したクラスからインスタンスを生成してください。

    Args:
        error_id: エラー情報を識別する文字列
        param_names: エラー情報のパラメータの名称
    """
    class ErrorInfo(ErrorInfoBase):
        @classmethod
        def get_param_names(cls):
            return param_names
        @classmethod
        def get_error_id(cls):
            return error_id
    return ErrorInfo


class ErrorInfoBase(Exception):
    """ステータスに登録するためのエラー情報

    コンポーネントのエラーの種別や詳細を保持するためのクラスです。<br>
    このクラスは、直接インスタンス化したり継承したりせずに、`ErrorType`関数を使って生成したクラスをインスタンス化してください。

    Attributes:
        errorTypeIndex (int): エラーパラメータのタイプ
        params (list[ErrorParam]): エラーパラメータ
    """
    def __init__(self, *params):
        super().__init__(*params)
        self.params = [self.force_parameter_type(x) for x in params]
    @classmethod
    def get_param_names(cls):
        return []
    @classmethod
    def get_error_id(cls):
        return -1
    def force_parameter_type(self, value: typing.Any):
        if isinstance(value, str):
            return value
        elif isinstance(value, int):
            return value
        elif isinstance(value, float):
            return value
        else:
            return str(value)

def HiveComponentInfo(uuid=None, name=None, tag=None, inports=None, outports=None, error_types:typing.Optional[list[ErrorInfoBase]]=None):  # noqa: N802
    if error_types is None:
        error_types = []

    def _(cls):
        cls._hive_uuid = uuid
        cls._hive_name = name
        cls._hive_tag = tag
        cls._hive_inports = inports
        cls._hive_outports = outports
        cls._hive_error_types = error_types
        cls._hive_error_id_map = {}
        for index, error_type in enumerate(error_types):
            cls._hive_error_id_map[error_type.get_error_id()] = index
        cls._hive_methods = []
        for methodname in dir(cls):
            o = getattr(cls, methodname)
            if getattr(o, '_is_hive_component_method', False):
                cls._hive_methods.append(methodname)
        return cls
    return _

class HiveLogLevel(IntEnum):
    """ログレベル型定義Enumクラス

    ログレベルを示すEnumクラスです。

    Attributes:
        ERROR(0): エラーログ
        WARNING(1): 警告ログ
        INFO(2): 通常情報ログ
        DEBUG(3): デバッグ用ログ
        TRACE(4): トレースログ

    """
    ERROR    = 0
    WARNING  = 1
    INFO     = 2
    DEBUG    = 3
    TRACE    = 4

class HiveLog():
    """ログ出力クラス
    """
    def __init__(self, api):
        self.__api = api
    def get_current_level(self):
        """ログレベル取得

        Returns:
          HiveLogLevel 現在のログレベルEnum
        """
        return HiveLogLevel(self.__api.get_current_log_level())
    def put(self, level:HiveLogLevel, *msg):
        message = " ".join([str(x) for x in msg])
        self.__api.put_log(level, message)
    def error(self, *msg):
        """エラーログ出力

        Args:
            msg: ログ出力する文字列
        """
        self.put(HiveLogLevel.ERROR, *msg)
    def warning(self, *msg):
        """警告ログ出力

        Args:
            msg: ログ出力する文字列
        """
        self.put(HiveLogLevel.WARNING, *msg)
    def info(self, *msg):
        """通常情報ログ出力

        Args:
            msg: ログ出力する文字列
        """
        self.put(HiveLogLevel.INFO, *msg)
    def debug(self, *msg):
        """デバッグログ出力

        Args:
            msg: ログ出力する文字列
        """
        self.put(HiveLogLevel.DEBUG, *msg)
    def trace(self, *msg):
        """トレースログ出力

        Args:
            msg: ログ出力する文字列
        """
        self.put(HiveLogLevel.TRACE, *msg)

class HiveFileDataPath(type(pathlib.Path())):
    @property
    def metainfo(self):
        return getattr(self, '_metainfo', None)
    def set_metainfo(self, metainfo):
        self._metainfo = metainfo
    def to_dict(self):
        result = self._metainfo.copy()
        result['filepath'] = str(self)
        return result

class HiveWindowData():
    """ウィンドウデータクラス

    入力ポートからカラムのデータを取得する際に、特定の時間単位でまとめられたデータのかたまりです。
    時間単位がどの程度になるかは入力ポートの設定により異なります。

    Attributes:
        time_range (tuple[int:2]): このウィンドウの時間範囲を表す２要素のタプル。最初の要素が開始時刻、２番目の要素が終了時刻を表す。どちらもナノ秒単位。
        window_id (int): ウィンドウを識別する数値。ウィンドウ毎に異なる値が取得されるが、常に１つずつ増加するとは限らないことに注意。
        event_id (int): イベント範囲を識別する数値。イベント定義されていない場合やイベント範囲外では0に固定。イベント中は1以上の値が入る。
        records (list[HiveRecord]): このウィンドウ内のレコードリスト
        columns (list[InColumn]): 取得した入力ポートに接続されたカラムの一覧。HiveInPort.get_columns()で取得したものと同じ。
        event (HiveInPortEventSetting): 入力ポートに設定されたイベント情報
    """
    def __init__(self, begin:int, end:int, window_id:int, records:list[HiveRecord], columns:list[InColumn], event_id:int=0, event:HiveInPortEventSetting=None):
        self.time_range = (begin, end)
        self.window_id = window_id
        self.records = records
        self.columns = columns
        self.event_id = event_id
        self.event = event

    def to_dict(self):
        d = {
            'time_range': self.time_range,
            'window_id': self.window_id,
            'event_id': self.event_id,
            'records': [ r.to_dict() for r in self.records ],
        }
        return d

class HiveRecordType(IntEnum):
    """レコード種別Enumクラス

    レコード種別を示すEnumクラスです。

    Attributes:
        RAW_DATA(0): 未加工データ
        STATISTICS(1): 集約データ
    """
    RAW_DATA   = 0
    STATISTICS = 1

class HiveRecord():
    """レコードクラス

    入力ポートからカラムのデータを取得する際に、同一時刻のデータをまとめたもの。<br>
    別カラムのデータでも同一時刻のものがあれば全て１つのインスタンスにまとめられます。レコードは２種類、未加工データと集約データがあり、`record_type`で識別できます。

    Attributes:
        record_type (HiveRecordType): このウィンドウ内のレコードリスト
        timestamp (int): このレコードに含まれるデータのタイムスタンプ。UNIXタイム（単位ナノ秒）
        data (list[HiveRecordData]): このレコードのデータのリスト
    """
    def __init__(self, record_type:int, timestamp:int, data:list[HiveRecordData], record_count:int):
        self.record_type = HiveRecordType(record_type)
        self.timestamp = timestamp
        self.data = data
        self.record_count = record_count

    def to_dict(self):
        d = {
            'timestamp': self.timestamp,
            'data': { f'{d.get_column_name()}': d.value for d in self.data },
            'record_type': self.record_type.name
        }
        return d

class HiveRecordData():
    """レコードデータクラス

    １レコード内の各カラムのデータ。

    Attributes:
        value (any): 実データ。数値、文字列、配列など、カラムの型に応じて異なる形式。
        column (InColumn): 対象カラムを示すオブジェクト
        stat_type (AggregationType): このデータの集約種別
    """
    def __init__(self, value:any, column:InColumn, stat_type:int, data_size:int):
        self.value = value
        self.column = column
        self.stat_type = AggregationType(stat_type)
        self.data_size = data_size

    def get_column_name(self):
        if self.stat_type == AggregationType.NONE:
            return f'{self.column.source_name}:{self.column.data_name}'
        else:
            return f'{self.column.source_name}:{self.column.data_name}:{self.stat_type.name}'

    def to_dict(self):
        return {
            'value': self.value,
            'source_name': self.column.source_name,
            'data_name': self.column.data_name,
        }

def hive_component_method(func):
    func._is_hive_component_method = True
    return func
    #def _wrapper(*args):
    #    comp_method_ret = comp_method(*args)

    #    is_json = False
    #    if type(comp_method_ret) is str:
    #        is_json = False
    #        str_ret = comp_method_ret
    #    else:
    #        is_json = True
    #        str_ret = json.dumps(comp_method_ret)
    #    method_ret = (str_ret, is_json)
    #    return method_ret
    #return _wrapper


class HiveCompError():
    """コンポーネントエラー情報クラス

    コンポーネント実行中、もしくは、エラーで停止した場合のエラー情報

    Attributes:
        error_type (str): コンポーネントのエラーの種別を示す文字列
        parameters (list[any]): エラーの付加情報
    """
    def __init__(self, error_type:str, parameters:list[any]):
        self.error_type = error_type
        self.parameters = parameters

class HiveCompStatus():
    """コンポーネントステータスクラス

    コンポーネントのステータスとエラー情報

    Attributes:
        status (str): コンポーネントの実行状態を表す文字列
        errors (list[HiveCompError]): コンポーネント実行中、もしくは、エラーで停止した場合のエラー情報
    """
    def __init__(self, status:str, errors:list[HiveCompError]):
        self.instance_status = status
        self.errors = errors

class HiveInPortEventSetting():
    """入力ポートのイベント設定情報クラス

    入力ポートに設定されたイベント情報を保持するクラス  
    このクラスの属性値を変更しても実際の入力ポート設定には反映されません

    Attributes:
        source_name (str): イベント判定の対象となっているコンポーネント名
        data_name (str): イベント判定の対象となっているカラム名
        pre_time (int): イベント区間前方の拡張時間範囲
        post_time (int): イベント区間後方の拡張時間範囲
    """
    def __init__(self, source_name:str, data_name:str, pre_time:int, post_time:int):
        self.source_name = source_name
        self.data_name = data_name
        self.pre_event_time = pre_time
        self.post_event_time = post_time

    def __str__(self):
        return f"[{self.source_name}:{self.data_name}] pre_event_time:{self.pre_event_time} post_event_time:{self.post_event_time}"

    def to_dict(self):
        return {
            'source_name': self.source_name,
            'data_name': self.data_name,
            'pre_event_time': self.pre_event_time,
            'post_event_time': self.post_event_time,
        }

