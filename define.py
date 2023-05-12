from enum import IntEnum, auto
from pathlib import Path

test_list_t = tuple[tuple, ...]
key_t = int | str


# テストケースタプルの格納データ
class Index(IntEnum):
    pk = 0
    type = auto()
    param1 = auto()
    param2 = auto()
    param3 = auto()


class Type(IntEnum):
    normal = auto()
    reversal = auto()
    if_and = auto()


__version__ = "1.0.0"
ENCODING = "utf-8"
ENCODING_CSV = "shift-jis"
OUT_DIR_PATH = Path("./out")

PTN_TRUE = "○"
PTN_FALSE = "-"
DELIMITER = ", "
REVERSAL_WORD = (
    (PTN_TRUE, PTN_FALSE),
    ("ON", "OFF"),
    ("TRUE", "FALSE"),
    ("True", "False"),
    ("true", "false"),
    ("ひらがな", "カタカナ"),
)
