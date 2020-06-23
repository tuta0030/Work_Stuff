import os
import datetime
import re
from openpyxl.utils import coordinate_to_tuple
import main_menu
import collections

HOW_MANY_WORDS_IN_COUNTER = 100
MENU_RESTRICTION = 200
ROW_RESTRICTION = 3000
COL_MAX = 3000
NO_FILE = '\n' + r'没有找到文件，请确认表格在正确的路径下，并确定表格文件名称格式正确'
STANDARD_MESSAGE = 'The photo was taken in natural light because there is a slight chromatic aberration between the ' \
                   'device and the monitor, please understand'
BRAND_TO_REPLACE_KW = open('kw_brand.txt', 'r', encoding='utf-8').read()
KW_FILTER_CHAR = ': * ( ) [ ] { } ,'


def get_date() -> str:
    time = ''.join(str(datetime.datetime.now()).split(' ')[0].split('-'))
    return str(time)


def get_coordinate(which_cell) -> tuple:
    return coordinate_to_tuple(str(which_cell).split('.')[-1][:-1])


def validate_product() -> str:
    print('')
    print(f'当前产品类别：' + open(os.curdir + '\\product_type.txt', 'r', encoding='utf-8').read())
    wanna_change = str(input("(0：继续，1：修改)："))
    if wanna_change == str(1):
        with open(os.curdir + '\\product_type.txt', 'w', encoding='utf-8') as pt:
            pt.write(input("请输入产品类别："))
        return open(os.curdir + '\\product_type.txt', 'r', encoding='utf-8').read()
    elif wanna_change == str(0):
        return open(os.curdir + '\\product_type.txt', 'r', encoding='utf-8').read()


def select_time() -> str:
    which_time = int(input("选择<需要处理的文件>名中的时间：0:默认时间（当前日期）， 1:自定义时间："))
    if which_time == 0:
        time = get_date()
        return time
    elif which_time == 1:
        time = str(input("请输入需要设置的时间(格式:年月日-比如：20200501 可省略年份)："))
        if len(time) == 4:
            time = str(datetime.datetime.now())[:4] + time
        return time
    elif which_time == -1:
        os.system('cls')
        main_menu.main_menu()
    else:
        print("只能输入0和1")
        select_time()


def get_column_until_none_cell(sheet, row_start: int, column_const: int) -> list:
    cell_list = []
    for i in range(row_start + 1, ROW_RESTRICTION):
        if sheet.cell(i, column_const).value is not None:
            sheet.cell(i, column_const).value = str(sheet.cell(i, column_const).value). \
                replace('\xa0', ' '). \
                replace('||', ' ')
            cell_list.append(sheet.cell(i, column_const))
    return cell_list


def __random_title(item_name: str, brand: str) -> str:
    _pattern = re.compile(r'\s°')
    length = len(item_name)
    item_name = re.sub(_pattern, '°', item_name)  # 移除°前的空格

    item_name_h = item_name.split(' ')[:-round(len(item_name.split(' ')) / 2)]
    item_name_t = item_name.split(' ')[round(len(item_name.split(' ')) / 2):]

    color_size = []

    # 将带有","的变体数值保留
    for word in item_name_t:
        if ',' in word or '(' in word or ')' in word:
            try:
                color_size.append(' '.join(item_name_t[item_name_t.index(word):]))
                item_name_t = item_name_t[:item_name_t.index(word)]
                if length > 199:
                    item_name_t = []
            except ValueError:
                item_name_t = []

    rand_item_name_t = list(set(item_name_t))
    rand_item_name_t = rand_item_name_t + color_size
    new_item_name = item_name_h + rand_item_name_t
    new_item_name = [word.capitalize() for word in new_item_name]
    new_item_name = ' '.join(new_item_name).replace('  ', ' ').replace(brand.capitalize(), brand)
    return new_item_name


def process_info(sheet, info_coordinate: tuple, info):
    """将传入的坐标表格的值全部修改为传入的INFO"""
    if info == str(-1):
        pass
    else:
        info_list = get_column_until_none_cell(sheet, info_coordinate[0], info_coordinate[1])
        for index, item in enumerate(info_list):
            info_list[index].value = info


def high_frequent_words(key_words_list: list):
    key_words_list = ' '.join(key_words_list).replace(BRAND_TO_REPLACE_KW, '')
    for each_char in KW_FILTER_CHAR.split(' '):
        key_words_list = key_words_list.replace(each_char, ' ')
    key_words_list = key_words_list.split(' ')
    key_words_list = [each_word.lower() for each_word in key_words_list]
    key_words_list = list(dict.fromkeys(key_words_list))
    kw_list = []
    for word, count in collections.Counter(key_words_list).most_common(HOW_MANY_WORDS_IN_COUNTER):
        kw_list.append(word.capitalize())
    return kw_list


def process_description(sheet, desc_coordinate: tuple):
    info_list = get_column_until_none_cell(sheet, desc_coordinate[0], desc_coordinate[1])
    for index, item in enumerate(info_list):
        if len(item.value) > 1500:
            info_list[index].value = ' '.join(str(item.value)[:-(len(item.value) - 1499)].split(' ')[:-1])


def cap_title(title: str, brand: str) -> str:
    title = title.split(' ')
    title = [word.capitalize() for word in title]
    title = ' '.join(title)
    title = title.replace(brand.capitalize(), brand)
    return title


def process_item_name(item_name: str, brand: str) -> str:
    item_name = __random_title(item_name, brand)
    return item_name


def process_bulletpoints(sheet, bullet_point_coordinate: tuple):
    bullet_points_dict = {'first_column': get_column_until_none_cell(sheet, bullet_point_coordinate[0],
                                                                     bullet_point_coordinate[1] + 0),
                          'second_column': get_column_until_none_cell(sheet, bullet_point_coordinate[0],
                                                                      bullet_point_coordinate[1] + 1),
                          'third_column': get_column_until_none_cell(sheet, bullet_point_coordinate[0],
                                                                     bullet_point_coordinate[1] + 2),
                          'fourth_column': get_column_until_none_cell(sheet, bullet_point_coordinate[0],
                                                                      bullet_point_coordinate[1] + 3),
                          'fifth_column': get_column_until_none_cell(sheet, bullet_point_coordinate[0],
                                                                     bullet_point_coordinate[1] + 4)
                          }
    for each_column in bullet_points_dict.keys():
        for index, each_line in enumerate(bullet_points_dict[each_column]):
            if len(each_line.value) > 500:
                bullet_points_dict[each_column][index].value = each_line.value[:499].replace('<', '(').replace('>', ')')
            if len(each_line.value) < 20:
                bullet_points_dict[each_column][index].value = STANDARD_MESSAGE


def process_price(sheet, coordinate: tuple, exchange_rate: float, lowest_price: int):
    price = get_column_until_none_cell(sheet, coordinate[0], coordinate[1])
    for index, item in enumerate(price):
        price[index].value = str(int(int(str(item.value).split('.')[0]) * exchange_rate) - 1)
        if int(price[index].value) < lowest_price:
            # 删除低于最低价格的行
            print(f"表格中{price[index]}的价格过低，正在删除")
            for col in range(1, COL_MAX):
                sheet.cell(coordinate_to_tuple(str(item).split('.')[-1][:-1])[0], col).value = None


def add_function(menu: dict, index: int, des: str, function):
    """添加程序到主菜单选项"""
    menu[index] = (des, function)


def intro():
    print("\n图沓的工具\n主菜单")
    print("请选择需要的操作：")
    print('')


def show_menu(ui: str, menu: dict):
    if ui in str(menu.keys()):
        for key, value in menu.items():
            if ui == str(key):
                print('\n当前选项：'+value[0])
                value[1]()
    else:
        print("无法识别的选项")
        show_menu(ui, menu)


def make_menu(functions: dict):
    """传入dict，key为描述，value为需要执行的函数"""
    _menu = {}
    index = 0
    for descreption, func in functions.items():
        _menu[(index, descreption)] = func
        index = index + 1

    for item in _menu.keys():
        print(str(item[0]) + '\t' + item[1])
    ui = input('输入选项：')
    if len(ui.split(' ')) > 1:
        for each_ui in ui.split(' '):
            for item, func in _menu.items():
                if each_ui == str(item[0]):
                    func()
    else:
        for item, func in _menu.items():
            if ui == str(item[0]):
                func()


def make_menu_part_functions(functions: dict):
    """传入dict，key为描述，value函数的名称"""
    _menu = {}
    index = 0
    for descreption, func_name in functions.items():
        _menu[(index, descreption)] = func_name
        index = index + 1

    for item in _menu.keys():
        print(str(item[0]) + '\t' + item[1])
    ui = input('输入选项：')
    if len(ui.split(' ')) > 1:
        for each_ui in ui.split(' '):
            for item, func_name in _menu.items():
                if each_ui == str(item[0]):
                    return func_name
    else:
        for item, func_name in _menu.items():
            if ui == str(item[0]):
                return func_name


# 索引用户输入的文件夹中的文件
def index_files() -> tuple:
    folder = input('输入包含表格的文件夹：')
    files = {}
    index = 0
    for folder, subfolder, file in os.walk(folder):
        for each_file in file:
            files[index] = folder + '\\' + each_file
            index += 1
    print("当前文件夹中包含的文件有：")
    for index, file in files.items():
        print(index, end='')
        print('\t' + file.split('\\')[-1])
    ui = str(input('请选择需要处理的文件：')).strip()
    which_file = ''
    for selection in files.keys():
        if len(ui.split(' ')) > 1:
            which_file = []
            for each_ui in ui.split(' '):
                which_file.append(files[int(each_ui)])
        if ui == str(selection):
            which_file = files[selection]
    return folder, which_file


def print_current_menu(current_menu: str):
    print('当前选项：'+current_menu)
    print('')


def back_to_main_menu():
    main_menu.main_menu()
    return 0


def multiple_file_process(process_class, class_parameter: dict, **pas_args):
    """可以传入的选项：method_para, process_method, 自动调用save_sheet """
    folder, which_file = index_files()
    if type(which_file) is list:
        for each_file in which_file:
            print('开始处理表格：' + each_file.split("\\")[-1])
            pas = process_class(each_file, class_parameter)
            pas_args['method_para'] = pas_args.get('method_para', None)
            if pas_args['method_para'] is None:
                pas.__getattribute__(pas_args['process_method'])()
            else:
                pas.__getattribute__(pas_args['process_method'])(*pas_args['method_para'])
            pas.__getattribute__('save_sheet')(folder, each_file.split('\\')[-1])
    else:
        print('开始处理表格：' + which_file.split("\\")[-1])
        pas = process_class(which_file, class_parameter)
        pas_args['method_para'] = pas_args.get('method_para', None)
        if pas_args['method_para'] is None:
            pas.__getattribute__(pas_args['process_method'])()
        else:
            pas.__getattribute__(pas_args['process_method'])(*pas_args['method_para'])
        pas.__getattribute__('save_sheet')(folder, which_file.split('\\')[-1])
    print("处理完成")


def main_menu_quit():
    try:
        quit()
    except Exception as e:
        print(e)

        class QuitMainMenu(Exception):
            pass

        raise QuitMainMenu('退出程序')


if __name__ == '__main__':
    pass
