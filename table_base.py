import os
from pathlib import Path

import define
from define import Index, Type, key_t, test_list_t


# テストの種類から全テストケースのテーブルを作成する
class TableBase():
    def __init__(self) -> None:
        self.table: list[list] = [[]]
        self.header: list[list] = [[]]

    # テーブルのヘッダ ( 左側 ) にデータを追加する
    def add_value_header(self, text: str) -> None:
        self.header[-1].append(text)
        return

    # テーブルの一番後ろにデータを追加する
    def add_value_table(self, text: str) -> None:
        self.table[-1].append(text)
        return

    # テーブルを改行して次の行に進む
    def new_line_table(self) -> None:
        self.table.append([])
        self.header.append([])
        return

    # 特定の列をクローンして指定された列に追加する
    def clone_column(self, from_x: int, to_x: int) -> None:
        for iy in range(len(self.table)):
            self.table[iy].insert(to_x, self.table[iy][from_x])
        return

    # テストリストのデータを最適化する
    def clean_test_list(self, test_list: test_list_t):
        test_list_c = []
        for row in test_list:
            test_list_c.append(list(row))
            if row[Index.type] == Type.reversal:
                test_list_c[-1][Index.pk] = "!" + str(test_list_c[-1][Index.param1])
        return test_list_c

    # テーブル情報を CSV 形式でテキストに出力する
    def save_csv(self, file_name: str | Path) -> None:
        file_name = define.OUT_DIR_PATH / file_name
        encoding = define.ENCODING
        if file_name.suffix == ".csv":
            encoding = define.ENCODING_CSV  # csv で出力するときは Excel でバグらないようにエンコードを変更する

        os.makedirs(file_name.parent, exist_ok=True)
        with open(file_name, "w", encoding=encoding) as f:
            for iy in range(len(self.table)):
                for row in self.header[iy]:
                    f.write(row + define.DELIMITER)

                for row in self.table[iy]:
                    f.write(row + define.DELIMITER)
                f.write("\n")
        return

    # テストリストからノーマル列の数を取得する
    def get_normal_num(self, test_list: test_list_t) -> int:
        count = 0
        for row in test_list:
            if row[Index.type] == Type.normal:
                count += 1
        return count

    # テストリストから指定されたキーの列を検索する
    def get_data_from_key(self, test_list: test_list_t, key: key_t) -> tuple | list:
        for row in test_list:
            if row[Index.pk] == key:
                return row
        raise ValueError(define.ERROR_MSG_NOT_FIND_KEY)

    # ストリストから指定されたキーの index を取得する
    def get_index_from_key(self, test_list: test_list_t, key: key_t) -> int:
        for i, row in enumerate(test_list):
            if row[Index.pk] == key:
                return i
        raise ValueError(define.ERROR_MSG_NOT_FIND_KEY)

    # テストリストから指定されたキーに該当するテーブルの列を取得する ( ! の反転処理や tuple の or 処理 )
    def get_table_row_from_key(self, test_list: test_list_t, key: key_t) -> tuple | list:
        if type(key) is tuple:
            result_row = None
            for row in key:
                if result_row is None:
                    result_row = self.get_table_row_from_key(test_list, row)
                else:
                    temp_table = self.get_table_row_from_key(test_list, row)
                    # 取得した行を OR でマージする ( どちらかの行が TRUE なら TRUE )
                    result_row = [define.PTN_TRUE if row == define.PTN_TRUE or temp_table[i] == define.PTN_TRUE else define.PTN_FALSE for i, row in enumerate(result_row)]
            if result_row is not None:
                return result_row
            raise ValueError(define.ERROR_MSG_OR_TUPLE)

        for i, row in enumerate(test_list):
            if type(key) is str and key[0] == "!":
                if row[Index.pk] == key[1:]:
                    return [self.word_reversal(row2) for row2 in self.table[i]]
            else:
                if row[Index.pk] == key:
                    return self.table[i]
        raise ValueError(define.ERROR_MSG_NOT_FIND_KEY)

    # 特定の単語を反転する
    def word_reversal(self, word: str) -> str:
        for row in define.REVERSAL_WORD:
            if word == row[0]:
                return row[1]
            if word == row[1]:
                return row[0]
        return word
