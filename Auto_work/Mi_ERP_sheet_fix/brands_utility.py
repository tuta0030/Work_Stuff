import datetime
import os


file_time = str(datetime.datetime.now()).replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
menu_item = {}

MAIN_FOLDER = open(os.curdir + '\\main_folder_path.txt', 'r', encoding='utf-8').read()
PATH_LISTING_FOLDER = MAIN_FOLDER + '\\listing_folder'
PATH_META_HTML = MAIN_FOLDER + '\\META.html'
PATH_URL_FOLDER = MAIN_FOLDER + '\\url'
PATH_DOWNLOADED_URL = PATH_URL_FOLDER + '\\Downloaded_url.txt'
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


def save_listing_html(html: str, listing_url: str):
    with open(PATH_LISTING_FOLDER + '\\' +
              str(datetime.datetime.now()).
              replace('-', '_').
              replace(':', '_').
              replace(' ', '_').
              replace('.', '_') +
              '.html', 'w', encoding='utf-8') as listing_html:
        listing_html.write(html)
    with open(PATH_URL_FOLDER + '\\Downloaded_url.txt', 'a', encoding='utf-8') as url_file:
        url_file.write(listing_url)
        url_file.write('\n')


def check_if_lisitng_html_downloaded(lisitng_url: str, all_urls: str):
    # 检查listing_url 是否在 brand_file_path里
    if lisitng_url in all_urls:
        return True
    else:
        return False


def get_failed_url() -> list:
    failed_listing = MAIN_FOLDER + '\\failed_lisitng_url.txt'
    if os.path.isfile(failed_listing):
        failed_listing = open(failed_listing, 'r', encoding='utf-8').read()
        failed_listing = failed_listing.split('\n')
        return failed_listing
    else:
        failed_listing = []
        return failed_listing


def get_downloaded_url(downloaded_url_path: str) -> list:
    pass


class DownloadBrands(object):

    def __init__(self, path: str):
        """传入列表页面的url，和需要保存文件的文件夹路径"""
        self.url = 'https://www.amazon.com/default'
        self.url_type = 'None'
        self.listing_urls = []
        self.failed_listing = []
        self.folder_path = path
        self.info_list = []
        self.amazon_head = self.url.split('/')[2]
        self.time_stamp = '[' + str(datetime.datetime.now()) + ']\t'
        self.brand_list = []
        self.user_agent = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'}
        self.cookie = open('cookies.txt', 'r', encoding='utf-8').read()[1:-1].split(';')
        self.cookie = [tuple(item.split('=', 1)) for item in self.cookie]
        try:
            self.cookie = {key: value for (key, value) in self.cookie}
        except ValueError:
            self.cookie = '没有找到cookies'
