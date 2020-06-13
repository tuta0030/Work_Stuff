# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 15:06
# @Author  : Eric_Shenarrzine
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : main_menu.py
# @Software: PyCharm

import os
import pas_utilits
from process_amazon_sheet import ProcessAmazonSheet
import brands

""" 
TODO:
    2.优化交互，操作流程
        2.2 兼容erp直接输出的文件日期名称
"""

menu = {}


def main_function():
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


def main_menu():
    while True:
        try:
            os.system('cls')
            pas_utilits.add_function(menu, 1, '表格处理主程序', main_function)
            pas_utilits.add_function(menu, 2, '品牌处理程序', brands.whole_function)
            pas_utilits.add_function(menu, 3, '退出', quit)
            pas_utilits.intro(menu)
            ui = str(input('输入需要的选项：'))
            pas_utilits.show_menu(ui, menu)
        except Exception as e:
            print(e)
        else:
            break


if __name__ == '__main__':
    main_menu()
