import os
import load_amazon_sheet
from openpyxl.utils import coordinate_to_tuple
import pas_utility
import send2trash
import output_usable_sheet_head

SECRET_CODE = '666'
BRAND_TO_REPLACE_KW = open('kw_brand.txt', 'r', encoding='utf-8').read()
KW_TRIMMER = 200


class ProcessAmazonSheet(load_amazon_sheet.LoadAmazonSheet):

    def __init__(self, sheet_path):
        try:
            load_amazon_sheet.LoadAmazonSheet.__init__(self, sheet_path)
            self.all_titles = []
        except FileNotFoundError as _e:
            print(pas_utility.NO_FILE)
            raise _e

    def cap_title(self):
        brand = input("输入不需要大写的品牌名（没有的话按回车继续）：")
        item_name_coordinate = coordinate_to_tuple(str(self.item_name_cell).split('.')[-1][:-1])
        title_list = pas_utility.get_column_until_none_cell(self.sheet,
                                                            item_name_coordinate[0],
                                                            item_name_coordinate[1])
        for index, title in enumerate(title_list):
            title_list[index].value = pas_utility.cap_title(title.value, brand)

    def process_title(self, brand: str):
        item_name_coordinate = coordinate_to_tuple(str(self.item_name_cell).split('.')[-1][:-1])
        title_list = pas_utility.get_column_until_none_cell(self.sheet,
                                                            item_name_coordinate[0],
                                                            item_name_coordinate[1])
        self.all_titles = [each_title.value for each_title in title_list]
        for index, title in enumerate(title_list):
            title_list[index].value = pas_utility.process_item_name(title.value, brand)

    def process_description(self):
        description_coordinate = coordinate_to_tuple(str(self.description).split('.')[-1][:-1])
        pas_utility.process_description(self.sheet, description_coordinate)

    def process_bulletpoints(self):
        # get bullet_point
        bullet_point_coordinate = coordinate_to_tuple(str(self.bullet_point_cell).split('.')[-1][:-1])
        # process bullet_point
        pas_utility.process_bulletpoints(self.sheet, bullet_point_coordinate)

    def process_price(self, exchange_rate: float, lowest_price: int):
        price_coordinate = coordinate_to_tuple(str(self.price_cell).split('.')[-1][:-1])
        pas_utility.process_price(self.sheet, price_coordinate, exchange_rate, lowest_price)

    def process_node(self, node):
        node_coordinate = coordinate_to_tuple(str(self.node_cell).split('.')[-1][:-1])
        pas_utility.process_info(self.sheet, node_coordinate, node)

    def process_keywords(self, keywords: str):
        if keywords == SECRET_CODE:
            processed_keywords = ' '.join(pas_utility.high_frequent_words(self.all_titles))\
                .replace(',', '').replace('*', '').replace(BRAND_TO_REPLACE_KW, '').replace('  ', ' ')\
                .replace('(', '').replace(')', '')[:KW_TRIMMER]
            keywords_coordinate = coordinate_to_tuple(str(self.keywords_cell).split('.')[-1][:-1])
            pas_utility.process_info(self.sheet, keywords_coordinate, processed_keywords)
        else:
            keywords_coordinate = coordinate_to_tuple(str(self.keywords_cell).split('.')[-1][:-1])
            pas_utility.process_info(self.sheet, keywords_coordinate, keywords)

    def process_item_type(self, keywords: str):
        keywords_coordinate = coordinate_to_tuple(str(self.item_type_cell).split('.')[-1][:-1])
        pas_utility.process_info(self.sheet, keywords_coordinate, keywords)

    def only_price(self):
        self.process_price(float(input("输入汇率：")), int(input("输入最低价格")))

    def process_sheet(self):
        self.process_title(str(input("请输入不需要首字母大写的品牌名(回车跳过)：")))
        self.process_bulletpoints()
        self.process_price(float(input("输入汇率：")), int(input("输入最低价格:")))
        self.process_node(str(input("分类节点(-1跳过)：")))
        self.process_keywords(str(input("关键词(-1跳过)：")))
        self.process_description()
        for row in range(1, 4):
            for col in range(1, 1000):
                self.sheet.cell(row, col).value = None

    def save_sheet(self, path: str, original_filename: str) -> None:
        self.wb.save(path+'\\_输出文件_'+original_filename+'.xlsx')
        output_usable_sheet_head.main(path+'\\_输出文件_'+original_filename+'.xlsx',
                                      path+'\\__完整文件_'+original_filename+'.xlsx')
        send2trash.send2trash(path+'\\_输出文件_'+original_filename+'.xlsx')


#  以相同数值处理多个表格的类
class ProcessWithSameParameter(ProcessAmazonSheet):

    def __init__(self, sheet_path, _same_parameter):
        ProcessAmazonSheet.__init__(self, sheet_path)
        self._same_parameter = _same_parameter

    def process_sheet(self):
        self.process_title(self._same_parameter['title'])
        self.process_bulletpoints()
        self.process_price(self._same_parameter['price'], self._same_parameter['lowest_pice'])
        self.process_node(self._same_parameter['node'])
        self.process_keywords(self._same_parameter['key_word'])
        self.process_description()
        for row in range(1, 4):
            for col in range(1, 1000):
                self.sheet.cell(row, col).value = None


# 处理亚马逊表格（全部）
def pas_main():
    folder, which_file = pas_utility.index_files()
    if type(which_file) is list:
        for each_file in which_file:
            pas = ProcessAmazonSheet(each_file)
            pas.process_sheet()
            pas.save_sheet(folder, each_file.split('\\')[-1])
    else:
        pas = ProcessAmazonSheet(which_file)
        pas.process_sheet()
        pas.save_sheet(folder, which_file.split('\\')[-1])


# 处理亚马逊表格（部分）
def pas_part():
    folder, which_file = pas_utility.index_files()
    if type(which_file) is list:
        for each_file in which_file:
            pas = ProcessAmazonSheet(each_file)
            print("选择需要单独处理的功能")
            _menu = {'仅处理价格': pas.only_price,
                     '仅标题首字母大写': pas.cap_title
                     }
            pas_utility.make_menu(_menu)
            pas.save_sheet(folder, each_file.split('\\')[-1])
    else:
        pas = ProcessAmazonSheet(which_file)
        print("选择需要单独处理的功能")
        _menu = {'仅处理价格': pas.only_price,
                 '仅标题首字母大写': pas.cap_title
                 }
        pas_utility.make_menu(_menu)
        pas.save_sheet(folder, which_file.split('\\')[-1])


# 以相同参数处理所有选择的表格文件（全部）
def pas_same_para():
    print("输入统一的参数：")
    _same_parameter = {"title": str(input("请输入不需要首字母大写的品牌名(回车跳过)：")),
                       'price': float(input("输入汇率：")),
                       'node': str(input("分类节点(-1跳过)：")),
                       'key_word': str(input("关键词(-1跳过)：")),
                       'lowest_pice': int(input("输入最低价格："))
                       }
    folder, which_file = pas_utility.index_files()
    if type(which_file) is list:
        for each_file in which_file:
            print('开始处理表格：'+each_file.split("\\")[-1])
            pas = ProcessWithSameParameter(each_file, _same_parameter)
            pas.process_sheet()
            pas.save_sheet(folder, each_file.split('\\')[-1])
    else:
        pas = ProcessWithSameParameter(which_file, _same_parameter)
        pas.process_sheet()
        pas.save_sheet(folder, which_file.split('\\')[-1])
    print("处理完成")


def main_function():
    while True:
        try:
            os.system('cls')
            pas_utility.print_current_menu('ERP表格相关')
            _menu = {'退回主菜单': pas_utility.back_to_main_menu,
                     '处理亚马逊表格（全部）': pas_main,
                     '处理亚马逊表格（部分）': pas_part,
                     '以相同参数处理所有选择的表格文件（全部）': pas_same_para}
            pas_utility.make_menu(_menu)
            main_function()
        except Exception as e:
            # raise e
            print(e)
            print('由于以上错误，无法处理本文件，请尝试重新输入正确的文件夹和文件序列号')
            main_function()
        else:
            break
