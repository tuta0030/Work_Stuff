import os
import pprint as pp
from load_words_list import load_words_list
import config_files


class GetKeywords(object):

    def __init__(self, amazon_dir_path: str) -> None:
        self.amazon_pages_path = config_files.get_amazon_pages_path(amazon_dir_path)
        self.xpath_listing_table = r'//*[@class="a-ordered-list a-vertical"]'
        self.words_list = load_words_list()

    def get_all_title(self, amazon_html: str) -> list:
        html_etree = config_files.get_html_element(amazon_html)
        html_table = html_etree.xpath(self.xpath_listing_table)
        xpath_title = r'//*[@class="aok-inline-block zg-item"]//*[@aria-hidden="true"]/text()'

        all_title = '\n'.join(html_table[0].xpath(xpath_title)).replace('\n', ' ').replace(',', ' ').lower()
        all_title = config_files.remove_words(self.words_list, all_title)
        all_title = list(filter(None, all_title.split(' ')))
        return all_title

    def get_key_words(self, lang: str) -> str:
        html_s = config_files.get_all_html(self.amazon_pages_path)
        all_title = self.get_all_title(html_s[lang.upper()])
        kws = pp.pformat(config_files.count_frequency(all_title)).replace('Counter', lang.upper()).replace('\n', ' ')
        return kws

    def get_key_words_all(self) -> list:
        all_key_words = []
        for lang in self.amazon_pages_path.keys():
            all_key_words.append(self.get_key_words(lang))
        return all_key_words


if __name__ == '__main__':
    path = os.curdir + "\\Amazon_Page"
    g = GetKeywords(path)
    g.get_key_words_all()
