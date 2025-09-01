import constants
from constants import ExIndex, test_list_t
from table_base import TableBase
from test_case_table import TestCaseTable


# 期待結果のテーブル
class ExResultTable(TableBase):
    # テストケーステーブルと期待する結果から期待結果のテーブルを生成する
    def set_ex_result_list(self, test_case_table: TestCaseTable, test_list: test_list_t, ex_result_list: test_list_t, add_test_case_table: bool = False) -> None:
        test_list = self.clean_test_list(test_list)
        if add_test_case_table:
            for iy in range(len(test_case_table.table)):
                if len(test_case_table.header[iy]) >= 1:
                    self.add_value_header(test_case_table.header[iy][0])
                if len(test_case_table.header[iy]) >= 2:
                    self.add_value_header(test_case_table.header[iy][1])
                for ix in range(len(test_case_table.table[iy])):
                    self.add_value_table(test_case_table.table[iy][ix])
                self.new_line_table()
            self.add_value_header("期待結果")
            self.add_value_header("------")
            self.new_line_table()
        for ex_result in ex_result_list:
            if add_test_case_table:     # テストケースがある場合はパターンの位置を合わせるために一番最初の空ヘッダーを追加する
                self.add_value_header("")
            self.add_value_header(ex_result[ExIndex.title])
            for ix in range(len(test_case_table.table[0])):
                for key_index in range(ExIndex.conditional_begin, len(ex_result)):
                    if test_case_table.get_table_row_from_key(test_list, ex_result[key_index])[ix] != constants.PTN_TRUE:
                        self.add_value_table(constants.EX_RESULT_FALSE)
                        break
                else:                   # 全ての条件を満たしていれば
                    self.add_value_table(constants.EX_RESULT_TRUE)
            self.new_line_table()
        return
