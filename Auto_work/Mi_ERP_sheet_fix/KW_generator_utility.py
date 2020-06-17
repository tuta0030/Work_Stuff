# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 10:46
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : KW_generator_utility.py
# @Software: PyCharm

import re
import os
from brands_utility import FILE_NAME_BRAND_FILE

UNI_CHAR = r'[\u4E00-\u9FA5\u00A0-\u00FF\u0100-\u017F\u0180-\u024F\u2E80-\u9FFFa-zA-Z0-9\'?]+\s'
PATH_MAIN = os.curdir
PATH_DATA_BASE = PATH_MAIN + r'\KW_data_base.txt'
NO_DB_MSG = r'没有找到关键词数据，请确认关键词已经添加到以下文件：E:\TUTA\文档\Python\创建工作日志和工作文件夹\KW_data_base.txt， 已自动创建文件模板'


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


# 将所有包含各国字符的关键词以列表形式返回
def get_db_conten_as_words_list(_data_base):
    _pattern = re.compile(UNI_CHAR)
    _result = re.findall(_pattern, str(_data_base))
    return _result


def how_many_type() -> list:
    kw_db_option_pattern = re.compile(r'.+(?=:{)')
    result = re.findall(kw_db_option_pattern, open(PATH_DATA_BASE, 'r', encoding='utf-8').read())
    index = 0
    indexed_result = []
    for item in result:
        indexed_result.append((index, item))
        index += 1
    return result


def indexing_kw_type(kw_types: list) -> dict:
    index = 0
    _indexed_types = {}
    for item in kw_types:
        _indexed_types[index] = item
        index += 1
    del _indexed_types[0]
    return _indexed_types


def show_current_kw_types(indexed_kw_type: dict):
    print("当前已有关键词：")
    print(str(indexed_kw_type)[1:-1])


def check_data_base():
    if os.path.isfile(PATH_DATA_BASE):
        return True
    else:
        with open(PATH_DATA_BASE, 'a', encoding='utf-8') as kw:
            kw.write("这句话替换成产品类目并添加对应国家的关键字到括号内：{\n\nEN: \nFR: \nDE: \nIT: \nES:\n\n}这句话替换成产品类目并添加对应国家的关键字到括号内")
        print(NO_DB_MSG)
        os.startfile(PATH_DATA_BASE)