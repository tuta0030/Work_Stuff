# -*- coding: utf-8 -*-
# @Time    : 2020/7/28 13:42
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : text_process.py
# @Software: PyCharm

import pas_utility as pasu
import os
import htm_file_warp
import openpyxl
import datetime

ROW_RANGE_RESTRICTION = 2000
COLUMN_RANGE_RESTRICTION = 2000
BR_PATTERN = ('(<(br)>)', '(</(br)>)')
SEPERATOR = '^^^'


class Translate:

    def __init__(self):
        self.file_directory = ''
        self.sheet = ''

    def load_sheet(self, which_file) -> dict:
        ws = openpyxl.load_workbook(which_file).get_sheet_by_name('sheet1')
        self.sheet = ws
        item_name_cell = find_cell(ws, 'item_name')
        bullet_point_cell = find_cell(ws, 'bullet_point1')
        color_name = find_cell(ws, 'color_name')
        color_map = find_cell(ws, 'color_map')
        size_name = find_cell(ws, 'size_name')
        size_map = find_cell(ws, 'size_map')
        description = find_cell(ws, 'product_description')
        sheet_cells = {'标题': item_name_cell,
                       '五点': bullet_point_cell,
                       '描述': description,
                       '变体-颜色': color_name,
                       '变体-尺寸': size_name,
                       '变体-颜色map': color_map,
                       '变体-尺寸map': size_map
                       }
        return sheet_cells

    @staticmethod
    def add_cor(each_cell) -> str:
        """add coordinate for cell content"""
        return f'{str(pasu.get_coordinate(each_cell))} {SEPERATOR} ' + str(each_cell.value)

    def get_all_column(self, sheet, which_content):
        """which_content should be the cell"""
        content_coordinate = pasu.get_coordinate(which_content)
        if which_content.value == 'bullet_point1':
            bullet_points_dict = {'first_column': pasu.get_column_until_none_cell(sheet, content_coordinate[0],
                                                                                  content_coordinate[1] + 0),
                                  'second_column': pasu.get_column_until_none_cell(sheet, content_coordinate[0],
                                                                                   content_coordinate[1] + 1),
                                  'third_column': pasu.get_column_until_none_cell(sheet, content_coordinate[0],
                                                                                  content_coordinate[1] + 2),
                                  'fourth_column': pasu.get_column_until_none_cell(sheet, content_coordinate[0],
                                                                                   content_coordinate[1] + 3),
                                  'fifth_column': pasu.get_column_until_none_cell(sheet, content_coordinate[0],
                                                                                  content_coordinate[1] + 4)
                                  }
            full_bp_list = []
            for key, value in bullet_points_dict.items():
                content_list = \
                    [self.add_cor(each_cell) for each_cell in value]
                full_bp_list.append(self.htm_warp(content_list))
            return '\n'.join(full_bp_list)
        content_list = pasu.get_column_until_none_cell(sheet,
                                                       content_coordinate[0],
                                                       content_coordinate[1])
        content_list = \
            [self.add_cor(each_cell).replace('<br>', BR_PATTERN[0]).replace('</br>', BR_PATTERN[1])
             for each_cell in content_list]
        return self.htm_warp(content_list)

    def save_as_html(self, what, content: str):
        out_path = '\\'.join(self.file_directory.split('\\')[:-1])
        with open(out_path + '\\' + what + '.htm', 'a', encoding='utf-8') as file:
            file.write(htm_file_warp.htm_file_head)
            file.write('\n')
            file.write(content)
            file.write('\n')
            file.write(htm_file_warp.htm_file_tail)
        print(f'保存 {what + ".htm"} 到 {self.file_directory}')

    @staticmethod
    def htm_warp(content: list) -> str:
        def add_htm_warp(title):
            return f"""<tr height="18" style='height:13.50pt;'> <td class="xl65" height="18" colspan="14" 
        style='height:13.50pt;mso-ignore:colspan;' x:str>{title}</td> <td></td> </tr> """

        all_titles = [add_htm_warp(each_title) for each_title in content]
        return '\n'.join(all_titles)

    def save_all(self):
        self.file_directory = indexing_files('输入表格文件路径:')
        content_dict = self.load_sheet(self.file_directory)
        for key, value in content_dict.items():
            save_this_content = self.get_all_column(self.sheet, value)
            self.save_as_html(f'所有内容_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}', save_this_content)
        pasu.back_to_main_menu()


class ReadTranslatedHtm(object):

    def __init__(self):
        self.directory = ''
        self.langs = []
        self.langs_dict = {}

    def find_all_txt_file(self) -> list:
        self.directory = input('输入txt文件路径:')
        files = []
        if self.directory == '-1':
            pasu.back_to_main_menu()
        elif not os.path.isdir(self.directory):
            print('请输入一个文件夹路径')
            self.find_all_txt_file()
        for folder, subfolder, file in os.walk(self.directory):
            for each_file in file:
                if each_file.split('.')[-1] == 'txt':
                    files.append(folder + '\\' + each_file)
        return files

    def get_langs(self, files: list):
        langs = []
        [langs.append(str(each_htm).replace('五点', '').replace('标题', '').replace('描述', '')
                      .split('\\')[-1].replace('.txt', ''))
         for each_htm in files]
        langs = list(set(langs))
        self.langs = langs

    def specify_price_node(self) -> tuple:
        exchange_rate = {}
        node = {}
        print(f'当前拥有的语言：{self.langs}')
        for each_lang in self.langs:
            exchange_rate[each_lang] = input(f'输入 {each_lang} 的汇率:')
            node[each_lang] = input(f'输入 {each_lang} 的节点:')
        return exchange_rate, node

    def get_langs_dict(self, files: list):
        for each_lang in self.langs:
            self.langs_dict[each_lang] = []
            for each_file in files:
                if each_lang in each_file:
                    self.langs_dict[each_lang].append(each_file)

    def get_langs_and_langs_dict(self, files):
        self.get_langs(files)
        self.get_langs_dict(files)

    def main(self):
        files = self.find_all_txt_file()
        self.get_langs_and_langs_dict(files)
        oc_file = indexing_files('输入表格文件所在路径:')
        original_wb = openpyxl.load_workbook(str(oc_file))
        original_sheet = original_wb.get_sheet_by_name('sheet1')

        exchange_rate, node = self.specify_price_node()

        node_list = get_content_list(original_sheet, 'recommended_browse_nodes')
        price_list = get_content_list(original_sheet, 'standard_price')
        price_list = [each_cell for each_cell in price_list if each_cell.value != '']

        for lang, file_list in self.langs_dict.items():
            for each_file in file_list:
                content_list = open(each_file, encoding='utf-8').read().split('\n')
                content_list = [each_line for each_line in content_list if each_line != '']
                content_list = [each_line for each_line in content_list if SEPERATOR in each_line]
                for each_content in content_list:
                    if len(each_content.split(SEPERATOR)[0]) > 12:
                        continue
                    each_content = str(each_content).split(SEPERATOR)
                    row = int(each_content[0].strip()[1:-1].replace('、', ',').split(',')[0])
                    col = int(each_content[0].strip()[1:-1].replace('、', ',').split(',')[1])
                    original_sheet.cell(row, col).value = each_content[-1].strip() \
                        .replace(BR_PATTERN[0], '<br>').replace(BR_PATTERN[1], '</br>') \
                        .replace('(<(Br)>)', '<br>').replace('(<(/Br)>)', '</br>')

            print(f'当前使用的节点：{node[lang]}')
            print(f'当前使用的汇率:{exchange_rate[lang]}')

            for each_node in node_list:
                row, col = pasu.get_coordinate(each_node)
                original_sheet.cell(int(row), int(col)).value = node[lang]
            for each_price in price_list:
                row, col = pasu.get_coordinate(each_price)
                original_sheet.cell(int(row), int(col)).value = \
                    int(float(each_price.value) * float(exchange_rate[lang]))

            out_file_name = self.directory + '\\' + lang + '_' + str(oc_file).split('\\')[-1]
            print(f'正在处理  {out_file_name}')
            original_wb.save(out_file_name)

        pasu.back_to_main_menu()


def get_content_list(sheet, cell_name: str) -> list:
    cell = find_cell(sheet, cell_name)
    cell_coordinate = pasu.get_coordinate(cell)
    content_list = pasu.get_column_until_none_cell(sheet, cell_coordinate[0], cell_coordinate[1])
    return content_list


def indexing_files(msg: str):
    file_directory = input(msg)
    files = {}
    index = 0
    if file_directory == '-1':
        pasu.back_to_main_menu()
    elif not os.path.isdir(file_directory):
        print('请输入一个文件夹路径')
        indexing_files(msg)
    for folder, subfolder, file in os.walk(file_directory):
        for each_file in file:
            files[index] = folder + '\\' + each_file
            index += 1
    print("当前文件夹中包含的文件有：")
    for index, file in files.items():
        print(index, end='')
        print('\t' + file.split('\\')[-1])
    ui = str(input('请选择文件：')).strip()
    for selection in files.keys():
        if len(ui.split(' ')) > 1:
            which_file = []
            for each_ui in ui.split(' '):
                which_file.append(files[int(each_ui)])
            return which_file
        elif ui == str(selection):
            which_file = files[selection]
            return which_file


def find_cell(sheet, cell_name: str):
    for _r in range(1, ROW_RANGE_RESTRICTION):
        for _c in range(1, COLUMN_RANGE_RESTRICTION):
            if sheet.cell(_r, _c).value == cell_name:
                return sheet.cell(_r, _c)


def main():
    translate = Translate()
    readtranslate = ReadTranslatedHtm()
    _menu = {'返回主菜单': pasu.back_to_main_menu,
             '通过表格保存htm文件': translate.save_all,
             '通过txt生成新的表格文件': readtranslate.main}
    pasu.make_menu(_menu)
