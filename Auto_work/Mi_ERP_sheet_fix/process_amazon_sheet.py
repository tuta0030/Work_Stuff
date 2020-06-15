import os
import load_amazon_sheet
from openpyxl.utils import coordinate_to_tuple
import pas_utilits
import main_menu


""" 
处理亚马逊表格的程序
TODO:
    2.2 兼容erp直接输出的文件日期名称
"""


class ProcessAmazonSheet(load_amazon_sheet.LoadAmazonSheet):

    def __init__(self, sheet_path):
        try:
            load_amazon_sheet.LoadAmazonSheet.__init__(self, sheet_path)
        except FileNotFoundError as _e:
            print(pas_utilits.NO_FILE)
            raise _e

    def cap_title(self, brand: str):
        item_name_coordinate = coordinate_to_tuple(str(self.item_name_cell).split('.')[-1][:-1])
        title_list = pas_utilits.get_column_until_none_cell(self.sheet,
                                                            item_name_coordinate[0],
                                                            item_name_coordinate[1])
        for index, title in enumerate(title_list):
            title_list[index].value = pas_utilits.cap_title(title.value, brand)

    def process_title(self, brand: str):
        item_name_coordinate = coordinate_to_tuple(str(self.item_name_cell).split('.')[-1][:-1])
        title_list = pas_utilits.get_column_until_none_cell(self.sheet,
                                                            item_name_coordinate[0],
                                                            item_name_coordinate[1])
        for index, title in enumerate(title_list):
            title_list[index].value = pas_utilits.process_item_name(title.value, brand)

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

    def only_price(self):
        self.process_price(float(input("输入汇率：")))

    def process_sheet(self):

        # ========= PROCESS TITLE =========
        self.process_title(str(input("请输入不需要首字母大写的品牌名：")))
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


def main_function():
    while True:
        try:
            print(pas_utilits.INTRO)
            only_functions = {}

            def add_only_func(menu: tuple, func):
                only_functions[menu] = func

            def only_cap_title(pas_instance):
                pas_instance.cap_title(str(input("请输入不需要首字母大写的品牌名(没有的话按回车继续)：")))

            def only_change_price(pas_instance):
                pas_instance.only_price()

            ui = input("0：主程序，1：单独功能，-1：退回主菜单：")
            _main_path = pas_utilits.validate_main_path()
            if ui == '-1':
                main_menu.main_menu()

            print("按照提示输入文件相关必要参数")
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
            if ui == '0':
                pas.process_sheet()
            elif ui == '1':
                add_only_func((1, '标题首字母大写'), only_cap_title)
                add_only_func((2, '处理价格'), only_change_price)
                menu_list = only_functions.keys()
                menu_list = [str(item)[1:-1].replace('\'', '') for item in menu_list]
                only_ui = input(f"选择需要的功能:{', '.join(menu_list)}:")
                for key, value in only_functions.items():
                    if only_ui == str(key[0]):
                        value(pas)
                        os.startfile(working_path)
            else:
                print("未知选项，退回主菜单")
                main_menu.main_menu()

            pas.save_sheet(working_path, _lang, _time)
            main_function()
        except Exception as e:
            print(e)
            # raise e
            print('\n')
        else:
            break
