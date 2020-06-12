import os
import pprint as pp
from load_words_list import load_words_list
import config_files
import re


def remove_brand(string: str):
    # TODO 不管用
    _brands = open('品牌名称.txt', 'r', encoding='utf-8').read()
    _brands = list(filter(None, list(set(_brands.split('|')))))
    _brands = str('|'.join(_brands))
    print('')
    print("_brands:" + _brands)
    print('')
    _pattern = re.compile('')
    _result = re.sub(_pattern, '', string)
    return _result


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
    test_str = 'Wall Shelf Shelves Floating Storage Of Metal Including Organ Rack Wooden Screws 100% 30mm 27mm Black Decor 12" Mounting Mount Tikai Bookcase Agsivo Living Tier Derful Scaffold Steam L Mounted Ible Tanburo D Décor 70 Cm  Ati Tiered Frames Tressed Rail  Decorative 17”x5.2” Collecti Ohls Kit 85cm Up  Sriwatana Shabby 200mm Coat Free More 9210-a Eycomb 3-piece Square Woltu Available 300mm Country Swing Bekvam Express Creative Birch Ornaments Vintage Spice Wm050-er Wood 2-tier Acrylic Bedroom  Hall Natural  Er Mdf Hook 80x29.5cm Chic Hiimiei Ir Brackets S Pre-assembled Bedroom. To Oak W Kids  3 Pack Color Showcase Welded Hooks Medium 15.7" Clas Y Set In Corner High Styl Shaped Solid Books String Harm Decor. ~ Rustic Box Kg -lipped Kitchen  Tassel Cast Large Dy Rectangle Wire E® Accessory Nursery 16.5 Bookshelves Hanging Sc E1 -white Ricoo Holder 44lbs Thicker Cealed Multiple 60/45/30 Lws24wt 58x11x52 Hexag Decorati Plank Sa Round Cube Products From'
    print(test_str)
    print(len(test_str))
    result = remove_brand(test_str)
    print(result)
    print(len(result))
