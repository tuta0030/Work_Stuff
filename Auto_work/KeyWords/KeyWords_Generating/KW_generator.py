import random
import datetime
import os
import re
import main_menu
from brands_utility import MAIN_FOLDER

PATH_MAIN_MENU_TO_HERE = os.pardir + "\\KeyWords\\KeyWords_Generating"


def write_keywords_to_working_txt(working_txt_path, g_keywords) -> None:
    with open(working_txt_path, 'a', encoding='utf-8') as w:
        oc_content = w.read()
        _pattern = re.compile(r'关键字keywords.+内容简介features')
        re.sub(_pattern, oc_content, g_keywords)
    return None


class RandKeyWord(object):

    def __init__(self):
        self.data_base_path = PATH_MAIN_MENU_TO_HERE + r'\KW_data_base.txt'
        self.how_many_to_keep = 0
        self.ui_kw = ''
        self.kw_cat = ''
        self.db_content = ''
        self.lang = {'EN': '', 'FR': '', 'DE': '', 'IT': '', 'ES': ''}
        self.uni_char = r'[\u4E00-\u9FA5\u00A0-\u00FF\u0100-\u017F\u0180-\u024F\u2E80-\u9FFFa-zA-Z0-9\'?]+\s'
        self._no_DB_msg = r'没有找到关键词数据，请确认关键词已经添加到以下文件：E:\TUTA\文档\Python\创建工作日志和工作文件夹\KW_data_base.txt， 已自动创建文件模板'
        self._no_match_msg = f'没有在数据库中找到您所需的关键词，请确保数据库({os.path.abspath(self.data_base_path)})中已经保存了您所需的内容并确认是否输入正确'
        self._out_keywords_path = ''
        self.working_txt_path = PATH_MAIN_MENU_TO_HERE + r'\需要输入的产品内容_产品编码(提交之后替换掉).txt'

    def check_data_base(self):
        if os.path.isfile(self.data_base_path):
            return True
        else:
            with open(self.data_base_path, 'a', encoding='utf-8') as kw:
                kw.write("这句话替换成产品类目并添加对应国家的关键字到括号内：{\n\nEN: \nFR: \nDE: \nIT: \nES:\n\n}这句话替换成产品类目并添加对应国家的关键字到括号内")
            print(self._no_DB_msg)
            os.startfile(self.data_base_path)

    def check_ui_kw(self):
        if re.findall(re.compile(self.ui_kw), str(self.kw_cat)):
            print('\n')
            print('正在为您生成所需的关键词...')
        else:
            print(self._no_match_msg)
            self.KW_generator_main()

    def get_ui(self):
        self.ui_kw = str(input("请输入需要生成的关键词类型(输入-1退出)："))
        if self.ui_kw == str(1):
            self.ui_kw = "智能手表"
        elif self.ui_kw == str(2):
            self.ui_kw = "U盘"
        elif self.ui_kw == str(-1):
            main_menu.main_menu()
        self.how_many_to_keep = int(input("需要保留前几位的关键词？："))
        if type(self.how_many_to_keep) != int:
            print("输入错误，需要输入正整数数字")
            self.how_many_to_keep = int(input("需要保留前几位的关键词？："))
        self._out_keywords_path = MAIN_FOLDER+f'\\{self.ui_kw}_{"_".join(str(datetime.datetime.now()).split(" ")[0].split("-"))}_{"_".join(str(datetime.datetime.now()).split(" ")[-1][:6].split(":"))}.txt '

    def get_keywords_cat(self):
        _pattern = re.compile(r'.+[:：]{')
        _result = re.findall(_pattern, self.db_content)
        self.kw_cat = _result

    def get_database_content(self, data_base_path, key_word):
        with open(data_base_path, 'r', encoding='utf-8') as db:
            content = db.read().split('\n')
            content = ' '.join(content)
            pattern = re.compile(str(key_word))
            _match = re.findall(pattern, content)
            if _match:
                self.db_content = content
            else:
                # print(self._no_match_msg)
                return None

    def set_lang_content(self, kw, db_content):  # working
        _pattern = re.compile(str(kw) + r'.*}' + str(kw), re.DOTALL)
        _result = re.findall(_pattern, db_content)

        # EN results
        _pattern_EN = re.compile(r'EN.*FR:', re.DOTALL)
        self.lang['EN'] = re.findall(_pattern_EN, str(_result))

        # FR results
        _pattern_FR = re.compile(r'FR.*DE:', re.DOTALL)
        self.lang['FR'] = re.findall(_pattern_FR, str(_result))

        # DE results
        _pattern_DE = re.compile(r'DE.*IT:', re.DOTALL)
        self.lang['DE'] = re.findall(_pattern_DE, str(_result))

        # IT results
        _pattern_IT = re.compile(r'IT.*ES:', re.DOTALL)
        self.lang['IT'] = re.findall(_pattern_IT, str(_result))

        # IT results
        _pattern_ES = re.compile(r'ES:.*}', re.DOTALL)
        self.lang['ES'] = re.findall(_pattern_ES, str(_result))

        # print(_result)
        return _result

    def get_db_conten_as_words_list(self, _data_base):
        _pattern = re.compile(self.uni_char)
        _result = re.findall(_pattern, str(_data_base))
        return _result

    def write_keywords(self, lang, keywords):
        _t = datetime.datetime.now()
        with open(self._out_keywords_path, 'a', encoding='utf-8') as f:
            f.write(f'{lang}: {keywords}')
            f.write('\n')
            f.write('\n')
            f.write("生成日期：" + str(_t) + "\t\t字数：" + str(len(keywords)))
            f.write('\n')
            f.write('\n')

    def mk_randKW(self, lang):
        self.set_lang_content(self.ui_kw, self.db_content)
        _this_db_list = self.get_db_conten_as_words_list(self.lang[str(lang)])
        _this_db_list = [item.lower() for item in _this_db_list]
        _rand_list = []
        _characters = ''
        for i in range(100):
            if i < self.how_many_to_keep:
                _rand_list.insert(i, _this_db_list[i])
            elif len(_characters) < 200:
                _rand_list.append(random.choice(_this_db_list))
                _rand_list = list(dict.fromkeys(_rand_list))
                _characters = ''.join(str(i).capitalize() for i in _rand_list)
            else:
                print("程序出错...（mk_randKW方法出现问题）")

        _rand_list.pop()
        print(f'{lang}：{_characters}')
        print('关键词长度：' + str(len(_characters)))
        self.write_keywords(lang, _characters)

    def again(self):
        _is_again = str(input("是否再次生成关键字？（Y/N）："))
        if _is_again == 'y' or _is_again == 'Y':
            print('\n\n')
            self.KW_generator_main()
        elif _is_again == 'n' or _is_again == 'N':
            main_menu.main_menu()
        else:
            _is_again = str(input("输入错误，请输入Y或N："))

    def KW_generator_main(self):
        self.check_data_base()
        self.get_ui()
        self.get_database_content(self.data_base_path, self.ui_kw)
        self.get_keywords_cat()
        self.check_ui_kw()
        print('\n')
        for i in self.lang.keys():
            try:
                self.mk_randKW(i)
            except IndexError:
                print("数据库信息错误，请确保填写了所有国家的关键词(错误类型：IndexError)")
        print('\n')
        os.startfile(self._out_keywords_path)
        self.again()


def main():
    kw = RandKeyWord()
    kw.KW_generator_main()


if __name__ == "__main__":
    main()
