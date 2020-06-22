# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 15:06
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : main_menu.py
# @Software: PyCharm

import os
import pas_utility
import process_amazon_sheet
import KW_generator

"""
TODO：
    1. 高频词首字母大写，去重，去自己的品牌名
    2. 添加单独批量处理部分表格内容的功能 √
    3. 根据sku或ean码，将目标文件夹中的所有包含本sku或ean的产品整理成新的delete表格 √
"""


def main_menu():
    while True:
        try:
            os.system('cls')
            pas_utility.intro()
            _menu = {'退出': pas_utility.main_menu_quit,
                     'ERP表格相关': process_amazon_sheet.main_function,
                     '关键词相关': KW_generator.menu,
                     }
            pas_utility.make_menu(_menu)
        except Exception as e:
            raise e
        else:
            break


if __name__ == '__main__':
    main_menu()
