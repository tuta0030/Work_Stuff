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
    import system_hotkey
    import keyboard
    from main_menu import main_menu
    while True:
        try:
            hotkey_random_clipboard = system_hotkey.SystemHotkey()
            hotkey_random_clipboard.register(('control', 'shift', 'r'), callback=random_clipboard)
            keyboard.wait('esc')
            main_menu()
        except Exception as e:
            raise e
        else:
            break
