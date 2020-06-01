import brands
import datetime
import re

ROW_RESTRICTION = 2000
STANDARD_MESSAGE = 'The photo was taken in natural light because there is a slight chromatic aberration between the device and the monitor, please understand'


def get_date() -> str:
    time = ''.join(str(datetime.datetime.now()).split(' ')[0].split('-'))
    return str(time)


def select_time() -> str:
    which_time = int(input("选择文件名中的时间：0:默认时间（当前日期）， 1:自定义时间(格式:年月日-比如：20200501)："))
    if which_time == 0:
        time = get_date()
        return time
    elif which_time == 1:
        time = str(input("请输入需要设置的时间："))
        return time
    else:
        print("只能输入0和1")
        select_time()


def get_column_until_none_cell(sheet, row_start: int, column_const: int) -> list:
    cell_list = []
    for i in range(row_start+1, ROW_RESTRICTION):
        if sheet.cell(i, column_const).value is not None:
            sheet.cell(i, column_const).value = str(sheet.cell(i, column_const).value).\
                replace('\xa0', ' ').\
                replace('||', ' ')
            cell_list.append(sheet.cell(i, column_const))
    return cell_list


#  TODO 重写 低优先级
def __check_brand(text_need_to_check: str, _brands: list, my_brand: str) -> str:
    _new_item_name = '-'
    for i in _brands:
        if i in text_need_to_check:
            text_need_to_check = text_need_to_check.replace(i, my_brand)
            __check_brand(text_need_to_check, _brands, my_brand)
        elif i not in text_need_to_check:
            _new_item_name = text_need_to_check
    return _new_item_name


def __random_title(item_name: str) -> str:
    _pattern = re.compile(r'\s°')
    length = len(item_name)
    item_name = re.sub(_pattern, '°', item_name)  # 移除°前的空格

    item_name_h = item_name.split(' ')[:-round(len(item_name.split(' '))/2)]
    item_name_t = item_name.split(' ')[round(len(item_name.split(' '))/2):]

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
    new_item_name = ' '.join(new_item_name).replace('  ', ' ')
    return new_item_name


def process_info(sheet, info_coordinate: tuple, info):
    """将传入的坐标表格的值全部修改为传入的INFO"""
    if info == str(-1):
        pass
    else:
        info_list = get_column_until_none_cell(sheet, info_coordinate[0], info_coordinate[1])
        for index, item in enumerate(info_list):
            info_list[index].value = info


def process_description(sheet, desc_coordinate: tuple):
    info_list = get_column_until_none_cell(sheet, desc_coordinate[0], desc_coordinate[1])
    for index, item in enumerate(info_list):
        if len(item.value) > 1500:
            info_list[index].value = ' '.join(str(item.value)[:-(len(item.value)-1499)].split(' ')[:-1])


def process_item_name(item_name: str) -> str:

    # random words
    item_name = __random_title(item_name)

    return item_name


def process_bulletpoints(sheet, bullet_point_coordinate: tuple):
    bullet_points_list_all_five = []
    for _i in range(5):
        bullet_points_list_all_five.append(get_column_until_none_cell(sheet,
                                           bullet_point_coordinate[0]+1,
                                           bullet_point_coordinate[1]+_i))

    # check if there is any empty bullet_point or any bullet_point length is under 10 character
    for _bp_list in bullet_points_list_all_five:
        for index, _bp in enumerate(_bp_list):
            if len(_bp.value) < 10 or _bp_list[index].value is None:
                if index > 0:
                    _bp_list[index].value = _bp_list[index-1].value
                    print("这里应该把前一个数值改成当前数值")
                elif index == 0:
                    _bp_list[index].value = STANDARD_MESSAGE
                    print("这里应该把空白数值填上标准数值")


def process_price(sheet, coordinate: tuple, exchange_rate: float):
    price = get_column_until_none_cell(sheet, coordinate[0], coordinate[1])
    for index, item in enumerate(price):
        price[index].value = str(int(int(str(item.value).split('.')[0])*exchange_rate)-1)
        if int(price[index].value) < 15:
            price[index].value = str(int(price[index].value) + 10)


def __test():
    pass


if __name__ == '__main__':
    __test()
    pass
