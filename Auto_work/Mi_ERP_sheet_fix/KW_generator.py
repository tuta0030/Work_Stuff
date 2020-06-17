import random
import datetime
import os
import re
import main_menu
import generating_kw_from_html as gk
import pas_utility
import KW_generator_utility as KWu


# 主程序的类
class RandKeyWord(object):

    def __init__(self):
        self.how_many_to_keep = 0
        self.ui_kw = ''
        self.kw_cat = ''
        self.how_many_type = []
        self.db_content = ''
        self.lang = {}
        self._no_match_msg = f'没有在数据库中找到您所需的关键词，请确保数据库({os.path.abspath(KWu.PATH_DATA_BASE)})中已经保存了您所需的内容并确认是否输入正确'
        self._out_keywords_path = ''
        self.working_txt_path = KWu.PATH_MAIN + r'\需要输入的产品内容_产品编码(提交之后替换掉).txt'

    # 检查是否找到了输入的关键词
    def check_ui_kw(self):
        if re.findall(re.compile(self.ui_kw), str(self.kw_cat)):
            print('\n')
            print('正在为您生成所需的关键词...')
        else:
            print(self._no_match_msg)
            self.KW_generator_main()

    # 选择需要生成的关键词
    def get_ui(self, indexed_kw_types: dict):
        self.ui_kw = str(input("请选择需要操作的关键词(0:打开关键词文件，-1退出)："))
        if self.ui_kw == str(0):
            os.startfile(KWu.PATH_DATA_BASE)
            main_menu.main_menu()
        elif self.ui_kw == str(-1):
            main_menu.main_menu()
        else:
            self.ui_kw = indexed_kw_types[int(self.ui_kw)]
        self.how_many_to_keep = int(input("需要保留前几位的关键词？："))
        if type(self.how_many_to_keep) != int:
            print("输入错误，需要输入正整数数字")
            self.how_many_to_keep = int(input("需要保留前几位的关键词？："))
        self._out_keywords_path = \
            KWu.find_storage_path() +\
            f'\\关键词文件_{self.ui_kw}{str(datetime.datetime.now()).replace(":", "_").replace(".", "_")}.txt '

    # 获取输出关键词时连接关键词类型和内容的开头
    def get_keywords_cat(self):
        _pattern = re.compile(r'.+[:：]{')
        _result = re.findall(_pattern, self.db_content)
        self.kw_cat = _result

    # 获取关键词库文本中的内容
    def get_database_content(self, data_base_path, key_word):
        with open(data_base_path, 'r', encoding='utf-8') as db:
            content = db.read().split('\n')
            content = ' '.join(content)
            brands = KWu.read_brand_file()
            brands = brands.split('|')
            for each_brand in brands:
                content = content.replace(each_brand, '')
            pattern = re.compile(str(key_word))
            _match = re.findall(pattern, content)
            if _match:
                self.db_content = content
                self.find_out_how_many_language(content)
            else:
                return None

    # 找出当前选择的关键词包含几个国家
    def find_out_how_many_language(self, specific_kw_content: str):
        _specific_pattern = re.compile(f'{self.ui_kw}[:：]'+'{'+'.*'+'}'+f'{self.ui_kw}')
        _specific_words = re.findall(_specific_pattern, specific_kw_content)
        _pattern = re.compile('[A-Z]{2}(?=:)')
        _result = re.findall(_pattern, str(_specific_words))
        for each_lang in _result:
            self.lang[each_lang] = []
        print('\n当前关键词所包含的国家：', end='')
        print(', '.join(self.lang.keys()))

    # 设置每个国家的语言和关键词
    def set_lang_content(self, kw, db_content):
        _pattern = re.compile(str(kw) + r'.*}' + str(kw), re.DOTALL)
        _result = re.findall(_pattern, db_content)

        countrys = list(self.lang.keys())
        for each_key in self.lang.keys():
            current_index = countrys.index(each_key)
            next_index = current_index + 1
            if each_key is not countrys[-1]:
                _pattern = re.compile(f'{countrys[current_index]}.*{countrys[next_index]}:', re.DOTALL)
                self.lang[each_key] = re.findall(_pattern, str(_result))
            else:
                _pattern = re.compile(f'{countrys[current_index]}.*'+'}', re.DOTALL)
                self.lang[each_key] = re.findall(_pattern, str(_result))
        return _result

    # 写入关键词文件
    def write_keywords(self, lang, keywords):
        _t = datetime.datetime.now()
        with open(self._out_keywords_path, 'a', encoding='utf-8') as f:
            f.write('\n')
            f.write(f'{lang}: {keywords}')
            f.write('\n')
            f.write('\n')
            f.write("生成日期：" + str(_t) + "\t\t字数：" + str(len(keywords)))
            f.write('\n')
            f.write('\n')

    # 随机关键词
    def mk_randKW(self, lang):
        self.set_lang_content(self.ui_kw, self.db_content)
        _this_db_list = KWu.get_db_conten_as_words_list(self.lang[str(lang)])
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

        _rand_list.pop()
        print(f'{lang}：{_characters}')
        print('关键词长度：' + str(len(_characters)))
        self.write_keywords(lang, _characters)

    # 是否继续
    def again(self):
        _is_again = str(input("是否再次生成关键字？（Y/N）："))
        if _is_again == 'y' or _is_again == 'Y':
            print('\n\n')
            self.KW_generator_main()
        elif _is_again == 'n' or _is_again == 'N':
            main_menu.main_menu()
        else:
            _is_again = str(input("输入错误，请输入Y或N："))

    # 主程序
    def KW_generator_main(self):
        indexed_kw_types = KWu.show_current_kw_types()
        self.get_ui(indexed_kw_types)
        self.get_database_content(KWu.PATH_DATA_BASE, self.ui_kw)
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


# 主程序:从关键词库生成关键词
def main():
    os.system('cls')
    kw = RandKeyWord()
    pas_utility.print_current_menu('从关键词库生成关键词')
    _menu = {'退回主菜单': pas_utility.back_to_main_menu,
             '生成关键词': kw.KW_generator_main,
             '重命名关键词': rename}
    pas_utility.make_menu(_menu)


# 重命名关键词
def rename():
    indexed_kw_types = KWu.show_current_kw_types()
    _ui = str(input("选择需要重命名的关键词："))
    _uo = str(input("输入新的词汇："))
    content = open(KWu.PATH_DATA_BASE, 'r', encoding='utf-8').read()
    content = content.replace(indexed_kw_types[int(_ui)], _uo)
    with open(KWu.PATH_DATA_BASE, 'w', encoding='utf-8') as f:
        f.write(content)
    pas_utility.back_to_main_menu()


# 创建新的关键词
def creat_new_kw():
    pass


# 菜单选项：用来调用主程序和子程序
def menu():
    os.system('cls')
    pas_utility.print_current_menu('关键词相关')
    function_menu = {'退回主菜单': pas_utility.back_to_main_menu,
                     '从关键词库生成关键词': main,
                     '从html文件生成关键词': gk.validate_html_path,
                     '添加新的关键字': creat_new_kw}
    pas_utility.make_menu(function_menu)


if __name__ == "__main__":
    main()
