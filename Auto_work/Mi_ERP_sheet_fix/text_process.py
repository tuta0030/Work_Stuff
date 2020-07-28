# -*- coding: utf-8 -*-
# @Time    : 2020/7/28 13:42
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : text_process.py
# @Software: PyCharm


def random_clipboard():
    import pyperclip
    from random import sample

    content = pyperclip.paste()
    content = content.split(' ')
    content = ' '.join(sample(content, len(content)))
    pyperclip.copy(content)
    pyperclip.paste()
    print(pyperclip.paste())


def title_case():
    import pyperclip

    content = pyperclip.paste()
    content = content.split(' ')
    content = [str(each_word).capitalize() for each_word in content]
    content = ' '.join(content)
    pyperclip.copy(content)
    print(pyperclip.paste())


def main_loop():
    while True:
        try:
            print('Not working yet...')
        except Exception as e:
            raise e
        else:
            break
