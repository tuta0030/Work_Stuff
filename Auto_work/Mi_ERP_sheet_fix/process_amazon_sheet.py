import os
import pas_utility as pasu
import pas_class as pasc
import xlrd
import xlsxwriter as xw
import output_usable_sheet_head as opsh


def pas_part():
    # key:功能描述， value:需要调用的函数名称
    part_functions = {'仅处理价格': 'only_price',
                      '仅标题首字母大写': 'cap_title',
                      '仅处理关键词': 'process_keywords'
                      }
    func_name = pasu.make_menu_part_functions(part_functions)
    if func_name == 'process_keywords':
        _parameter = {}
        pasu.multiple_file_process(pasc.ProcessWithSameParameter,
                                   _parameter,
                                   process_method=func_name,
                                   method_para=str(input("关键词(-1跳过)：")))
    else:
        _parameter = {}
        pasu.multiple_file_process(pasc.ProcessWithSameParameter, _parameter, process_method=func_name)


# 处理选择的表格文件（全部）
def pas_same_para():
    print("输入统一的参数：")
    _parameter = {"title": str(input("请输入不需要首字母大写的品牌名(回车跳过)：")),
                  'price': float(input("输入汇率：")),
                  'node': str(input("分类节点(-1跳过)：")),
                  'key_word': str(input("关键词(-1跳过)：")),
                  'lowest_pice': int(input("输入最低价格："))
                  }
    pasu.multiple_file_process(pasc.ProcessWithSameParameter,
                               _parameter,
                               process_method='process_sheet')


def new_del_sheet_by_sku():  # P19tXn5b9-13739855566055684826  D:\小米ERP相关数据\上传产品表格\20200613_置物架
    _ui = input('输入sku/ean:')
    folder, which_file = pasu.index_files()
    print(which_file)
    if type(which_file) is str:
        opsh.write_sku_delete_file(folder, which_file, _ui)
    elif type(which_file) is list:
        for each_file in which_file:
            opsh.write_sku_delete_file(folder, each_file, _ui)
    pasu.back_to_main_menu()


# 更新或下架产品
def pas_update_delete():
    _ui = input('选择需要的选项：0: delete, 1: update:')
    _ui = 'delete' if _ui == '0' else 'update'
    _parameters = {'update_delete': _ui}
    pasu.multiple_file_process(pasc.ProcessWithSameParameter,
                               _parameters,
                               process_method='process_update_delete',
                               _parameter=_parameters,
                               method_para=_parameters
                               )


def main_function():
    while True:
        try:
            os.system('cls')
            pasu.print_current_menu('ERP表格相关')
            _menu = {'退回主菜单': pasu.back_to_main_menu,
                     '处理选择的表格文件（单独功能）': pas_part,
                     '处理选择的表格文件（全部功能）': pas_same_para,
                     '下架目标sku/ean产品': new_del_sheet_by_sku,
                     '更新或下架产品': pas_update_delete}
            pasu.make_menu(_menu)
            main_function()
        except Exception as e:
            raise e
            print(e)
            input('由于以上错误，无法处理本文件，请尝试重新输入正确的文件夹和文件序列号')
            main_function()
        else:
            break
