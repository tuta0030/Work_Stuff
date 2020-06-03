import os
import requests
from lxml import etree
import datetime
import xpath_database
import time


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
# 保存文件时用的时间戳 [:10] 来获取时间到当日
FILE_TIME = str(datetime.datetime.now()).replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
AMAZON_MAIN_FOLDER = open(os.curdir+'\\main_folder_path.txt', 'r', encoding='utf-8').read()


class DownloadBrands(object):

    def __init__(self, url: str, path: str):
        """传入列表页面的url，和需要保存文件的文件夹路径"""
        self.url = url
        self.url_type = 'None'
        self.folder_path = path
        self.info_list = []
        self.amazon_head = self.url.split('/')[2]
        self.time_stamp = '['+str(datetime.datetime.now())+']\t'
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

    def check_url(self):
        if 's?k=' in self.url and 'me=' not in self.url:
            print(self.time_stamp+"这个是搜索页面")
            self.url_type = 'search_page'
        elif 's?k=' in self.url and 'me=' in self.url:
            print(self.time_stamp+"这个是店铺里的搜索页面")
            self.url_type = 'store_search_page'
        else:
            print(self.time_stamp+"这个是未识别的页面，按照搜索页处理")
            self.url_type = 'search_page'

    def download_meta_html(self, url: str):  # 如果不是必要的情况下不要调用，这个会向亚马逊请求下载html
        html = requests.get(url, headers=self.user_agent, cookies=self.cookie, timeout=5)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        # 保存html文件
        with open(self.folder_path+'\\' +
                  FILE_TIME +
                  '.html',
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
                    links[index] = self.amazon_head+link
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
        _links_folder = self.folder_path + '\\' + self.url.split('s?k=')[-1].split('&')[0] + '_' + FILE_TIME[:10]
        if _links_folder.split('\\')[-1] not in os.listdir(self.folder_path):
            os.mkdir(_links_folder)
        with open(_links_folder + '\\' + FILE_TIME + '.txt',
                  'a', encoding='utf-8') as link_file:
            link_file.write(self.time_stamp)
            link_file.write(links[index])
            link_file.write('\n')
        print(self.time_stamp+f'保存 {links[index]}')

    def check_if_lisitng_html_downloaded(self, lisitng_url: str, brand_file_path: str):
        # TODO 写一个处理和查找文件夹的方法来检查html文件是否已经下载
        # 检查listing_url 是否在 brand_file_path里
        pass

    def download_all_listing_htmls(self, meta_html: str, listing_folder_path: str):
        listing_url_list = self.find_all_listing(meta_html)
        # TODO 验证链接是否已经下载，解决404问题
        for listing_url in listing_url_list:
            try:
                self.check_if_lisitng_html_downloaded(listing_url)
                print(self.time_stamp+'开始下载以下html：')
                print('http://'+listing_url)
                html = requests.get('http://'+listing_url, headers=self.user_agent, cookies=self.cookie, timeout=5)
                html.raise_for_status()
                html.encoding = html.apparent_encoding
                with open(listing_folder_path+'\\'+f'{FILE_TIME}.html', 'w', encoding='utf-8') as listing_html:
                    listing_html.write(html.text)
                time.sleep(1)
            except requests.exceptions.HTTPError:
                print(self.time_stamp+'下载失败，页面404')
                print('http://'+listing_url)
                continue
        os.startfile(listing_folder_path)

    def find_brand(self, html: str):
        html = etree.HTML(html, etree.HTMLParser())
        brand = html.xpath(xpath_database.brand)
        shipped_by = html.xpath(xpath_database.shipped_by)
        self.brand_list.append(' '.join(brand))
        self.brand_list.append(' '.join(shipped_by))
        self.brand_list = list(filter(None, self.brand_list))

    def find_all_brand(self, folder_path: str):
        print(self.time_stamp+'文件夹中找到以下html：')
        for html_file in os.listdir(folder_path):
            print('\t'+folder_path+'\\'+html_file)
            html = open(folder_path+'\\'+html_file, 'r', encoding='utf-8').read()
            self.find_brand(html)

    def save_brand(self, my_brand: str, brand_file_path: str):
        for each_brand in self.brand_list:
            if brand_file_path.split('\\')[-1] in os.listdir(self.folder_path):
                with open(brand_file_path, 'r', encoding='utf-8') as r:
                    content = r.read()
                    if each_brand not in content:
                        with open(brand_file_path, 'a', encoding='utf-8') as b:
                            b.write(each_brand+'|'+my_brand)
                            b.write('\n')
            elif brand_file_path.split('\\')[-1] not in os.listdir(self.folder_path):
                with open(brand_file_path, 'a', encoding='utf-8') as b:
                    b.write(each_brand + '|' + my_brand)
                    b.write('\n')
        os.startfile(brand_file_path)


if __name__ == '__main__':
    _file_name = r'2020_05_27_15_37_43_568600'+'.html'
    # https://www.amazon.co.uk/s?k=3+Tier+plastic+stackable+Storage+box&ref=nb_sb_noss
    # https://www.amazon.com/s?k=Gloves&i=merchant-items&me=A3NTN1MMYANFVX&qid=1590805429&ref=sr_pg_3
    _url = r'https://www.amazon.com/s?k=Gloves&i=merchant-items&me=A3NTN1MMYANFVX&qid=1590805429&ref=sr_pg_3'
    _html = open(f'D:\\Amazon_html_for_brand_search\\{_file_name}',
                 'r',
                 encoding='utf-8').read()
    # 创建实例
    download_brand = DownloadBrands(_url, AMAZON_MAIN_FOLDER)
    download_brand.check_url()
    # download_brand.download_all_listing_htmls(_html, _folder_path+'\\'+'listing_folder_2020_05_30')
    download_brand.find_all_brand(AMAZON_MAIN_FOLDER+'\\'+'listing_folder_2020_05_30')
    brand_file_name = AMAZON_MAIN_FOLDER+'\\品牌名替换文件_'+FILE_TIME[:10]+'.txt'
    download_brand.save_brand('DALUXE', brand_file_name)
