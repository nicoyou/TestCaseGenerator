import define
from define import ExIndex, test_list_t
from table_base import TableBase
from test_case_table import TestCaseTable


# 期待結果のテーブル
class ExResultTable(TableBase):
    # テストケーステーブルと期待する結果から期待結果のテーブルを生成する
    def set_ex_result_list(self, test_case_table: TestCaseTable, test_list: test_list_t, ex_result_list: test_list_t) -> None:
        for ex_result in ex_result_list:
            self.add_value_header(ex_result[ExIndex.title])
            for ix in range(len(test_case_table.table[0])):
                for key_index in range(ExIndex.conditional_begin, len(ex_result)):
                    if test_case_table.table[self.get_index_from_key(test_list, ex_result[key_index])][ix] != define.PTN_TRUE:
                        self.add_value_table(define.EX_RESULT_FALSE)
                        break
                else:   # 全ての条件を満たしていれば
                    self.add_value_table(define.EX_RESULT_TRUE)
            self.new_line_table()
        return
