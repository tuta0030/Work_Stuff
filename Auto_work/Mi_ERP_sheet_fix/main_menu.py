# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 15:06
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : main_menu.py
# @Software: PyCharm

import os
import pas_utility
import process_amazon_sheet
import brands
import KW_generator

"""
待添加功能：
    表格程序：
        1. 添加可以选择处理多个表格文件的功能 √
    品牌程序：
        1. 添加下载JS Page报错之后自动更换user agent和cookie继续下载的功能
        3. 添加通过排名页面生成关键词的功能
    关键词程序：
        0. 优化关键词库的交互
            0.0 关键词显示的时候将关键词添加索引的功能 √
            0.1 可以选择特定关键词添加特定语言的功能
            0.2 可以选择重命名某个关键词类别的功能 √
            0.3 可以添加新的关键词的功能
        1. 添加从下载好的亚马逊html页面中获取高频率关键词的功能
            1.1 验证各国html文件路径
            1.2 从html文件夹中导入html文件并解析标题
"""


def main_menu():
    while True:
        try:
            os.system('cls')
            pas_utility.intro()
            _menu = {'退出': pas_utility.main_menu_quit,
                     'ERP表格相关': process_amazon_sheet.main_function,
                     '品牌相关': brands.whole_function,
                     '关键词相关': KW_generator.menu,
                     '打开根目录': pas_utility.open_folder,
                     }
            pas_utility.make_menu(_menu)
        except Exception as e:
            raise e
        else:
            break


if __name__ == '__main__':
    main_menu()
