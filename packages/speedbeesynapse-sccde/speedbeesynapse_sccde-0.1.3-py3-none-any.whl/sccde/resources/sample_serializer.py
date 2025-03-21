"""
各種プリミティブ型のスカラーカラムを作成し、指定した間隔で登録するコンポーネント
登録する値は0から順次増加。

パラメータ
  {
    "interval_ms": 1000,
    "diff": 1
  }
  interval_ms: 登録間隔（ミリ秒）
  diff: 登録する値の増分

出力ポート
  以下のカラムを作成
    カラム名  データ型   登録値
  ------------------------------------
    bool      BOOLEAN    Xを2で割ったあまりが1ならtrue,0ならfalse
    int8      INT8       X（上下限あり）
    int16     INT16      X（上下限あり）
    int32     INT32      X（上下限あり）
    int64     INT64      X（上下限あり）
    uint8     UINT8      X（上下限あり） Xが負数なら登録除外
    uint16    UINT16     X（上下限あり） Xが負数なら登録除外
    uint32    UINT32     X（上下限あり） Xが負数なら登録除外
    uint64    UINT64     X（上下限あり） Xが負数なら登録除外
    float     FLOAT      X+0.123
    double    DOUBLE     X+0.123
    str       STRING     Xの十進数文字列
    bin       BINARY     Xの十進数文字列のUTF8
"""

from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import time
import json

class Param:
    def __init__(self, interval, diff):
        self.interval = interval
        self.diff = diff

@HiveComponentInfo(uuid='{{REPLACED-UUID}}', name='スカラ型カウントアップ', inports=1, outports=1)
class HiveComponent(HiveComponentBase):
    def main(self, _param):

        self.fileclm = self.out_port1.Column('JSONFILE', DataType.FILE)

        #with self.in_port0.ContinuousReader(start=self.get_timestamp()) as reader:
        with self.in_port1.ContinuousReader(start=self.get_timestamp()) as reader:
            while self.is_runnable():
                window_data = reader.read()
                if not window_data:
                    self.log.info("no data yet")
                    continue

                xml_data = self.make_xml(window_data)
                if xml_data:
                    self.insert_xml(xml_data)

    def insert_xml(self, data):
        with self.file.open_file() as fo:
            ts = self.get_timestamp()
            print('timestamp', ts)
            filename = "a"
            media_type = "text/plain"
            begin_timestamp = 1
            end_timestamp = 2
            meta = {
                'filename': 'a',
                'media_type': 'text/plain',
                'begin_timestamp': 1,
                'end_timestamp': 2,
            }
            self.file.insert_file(fo, ts, meta)

    def process_data(self, window_data):
        data_object = {}

        for record in window_data.records:
            for columnvalue in record.data:
                if not isinstance(columnvalue.value, pathlib.Path):
                    print(columnvalue.value)
                    with columnvalue.value.open() as fo:
                        data = fo.read()

            #self.log.info(f"{record.record_type.name} {record.timestamp}")
            #for columnvalue in record.data:
            #    self.log.info(f"{columnvalue.column} {columnvalue.stat_type} : {columnvalue.value}")

        self.log.info('HiveComponent.run() end')

    def parse_param(self, param):
        if type(param)==dict:
            interval = int(param.get('interval_ms', 1000))
            diff = int(param.get('diff', 1))
            return Param(interval/1000.0, diff)
        else:
            return Param(1.0, 2, 1)


