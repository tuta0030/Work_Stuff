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
import xlsxwriter

ROW_RANGE_RESTRICTION = 2000
COLUMN_RANGE_RESTRICTION = 2000
BR_PATTERN = ('(<(br)>)', '(</(br)>)')


class Translate:

    def __init__(self):
        self.file_directory = ''
        self.sheet = ''

    def load_sheet(self, which_file) -> dict:
        ws = openpyxl.load_workbook(which_file).get_sheet_by_name('sheet1')
        self.sheet = ws

        def find_cell(sheet, cell_name: str):
            for _r in range(1, ROW_RANGE_RESTRICTION):
                for _c in range(1, COLUMN_RANGE_RESTRICTION):
                    if sheet.cell(_r, _c).value == cell_name:
                        return sheet.cell(_r, _c)

        item_name_cell = find_cell(ws, 'item_name')
        bullet_point_cell = find_cell(ws, 'bullet_point1')
        # keywords_cell = find_cell(ws, 'generic_keywords1')
        description = find_cell(ws, 'product_description')
        sheet_cells = {'标题': item_name_cell,
                       '五点': bullet_point_cell,
                       '描述': description}
        return sheet_cells

    @staticmethod
    def add_cor(each_cell) -> str:
        """add coordinate for cell content"""
        return f'[[[{str(pasu.get_coordinate(each_cell))}]]] ' + str(each_cell.value)

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
                [print(each_cell.value) for each_cell in value]
                content_list = \
                    [self.add_cor(each_cell) for each_cell in value]
                full_bp_list.append(self.htm_warp(content_list))
            return '\n'.join(full_bp_list)
        content_list = pasu.get_column_until_none_cell(sheet,
                                                       content_coordinate[0],
                                                       content_coordinate[1])
        [print(each_cell.value) for each_cell in content_list]
        content_list = \
            [self.add_cor(each_cell).replace('<br>', BR_PATTERN[0]).replace('</br>', BR_PATTERN[1])
             for each_cell in content_list]
        return self.htm_warp(content_list)

    def indexing_files(self):
        self.file_directory = input('输入表格文件路径:')
        files = {}
        index = 0
        if self.file_directory == '-1':
            pasu.back_to_main_menu()
        elif not os.path.isdir(self.file_directory):
            print('请输入一个文件夹路径')
            self.indexing_files()
        for folder, subfolder, file in os.walk(self.file_directory):
            for each_file in file:
                files[index] = folder + '\\' + each_file
                index += 1
        print("当前文件夹中包含的文件有：")
        for index, file in files.items():
            print(index, end='')
            print('\t' + file.split('\\')[-1])
        ui = str(input('请选择需要处理的文件：')).strip()
        for selection in files.keys():
            if len(ui.split(' ')) > 1:
                which_file = []
                for each_ui in ui.split(' '):
                    which_file.append(files[int(each_ui)])
                return which_file
            elif ui == str(selection):
                which_file = files[selection]
                return which_file

    def save_as_html(self, what, content: str):
        with open(self.file_directory + '\\' + what + '.htm', 'w', encoding='utf-8') as file:
            file.write(htm_file_warp.htm_file_head)
            file.write('\n')
            file.write(content)
            file.write('\n')
            file.write(htm_file_warp.htm_file_tail)

    @staticmethod
    def htm_warp(content: list) -> str:
        def add_htm_warp(title):
            return f"""<tr height="18" style='height:13.50pt;'> <td class="xl65" height="18" colspan="14" 
        style='height:13.50pt;mso-ignore:colspan;' x:str>{title}</td> <td></td> </tr> """

        all_titles = [add_htm_warp(each_title) for each_title in content]
        return '\n'.join(all_titles)

    def save_all(self):
        content_dict = self.load_sheet(self.indexing_files())
        for key, value in content_dict.items():
            save_this_content = self.get_all_column(self.sheet, value)
            if key == '五点':
                self.save_as_html(key, save_this_content)
            self.save_as_html(key, save_this_content)


class ReadTranslatedHtm(object):

    def __init__(self):
        self.directory = ''
        self.langs = []
        self.langs_dict = {}

    def find_all_htm_file(self) -> list:
        self.directory = input('输入htm文件路径:')
        files = []
        if self.directory == '-1':
            pasu.back_to_main_menu()
        elif not os.path.isdir(self.directory):
            print('请输入一个文件夹路径')
            self.find_all_htm_file()
        for folder, subfolder, file in os.walk(self.directory):
            for each_file in file:
                if each_file.split('.')[-1] == 'htm' and \
                       (str(each_file) != '五点.htm' and
                        str(each_file) != '标题.htm' and
                        str(each_file) != '描述.htm'):
                    files.append(folder + '\\' + each_file)
        return files

    def get_langs(self, files: list):
        langs = []
        [langs.append(str(each_htm).replace('五点', '').replace('标题', '').replace('描述', '')
                      .split('\\')[-1].replace('.htm', ''))
         for each_htm in files]
        langs = list(set(langs))
        self.langs = langs

    def main(self):
        files = self.find_all_htm_file()
        self.get_langs(files)
        for each_lang in self.langs:
            self.langs_dict[each_lang] = []
            for each_file in files:
                if each_lang in each_file:
                    self.langs_dict[each_lang].append(each_file)

        print(self.langs_dict)


def main():
    translate = Translate()
    readtranslate = ReadTranslatedHtm()
    _menu = {'通过表格保存htm文件': translate.save_all,
             '通过htm生成新的表格文件': readtranslate.main}
    pasu.make_menu(_menu)
