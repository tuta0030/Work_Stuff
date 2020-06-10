import os
import requests
from lxml import etree
import xpath_database
import time
from send2trash import send2trash as d
import random
import brands_utility as bu

"""
TODO:
    1. 检查JS Page，假如是JS Page，从已下载的url文件当中去除JS Page的url
    4. 添加切换user-agent,ip,cookie重试失败url的功能
"""


class DownloadBrands(bu.DownloadBrands):

    def __init__(self, path: str):
        bu.DownloadBrands.__init__(self, path)

    def check_meta_url_html_file(self):
        if os.path.isfile(os.curdir + '\\meta_html_url.txt') and \
                open(os.curdir + '\\meta_html_url.txt', 'r', encoding='utf-8').read()[:5] == 'https':
            self.url = open(os.curdir + '\\meta_html_url.txt', 'r', encoding='utf-8').read()
        else:
            self.url = input("未找到meta_url文件，请输入url:")
            with open('meta_html_url.txt', 'w', encoding='utf-8') as f:
                f.write(self.url)

    def check_url_type(self):
        if 's?k=' in self.url and 'me=' not in self.url:
            print(self.time_stamp + "这个是搜索页面")
            self.url_type = 'search_page'
        elif 's?k=' in self.url and 'me=' in self.url:
            print(self.time_stamp + "这个是店铺里的搜索页面")
            self.url_type = 'store_search_page'
        elif 'Best-Sellers' in self.url:
            print(self.time_stamp + "这个是排名页面")
            self.url_type = 'rank_page'
        elif self.url == '-1':
            self.main_menu()
        else:
            print(self.time_stamp + "这个是未识别的页面，请重新输入")
            # raise bu.URLError('错误：未识别的url')
            self.main_menu()

    def download_meta_html(self, url: str):
        html = requests.get(url, headers=self.user_agent, cookies=self.cookie, timeout=10)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        # 保存html文件
        with open(bu.PATH_META_HTML,
                  'w',
                  encoding='utf-8') as h:
            h.write(html.text)
        os.startfile(self.folder_path)

    def download_by_requests(self, url: str):
        html = requests.get('http://' + url,
                            headers=self.user_agent,
                            cookies=self.cookie,
                            timeout=5)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        bu.save_listing_html(html.text, url)
        if bu.JS_PAGE_SIGN in html.text:
            raise bu.JSPageError('JS Page, 请更换cookie')

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
        elif self.url_type == 'rank_page':
            all_listing = html.xpath(xpath_database.rank_page_all_listing)[0]
            for i in all_listing:
                links = i.xpath(xpath_database.rank_page_all_link)
                for index, link in enumerate(links):
                    links[index] = self.amazon_head + link
                    lisitng_list.append(links[index])
                    self.save_links(links, index)
            return lisitng_list

    def save_links(self, links: list, index: int):
        _links_folder = ''
        if self.url_type == 'search_page':
            _links_folder = bu.PATH_URL_FOLDER + \
                            '\\' + self.url.split('s?k=')[-1].split('&')[0] + '_' + bu.file_time[:10]
        elif self.url_type == 'rank_page':
            _links_folder = bu.PATH_URL_FOLDER + \
                            '\\' + self.url.split('/')[3] + '_' + bu.file_time[:10]
        if os.path.isdir(bu.PATH_URL_FOLDER):
            with open(_links_folder + '.txt',
                      'a', encoding='utf-8') as link_file:
                link_file.write(self.time_stamp)
                link_file.write(links[index])
                link_file.write('\n')
            print(self.time_stamp + links[index])
        else:
            os.mkdir(bu.PATH_URL_FOLDER)

    def download_all_listing_htmls(self, meta_html: str):
        failed_listing = bu.get_failed_url()
        if failed_listing != [] or failed_listing is not None:
            self.listing_urls = self.find_all_listing(meta_html) + failed_listing
        else:
            self.listing_urls = self.find_all_listing(meta_html)
        _all_urls = bu.read_downloaded_urls(bu.PATH_DOWNLOADED_URL)
        try:
            for listing_url in self.listing_urls:
                try:
                    if bu.check_if_lisitng_html_downloaded(listing_url, _all_urls) is False:
                        print(self.time_stamp + '开始下载以下html：')
                        print('http://' + listing_url)
                        self.download_by_requests(listing_url)
                        time.sleep(random.randrange(1, 10))
                    else:
                        print(self.time_stamp + listing_url + '已经下载，跳过')
                except Exception as e:
                    print(self.time_stamp + str(e))
                    self.failed_listing.append(listing_url)
        except bu.JSPageError:
            with open(bu.MAIN_FOLDER + '\\failed_lisitng_url.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.failed_listing))
            self.main_menu()
            os.startfile('cookies.txt')

    def find_brand(self, html: str):
        try:
            html = etree.HTML(html, etree.HTMLParser())
            brand = html.xpath(xpath_database.brand)
            shipped_by = html.xpath(xpath_database.shipped_by)
            self.brand_list.append(' '.join(brand))
            self.brand_list.append(' '.join(shipped_by))
            self.brand_list = list(filter(None, self.brand_list))
        except Exception as e:
            print(e)

    def find_all_brand(self, listing_html_folder_path: str):
        print(self.time_stamp + '文件夹中找到以下html：')
        for html_file in os.listdir(listing_html_folder_path):
            print('\t' + listing_html_folder_path + '\\' + html_file)
            html = open(listing_html_folder_path + '\\' + html_file, 'r', encoding='utf-8').read()
            self.find_brand(html)

    def save_brand(self, my_brand: str, brand_file_path: str):
        class BrandFileError(Exception):
            pass
        if self.url_type == 'search_page':
            for each_brand in self.brand_list:
                if '{' not in each_brand:
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
                        raise BrandFileError('保存brand文件失败，save_brand error')
        elif self.url_type == 'rank_page':
            for each_brand in self.brand_list:
                with open(brand_file_path, 'a', encoding='utf-8') as b:
                    b.write(each_brand + '|')
        else:
            print(self.url_type)
            raise BrandFileError('保存brand文件失败，save_brand error')
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
            self.detele_listing_html(bu.PATH_LISTING_FOLDER)

    def function_one(self):
        # 下载元url
        self.url = input("请输入url:")
        with open('meta_html_url.txt', 'w', encoding='utf-8') as f:
            f.write(self.url)
        self.check_url_type()
        self.download_meta_html(self.url)
        self.main_menu()

    def function_two(self):
        # 查看元html中所有listing的url
        self.check_url_type()
        self.listing_urls = self.find_all_listing(open(bu.PATH_META_HTML, 'r', encoding='utf-8').read())
        self.main_menu()

    def function_three(self):
        # 创建品牌关键词替换文本文件
        self.check_url_type()
        _my_brand = input('输入自己的品牌名：')
        self.find_all_brand(bu.PATH_LISTING_FOLDER)
        self.save_brand(_my_brand, bu.FILE_NAME_BRAND_FILE)
        self.main_menu()

    def function_four(self):
        # (慎用) 清除html文件
        self.detele_listing_html(bu.PATH_LISTING_FOLDER)

    def function_five(self):
        # (慎用) 下载所有的元html中所有listing的html文件
        self.check_url_type()
        self.download_all_listing_htmls(open(bu.PATH_META_HTML, 'r', encoding='utf-8').read())
        self.main_menu()

    def main_menu(self):
        self.check_meta_url_html_file()
        bu.add_function(1, '下载元url', self.function_one)
        bu.add_function(2, '查看元html中所有listing的url', self.function_two)
        bu.add_function(3, '创建品牌关键词替换文本文件', self.function_three)
        bu.add_function(4, '(慎用) 清除html文件', self.function_four)
        bu.add_function(5, '(慎用) 下载所有的元html中所有listing的html文件', self.function_five)
        bu.intro()
        ui = str(input("输入需要的功能："))

        if ui in str(bu.menu_item.keys()):
            for key, value in bu.menu_item.items():
                if ui == str(key):
                    value[1]()
        else:
            input("无法识别的选项，回车继续")
            self.main_menu()


if __name__ == '__main__':
    # 创建实例
    download_brand = DownloadBrands(bu.MAIN_FOLDER)
    download_brand.main_menu()
