import os
import custom_error
import re


def load_words_list() -> list:
    words_list = check_dir()
    return words_list


def check_dir() -> list:  # TODO 更好地替换
    path = os.listdir(os.curdir)
    if "品牌名称.txt" in path:
        with open('品牌名称.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('\n', ' ').replace(',', ' ')
            content = content.split(' ')
            content = list(filter(None, content))
            return content
    elif "品牌名称.txt" not in path:
        with open('品牌名称.txt', 'w', encoding='utf-8') as f:
            common_words = 'iphone apple philips dyson dell samsung huawei '
            f.write(common_words)
            content = common_words.replace('\n', ' ').replace(',', ' ')
            content = content.split(' ')
            content = list(filter(None, content))
            return content
    else:
        e = custom_error.MyExcepetion("创建品牌名文件出错", Exception)
        raise e


def load_kw_database() -> str:
    kw_db_path = os.pardir + '\\KeyWords_Generating\\KW_data_base.txt'
    with open(kw_db_path, 'r', encoding='utf-8') as kwf:
        kw_database = kwf.read()
        kw_database = format_database(kw_database)
        # print(kw_database)
    return kw_database


def format_database(kw_database: str) -> str:
    lang_pattern = re.compile(r'EN:.+?(?=FR:)', re.DOTALL)
    content_need_format = re.findall(lang_pattern, kw_database)
    content_need_format = ''.join(content_need_format)
    formated_kwdb = content_need_format.replace('\n', '_').replace(' ', '_')
    print(formated_kwdb)
    return formated_kwdb


if __name__ == '__main__':
    print('3123'.isdigit())
