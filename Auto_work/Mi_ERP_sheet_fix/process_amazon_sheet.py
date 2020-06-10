import os
import load_amazon_sheet
from openpyxl.utils import coordinate_to_tuple
import pas_utilits

""" 
TODO:
    2.优化交互，操作流程
        2.2 兼容erp直接输出的文件日期名称
"""


class ProcessAmazonSheet(load_amazon_sheet.LoadAmazonSheet):

    def __init__(self, sheet_path):
        try:
            load_amazon_sheet.LoadAmazonSheet.__init__(self, sheet_path)
        except FileNotFoundError as _e:
            print(pas_utilits.NO_FILE)
            raise _e

    def process_title(self):
        item_name_coordinate = coordinate_to_tuple(str(self.item_name_cell).split('.')[-1][:-1])
        title_list = pas_utilits.get_column_until_none_cell(self.sheet,
                                                            item_name_coordinate[0],
                                                            item_name_coordinate[1])
        for index, title in enumerate(title_list):
            title_list[index].value = pas_utilits.process_item_name(title.value)

    def process_description(self):
        description_coordinate = coordinate_to_tuple(str(self.description).split('.')[-1][:-1])
        pas_utilits.process_description(self.sheet, description_coordinate)

    def process_bulletpoints(self):
        # get bullet_point
        bullet_point_coordinate = coordinate_to_tuple(str(self.bullet_point_cell).split('.')[-1][:-1])
        # process bullet_point
        pas_utilits.process_bulletpoints(self.sheet, bullet_point_coordinate)

    def process_price(self, exchange_rate: float):
        price_coordinate = coordinate_to_tuple(str(self.price_cell).split('.')[-1][:-1])
        pas_utilits.process_price(self.sheet, price_coordinate, exchange_rate)

    def process_node(self, node):
        node_coordinate = coordinate_to_tuple(str(self.node_cell).split('.')[-1][:-1])
        pas_utilits.process_info(self.sheet, node_coordinate, node)

    def process_keywords(self, keywords: str):
        keywords_coordinate = coordinate_to_tuple(str(self.keywords_cell).split('.')[-1][:-1])
        pas_utilits.process_info(self.sheet, keywords_coordinate, keywords)

    def process_item_type(self, keywords: str):
        keywords_coordinate = coordinate_to_tuple(str(self.item_type_cell).split('.')[-1][:-1])
        pas_utilits.process_info(self.sheet, keywords_coordinate, keywords)

    def process_sheet(self):

        # ========= PROCESS TITLE =========
        self.process_title()
        # ========= PROCESS TITLE =========
        self.process_bulletpoints()
        # ========= PROCESS PRICE =========
        self.process_price(float(input("输入汇率：")))
        # ========= PROCESS NODE =========
        self.process_node(str(input("分类节点：")))
        # ========= PROCESS KEYWORDS =========
        self.process_keywords(str(input("关键词：")))
        # ========= PROCESS DESCRIPTION =========
        self.process_description()
        # ========= REMOVE FIRST THREE ROW =========
        for row in range(1, 4):
            for col in range(1, 1000):
                self.sheet.cell(row, col).value = None

    def save_sheet(self, path: str, country: str, time: str) -> None:
        self.wb.save(path+'\\'+country+'_输出文件_'+time+'.xlsx')


if __name__ == '__main__':
    while True:
        try:
            print(pas_utilits.INTRO)

            _main_path = pas_utilits.validate_main_path()
            _time = pas_utilits.select_time()
            _product = pas_utilits.validate_product()
            _country = str(input("输入文件中的国家："))
            _lang = str(input("输出文件中的国家："))

            if os.path.isfile(f"{_main_path}\\{_time}_{_product}\\{_product}{_country}_亚马逊表_{_time}.xlsx"):
                original_file = f"{_main_path}\\{_time}_{_product}\\{_product}{_country}_亚马逊表_{_time}.xlsx"
            else:
                original_file = f"{_main_path}\\{_time}_{_product}\\{str(input('未找到文件，请手动输入文件名：'))}"
            working_path = f"{_main_path}\\{_time}_{_product}"

            pas = ProcessAmazonSheet(original_file)
            pas.process_sheet()
            pas.save_sheet(working_path, _lang, _time)
            os.startfile(working_path)
        except Exception as e:
            print(e)
            # raise e
            print('\n')
        else:
            break
