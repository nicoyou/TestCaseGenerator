from define import Type
from ex_result_table import ExResultTable
from test_case_table import TestCaseTable

if __name__ == "__main__":
    TEST_LIST = (
        (1, Type.normal, "オプション 1", "ON"),
        (None, Type.reversal, 1),
        (2, Type.normal, "オプション 2", "ON"),
        (-2, Type.reversal, 2),
        (None, Type.normal, "", "テキスト入力あり"),
        (None, Type.if_and, "", "オプション 1 が有効、2 が無効のときのみ使用できる設定", 1, -2),
    )

    EX_RESULT_LIST = (
        ("オプション 1 が正常に利用できる", 1),
        ("オプション 2 が正常に利用できる", 2),
        ("オプション 1 が有効でオプション 2 が無効の場合のみアクセスできる機能", 1, -2),
    )

    tct = TestCaseTable()
    tct.set_test_list(TEST_LIST)
    tct.save_csv("result.csv")

    ert = ExResultTable()
    ert.set_ex_result_list(tct, TEST_LIST, EX_RESULT_LIST)
    ert.save_csv("ex_result.csv")
