from enum import IntEnum, auto
from pathlib import Path

test_list_t = tuple[tuple, ...]
key_t = int | str | tuple


# テストケースを作成するために登録する機能の種類
class Type(IntEnum):
    normal = auto()     # 倍々でテストケースが増加する機能
    reversal = auto()   # 特定の機能の反対を表す
    if_and = auto()     # 特定の条件で使用できる機能 ( 必要な機能を and 条件で指定する )


# テストケースタプルの格納データ
class Index(IntEnum):
    pk = 0
    type = auto()
    param1 = auto()
    param2 = auto()
    param3 = auto()


# 期待結果タプルの格納データ
class ExIndex(IntEnum):
    title = 0
    conditional_begin = auto()


__version__ = "1.1.0"
ENCODING = "utf-8"
ENCODING_CSV = "shift-jis"
OUT_DIR_PATH = Path("./out")

PTN_TRUE = "○"
PTN_FALSE = "-"
EX_RESULT_TRUE = "●"
EX_RESULT_FALSE = ""
DELIMITER = ", "
REVERSAL_WORD = (
    (PTN_TRUE, PTN_FALSE),
    (EX_RESULT_TRUE, EX_RESULT_FALSE),
    ("ON", "OFF"),
    ("TRUE", "FALSE"),
    ("True", "False"),
    ("true", "false"),
    ("ひらがな", "カタカナ"),
)

ERROR_MSG_NOT_FIND_KEY = "未定義のキーが指定されました"
ERROR_MSG_CANT_USE_NORMAL = "Type.if_xxx 系が指定された後で Type.normal 系を使用することはできません"
ERROR_MSG_NO_TYPE = "使用できない機能タイプが指定されました"
ERROR_MSG_OR_TUPLE = "不正な OR 条件が指定されました"
