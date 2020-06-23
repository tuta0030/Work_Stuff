# -*- coding: utf-8 -*-
# @Time    : 2020/6/18 11:22
# @Author  : Eric Shen
# @Email   : Eric_Shenarrzine@outlook.com
# @File    : output_usable_sheet_head.py
# @Software: PyCharm

import xlsxwriter
import xlrd

AMAZON_SHEET_HEAD_NUM = 3


def main(original_file, body_file, out_file_name: str):
    head_dict = {}
    body_dict = {}

    body_file = xlrd.open_workbook(body_file).sheets()[0]
    head_file = xlrd.open_workbook(original_file).sheets()[0]

    for row in range(AMAZON_SHEET_HEAD_NUM):
        head_data = head_file.row_values(row)
        head_dict[row] = head_data

    row_index = 0
    for row in range(body_file.nrows):
        body_data = body_file.row_values(row)
        if body_data[0] != '':
            body_dict[row_index] = body_data
            row_index += 1

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


def get_head(original_file: str) -> dict:
    head_dict = {}
    head_file = xlrd.open_workbook(original_file).sheets()[0]
    for row in range(AMAZON_SHEET_HEAD_NUM):
        head_data = head_file.row_values(row)
        head_dict[row] = head_data
    return head_dict


def write_sku_delete_file(folder: str, which_file, sku: str):
    wb = xlrd.open_workbook(which_file)
    ws = wb.sheets()[0]
    original_content = {}
    out_put_content = {}
    for row in range(ws.nrows):
        row_data = ws.row_values(row)
        original_content[row] = row_data
    if ' ' in sku:
        sku = sku.split(' ')
        out_index = 0
        for each_sku in sku:
            for row_number, each_row in original_content.items():
                if each_sku in each_row:
                    out_put_content[out_index] = each_row
                    out_index += 1
    else:
        out_index = 0
        for row_number, each_row in original_content.items():
            if sku in each_row:
                out_put_content[out_index] = each_row
                out_index += 1
    finall_wb = xlsxwriter.Workbook(folder + f'\\_下架的_' + which_file.split("\\")[-1])
    finall_ws = finall_wb.add_worksheet('sheet1')
    head_dict = get_head(which_file)
    for row, row_value in head_dict.items():
        col_n = 0
        for col in row_value:
            finall_ws.write(row, col_n, col)
            col_n += 1
    for row, row_value in out_put_content.items():
        col_n = 0
        for col in row_value:
            if col == 'update':
                col = 'delete'
            finall_ws.write(row + AMAZON_SHEET_HEAD_NUM, col_n, col)
            col_n += 1
    finall_wb.close()

    # C:\Users\Administrator\Desktop\sheet_test
