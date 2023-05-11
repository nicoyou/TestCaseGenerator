import define
from define import Index, Type, test_list_t
from table_base import TableBase


# テストの種類から全テストケースのテーブルを作成する
class TestCaseTable(TableBase):
    # テストの種類からテストケーステーブルを生成する
    def set_test_list(self, test_list: test_list_t) -> None:
        for iy in range(len(test_list)):
            if test_list[iy][Index.type] == Type.normal:
                self.now_normal_num += 1
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])
            elif test_list[iy][Index.type] == Type.reversal:
                self.add_value_header(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param1])
                self.add_value_header(self.word_reversal(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param2]))
            elif test_list[iy][Index.type] == Type.if_and:
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])

            for ix in range(2**self.get_normal_num(test_list)):
                if test_list[iy][Index.type] == Type.normal:
                    if (ix // (2**self.get_normal_num(test_list) / (2**self.now_normal_num))) % 2 == 0:
                        self.add_value_table(define.PTN_TRUE)
                    else:
                        self.add_value_table(define.PTN_FALSE)
                elif test_list[iy][Index.type] == Type.reversal:                                                                          # 参照元テーブル列を反転する
                    self.add_value_table(self.word_reversal(self.table[self.get_index_from_key(test_list, test_list[iy][Index.param1])][ix]))
                elif test_list[iy][Index.type] == Type.if_and:
                    ptn_add_flag = False
                    for jx in range(len(self.table[0])):
                        column = [temp_row[jx] for temp_row in self.table[:-1]]                                                           # 縦の一列のみ取得する
                        for if_and_key_i in range(len(test_list[iy]) - Index.param3):                                                     # 条件の数だけループする
                            if column[self.get_index_from_key(test_list, test_list[iy][Index.param3 + if_and_key_i])] != define.PTN_TRUE: # 条件の PTN が〇かどうかをチェックする
                                break
                            if if_and_key_i == len(test_list[iy]) - Index.param3 - 1:                                                     # 全ての条件を達していれば
                                if ix == jx:
                                    self.add_value_table(define.PTN_TRUE)
                                    ptn_add_flag = True
                    if not ptn_add_flag:
                        self.add_value_table(define.PTN_FALSE)
            self.new_line_table()
        self.table.pop()                                                                                                                  # TODO: 最後の空テーブルを削除する

        for iy in range(len(test_list)):
            if test_list[iy][Index.type] == Type.if_and:    # if_and 条件の列があれば
                for ix in range(len(self.table[iy]) - 1, -1, -1):
                    if self.table[iy][ix] == define.PTN_TRUE:
                        self.clone_column(ix, ix)
                        self.table[iy][ix] = define.PTN_FALSE
        return
