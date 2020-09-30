import text_process
import process_amazon_sheet
import os

_meta_path = r'D:\上传表格文件\test\auto_all'


def check_sub_folders(meta_path):
    files = []
    folders = []
    for dir_path, dir_names, dir_files in os.walk(meta_path):
        for f_name in dir_files:
            files.append(os.path.join(dir_path, f_name))
        for d_name in dir_names:
            folders.append(os.path.join(dir_path, d_name))
    if not folders:
        return files
    else:
        return folders


if __name__ == '__main__':
    print('Starting All In One Process...')
    print(check_sub_folders(_meta_path))
