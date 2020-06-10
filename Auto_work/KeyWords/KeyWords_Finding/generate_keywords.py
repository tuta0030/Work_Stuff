import os
import get_keywords_from_amazon_ranking_html as gkw
import tkinter as tk

"""
TODO:
    1.添加获取品牌名的功能
    2.添加替换品牌名的功能
"""

is_update = 0  # 用来让生成关键字的按钮生效的全局变量

KEYWORDSLIMITS = 1000


def gen_new_kw(counter_data: list, kw_to_keep: int) -> str:
    keywords_with_lang = []
    for kw in counter_data:
        lang = kw[:2]
        key_words = kw[4:-2]
        key_words = key_words.split(',')
        new_kw = []
        for word in key_words:
            new_kw.append(''.join(list(filter(None, word.split(':')[0].replace('\'', ' ').split(' ')))).capitalize())
        key_words = ' '.join(new_kw)  # 清楚多余空格之后的关键字
        keywords_with_lang.append(lang+':'+key_words)  # 和国家合并之后的关键字
    _final_data = []
    for word in keywords_with_lang:
        keywords_without_lang = word.split(':')[-1]
        _final_data.append(word.split(':')[0]+': '+trim_data(keywords_without_lang, KEYWORDSLIMITS, kw_to_keep))
    formatted_kw = '\n\n\n'.join(_final_data)
    return formatted_kw


def update_data(amz_page: str, kw_to_keep: int, text_widget: tk.Text, button_widget: tk.Button) -> None:

    def update():
        global is_update
        is_update += 1
        if is_update != 0:
            _data_with_limit = gen_new_kw(gkw.GetKeywords(amz_page).get_key_words_all(), kw_to_keep)
            # rand_int = random.randint(1, 9999)
            text_widget.replace('0.0', 'end', _data_with_limit)
            print(_data_with_limit)
            is_update = 0

    button_widget.configure(command=lambda: update())


def random_kw(_keywords_list: list, kw_to_keep: int) -> list:
    list_head = _keywords_list[:kw_to_keep]
    list_tail = list(set(_keywords_list[kw_to_keep:]))
    return list_head + list_tail


def trim_data(keywords_without_lang: str, limit: int, kw_to_keep: int) -> str:
    _keywords_list = keywords_without_lang.split(' ')
    _keywords_list = random_kw(_keywords_list, kw_to_keep)
    _final_data = []
    for i in range(len(_keywords_list)):
        if len(' '.join(_final_data)) < limit:
            _final_data.append(_keywords_list[i])
    final_data = ' '.join(_final_data)
    final_data = final_data + '\n 字数：' + str(len(final_data))
    return final_data


if __name__ == '__main__':
    AMAZON_PAGES = os.curdir + "\\Amazon_Page"
    _data = gkw.GetKeywords(AMAZON_PAGES).get_key_words_all()
    print(gen_new_kw(_data, 3))
