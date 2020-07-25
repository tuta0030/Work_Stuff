# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 10:46
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : KW_generator_utility.py
# @Software: PyCharm

import re
import os
import json
import pas_utility as pasu
import pyperclip
from random import sample
from send2trash import send2trash

UNI_CHAR = r'[\u4E00-\u9FA5\u00A0-\u00FF\u0100-\u017F\u0180-\u024F\u2E80-\u9FFFa-zA-Z0-9\'?]+\s'
PATH_MAIN = os.curdir
PATH_DATA_BASE = PATH_MAIN + r'\KW_data_base.txt'
NO_DB_MSG = r'没有找到关键词数据，请确认关键词已经添加到以下文件：E:\TUTA\文档\Python\创建工作日志和工作文件夹\KW_data_base.txt， 已自动创建文件模板'
BP_HINT = '在此文件中添加新的五点描述，每条描述用回车隔开'


def write_keywords_to_working_txt(working_txt_path, g_keywords) -> None:
    with open(working_txt_path, 'a', encoding='utf-8') as w:
        oc_content = w.read()
        _pattern = re.compile(r'关键字keywords.+内容简介features')
        re.sub(_pattern, oc_content, g_keywords)
    return None


def find_storage_path() -> str:
    if os.path.isdir(open(os.curdir+'\\main_folder_path.txt', 'r', encoding='utf-8').read()):
        return open(os.curdir+'\\main_folder_path.txt', 'r', encoding='utf-8').read()
    else:
        with open(os.curdir+'\\main_folder_path.txt', 'w', encoding='utf-8') as f:
            f.write(input('未设定输出关键词的文件夹，输入需要设定的文件夹路径：'))
        return open(os.curdir+'\\main_folder_path.txt', 'r', encoding='utf-8').read()


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


def show_current_kw_types() -> dict:
    check_data_base()
    kw_types = how_many_type()
    indexed_kw_types = indexing_kw_type(kw_types)
    print("当前已有关键词：")
    print(str(indexed_kw_types)[1:-1])
    return indexed_kw_types


def check_data_base():
    if os.path.isfile(PATH_DATA_BASE):
        return True
    else:
        with open(PATH_DATA_BASE, 'a', encoding='utf-8') as kw:
            kw.write("这句话替换成产品类目并添加对应国家的关键字到括号内：{\n\nEN: \nFR: \nDE: \nIT: \nES:\n\n}这句话替换成产品类目并添加对应国家的关键字到括号内")
        print(NO_DB_MSG)
        os.startfile(PATH_DATA_BASE)


def process_new_kw():
    ui = input("输入添加的关键词名称：")
    new_kw_content = open('new_kw_temp.txt', 'r', encoding='utf-8').read().replace('格式示例，如果没有这些国家可以删掉', '')
    with open('KW_data_base.txt', 'a', encoding='utf-8') as f:
        f.write('\n')
        f.write('\n')
        f.write(ui+':{')
        f.write('\n')
        f.write(new_kw_content)
        f.write('\n')
        f.write('\n')
        f.write('}'+ui)


def edit_bullet_points():
    #           0.1: add bullet points into file
    #           0.2: remove bullet points
    #           0.3: edit specific catagory's bullet points
    def save_json_file(file):
        with open('random_bullet_points.json', 'w', encoding='utf-8') as f:
            json.dump(file, f, ensure_ascii=False)

    def index_rbp_json(json_content: dict):
        _index = 0
        _indexed_json_content = {}
        for k, v in json_content.items():
            _indexed_json_content[(_index, k)] = v
            print(_index, end='\t')
            print(k)
            _index += 1
        _which_product = input('请选择(-1退出)：')
        if _which_product == str(-1):
            edit_bullet_points()
        for k, v in _indexed_json_content.items():
            _index, key = k
            if _which_product == str(_index):
                print(f'已选择：{key}')
                return key

    def add_bp(current_bp: list):
        if current_bp is None or current_bp == []:
            current_bp = []
        with open('new_bp_template.txt', 'w', encoding='utf-8') as f:
            f.write(BP_HINT)
            for each_bp in current_bp:
                f.write(each_bp)
                f.write('\n')
        os.startfile('new_bp_template.txt')
        is_finished = input('是否添加完成(y/n)?')
        if is_finished == 'y':
            return_list = open('new_bp_template.txt', 'r', encoding='utf-8').read().replace(BP_HINT, '').split('\n')
            return_list = [each_line[:-1] for each_line in return_list if each_line.strip().endswith('.')]
            send2trash('new_bp_template.txt')
            return_list = [each_line for each_line in return_list if each_line != '']
            print(return_list)
            input('回车继续')
            return return_list
        else:
            print('未添加完成，取消添加...')
            send2trash('new_bp_template.txt')

    def add_bullet_points():
        file = open('random_bullet_points.json', 'r', encoding='utf-8').read()
        file = json.loads(file)
        
        which_product = input('请输入需要添加的内容名称：')
        if which_product not in file.keys():
            print('没有此名称，添加新的内容...')
            file[which_product] = add_bp([])
            save_json_file(file)
        else:
            file = open('random_bullet_points.json', 'r', encoding='utf-8').read()
            file = json.loads(file)
            print('已有名称，添加更多...')
            file[which_product] = add_bp(file[which_product])
            save_json_file(file)
        pasu.back_to_main_menu()

    def remove_bullet_points():
        file = open('random_bullet_points.json', 'r', encoding='utf-8').read()
        file = json.loads(file)
        which_product = index_rbp_json(file)
        print(f'删除{file[which_product]}')
        del file[which_product]
        save_json_file(file)
        pasu.back_to_main_menu()

    _menu = {'返回': random_bullet_point,
             '添加五点描述': add_bullet_points,
             '删除五点描述': remove_bullet_points
             # '编辑五点描述': edit_which
             }
    pasu.make_menu(_menu)


def mk_random_bulletpoints() -> str:
    content = open('random_bullet_points.json', 'r', encoding='utf-8').read()
    content = json.loads(content)

    def index_rbp_json(json_content: dict):
        _index = 0
        _menu = {}
        for k, v in json_content.items():
            _menu[(_index, k)] = v
            print(_index, end='\t')
            print(k)
            _index += 1
        _which_product = input('请选择：')
        for k, v in _menu.items():
            _index, key = k
            if _which_product == str(_index):
                print(f'已选择：{key}')
                return '\n'.join(sample(v, 5))

    _out_bullet_points = index_rbp_json(content)
    print(_out_bullet_points)
    pyperclip.copy(_out_bullet_points)

    def _again():
        again = input('是否再次生成？(y/n):')
        if again == 'y':
            mk_random_bulletpoints()
        elif again == 'n':
            pasu.back_to_main_menu()
        else:
            '请输入y或n'
            _again()
    _again()
    return _out_bullet_points


def random_bullet_point():
    _menu = {'回主菜单': pasu.back_to_main_menu,
             '编辑五点描述': edit_bullet_points,
             '生成随机五点描述': mk_random_bulletpoints}
    pasu.make_menu(_menu)
