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


def main_menu():
    while True:
        try:
            os.system('cls')
            pas_utility.intro()
            _menu = {'退出': pas_utility.main_menu_quit,
                     'ERP表格相关': process_amazon_sheet.main_function,
                     '关键词相关': KW_generator.menu,
                     '爬取ASIN，价格和主图链接': pas_utility.asin_price_menu
                     }
            pas_utility.make_menu(_menu)
        except Exception as e:
            raise e
        else:
            break


if __name__ == '__main__':
    main_menu()
