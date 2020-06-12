import os
import re
from lxml import etree
import collections
import tkinter as tk


def config_brand(path):
    os.startfile(path)


def get_amazon_pages_path(amazon_dir_path: str) -> dict:
    amazon_pages_path = {}
    for i in os.listdir(amazon_dir_path):
        amazon_pages_path[f'{i[:2]}'] = os.path.abspath(amazon_dir_path)+'\\'+i
    return amazon_pages_path


def get_html_element(html: str):
    html_etree_element = etree.HTML(html, etree.HTMLParser())
    return html_etree_element


def get_all_html(amazon_pages_path: dict) -> dict:
    html_s = {}
    for k, v in amazon_pages_path.items():
        html_s[k] = open(v, 'r', encoding='utf-8').read()
    return html_s


def remove_words(word_list: list, all_title: str) -> str:  # TODO 更好地替换
    for i in word_list:
        pattern = re.compile(i)
        all_title = re.sub(pattern, '', all_title)
    single_digits = re.compile(open('品牌名称.txt', 'r', encoding='utf-8').read())
    all_title = re.sub(single_digits, ' ', all_title)
    return all_title


def count_frequency(all_title: list) -> dict:
    frequency_dict = collections.Counter(all_title)
    return frequency_dict


def trim_data(data_list: list) -> str:
    trimmed_data = []
    for i in data_list:
        i = i.split(',')
        i = i[:50]
        i = ','.join(i)
        i = i.replace(',', '\n')
        trimmed_data.append(i)
    trimmed_data = '\n\n\n\n'.join(trimmed_data)
    return trimmed_data


def save_amz_kw(data: str, data_base_path: str, kw_name: str) -> None:
    if len(kw_name) > 0:
        with open(data_base_path, 'a', encoding='utf-8') as kw_db:
            kw_db.write(kw_name+':{\n')
            kw_db.write(data)
            kw_db.write('}'+kw_name)


def load_kw_db_keywords(path_of_kw_db: str) -> str:  # TODO
    pass


def validate_entry(entry: tk.Entry) -> int:  # TODO
    print('entry里的内容：')
    content = entry.get()
    print(content)
    return 0


if __name__ == '__main__':
    paths = os.curdir + "\\Amazon_Page"
    print(get_amazon_pages_path(paths))
