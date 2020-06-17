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

    def cap_title(self):
        brand = input("输入不需要大写的品牌名（没有的话按回车继续）：")
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

    def save_sheet(self, path: str, original_filename: str) -> None:
        self.wb.save(path+'\\输出文件_'+original_filename+'.xlsx')


def index_files() -> tuple:
    # 输入文件夹路径
    folder = input('输入包含表格的文件夹：')
    # 索引并列出文件夹中的表格
    files = {}
    index = 0
    for folder, subfolder, file in os.walk(folder):
        for each_file in file:
            files[index] = folder + '\\' + each_file
            index += 1
    print("当前文件夹中包含的文件有：")
    for index, file in files.items():
        print(index, end='')
        print('\t' + file.split('\\')[-1])
    # 通过下标选择需要处理的表格文件
    ui = input('请选择需要处理的文件：')
    # 传入表格文件的路径
    which_file = ''
    for selection in files.keys():
        if len(ui.split(' ')) > 1:
            which_file = []
            for each_ui in ui.split(' '):
                which_file.append(files[int(each_ui)])
        if ui == str(selection):
            which_file = files[selection]
    return folder, which_file


def pas_main():
    folder, which_file = index_files()
    if type(which_file) is list:
        for each_file in which_file:
            pas = ProcessAmazonSheet(each_file)
            pas.process_sheet()
            pas.save_sheet(folder, each_file.split('\\')[-1])
    else:
        pas = ProcessAmazonSheet(which_file)
        pas.process_sheet()
        pas.save_sheet(folder, which_file.split('\\')[-1])


def pas_part():
    folder, which_file = index_files()
    if type(which_file) is list:
        for each_file in which_file:
            pas = ProcessAmazonSheet(each_file)
            print("选择需要单独处理的功能")
            _menu = {'仅处理价格': pas.only_price,
                     '仅标题首字母大写': pas.cap_title
                     }
            pas_utilits.make_menu(_menu)
            pas.save_sheet(folder, each_file.split('\\')[-1])
    else:
        pas = ProcessAmazonSheet(which_file)
        print("选择需要单独处理的功能")
        _menu = {'仅处理价格': pas.only_price,
                 '仅标题首字母大写': pas.cap_title
                 }
        pas_utilits.make_menu(_menu)
        pas.save_sheet(folder, which_file.split('\\')[-1])


def main_function():
    while True:
        try:
            os.system('cls')
            print("当前选项：处理亚马逊表格")
            print('')
            _menu = {'退回主菜单': main_menu.main_menu,
                     '处理亚马逊表格（全部）': pas_main,
                     '处理亚马逊表格（部分）': pas_part}
            pas_utilits.make_menu(_menu)
            main_function()
        except Exception as e:
            # raise e
            print(e)
            print('由于以上错误，无法处理本文件，请尝试重新输入正确的文件夹和文件序列号')
            main_function()
        else:
            break
