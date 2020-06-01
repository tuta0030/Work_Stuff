import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolled_text
import config_files
import get_keywords_from_amazon_ranking_html as gkw
import os
import generate_keywords


LARGE_FONT = ("Verdana", 12)
BRAND_TEXT = os.curdir + "\\品牌名称.txt"
AMAZON_PAGES = open(os.curdir + "\\亚马逊页面.txt", 'r', encoding='utf-8').read()
KEYWORDS_LENGTH = 200
DATA_BASE_PATH = os.pardir+r'\KeyWords_Generating\KW_data_base.txt'
KW_TO_KEEP = int(open(os.curdir+'\\需要保留的关键词数量.txt').read())


class GUILayout(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("创建关键词")
        self.resolution = "800x600"
        self.geometry(self.resolution)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, KeyWordsPage, GenKeyWordsPage, ExistKeyWords):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='首页', font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        button_config_brand = ttk.Button(self, text='修改品牌名称文件',
                                         command=lambda: config_files.config_brand(BRAND_TEXT))
        button_config_brand.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')

        button_get_keywords = ttk.Button(self, text='查看关键词频率',
                                         command=lambda: controller.show_frame(KeyWordsPage))
        button_get_keywords.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')

        button_get_keywords = ttk.Button(self, text='通过亚马逊页面生成新的关键词',
                                         command=lambda: controller.show_frame(GenKeyWordsPage))
        button_get_keywords.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')

        button_get_keywords = ttk.Button(self, text='从关键词库生成新的关键词(不能用)',
                                         command=lambda: controller.show_frame(ExistKeyWords))
        button_get_keywords.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')


class KeyWordsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='从亚马逊页面获取的关键词（仅显示前50个词）', font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        button_config_brand = ttk.Button(self, text='返回首页',
                                         command=lambda: controller.show_frame(StartPage))
        button_config_brand.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')

        data = gkw.GetKeywords(AMAZON_PAGES).get_key_words_all()
        data = config_files.trim_data(data)
        text = scrolled_text.ScrolledText(self)
        text.insert('end', data)
        text.pack(padx=10, pady=10, expand=True, fill='both')


class GenKeyWordsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text='关键词', font=LARGE_FONT)
        # label_how_many = tk.Label(self, text='需要保留的关键位数', font=LARGE_FONT)
        button_back_to_home = ttk.Button(self, text='返回首页',
                                         command=lambda: controller.show_frame(StartPage))

        # 文本框更新
        text = scrolled_text.ScrolledText(self)
        button_gen_kw = ttk.Button(self, text='生成关键字')
        # e_how_many_to_keep = tk.Entry(self, text='输入需要保留的关键词位数(默认保留前5个词)')

        # _kw_to_keep = config_files.validate_entry(e_how_many_to_keep)

        generate_keywords.update_data(AMAZON_PAGES, KW_TO_KEEP, text, button_gen_kw)

        #  TODO 保存关键字
        # label_kw_name = tk.Label(self, text='输入关键词名称', font=LARGE_FONT)
        # e_kw_name = tk.Entry(self, text="关键词名称")
        # button_save_kw = ttk.Button(self, text='保存关键词到关键词库(不能用)',
        #                           command=lambda: config_files.save_amz_kw(generate_keywords.update_data(AMAZON_PAGES,
        #                                                                      KW_TO_KEEP, text, button_gen_kw)[2],
        #                                                                      DATA_BASE_PATH, e_kw_name.get()))

        label_title.pack(padx=10, pady=10)
        text.pack(padx=10, pady=10, expand=True, fill='both')
        # label_how_many.pack(side='top', expand=True)
        # e_how_many_to_keep.pack(side='top', expand=True)
        button_gen_kw.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')
        button_back_to_home.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')
        # label_kw_name.pack(side='top', anchor='n', padx=10, pady=5)
        # e_kw_name.pack(side='top', anchor='n', padx=10, pady=5)
        # button_save_kw.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')


class ExistKeyWords(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='关键词', font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        button_config_brand = ttk.Button(self, text='返回首页',
                                         command=lambda: controller.show_frame(StartPage))
        button_config_brand.pack(side='top', anchor='nw', padx=10, pady=5, fill='both')

        data = config_files.load_kw_db_keywords
        text = scrolled_text.ScrolledText(self)
        text.insert('end', data)
        text.pack(padx=10, pady=10, expand=True, fill='both')


if __name__ == '__main__':
    app = GUILayout()
    app.mainloop()

