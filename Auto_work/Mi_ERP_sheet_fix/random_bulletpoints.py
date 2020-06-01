import os
import re
import pyperclip


def load_bulletpoints_file(bp_path: str, product_name: str) -> str:
    pattern = re.compile(f'(?<={product_name}：)'+'{.+}'+f'(?={product_name})', re.DOTALL)
    content = open(bp_path, 'r', encoding='utf-8').read()
    try:
        result = re.findall(pattern, content)[0][1:-1]
        return result
    except IndexError:
        print("无法找到输入的产品描述")
        return '因为啥也找不到所以返回了这个可爱又迷人的null'


def mk_random_bulletpoints(product_bp: str) -> str:
    bp_list = list(filter(None, product_bp.split('\n')))
    result = '\n'.join(list(set(bp_list))[:5])
    print(result)
    pyperclip.copy(result)
    return result


path = os.curdir + '\\描述.txt'


if __name__ == '__main__':
    _product_name = str(input("请输入产品类别："))
    _product_bp = load_bulletpoints_file(path, _product_name)
    mk_random_bulletpoints(_product_bp)



