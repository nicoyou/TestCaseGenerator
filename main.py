from define import Type
from ex_result_table import ExResultTable
from test_case_table import TestCaseTable

if __name__ == "__main__":
    TEST_LIST = (
        ("a", Type.normal, "オプション 1", "ON"),
        (None, Type.reversal, "a"),
        ("b", Type.normal, "オプション 2", "ON"),
        (None, Type.reversal, "b"),
        (None, Type.normal, "", "テキスト入力あり"),
        (None, Type.if_and, "", "オプション 1 が有効、2 が無効のときのみ使用できる設定", "a", "!b"),
    )

    EX_RESULT_LIST = (
        ("オプション 1 が正常に利用できる", "a"),
        ("オプション 2 が正常に利用できる", "b"),
        ("オプション 1 が有効でオプション 2 が無効の場合のみアクセスできる機能", "a", "!b"),
    )

    tct = TestCaseTable()
    tct.set_test_list(TEST_LIST)
    tct.save_csv("result.csv")

    ert = ExResultTable()
    ert.set_ex_result_list(tct, TEST_LIST, EX_RESULT_LIST)
    ert.save_csv("ex_result.csv")
