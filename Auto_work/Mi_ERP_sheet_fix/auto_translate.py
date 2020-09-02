import pynput
import pyperclip
import os
import pyautogui
import threading


def make_txt_hotkey():
    """使用剪贴板生成utf-8文本文件的全局快捷键"""
    def main():
        def past_content_into_utf_txt():
            print('Global hotkey activated!')
            out_path = 'c:\\hotkey_folder'
            if not os.path.isdir(out_path):
                os.mkdir(out_path)
            with open(f'{out_path}\\剪贴板中内容创建的utf-8文件.txt', 'w', encoding='utf-8') as f:
                f.write(pyperclip.paste())
            os.startfile(out_path)

        def for_canonical(f):
            return lambda k: f(listener.canonical(k))

        hotkey = pynput.keyboard.HotKey(pynput.keyboard.HotKey.parse('<ctrl>+<shift>+f'), past_content_into_utf_txt)

        with pynput.keyboard.Listener(on_press=for_canonical(hotkey.press),
                                      on_release=for_canonical(hotkey.release)) as listener:
            listener.join()
            listener.stop()

    hotkey_thread = threading.Thread(target=main)
    hotkey_thread.start()


def check_bottom() -> bool:
    while True:
        bottom = pyautogui.locateCenterOnScreen(r'web_page_bottom.png')
        if bottom:
            print(f'Find bottom {bottom}')
            break
    return True


if __name__ == '__main__':
    v2ray_purple = pyautogui.locateCenterOnScreen('v2ray_purple.png')
    pyautogui.moveTo(v2ray_purple)
    pyautogui.rightClick()
    pyautogui.moveTo(1376, 911)
