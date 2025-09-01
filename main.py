from constants import Type
from ex_result_table import ExResultTable
from test_case_table import TestCaseTable

if __name__ == "__main__":
    TEST_LIST = (
        ("a", Type.normal, "オプション 1", "ON"),
        (None, Type.reversal, "a"),
        ("b", Type.normal, "オプション 2", "ON"),
        (None, Type.reversal, "b"),
        ("text", Type.normal, "", "テキスト入力あり"),
        ("c", Type.if_and, "", "オプション 1 が有効、2 が無効のときのみ使用できる設定 C", "a", "!b"),
    )

    EX_RESULT_LIST = (
        ("オプション 1 が正常に利用できる", "a"),
        ("オプション 2 が正常に利用できる", "b"),
        ("オプション 1 が有効でオプション 2 が無効の場合のみ使用できる機能", "a", "!b"),
        ("オプション 1 が有効で、オプション 2 が有効かテキスト入力が有効な場合に使用できる機能 ( OR )", "a", ("b", "text")),
    )

    tct = TestCaseTable()
    tct.set_test_list(TEST_LIST)
    tct.save_csv("result.csv")

    ert = ExResultTable()
    ert.set_ex_result_list(tct, TEST_LIST, EX_RESULT_LIST, add_test_case_table=True)
    ert.save_csv("ex_result.csv")
