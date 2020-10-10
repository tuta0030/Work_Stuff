import text_process
import process_amazon_sheet
import pas_utility
import openpyxl
import xlsxwriter
import os

_meta_path = r'D:\上传表格文件\test\auto_all'


def merge_all_sheet() -> None:
    """
    保留前三行，合并剩下的所有行
    """
    filename = r'D:\上传表格文件\test\FENGRUDING_UK_亚马逊表_20200828142908.xlsx'
    wb = openpyxl.load_workbook(filename)
    sheet = wb['sheet1']
    print(sheet.max_row)
    pass


def check_sub_folders(meta_path) -> tuple:
    """Check if there is sub folders.

    Pass in a path wanna to check,
    return a tuple (bool, list)
    True if there are sub folders, list of the sub folders path
    False if there are none sub folders, list of the files path

    """
    files = []
    folders = []
    for dir_path, dir_names, dir_files in os.walk(meta_path):
        for f_name in dir_files:
            files.append(os.path.join(dir_path, f_name))
        for d_name in dir_names:
            folders.append(os.path.join(dir_path, d_name))
    if not folders:
        return False, files
    else:
        return True, folders


if __name__ == '__main__':
    # print('Starting All In One Process...')
    # print(check_sub_folders(_meta_path))
    merge_all_sheet()
