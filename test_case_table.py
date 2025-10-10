from tqdm import tqdm

import constants
from constants import CaseType, Index, test_list_t
from table_base import TableBase


# テストの種類から全テストケースのテーブルを作成する
class TestCaseTable(TableBase):
    # テストの種類からテストケーステーブルを生成する
    def set_test_list(self, test_list: test_list_t) -> None:
        test_list = self.clean_test_list(test_list)

        # group 因子の定義を事前に収集する
        groups_info: dict = {}
        for row in test_list:
            if row[Index.type] == CaseType.group:
                if row[Index.param1] is None:
                    parent_key = row[Index.pk]
                    groups_info[parent_key] = groups_info.get(parent_key, {"name": row[Index.param2], "levels": []})
                    groups_info[parent_key]["name"] = row[Index.param2]
                    groups_info[parent_key]["levels"].append((row[Index.pk], row[Index.param3]))
                else:
                    parent_key = row[Index.param1]
                    groups_info[parent_key] = groups_info.get(parent_key, {"name": None, "levels": []})
                    groups_info[parent_key]["levels"].append((row[Index.pk], row[Index.param3]))

        # グループ親の順序と各レベル数
        parent_order: list = list(groups_info.keys())
        levels_count: list[int] = [len(groups_info[parent]["levels"]) for parent in parent_order]

        child_to_parent_level_index: dict = {}
        for parent_index, parent in enumerate(parent_order):
            for level_index, (pk, _label) in enumerate(groups_info[parent]["levels"]):
                child_to_parent_level_index[pk] = (parent_index, level_index)

        # boolean 因子基底列数とグループによる乗数
        base_cols = 2**self.get_boolean_group_count(test_list)
        group_multiplier = 1
        for c in levels_count:
            group_multiplier *= max(1, c)

        current_boolean_group_count = 0     # 現在までの因子の数
        use_conditions = False              # 条件分岐を使用したかどうか ( 今後はノーマルノードが使用できなくなる )
        for iy in tqdm(range(len(test_list))):
            if test_list[iy][Index.type] == CaseType.boolean:
                current_boolean_group_count += 1
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])
            elif test_list[iy][Index.type] == CaseType.reversal:
                self.add_value_header(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param1])
                self.add_value_header(self.word_reversal(self.get_data_from_key(test_list, test_list[iy][Index.param1])[Index.param2]))
            elif test_list[iy][Index.type] == CaseType.group:
                if test_list[iy][Index.param1] is None:
                    self.add_value_header(test_list[iy][Index.param2])
                    self.add_value_header(test_list[iy][Index.param3])
                else:
                    parent_key = test_list[iy][Index.param1]
                    self.add_value_header(groups_info.get(parent_key, {}).get("name", ""))
                    self.add_value_header(test_list[iy][Index.param3])
            elif test_list[iy][Index.type] == CaseType.if_and:
                use_conditions = True
                self.add_value_header(test_list[iy][Index.param1])
                self.add_value_header(test_list[iy][Index.param2])

            if not use_conditions:
                for ix in range(base_cols * group_multiplier):
                    if test_list[iy][Index.type] == CaseType.boolean:
                        if ((ix % base_cols) // (2**self.get_boolean_group_count(test_list) / (2**current_boolean_group_count))) % 2 == 0:
                            self.add_value_table(constants.PATTERN_TRUE)
                        else:
                            self.add_value_table(constants.PATTERN_FALSE)
                    elif test_list[iy][Index.type] == CaseType.reversal:    # 参照元テーブル列を反転する
                        self.add_value_table(self.word_reversal(self.get_table_row_from_key(test_list, test_list[iy][Index.param1])[ix]))
                    elif test_list[iy][Index.type] == CaseType.group:

                        # カルテシアン積のグループ列から対象親のレベルのみ one-hot
                        current_pk = test_list[iy][Index.pk]
                        if current_pk in child_to_parent_level_index:
                            parent_idx, level_idx = child_to_parent_level_index[current_pk]

                            # 当該親より手前のグループの積
                            stride = 1
                            for ci in range(parent_idx):
                                stride *= levels_count[ci]

                            # 当該親の現在レベルを取得
                            current_group_index = (ix // (base_cols * stride)) % levels_count[parent_idx]
                            target = constants.PATTERN_TRUE if current_group_index == level_idx else constants.PATTERN_FALSE
                        else:
                            target = constants.PATTERN_FALSE
                        self.add_value_table(target)
                    else:
                        raise ValueError(constants.ERROR_MSG_NO_TYPE)
            else:
                for ix in range(len(self.table[0])):
                    if test_list[iy][Index.type] == CaseType.if_and:
                        is_pattern_additional = False
                        for if_and_key_i in range(len(test_list[iy]) - Index.param3):                                                               # 条件の数だけループする
                            if self.get_table_row_from_key(test_list, test_list[iy][Index.param3 + if_and_key_i])[ix] != constants.PATTERN_TRUE:    # 条件の PTN が有効かどうかをチェックする
                                break
                        else:                                                                                                                       # 全ての条件がを満たしていれば
                            self.add_value_table(constants.PATTERN_TRUE)
                            is_pattern_additional = True
                        if not is_pattern_additional:
                            self.add_value_table(constants.PATTERN_FALSE)
                    elif test_list[iy][Index.type] in [CaseType.boolean, CaseType.reversal, CaseType.group]:
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
