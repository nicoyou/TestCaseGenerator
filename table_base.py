import os
from pathlib import Path

import define
from define import Index, Type, key_t, test_list_t


# テストの種類から全テストケースのテーブルを作成する
class TableBase():
    def __init__(self) -> None:
        self.now_normal_num: int = 0
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
    def get_data_from_key(self, test_list: test_list_t, key: key_t) -> tuple:
        for row in test_list:
            if row[Index.pk] == key:
                return row
        return ()

    # ストリストから指定されたキーの index を取得する
    def get_index_from_key(self, test_list: test_list_t, key: key_t) -> int:
        for i, row in enumerate(test_list):
            if row[Index.pk] == key:
                return i
        return -1

    # 特定の単語を反転する
    def word_reversal(self, word: str) -> str:
        for row in define.REVERSAL_WORD:
            if word == row[0]:
                return row[1]
            if word == row[1]:
                return row[0]
        return word
