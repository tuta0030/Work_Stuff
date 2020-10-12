# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 15:06
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : main_menu.py
# @Software: PyCharm

from Auto_work.Mi_ERP_sheet_fix import pas_utility
from Auto_work.Mi_ERP_sheet_fix import process_amazon_sheet
from Auto_work.Auto_oofay.Generate_random_keywords_bulletpoints import KW_generator
from Auto_work.Auto_oofay.Make_working_folders_and_logs import make_folder_and_log
from Auto_work.Make_invoice import generate_invoice
from Auto_work.Mi_ERP_sheet_fix.Process_text_files import text_process
from Auto_work.Mi_ERP_sheet_fix.Auto_translate import auto_translate


def main_menu():
    while True:
        try:
            auto_translate.make_txt_hotkey()
            pas_utility.intro()
            _menu = {'退出': pas_utility.main_menu_quit,
                     'ERP表格相关': process_amazon_sheet.main_function,
                     '关键词相关': KW_generator.menu,
                     '五点描述': KW_generator.KWu.random_bullet_point,
                     '解析ASIN，价格和主图链接': pas_utility.asin_price_menu,
                     '创建工作文件夹': make_folder_and_log.main,
                     '生成发票': generate_invoice.main,
                     '文本处理程序(输出翻译文件)': text_process.main,
                     }
            pas_utility.make_menu(_menu)
        except Exception as e:
            raise e
            print(e)
            print('由于以上错误导致程序出错，请重试')
            input('回车继续')
            pas_utility.back_to_main_menu(enter_quit=True)
        else:
            break


if __name__ == '__main__':
    main_menu()
