from define import Type
from test_case_table import TestCaseTable

if __name__ == "__main__":
    TEST_LIST = (
        (1, Type.normal, "オプション 1", "ON"),
        (None, Type.reversal, 1),
        (2, Type.normal, "オプション 2", "ON"),
        (-2, Type.reversal, 2),
        (None, Type.normal, "", "テキスト入力あり"),
        (None, Type.if_and, "", "オプション 1 が有効、2 が無効のときのみ使用できる機能", 1, -2),
    )

    t = TestCaseTable()
    t.set_test_list(TEST_LIST)
    t.save_csv("result.txt")
    t.save_csv("result.csv")
