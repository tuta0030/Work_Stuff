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


def check_bottom():
    global _is_bottom
    _t = threading.current_thread()
    while getattr(_t, 'do_run', True):
        bottom = pyautogui.locateCenterOnScreen(r'web_page_bottom.png')
        if bottom:
            _is_bottom = True
            print(f'Find bottom {bottom} {_is_bottom}')
    print('Stop the check_bottom thread...')


if __name__ == '__main__':
    _is_bottom = False
    t = threading.Thread(target=check_bottom)
    t.start()
    while True:
        pyautogui.scroll(-150)
        pyautogui.sleep(0.3)
        if _is_bottom is True:
            t.do_run = False
            break
