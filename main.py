from constants import CaseType
from ex_result_table import ExResultTable
from test_case_table import TestCaseTable

if __name__ == "__main__":
    TEST_LIST = (
        ("a", CaseType.boolean, "オプション 1", "ON"),
        (None, CaseType.reversal, "a"),
        ("b", CaseType.boolean, "オプション 2", "ON"),
        (None, CaseType.reversal, "b"),
        ("c-1", CaseType.group, None, "オプション 3", "DEBUG"),
        ("c-2", CaseType.group, "c-1", None, "INFO"),
        ("c-3", CaseType.group, "c-1", None, "WARNING"),
        ("c-4", CaseType.group, "c-1", None, "ERROR"),
        ("text", CaseType.boolean, "", "テキスト入力あり"),
        ("c", CaseType.if_and, "", "オプション 1 が有効、2 が無効のときのみ使用できる設定 C", "a", "!b"),
    )

    EX_RESULT_LIST = (
        ("すべての条件で期待される", ),
        ("オプション 1 が正常に利用できる", ("a", )),
        ("オプション 2 が正常に利用できる", ("b", )),
        ("オプション 3 が INFO の場合", ("c-2", )),
        ("オプション 1 が有効でオプション 2 が無効の場合のみ使用できる機能", ("a", "!b")),
        ("オプション 1 が有効で、オプション 2 が有効かテキスト入力が有効な場合に使用できる機能 ( OR )", ("a", ("b", "text"))),
    )

    tct = TestCaseTable()
    tct.set_test_list(TEST_LIST)
    tct.save_csv("result.csv")

    ert = ExResultTable()
    ert.set_ex_result_list(tct, TEST_LIST, EX_RESULT_LIST, add_test_case_table=True)
    ert.save_csv("ex_result.csv")
