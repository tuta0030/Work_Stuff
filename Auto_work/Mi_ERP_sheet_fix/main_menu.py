# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 15:06
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : main_menu.py
# @Software: PyCharm

import os
import pas_utilits
import process_amazon_sheet
import brands
import KW_generator

"""
想要添加的特性：
    表格程序：
        1. 优化菜单选项，尽可能分离处理各类数据的选项
    品牌程序：
        1. 添加下载JS Page报错之后自动更换user agent和cookie继续下载的功能
        2. 仅输出一个品牌名替换文本，方便修改和调用
    关键词程序：
        1. 添加列出当先可以直接生成的关键词的菜单
        2. 添加可以直接调用现有的品牌名输出文件的功能
"""

menu = {}


def main_menu():
    while True:
        try:
            os.system('cls')
            pas_utilits.add_function(menu, 1, 'ERP表格相关', process_amazon_sheet.main_function)
            pas_utilits.add_function(menu, 2, '品牌相关', brands.whole_function)
            pas_utilits.add_function(menu, 3, '关键词相关', KW_generator.main)
            pas_utilits.add_function(menu, 4, '打开根目录', pas_utilits.open_folder)
            pas_utilits.add_function(menu, 0, '退出', quit)
            pas_utilits.intro(menu)
            ui = str(input('输入需要的选项：'))
            pas_utilits.show_menu(ui, menu)
        except Exception as e:
            print(e)
        else:
            break


if __name__ == '__main__':
    main_menu()
