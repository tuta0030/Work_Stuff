# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 10:46
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : KW_generator_utility.py
# @Software: PyCharm

import re
import os
from brands_utility import FILE_NAME_BRAND_FILE


def write_keywords_to_working_txt(working_txt_path, g_keywords) -> None:
    with open(working_txt_path, 'a', encoding='utf-8') as w:
        oc_content = w.read()
        _pattern = re.compile(r'关键字keywords.+内容简介features')
        re.sub(_pattern, oc_content, g_keywords)
    return None


def read_brand_file() -> str:
    brands = open(FILE_NAME_BRAND_FILE, 'r', encoding='utf-8').read()
    return brands


def find_storage_path() -> str:
    if os.path.isdir(open(os.curdir+'\\main_folder_path.txt', 'r', encoding='utf-8').read()):
        return open(os.curdir+'\\main_folder_path.txt', 'r', encoding='utf-8').read()
    else:
        with open(os.curdir+'\\main_folder_path.txt', 'w', encoding='utf-8') as f:
            f.write(input('未找到品牌和关键词的根目录，输入需要设定的文件夹路径：'))


def how_many_type(data_base_path: str) -> list:
    kw_db_option_pattern = re.compile(r'.+(?=:{)')
    result = re.findall(kw_db_option_pattern, open(data_base_path, 'r', encoding='utf-8').read())
    index = 0
    indexed_result = []
    for item in result:
        indexed_result.append((index, item))
        index += 1
    print(f"\n\n已有关键词：{indexed_result[1:]}")
    return result


def indexing_kw_db(ui, how_many_type_returned_value: list) -> str:
    index = 1
    types = {}
    which_type = ''
    for item in how_many_type_returned_value:
        types[index] = item
    for each_selection in types.keys():
        if ui == str(each_selection):
            which_type = types[each_selection]
    return which_type
