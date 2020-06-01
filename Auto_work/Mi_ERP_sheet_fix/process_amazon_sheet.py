import os
import load_amazon_sheet
from openpyxl.utils import coordinate_to_tuple
import pas_utilits

""" 
TODO:
    1.完成brand模组
    2.优化交互，操作流程
    3.尝试使用git
"""


class ProcessAmazonSheet(load_amazon_sheet.LoadAmazonSheet):

    def __init__(self, sheet_path):
        try:
            load_amazon_sheet.LoadAmazonSheet.__init__(self, sheet_path)
        except FileNotFoundError as e:
            print("没有找到文件")
            print(str(e))

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
    # test_original_path = os.curdir + "\\水龙头UK_亚马逊表_20200511134434.xlsx"
    # test_working_path = os.curdir

    # time = pas_utilits.get_date()  # "20200522"
    _time = pas_utilits.select_time()
    product = str(input("输入文件名中的产品类别："))
    _country = str(input("输入文件中的国家："))

    lang = str(input("输出文件中的国家："))
    original_file = f"D:\\小米ERP相关数据\\上传产品表格\\{_time}_{product}\\{product}{_country}_亚马逊表_{_time}.xlsx"
    working_path = f"D:\\小米ERP相关数据\\上传产品表格\\{_time}_{product}"

    pas = ProcessAmazonSheet(original_file)
    pas.process_sheet()
    pas.save_sheet(working_path, lang, _time)
    os.startfile(working_path)
