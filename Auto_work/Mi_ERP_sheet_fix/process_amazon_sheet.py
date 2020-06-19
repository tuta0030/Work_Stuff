import os
import load_amazon_sheet
from openpyxl.utils import coordinate_to_tuple
import pas_utility as pasu
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
            print(pasu.NO_FILE)
            raise _e

    def cap_title(self):
        brand = input("输入不需要大写的品牌名（没有的话按回车继续）：")
        item_name_coordinate = pasu.get_coordinate(self.item_name_cell)
        title_list = pasu.get_column_until_none_cell(self.sheet,
                                                     item_name_coordinate[0],
                                                     item_name_coordinate[1])
        for index, title in enumerate(title_list):
            title_list[index].value = pasu.cap_title(title.value, brand)

    def process_title(self, brand: str):
        item_name_coordinate = pasu.get_coordinate(self.item_name_cell)
        title_list = pasu.get_column_until_none_cell(self.sheet,
                                                     item_name_coordinate[0],
                                                     item_name_coordinate[1])
        self.all_titles = [each_title.value for each_title in title_list]
        for index, title in enumerate(title_list):
            title_list[index].value = pasu.process_item_name(title.value, brand)

    def process_description(self):
        description_coordinate = pasu.get_coordinate(self.description)
        pasu.process_description(self.sheet, description_coordinate)

    def process_bulletpoints(self):
        bullet_point_coordinate = pasu.get_coordinate(self.bullet_point_cell)
        pasu.process_bulletpoints(self.sheet, bullet_point_coordinate)

    def process_price(self, exchange_rate: float, lowest_price: int):
        price_coordinate = pasu.get_coordinate(self.price_cell)
        pasu.process_price(self.sheet, price_coordinate, exchange_rate, lowest_price)

    def process_node(self, node):
        node_coordinate = pasu.get_coordinate(self.node_cell)
        pasu.process_info(self.sheet, node_coordinate, node)

    def process_update_delete(self, _same_parameter: dict):
        update_coordinate = pasu.get_coordinate(self.update_delete)
        pasu.process_info(self.sheet, update_coordinate, _same_parameter['update_delete'])

    def process_keywords(self, keywords: str):
        if keywords == SECRET_CODE:
            processed_keywords = ' '.join(pasu.high_frequent_words(self.all_titles)) \
                                     .replace(',', '').replace('*', '').replace(BRAND_TO_REPLACE_KW, '') \
                                     .replace('(', '').replace(')', '')[:KW_TRIMMER]
            processed_keywords = processed_keywords.replace('  ', ' ')
            keywords_coordinate = coordinate_to_tuple(str(self.keywords_cell).split('.')[-1][:-1])
            pasu.process_info(self.sheet, keywords_coordinate, processed_keywords)
        else:
            keywords_coordinate = coordinate_to_tuple(str(self.keywords_cell).split('.')[-1][:-1])
            pasu.process_info(self.sheet, keywords_coordinate, keywords)

    def process_item_type(self, keywords: str):
        keywords_coordinate = coordinate_to_tuple(str(self.item_type_cell).split('.')[-1][:-1])
        pasu.process_info(self.sheet, keywords_coordinate, keywords)

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

    def save_sheet(self, path: str, original_file: str) -> None:
        file_name = original_file.split('\\')[-1]
        _out_put_file_name = '\\_输出文件_' + file_name + '.xlsx'
        self.wb.save(_out_put_file_name)
        output_usable_sheet_head.main(path+'\\'+original_file,
                                      _out_put_file_name,
                                      path + '\\__完整文件_' + file_name + '.xlsx')
        send2trash.send2trash(_out_put_file_name)


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


# 处理亚马逊表格（单独功能）
def pas_part():
    # key:功能描述， value:需要调用的函数名称
    part_functions = {'仅处理价格': 'only_price',
                      '仅标题首字母大写': 'cap_title',
                      '仅处理关键词': 'process_keywords'
                      }
    func_name = pasu.make_menu_part_functions(part_functions)
    if func_name == 'process_keywords':
        _parameter = {}
        pasu.multiple_file_process(ProcessWithSameParameter,
                                   _parameter,
                                   process_method=func_name,
                                   method_para=str(input("关键词(-1跳过)：")))
    else:
        _parameter = {}
        pasu.multiple_file_process(ProcessWithSameParameter, _parameter, process_method=func_name)


# 处理选择的表格文件（全部）
def pas_same_para():
    print("输入统一的参数：")
    _parameter = {"title": str(input("请输入不需要首字母大写的品牌名(回车跳过)：")),
                  'price': float(input("输入汇率：")),
                  'node': str(input("分类节点(-1跳过)：")),
                  'key_word': str(input("关键词(-1跳过)：")),
                  'lowest_pice': int(input("输入最低价格："))
                  }
    pasu.multiple_file_process(ProcessWithSameParameter,
                               _parameter,
                               process_method='process_sheet')


# 更新或下架产品
def pas_update_delete():
    _ui = input('选择需要的选项：0: delete, 1: update:')
    _ui = 'delete' if _ui == '0' else 'update'
    _parameters = {'update_delete': _ui}
    pasu.multiple_file_process(ProcessWithSameParameter,
                               _parameters,
                               process_method='process_update_delete',
                               _parameter=_parameters,
                               method_para=_parameters
                               )


def main_function():
    while True:
        try:
            os.system('cls')
            pasu.print_current_menu('ERP表格相关')
            _menu = {'退回主菜单': pasu.back_to_main_menu,
                     '处理选择的表格文件（单独功能）': pas_part,
                     '处理选择的表格文件（全部功能）': pas_same_para,
                     '更新或下架产品': pas_update_delete}
            pasu.make_menu(_menu)
            main_function()
        except Exception as e:
            raise e
            print(e)
            input('由于以上错误，无法处理本文件，请尝试重新输入正确的文件夹和文件序列号')
            main_function()
        else:
            break
