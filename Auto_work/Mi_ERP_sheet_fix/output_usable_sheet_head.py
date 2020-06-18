# -*- coding: utf-8 -*-
# @Time    : 2020/6/18 11:22
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : output_usable_sheet_head.py
# @Software: PyCharm

import xlsxwriter
import xlrd


def main(body_file, out_file_name: str):
    head_dict = {}
    body_dict = {}

    headless_file = xlrd.open_workbook(body_file).sheets()[0]
    head_file = xlrd.open_workbook('head.xlsx').sheets()[0]

    for row in range(head_file.nrows):
        head_data = head_file.row_values(row)
        head_dict[row] = head_data

    for row in range(headless_file.nrows):
        body_data = headless_file.row_values(row)
        body_dict[row] = body_data

    finall_wb = xlsxwriter.Workbook(out_file_name)
    finall_ws = finall_wb.add_worksheet('sheet1')
    for row, row_value in head_dict.items():
        col_n = 0
        for col in row_value:
            finall_ws.write(row, col_n, col)
            col_n += 1
    for row, row_value in body_dict.items():
        col_n = 0
        for col in row_value:
            finall_ws.write(row, col_n, col)
            col_n += 1
    finall_wb.close()
    return finall_wb

    # C:\Users\Administrator\Desktop\sheet_test
