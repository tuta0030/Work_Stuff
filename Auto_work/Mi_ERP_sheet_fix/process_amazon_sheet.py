import os
import pas_utility as pasu
import pas_class as pasc
import output_usable_sheet_head as opsh


# 统一处理选择的表格文件（全部）
def pas_same_para():
    print("输入统一的参数：")
    _parameter = {"title": str(input("请输入不需要首字母大写的品牌名(回车跳过)：")),
                  'node': str(input("分类节点(-1跳过)：")),
                  'key_word': str(input("关键词(-1跳过)：")),
                  'lowest_pice': int(input("输入最低价格："))
                  }
    pasu.multiple_file_process(pasc.ProcessWithSameParameter,
                               _parameter,
                               process_method='process_sheet')


def new_del_sheet_by_sku():  # P1c0pb53f-11683870895082338686 P1c0jk98b-2237820982760922098
    # D:\小米ERP相关数据\上传产品表格\20200619_充气游泳池
    _ui = input('输入sku/ean:')
    folder, which_file = pasu.index_files()
    if type(which_file) is str:
        print('处理(' + which_file + ')...')
        opsh.write_sku_delete_file(folder, which_file, _ui)
    elif type(which_file) is list:
        for each_file in which_file:
            print('处理(' + each_file + ')...')
            opsh.write_sku_delete_file(folder, each_file, _ui)
    input('处理完成')
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
                               method_para=[_ui]
                               )


def main_function():
    while True:
        try:
            _menu = {'退回主菜单': pasu.back_to_main_menu,
                     '处理选择的表格文件（全部功能）': pas_same_para,
                     '下架目标sku/ean产品': new_del_sheet_by_sku,
                     '更新或下架产品': pas_update_delete}
            pasu.make_menu(_menu)
            main_function()
        except Exception as e:
            raise e
        else:
            break
