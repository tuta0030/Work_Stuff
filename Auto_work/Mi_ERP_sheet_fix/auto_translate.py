import pynput
import pyperclip
import os
import pyautogui


def make_txt_hotkey():

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


def check_bottom() -> bool:
    while True:
        bottom = pyautogui.locateCenterOnScreen(r'web_page_bottom.png')
        if bottom:
            print(f'Find bottom {bottom}')
            break
    return True


if __name__ == '__main__':
    print(check_bottom())
