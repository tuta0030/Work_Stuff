import os
import sys


class MakeProfile(object):

    def __init__(self) -> None:
        self.sku = ''
        self.profile_path = os.path.abspath(os.curdir+'\\sku_profile.py')
        self.working_path = ''

# get functions

# Side functions

    def write_into_sku_profile(self, dict_for_sku_profile) -> None:
        with open(self.profile_path, 'w', encoding='utf-8') as _f:
            _f.write(f'path = {dict_for_sku_profile}')
            _f.write('\n')

    def check_what_lost(self, path_dict):
        from Auto_work.Auto_oofay.Make_working_folders_and_logs import sku_profile
        k = sku_profile.path.keys()
        if 'working_path' not in k:
            path_dict['working_path'] = str(input("路径缺失：请输入 工作文件夹 路径："))
        if 'log_path' not in k:
            path_dict['log_path'] = str(input("路径缺失：请输入 工作日志 路径："))
        if 'template_path' not in k:
            path_dict['template_path'] = str(input("路径缺失：请输入 工作文件夹模板 路径："))
        if 'log_template_path' not in k:
            path_dict['log_template_path'] = str(input("路径缺失：请输入 工作日志模板 路径："))
        return path_dict

    def mk_profile(self) -> None:
        _path = {}
        self.write_into_sku_profile(_path)
        _path = self.check_what_lost(_path)
        if os.path.isdir(_path['working_path']) is True \
           and os.path.isdir(_path['log_path']) is True \
           and os.path.isdir(_path['template_path']) is True\
           and os.path.isfile(_path['log_template_path']) is True:

            self.write_into_sku_profile(_path)
        else:
            print("输入的路径错误，请输入正确的路径：")
            self.mk_profile()

# Main functions
    def check_profile(self) -> dict:
        for item in os.listdir(os.curdir):
            if 'sku_profile.py' not in os.listdir(os.curdir):
                print("没有找到预设文件，请按照提示输入预设文件所需的信息之后重启程序")
                self.mk_profile()
                quit()
            elif item == 'sku_profile.py':
                print("找到预设文件")
                from Auto_work.Auto_oofay.Make_working_folders_and_logs import sku_profile
                new_path_dict = self.check_what_lost(sku_profile.path)
                self.write_into_sku_profile(new_path_dict)
                sys.path.insert(1, self.profile_path)
                return sku_profile.path
        else:
            raise FileNotFoundError

    def main(self) -> None:
        self.working_path = self.check_profile()


if __name__ == '__main__':
    try:
        m = MakeProfile()
        m.main()
    except Exception as e:
        raise e




























