import os
import requests
from lxml import etree
import datetime
import xpath_database
import time
from send2trash import send2trash as d
import random

"""
流程：
    1 输入url
    2 分析url类别
        2.1 获取浏览器headers
        2.2 获取浏览器cookies
        2.3 （可选）如果需要的话，添加代理ip
    3 下载url页面在默认文件夹
    4 载入默认文件夹中的html
    5 解析html文件，
        5.2 找到所有的listing链接信息 
        5.3 并且把他们合并成新的可以去爬取的url 
    6 将所有的listing url保存在文档当中并加上时间戳和输入的url的相关信息 
    7 输入需要查找的listing url文件
    8 下载 需要查找的listing url文件 中的所有html页面
    9 解析所有的html页面并将里面的brand相关信息保存成文本文件，并且符合 "品牌|自己的品牌" 的格式 <-

"""

file_time = str(datetime.datetime.now()).replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
menu_item = {}

MAIN_FOLDER = open(os.curdir + '\\main_folder_path.txt', 'r', encoding='utf-8').read()
PATH_LISTING_FOLDER = MAIN_FOLDER + '\\listing_folder'
PATH_META_HTML = MAIN_FOLDER + '\\META.html'
PATH_URL_FOLDER = MAIN_FOLDER + '\\url'
PATH_DOWNLOADED_URL = PATH_URL_FOLDER+'\\Downloaded_url.txt'
FILE_NAME_BRAND_FILE = MAIN_FOLDER + '\\品牌名替换文件_' + file_time[:10] + '.txt'


def intro():
    print('')
    print('图沓的处理亚马逊品牌工具')
    print("请选择需要的操作：")
    print('')
    for key, value in menu_item.items():
        print(key, end='')
        print(': ', end='')
        print(value[0])
    print('')


def add_function(index: int, name: str, func):
    menu_item[index] = (name, func)


def read_downloaded_urls(downloaded_url_file: str) -> str:
    if os.path.isfile(downloaded_url_file):
        file_list = open(downloaded_url_file, 'r', encoding='utf-8').read()
        return file_list
    else:
        print('没有任何已经下载过的url，创建空白文件')
        with open(downloaded_url_file, 'w', encoding='utf-8') as f:
            f.write('www.amazon.com/default')
        read_downloaded_urls(downloaded_url_file)


def save_listing_html(html, listing_url: str):
    with open(PATH_LISTING_FOLDER + '\\' +
              str(datetime.datetime.now()).
              replace('-', '_').
              replace(':', '_').
              replace(' ', '_').
              replace('.', '_') +
              '.html', 'w', encoding='utf-8') as listing_html:
        listing_html.write(html.text)
    with open(PATH_URL_FOLDER+'\\Downloaded_url.txt', 'a', encoding='utf-8') as url_file:
        url_file.write(listing_url)
        url_file.write('\n')


def check_if_lisitng_html_downloaded(lisitng_url: str, all_urls: str):
    # 检查listing_url 是否在 brand_file_path里
    if lisitng_url in all_urls:
        return True
    else:
        return False


class DownloadBrands(object):

    def __init__(self, path: str):
        """传入列表页面的url，和需要保存文件的文件夹路径"""
        self.url = 'https://www.amazon.com/default'
        self.url_type = 'None'
        self.listing_urls = []
        self.folder_path = path
        self.info_list = []
        self.amazon_head = self.url.split('/')[2]
        self.time_stamp = '[' + str(datetime.datetime.now()) + ']\t'
        self.brand_list = []
        self.user_agent = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'}
        self.cookie = {"session-id": "261-2425092-6884821",
                       "i18n-prefs": "GBP",
                       "ubid-acbuk": "262-2317385-1373932",
                       "x-wl-uid": "1dhLcf8cUWGR//3KjLB96k+JeOgJNGCMrS5OekERN/fBkfcPTQNdrdr1H5tHKr8QpL4RPV4aOyoE=",
                       "session-token": "f1gKKjPecdKwt1CnTPbPDgKT4rOj/8WtiCWrEBv9vaP4SKfBmKdRrYt+3bXb"
                                        "+LHYmkvMfRwud9rXlxNRXlVW9Awjm5ubYAESC2B87sq6sf7bxUk6P3Z2i7lNDy"
                                        "+SpxaN83g1Z95jzpEudokcwXTZX3vekAF+W3LudgQ0xiKQkkP+7hIQv28f60pXqdnjMjDn",
                       "session-id-time": "2082758401l",
                       "csm-hit": "tb:CY69MPPSJNFECB3Y8YV8+s-YWBTVJQGA3E145WPM9EH|1590564415011&t:1590564415012&adb"
                                  ":adblk_yes"}

    def check_meta_url(self):
        if os.path.isfile(os.curdir + '\\meta_html_url.txt') and \
                open(os.curdir + '\\meta_html_url.txt', 'r', encoding='utf-8').read()[:5] == 'https':
            self.url = open(os.curdir + '\\meta_html_url.txt', 'r', encoding='utf-8').read()
        else:
            self.url = input("未找到meta_url文件，请输入url:")
            with open('meta_html_url.txt', 'w', encoding='utf-8') as f:
                f.write(self.url)

    def check_url(self):
        if 's?k=' in self.url and 'me=' not in self.url:
            print(self.time_stamp + "这个是搜索页面")
            self.url_type = 'search_page'
        elif 's?k=' in self.url and 'me=' in self.url:
            print(self.time_stamp + "这个是店铺里的搜索页面")
            self.url_type = 'store_search_page'
        elif self.url == '-1':
            self.main_menu()
        else:
            print(self.time_stamp + "这个是未识别的页面，请重新输入")
            self.check_url()

    def download_meta_html(self, url: str):
        self.url = input("输入url:")

        html = requests.get(url, headers=self.user_agent, cookies=self.cookie, timeout=10)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        # 保存html文件
        with open(PATH_META_HTML,
                  'w',
                  encoding='utf-8') as h:
            h.write(html.text)
        os.startfile(self.folder_path)

    def find_all_listing(self, html: str) -> list:
        """传入html，返回html里面包含的lisitng链接"""
        html = etree.HTML(html, etree.HTMLParser())
        lisitng_list = []
        if self.url_type == 'search_page':
            all_listing = html.xpath(xpath_database.all_listing)[0][0]
            for i in all_listing:
                links = i[0].xpath(xpath_database.search_page_all_link)[:-1]
                for index, link in enumerate(links):
                    links[index] = self.amazon_head + link
                    lisitng_list.append(links[index])
                    self.save_links(links, index)
            return lisitng_list
        elif self.url_type == 'store_search_page':
            all_listing = html.xpath(xpath_database.all_listing)[0][0]
            for i in all_listing:
                links = i.xpath(xpath_database.search_page_all_link)[:16]
                for index, link in enumerate(links):
                    links[index] = self.amazon_head + link
                    lisitng_list.append(links[index])
                    self.save_links(links, index)
            return lisitng_list

    def save_links(self, links: list, index: int):
        _links_folder = PATH_URL_FOLDER + '\\' + self.url.split('s?k=')[-1].split('&')[0] + '_' + file_time[:10]
        if os.path.isdir(PATH_URL_FOLDER):
            with open(_links_folder + '.txt',
                      'a', encoding='utf-8') as link_file:
                link_file.write(self.time_stamp)
                link_file.write(links[index])
                link_file.write('\n')
            print(self.time_stamp + links[index])
        else:
            os.mkdir(PATH_URL_FOLDER)

    def download_all_listing_htmls(self, meta_html: str):
        self.listing_urls = self.find_all_listing(meta_html)
        _all_urls = read_downloaded_urls(PATH_DOWNLOADED_URL)
        for listing_url in self.listing_urls:
            try:
                if check_if_lisitng_html_downloaded(listing_url, _all_urls) is False:
                    print(self.time_stamp + '开始下载以下html：')
                    print('http://' + listing_url)
                    html = requests.get('http://' + listing_url,
                                        headers=self.user_agent,
                                        cookies=self.cookie,
                                        timeout=5)
                    html.raise_for_status()
                    html.encoding = html.apparent_encoding
                    save_listing_html(html, listing_url)
                    time.sleep(random.randrange(1, 2))
            except requests.exceptions.HTTPError as e:
                print(self.time_stamp + str(e))
                print('http://' + listing_url)
                continue
        # os.startfile(listing_folder_path)

    def find_brand(self, html: str):
        html = etree.HTML(html, etree.HTMLParser())
        brand = html.xpath(xpath_database.brand)
        shipped_by = html.xpath(xpath_database.shipped_by)
        self.brand_list.append(' '.join(brand))
        self.brand_list.append(' '.join(shipped_by))
        self.brand_list = list(filter(None, self.brand_list))

    def find_all_brand(self, listing_html_folder_path: str):
        print(self.time_stamp + '文件夹中找到以下html：')
        for html_file in os.listdir(listing_html_folder_path):
            print('\t' + listing_html_folder_path + '\\' + html_file)
            html = open(listing_html_folder_path + '\\' + html_file, 'r', encoding='utf-8').read()
            self.find_brand(html)

    def save_brand(self, my_brand: str, brand_file_path: str):
        for each_brand in self.brand_list:
            if brand_file_path.split('\\')[-1] in os.listdir(self.folder_path):
                with open(brand_file_path, 'r', encoding='utf-8') as r:
                    content = r.read()
                    if each_brand not in content:
                        with open(brand_file_path, 'a', encoding='utf-8') as b:
                            b.write(each_brand + '|' + my_brand)
                            b.write('\n')
            elif brand_file_path.split('\\')[-1] not in os.listdir(self.folder_path):
                with open(brand_file_path, 'a', encoding='utf-8') as b:
                    b.write(each_brand + '|' + my_brand)
                    b.write('\n')
            else:
                class BrandFileError(Exception):
                    pass

                raise BrandFileError
        os.startfile(brand_file_path)

    def detele_listing_html(self, lisitng_html_folder_path: str):
        _make_sure = input("确定？（Y/N）:")
        if _make_sure == 'y' or _make_sure == 'Y':
            for folder, subfolder, file in os.walk(lisitng_html_folder_path):
                for item in file:
                    file_path = folder + '\\' + item
                    print(self.time_stamp + '已删除 ' + file_path)
                    d(file_path)
            input("完成，按回车回到主菜单")
            self.main_menu()
        elif _make_sure == 'n' or _make_sure == 'N':
            self.main_menu()
        else:
            print("无法识别")
            self.detele_listing_html(PATH_LISTING_FOLDER)

    def function_one(self):
        # 下载元url
        self.url = input("请输入url:")
        with open('meta_html_url.txt', 'w', encoding='utf-8') as f:
            f.write(self.url)
        self.check_url()
        self.download_meta_html(self.url)
        self.main_menu()

    def function_two(self):
        # 查看元html中所有listing的url
        self.check_url()
        self.listing_urls = self.find_all_listing(open(PATH_META_HTML, 'r', encoding='utf-8').read())
        self.main_menu()

    def function_three(self):
        # 创建品牌关键词替换文本文件
        _my_brand = input('输入自己的品牌名：')
        self.find_all_brand(PATH_LISTING_FOLDER)
        self.save_brand(_my_brand, FILE_NAME_BRAND_FILE)
        self.main_menu()

    def function_four(self):
        # (慎用) 清除html文件
        self.detele_listing_html(PATH_LISTING_FOLDER)

    def function_five(self):
        # (慎用) 下载所有的元html中所有listing的html文件
        self.check_url()
        self.download_all_listing_htmls(open(PATH_META_HTML, 'r', encoding='utf-8').read())

    def main_menu(self):
        self.check_meta_url()
        add_function(1, '下载元url', self.function_one)
        add_function(2, '查看元html中所有listing的url', self.function_two)
        add_function(3, '创建品牌关键词替换文本文件', self.function_three)
        add_function(4, '(慎用) 清除html文件', self.function_four)
        add_function(5, '(慎用) 下载所有的元html中所有listing的html文件', self.function_five)
        intro()
        ui = str(input("输入需要的功能："))

        if ui in str(menu_item.keys()):
            for key, value in menu_item.items():
                if ui == str(key):
                    value[1]()
        else:
            input("无法识别的选项，回车继续")
            self.main_menu()


if __name__ == '__main__':
    # 创建实例
    download_brand = DownloadBrands(MAIN_FOLDER)
    download_brand.main_menu()
