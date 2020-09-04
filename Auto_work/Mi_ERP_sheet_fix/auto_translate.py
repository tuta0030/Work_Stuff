import pynput
import pyperclip
import os
import pyautogui
import threading

LANGUAGES_PNG = {
                 'DE': 'translate_DE.png',
                 'FR': 'translate_FR.png',
                 'IT': 'translate_IT.png',
                 'ES': 'translate_ES.png',
                 'JP': 'translate_JP.png',
                 'NL': 'translate_NL.png',
                 }


def make_txt_hotkey(**kwargs):
    """使用剪贴板生成utf-8文本文件的全局快捷键"""
    _f_name = kwargs.get('file_name', '剪贴板中内容创建的utf-8文件')

    def main():
        def past_content_into_utf_txt():
            print('Global hotkey activated!')
            out_path = 'c:\\hotkey_folder'
            if not os.path.isdir(out_path):
                os.mkdir(out_path)
            with open(f'{out_path}\\{_f_name}.txt', 'w', encoding='utf-8') as f:
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
            print(f'已到页面底部 {bottom} {_is_bottom}')
    print('停止查找页面底部线程...')


if __name__ == '__main__':
    js_auto_scroll = """setInterval(function(){window.scrollBy(0,50);},100);"""
    _is_bottom = False

    def select_all():
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.sleep(1)

    def save_with_file_name(file_name: str):
        out_path = 'c:\\hotkey_folder'
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        with open(f'{out_path}\\{file_name}.txt', 'w', encoding='utf-8') as f:
            f.write(pyperclip.paste())

    def get_folder_name() -> str:
        while True:
            t_icon = pyautogui.locateCenterOnScreen('translate_icon.png')
            print(t_icon)
            if t_icon:
                pyautogui.moveTo(t_icon)
                pyautogui.moveRel(-100, 0)
                pyautogui.leftClick()
                select_all()
                content = pyperclip.paste()
                return str(content).split('/')[-2]

    def change_translate_language(target_lang):
        """which_language 需要传入需要定位的语言的png图像"""
        while True:
            t_icon = pyautogui.locateCenterOnScreen('translate_icon.png')
            print(f'找到翻译按钮 {t_icon}')
            if t_icon:
                pyautogui.moveTo(t_icon)
                pyautogui.leftClick()
                pyautogui.moveRel(0, 40)
                pyautogui.leftClick()
                pyautogui.sleep(0.5)
                pyautogui.moveRel(0, 40)
                pyautogui.leftClick()
                pyautogui.sleep(0.5)
                pyautogui.leftClick()
                pyautogui.sleep(0.5)
                pyautogui.moveRel(180, 0)
                while True:
                    t_lang = pyautogui.locateCenterOnScreen(target_lang)
                    if not t_lang:
                        pyautogui.scroll(-1000)
                    elif t_lang:
                        pyautogui.moveTo(t_lang)
                        pyautogui.leftClick()
                        pyautogui.sleep(0.5)
                        while True:
                            t_confirm = pyautogui.locateCenterOnScreen('translate_confirm_button.png')
                            if t_confirm:
                                pyautogui.moveTo(t_confirm)
                                pyautogui.leftClick()
                                print(f'找到确定按钮 {t_confirm}')
                                pyautogui.moveRel(0, 100)
                                pyautogui.leftClick()
                                return True


    def auto_translate(key_lang, value_png):
        if change_translate_language(value_png):
            thread_check_bottom = threading.Thread(target=check_bottom)
            thread_check_bottom.start()
            while not _is_bottom:
                pyautogui.scroll(-500)
                pyautogui.sleep(0.4)
            else:
                thread_check_bottom.do_run = False
                _file_name = get_folder_name() + '_' + key_lang
                pyautogui.moveRel(0, 200)
                pyautogui.sleep(0.5)
                pyautogui.leftClick()
                pyautogui.keyDown('home')
                pyautogui.sleep(0.5)
                pyautogui.keyUp('home')
                pyautogui.sleep(0.5)
                select_all()
                save_with_file_name(_file_name)


    for _key_lang, _value_png in LANGUAGES_PNG.items():
        auto_translate(_key_lang, _value_png)
        _is_bottom = False
    os.startfile('c:\\hotkey_folder')
