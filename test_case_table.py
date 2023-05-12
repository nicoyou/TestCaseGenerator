import define
from define import Index, Type, test_list_t
from table_base import TableBase


# テストの種類から全テストケースのテーブルを作成する
class TestCaseTable(TableBase):
    # テストの種類からテストケーステーブルを生成する
    def set_test_list(self, test_list: test_list_t) -> None:
        now_normal_num = 0      # 現在までの Type.normal の数
        use_conditions = False  # 条件分岐を使用したかどうか ( 今後はノーマルノードが使用できなくなる )
        test_list = self.clean_test_list(test_list)
        for iy in range(len(test_list)):
            if test_list[iy][Index.type] == Type.normal:
                now_normal_num += 1
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])
            elif test_list[iy][Index.type] == Type.reversal:
                self.add_value_header(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param1])
                self.add_value_header(self.word_reversal(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param2]))
            elif test_list[iy][Index.type] == Type.if_and:
                use_conditions = True
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])

            if not use_conditions:
                for ix in range(2**self.get_normal_num(test_list)):
                    if test_list[iy][Index.type] == Type.normal:
                        if (ix // (2**self.get_normal_num(test_list) / (2**now_normal_num))) % 2 == 0:
                            self.add_value_table(define.PTN_TRUE)
                        else:
                            self.add_value_table(define.PTN_FALSE)
                    elif test_list[iy][Index.type] == Type.reversal:                                                                      # 参照元テーブル列を反転する
                        self.add_value_table(self.word_reversal(self.get_table_row_from_key(test_list, test_list[iy][Index.param1])[ix]))
            else:
                for ix in range(len(self.table[0])):
                    if test_list[iy][Index.type] == Type.if_and:
                        ptn_add_flag = False
                        for if_and_key_i in range(len(test_list[iy]) - Index.param3):                                                     # 条件の数だけループする
                            if self.get_table_row_from_key(test_list, test_list[iy][Index.param3 + if_and_key_i])[ix] != define.PTN_TRUE: # 条件の PTN が〇かどうかをチェックする
                                break
                        else:                                                                                                             # 全ての条件がを満たしていれば
                            self.add_value_table(define.PTN_TRUE)
                            ptn_add_flag = True
                        if not ptn_add_flag:
                            self.add_value_table(define.PTN_FALSE)
                if test_list[iy][Index.type] == Type.if_and:                                                                              # if_and 条件の列があれば
                    for ix in range(len(self.table[iy]) - 1, -1, -1):
                        if self.table[iy][ix] == define.PTN_TRUE:
                            self.clone_column(ix, ix)
                            self.table[iy][ix] = define.PTN_FALSE

            if iy != len(test_list) - 1:
                self.new_line_table()
