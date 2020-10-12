import os
import shutil
import datetime
from Auto_work.Auto_oofay.Make_working_folders_and_logs import makeprofile, sku_profile
from Auto_work import main_menu


class MkWorkingFile(object):

    def __init__(self):
        self.product = ''
        self.no_template_msg = r'文件模板没有找到，请配置文件模板到以下路径：E:\TUTA\文档\Python\创建工作日志和工作文件夹'
        self.folder_temp_name_str = "日期_序列号_产品名称"
        self.invalid_input_msg = "输入错误，请重新输入"
        m = makeprofile.MakeProfile()
        m.main()

    @staticmethod
    def get_dest_path() -> str:
        _path = sku_profile.path['working_path']
        return _path

    @staticmethod
    def get_file_template_path() -> str:
        try:
            import Auto_work.Auto_oofay.Make_working_folders_and_logs.sku_profile
            ftpath = sku_profile.path['template_path']
            return ftpath
        except Exception as e:
            raise e

    @staticmethod
    def get_time():
        _year = str(datetime.datetime.now()).split(' ')[0].split('-')[0]
        _month = str(datetime.datetime.now()).split(' ')[0].split('-')[1]
        _day = str(datetime.datetime.now()).split(' ')[0].split('-')[2]
        filename_time = f'{_year}{_month}{_day}'
        return filename_time

    def get_dest_name_product(self):
        self.product = str(input("请输入需要创建的产品名称(0：产品名称)："))
        if self.product == str(0):
            self.product = "产品名称"

    def get_dest_name(self, product_index):
        _filename_time = self.get_time()
        filename = f'{_filename_time}_{str(product_index).zfill(2)}_{self.product}'
        return filename

    def openfolder(self):
        os.startfile(self.get_dest_path())

    @staticmethod
    def copy_file(dest_name, dest_path, template_path):
        print(f'把 （{template_path}） 复制到 （{dest_path}） 重命名为 {dest_name} 最后的路径是 {dest_path}\\{dest_name}')
        shutil.copytree(template_path, f'{dest_path}\\{dest_name}')

    def mk_files(self):
        self.get_dest_name_product()
        start = int(input("请输入开始的序列号(-1退出到选项)："))
        if start == -1:
            self.main()
        end = int(input("请输入结束的序列号：")) + 1
        for product_index in range(start, end):
            self.copy_file(self.get_dest_name(product_index), self.get_dest_path(), self.get_file_template_path())

    def options(self):
        _option = int(input("选项[1：创建文件，-1：退出]："))
        if _option == 1:
            self.mk_files()
        elif _option == -1:
            quit()
        else:
            print(self.invalid_input_msg)
            self.options()

    def again(self):
        _is_again = str(input("是否再次创建(Y/N)："))
        if _is_again == 'y' or _is_again == 'Y':
            self.main()
        elif _is_again == 'n' or _is_again == 'N':
            self.openfolder()
            main_menu.main_menu()
        else:
            print(self.invalid_input_msg)
            self.again()

    def main(self):
        self.options()
        self.again()


def main():
    try:
        f1 = MkWorkingFile()
        f1.main()
    except Exception as _e:
        raise _e


if __name__ == "__main__":
    pass








