# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 18:10
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : pas_class.py
# @Software: PyCharm

import load_amazon_sheet
import send2trash
import output_usable_sheet_head
from openpyxl.utils import coordinate_to_tuple
import pas_utility as pasu
import random


SECRET_CODE = '666'
KW_TRIMMER = 200
ALPHABET = list('ABCDEFGHIJKLMNOPQISTUVWXYZ')


class ProcessAmazonSheet(load_amazon_sheet.LoadAmazonSheet):

    def __init__(self, sheet_path):
        try:
            load_amazon_sheet.LoadAmazonSheet.__init__(self, sheet_path)
            self.all_titles = []
        except FileNotFoundError as _e:
            print(pasu.NO_FILE)
            raise _e

    def process_title(self):
        item_name_coordinate = pasu.get_coordinate(self.item_name_cell)
        title_list = pasu.get_column_until_none_cell(self.sheet,
                                                     item_name_coordinate[0],
                                                     item_name_coordinate[1])
        self.all_titles = [each_title.value for each_title in title_list]
        for index, title in enumerate(title_list):
            title_list[index].value = pasu.process_item_name(title.value)

    def process_part_number(self):
        part_number_coordinate = pasu.get_coordinate(self.part_number_cell)
        part_number = ''.join(random.sample(ALPHABET, 2)) + '-' + str(random.randint(100, 999))
        pasu.process_info(self.sheet, part_number_coordinate, part_number)

    def process_model_number(self):
        model_coordinate = pasu.get_coordinate(self.model_cell)
        model_number = ''.join(random.sample(ALPHABET, 1)) + str(random.randint(10, 99))
        pasu.process_info(self.sheet, model_coordinate, model_number)

    def process_description(self):
        description_coordinate = pasu.get_coordinate(self.description)
        pasu.process_description(self.sheet, description_coordinate)

    def process_bulletpoints(self):
        bullet_point_coordinate = pasu.get_coordinate(self.bullet_point_cell)
        pasu.process_bulletpoints(self.sheet, bullet_point_coordinate)

    def process_price(self, lowest_price: int):
        price_coordinate = pasu.get_coordinate(self.price_cell)
        pasu.process_price(self.sheet, price_coordinate, lowest_price, self.current_file)

    def process_node(self, node):
        node_coordinate = pasu.get_coordinate(self.node_cell)
        pasu.process_info(self.sheet, node_coordinate, node)

    def process_update_delete(self, _ui: str):
        update_coordinate = pasu.get_coordinate(self.update_delete)
        pasu.process_info(self.sheet, update_coordinate, _ui)

    def process_ship_time(self):
        fulfillment_latency_coordinate = pasu.get_coordinate(self.fulfillment_latency)
        pasu.process_info(self.sheet, fulfillment_latency_coordinate, 3)

    def process_keywords(self, keywords: str):
        if keywords == SECRET_CODE:
            # 获取所有的标题
            item_name_coordinate = pasu.get_coordinate(self.item_name_cell)
            title_list = pasu.get_column_until_none_cell(self.sheet,
                                                         item_name_coordinate[0],
                                                         item_name_coordinate[1])
            self.all_titles = [each_title.value for each_title in title_list]
            # 用标题高频词处理关键字
            processed_keywords = ' '.join(pasu.high_frequent_words(self.all_titles))[:KW_TRIMMER]
            if pasu.cjk_detect(processed_keywords) is not None:
                processed_keywords = processed_keywords[:50]
            processed_keywords = processed_keywords.replace('  ', ' ')
            # 处理关键词
            keywords_coordinate = coordinate_to_tuple(str(self.keywords_cell).split('.')[-1][:-1])
            pasu.process_info(self.sheet, keywords_coordinate, processed_keywords)
        else:
            keywords_coordinate = coordinate_to_tuple(str(self.keywords_cell).split('.')[-1][:-1])
            pasu.process_info(self.sheet, keywords_coordinate, keywords)

    def process_item_type(self, keywords: str):
        keywords_coordinate = coordinate_to_tuple(str(self.item_type_cell).split('.')[-1][:-1])
        pasu.process_info(self.sheet, keywords_coordinate, keywords)

    def save_sheet(self, path: str, original_file: str) -> None:
        file_name = original_file.split('\\')[-1]
        _out_put_file_name = path + '\\_输出文件_' + file_name.replace('.xlsx', '') + '.xlsx'
        self.wb.save(_out_put_file_name)
        output_usable_sheet_head.main(path+'\\'+original_file,
                                      _out_put_file_name,
                                      path + '\\__完整文件_' + file_name.replace('.xlsx', '') + '.xlsx')
        send2trash.send2trash(path + '\\_输出文件_' + file_name.replace('.xlsx', '') + '.xlsx')


#  以相同数值处理多个表格的类
class ProcessWithSameParameter(ProcessAmazonSheet):

    def __init__(self, sheet_path, _same_parameter):
        ProcessAmazonSheet.__init__(self, sheet_path)
        self._same_parameter = _same_parameter

    def process_sheet(self):
        self.process_title()
        self.process_bulletpoints()
        self.process_price(self._same_parameter['lowest_pice'])
        self.process_node(self._same_parameter['node'])
        self.process_keywords(self._same_parameter['key_word'])
        self.process_model_number()
        self.process_part_number()
        self.process_ship_time()
        self.process_description()
        for row in range(1, 4):
            for col in range(1, 1000):
                self.sheet.cell(row, col).value = None
