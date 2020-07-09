import os
import shutil
import datetime
import makeprofile
import main_menu


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
        import sku_profile
        _path = sku_profile.path['working_path']
        return _path

    @staticmethod
    def get_log_dest_path() -> str:
        import sku_profile
        _log_dest_path = sku_profile.path['log_path']
        return _log_dest_path

    @staticmethod
    def get_file_template_path() -> str:
        try:
            import sku_profile
            ftpath = sku_profile.path['template_path']
            return ftpath
        except Exception as e:
            raise e

    @staticmethod
    def get_log_template():
        try:
            import sku_profile
            ltpath = sku_profile.path['log_template_path']
            return ltpath
        except Exception as e:
            raise e

    def get_log_dest_name(self):
        _log_dest_name = f'log_{self.get_time()}'
        return _log_dest_name

    @staticmethod
    def get_time():
        _year = str(datetime.datetime.now()).split(' ')[0].split('-')[0]
        _month = str(datetime.datetime.now()).split(' ')[0].split('-')[1]
        _day = str(datetime.datetime.now()).split(' ')[0].split('-')[2]
        filename_time = f'{_year}{_month}{_day}'
        return filename_time

    def get_dest_name_product(self):
        self.product = str(input("请输入需要创建的产品名称(0：产品名称，1:智能手表)："))
        if self.product == str(1):
            self.product = "智能手表"
        elif self.product == str(0):
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

    @staticmethod
    def mk_log(log_dest_name, log_dest_path, log_template):
        print(f'把（{log_template}）复制到 （{log_dest_path}） 重命名为（{log_dest_name}.txt） 最后的路径是（{log_dest_path}\\{log_dest_name}）')
        shutil.copy(log_template, f'{log_dest_path}\\{log_dest_name}.txt')

    def mk_files(self):
        self.get_dest_name_product()
        start = int(input("请输入开始的序列号(-1退出到选项)："))
        if start == -1:
            self.main()
        end = int(input("请输入结束的序列号：")) + 1
        for product_index in range(start, end):
            self.copy_file(self.get_dest_name(product_index), self.get_dest_path(), self.get_file_template_path())
        _do_we_need_log = str(input("是否同时创建日志文件（Y/N）:"))
        if _do_we_need_log == 'y' or _do_we_need_log == 'Y':
            self.mk_log(self.get_log_dest_name(), self.get_log_dest_path(), self.get_log_template())
        elif _do_we_need_log == 'n' or _do_we_need_log == 'N':
            self.again()
        else:
            print(self.invalid_input_msg)
            _do_we_need_log = str(input("是否同时创建日志文件（Y/N）:"))

    def options(self):
        _option = int(input("选项[1：创建文件，2：创建日志，-1：退出]："))
        if _option == 1:
            self.mk_files()
        elif _option == 2:
            self.mk_log(self.get_log_dest_name(), self.get_log_dest_path(), self.get_log_template())
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
        print(str(_e))
        with open(os.curdir+"\\error_log.txt", 'a', encoding='utf-8') as ef:
            ef.write(f"{datetime.datetime.now()} - {str(_e).encode('utf-8')}\n")
        raise _e


if __name__ == "__main__":
    pass








