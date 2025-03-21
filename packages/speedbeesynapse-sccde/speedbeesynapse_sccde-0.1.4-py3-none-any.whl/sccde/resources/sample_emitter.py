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

@HiveComponentInfo(uuid='{{REPLACED-UUID}}', name='スカラ型カウントアップ', inports=0, outports=1)
class HiveComponent(HiveComponentBase):
    def main(self, _param):
        self.bool  = self.out_port1.Column('bool', DataType.BOOLEAN)
        self.i8  = self.out_port1.Column('int8', DataType.INT8)
        self.i16 = self.out_port1.Column('int16', DataType.INT16)
        self.i32 = self.out_port1.Column('int32', DataType.INT32)
        self.i64 = self.out_port1.Column('int64', DataType.INT64)
        self.u8  = self.out_port1.Column('uint8', DataType.UINT8)
        self.u16 = self.out_port1.Column('uint16', DataType.UINT16)
        self.u32 = self.out_port1.Column('uint32', DataType.UINT32)
        self.u64 = self.out_port1.Column('uint64', DataType.UINT64)
        self.flt = self.out_port1.Column('float', DataType.FLOAT)
        self.dbl = self.out_port1.Column('double', DataType.DOUBLE)
        self.str = self.out_port1.Column('str', DataType.STRING)
        self.bin = self.out_port1.Column('bin', DataType.BINARY)

        count = 0
        param = self.parse_param(_param)

        while self.is_runnable():
            ts = self.get_timestamp()

            self.bool.insert(count % 2, ts)
            self.i8.insert(count, ts)
            self.i16.insert(count, ts)
            self.i32.insert(count, ts)
            self.i64.insert(count, ts)
            if count >= 0:
                self.u8.insert(count, ts)
                self.u16.insert(count, ts)
                self.u32.insert(count, ts)
                self.u64.insert(count, ts)
            self.flt.insert(count + 0.123, ts)
            self.dbl.insert(count + 0.123, ts)
            self.str.insert(str(count), ts)
            self.bin.insert(bytes(str(count), 'utf8'), ts)

            count += param.diff
            time.sleep(param.interval)

    def parse_param(self, param):
        if type(param)==dict:
            interval = int(param.get('interval_ms', 1000))
            diff = int(param.get('diff', 1))
            return Param(interval/1000.0, diff)
        else:
            return Param(1.0, 2, 1)


