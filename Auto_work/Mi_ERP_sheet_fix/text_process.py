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


class Translate:

    def __init__(self):
        self.file_directory = input('输入表格文件路径:')
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
        keywords_cell = find_cell(ws, 'generic_keywords1')
        description = find_cell(ws, 'product_description')
        sheet_cells = {'标题': item_name_cell,
                       '五点': bullet_point_cell,
                       '关键字': keywords_cell,
                       '描述': description}
        return sheet_cells

    def select_which_content(self, content_cell: dict):
        _menu = {}
        index = 0
        for descreption, cell in content_cell.items():
            _menu[(index, descreption)] = cell
            index = index + 1
        for item in _menu.keys():
            print(str(item[0]) + '\t' + item[1])
            print('')
        ui = input('输入选项：')
        if len(ui.split(' ')) > 1:
            for each_ui in ui.split(' '):
                for item, cell in _menu.items():
                    if each_ui == str(item[0]):
                        return cell
        else:
            for item, cell in _menu.items():
                if ui == str(item[0]):
                    return cell

    def get_all_column(self, sheet, which_content):
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
            for key, value in bullet_points_dict.items():
                [print(each_cell.value) for each_cell in value]
        content_list = pasu.get_column_until_none_cell(sheet,
                                                       content_coordinate[0],
                                                       content_coordinate[1])
        [print(each_cell.value) for each_cell in content_list]

    def indexing_files(self):
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

    def save_as_html(self, what, content):
        out_path = input('输入需要保存的路径:')
        if not os.path.isdir(out_path):
            print('输入的路径错误，请重新输入')
            self.save_as_html(what, content)
        with open(out_path + '\\' + what + '.htm', 'w', encoding='utf-8') as file:
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


# D:\小米ERP相关数据\上传产品表格\test\FENGRUDING_AE_desk_lamp_亚马逊表_20200729164603.xlsx


def main():
    translate = Translate()
    which_content = translate.select_which_content(translate.load_sheet(translate.indexing_files()))
    translate.get_all_column(translate.sheet, which_content)
