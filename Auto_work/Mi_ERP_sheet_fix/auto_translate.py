import pynput
import pyperclip
import os


def make_txt_hotkey():

    def on_activate():
        print('Global hotkey activated!')
        out_path = 'c:\\hotkey_folder'
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        with open(f'{out_path}\\剪贴板中内容创建的utf-8文件.txt', 'w', encoding='utf-8') as f:
            f.write(pyperclip.paste())
        os.startfile(out_path)

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    hotkey = pynput.keyboard.HotKey(pynput.keyboard.HotKey.parse('<ctrl>+<shift>+f'), on_activate)

    with pynput.keyboard.Listener(on_press=for_canonical(hotkey.press),
                                  on_release=for_canonical(hotkey.release)) as listener:
        listener.join()
        listener.stop()


make_txt_hotkey()
