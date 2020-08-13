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
import make_folder_and_log
import generate_invoice
import text_process


def main_menu():
    while True:
        try:
            pas_utility.intro()
            _menu = {'退出': pas_utility.main_menu_quit,
                     'ERP表格相关': process_amazon_sheet.main_function,
                     '关键词相关': KW_generator.menu,
                     '解析ASIN，价格和主图链接': pas_utility.asin_price_menu,
                     '创建工作文件夹': make_folder_and_log.main,
                     '五点描述': KW_generator.KWu.random_bullet_point,
                     '生成发票': generate_invoice.main,
                     '文本处理程序(输出翻译文件)': text_process.main,
                     }
            pas_utility.make_menu(_menu)
        except Exception as e:
            raise e
            print(e)
            print('由于以上错误导致程序出错，请重试')
            input('回车继续')
            main_menu()
        else:
            break


if __name__ == '__main__':
    main_menu()
