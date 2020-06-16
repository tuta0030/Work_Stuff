# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 17:12
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : generating_kw_from_html.py
# @Software: PyCharm

import os


def validate_html_path():
    try:
        if os.path.isfile(os.curdir+'\\html_path.txt'):
            html_path = open('html_path.txt', 'r', encoding='utf-8').read()
        else:
            with open('html_path.txt', 'w', encoding='utf-8') as f:
                f.write(str(input("未找到亚马逊html页面路径，请输入亚马逊html文件夹路径:")))
    except Exception as e:
        raise e
