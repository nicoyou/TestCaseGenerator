from tqdm import tqdm

import constants
from constants import CaseType, Index, test_list_t
from table_base import TableBase


# テストの種類から全テストケースのテーブルを作成する
class TestCaseTable(TableBase):
    # テストの種類からテストケーステーブルを生成する
    def set_test_list(self, test_list: test_list_t) -> None:
        current_boolean_group_count = 0     # 現在までの因子の数
        use_conditions = False      # 条件分岐を使用したかどうか ( 今後はノーマルノードが使用できなくなる )
        test_list = self.clean_test_list(test_list)
        for iy in tqdm(range(len(test_list))):
            if test_list[iy][Index.type] == CaseType.boolean:
                current_boolean_group_count += 1
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])
            elif test_list[iy][Index.type] == CaseType.reversal:
                self.add_value_header(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param1])
                self.add_value_header(self.word_reversal(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param2]))
            elif test_list[iy][Index.type] == CaseType.if_and:
                use_conditions = True
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])

            if not use_conditions:
                for ix in range(2**self.get_boolean_group_count(test_list)):
                    if test_list[iy][Index.type] == CaseType.boolean:
                        if (ix // (2**self.get_boolean_group_count(test_list) / (2**current_boolean_group_count))) % 2 == 0:
                            self.add_value_table(constants.PATTERN_TRUE)
                        else:
                            self.add_value_table(constants.PATTERN_FALSE)
                    elif test_list[iy][Index.type] == CaseType.reversal:                                                                            # 参照元テーブル列を反転する
                        self.add_value_table(self.word_reversal(self.get_table_row_from_key(test_list, test_list[iy][Index.param1])[ix]))
                    else:
                        raise ValueError(constants.ERROR_MSG_NO_TYPE)
            else:
                for ix in range(len(self.table[0])):
                    if test_list[iy][Index.type] == CaseType.if_and:
                        is_pattern_additional = False
                        for if_and_key_i in range(len(test_list[iy]) - Index.param3):                                                               # 条件の数だけループする
                            if self.get_table_row_from_key(test_list, test_list[iy][Index.param3 + if_and_key_i])[ix] != constants.PATTERN_TRUE:    # 条件の PTN が〇かどうかをチェックする
                                break
                        else:                                                                                                                       # 全ての条件がを満たしていれば
                            self.add_value_table(constants.PATTERN_TRUE)
                            is_pattern_additional = True
                        if not is_pattern_additional:
                            self.add_value_table(constants.PATTERN_FALSE)
                    elif test_list[iy][Index.type] == CaseType.boolean or test_list[iy][Index.type] == CaseType.reversal:
                        raise ValueError(constants.ERROR_MSG_CANT_USE_BOOLEAN)
                    else:
                        raise ValueError(constants.ERROR_MSG_NO_TYPE)

                if test_list[iy][Index.type] == CaseType.if_and:    # if_and 条件の列があれば
                    for ix in range(len(self.table[iy]) - 1, -1, -1):
                        if self.table[iy][ix] == constants.PATTERN_TRUE:
                            self.clone_column(ix, ix)
                            self.table[iy][ix] = constants.PATTERN_FALSE

            if iy != len(test_list) - 1:
                self.new_line_table()
