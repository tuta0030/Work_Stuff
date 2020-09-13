from order_info import info
import re
from lxml import etree


def search_in_text(item: str, txt: str):
    pattern = re.compile(f'(?<={item}_:_).+?(?=_Item total)')
    return re.search(pattern, txt)


def parse_page_lxml(self, sheet_info: dict, sheet):
    html = self.get_html_etree()
    shipping_raw_info = '_'.join(html.xpath(self.xpath['quantity']+'//text()'))
    orders_table = html.xpath(self.xpath['items_table']+'//tr')

    def get_orders_table_items(orders) -> list:
        orders_list = []
        for each_order in orders:
            td_text = \
                [each_text for each_text in each_order.xpath('td//text()') if str(each_text).strip() != ':']

            name = td_text[1]
            sku = td_text[5].split(' ')[-1]
            sub_total = td_text[-3]
            price = td_text[-5]
            num = td_text[-6]

            td_dict = {'name': name,
                       'price': price,
                       'sku': sku,
                       'sub_total': sub_total,
                       'num': num
                       }
            for k, v in td_dict.items():
                print(f'{k}:\t{v}')
            orders_list.append(td_dict)
        print(orders_list)
        return orders_list

    orders_lists = get_orders_table_items(orders_table)

    def mk_more_orders_in_sheet():
        if len(orders_lists) != 1:
            row = 16
            total = []
            money_sign = ''
            for each_order in orders_lists:
                sheet.insert_rows(row)
                sheet.cell(row, 5).value = each_order['num']
                sheet.cell(row, 6).value = each_order['sub_total']
                money_sign = each_order['sub_total'][:1]
                total.append(float(each_order['sub_total'][1:]))
                sheet.cell(row, 3).value = each_order['name']
                sheet.cell(row, 1).value = each_order['sku']
                sheet.cell(row, 4).value = each_order['price']
            nonlocal sheet_info
            sheet_info['total'].value = money_sign + str(sum(total))

    elements_buyer_info = html.xpath(self.xpath['buyer_info']+'//text()')
    elements_order_num = html.xpath(self.xpath['order_id'] + '//text()')[0]
    elements_date = html.xpath(self.xpath['date']+'//text()')[0]
    elements_price = html.xpath(self.xpath['price']+'//text()')[-1]
    elements_signature = html.xpath(self.xpath['signature']+'//text()')[0]

    elements_quantity = html.xpath(self.xpath['quantity']+'//text()')[22]
    elements_sub_total = html.xpath(self.xpath['sub_total']+'//text()')[0]
    elements_product_name = html.xpath(self.xpath['product_name']+'//text()')[0]
    elements_sku = html.xpath(self.xpath['SKU']+'//text()')[-1][2:].strip()

    try:
        elements_shipping_cost = search_in_text('Shipping total', shipping_raw_info)[0]
    except TypeError:
        elements_shipping_cost = '0'
    try:
        elements_phone = html.xpath(self.xpath['phone'] + '//text()')[0]
    except IndexError:
        elements_phone = '需要手动添加电话'
    try:
        elements_total = html.xpath(self.xpath['total'] + '//text()')[0]
    except IndexError:
        elements_total = html.xpath(self.xpath['refund'] + '//text()')[0]

    info['order_id'] = elements_order_num
    info['SKU'] = elements_sku
    info['product_name'] = elements_product_name
    info['date'] = elements_date
    info['price'] = elements_price
    info['quantity'] = elements_quantity
    info['sub_total'] = elements_sub_total
    info['amount'] = elements_sub_total
    info['ship_cost'] = elements_shipping_cost
    info['total'] = elements_total
    info['signature'] = elements_signature
    info['phone'] = elements_phone
    info['buyer_info'] = '\n'.join(elements_buyer_info) + '\n' + elements_phone

    sheet_info['SKU'].value = info['SKU']
    sheet_info['product_name'].value = info['product_name']
    sheet_info['date'].value = info['date']
    sheet_info['price'].value = info['price']
    sheet_info['quantity'].value = info['quantity']
    sheet_info['sub_total'].value = info['sub_total']
    sheet_info['amount'].value = info['amount']
    sheet_info['ship_cost'].value = info['ship_cost']
    sheet_info['total'].value = info['total']
    sheet_info['signature'].value = info['signature']
    sheet_info['buyer_info'].value = info['buyer_info']
    sheet_info['order_id'] = info['order_id']

    mk_more_orders_in_sheet()

    print("订单号：" + info['order_id'])
    print("下单日期：" + info['date'])
    print("SKU:" + info['SKU'])
    print("产品名称：" + info['product_name'])
    print("价格：" + info['price'])
    print("数量：" + info['quantity'])
    print("总价：" + info['amount'])
    print("小计：" + info['sub_total'])
    print("运费：" + info['ship_cost'])
    print("总计：" + info['total'])
    print("签名：" + info['signature'])
    print("买家信息：" + '\n' + info['buyer_info'])
    print("电话：" + elements_phone)
    print('订单:' + str(orders_table))


def mk_new_html(html_element):
    return etree.HTML(etree.tostring(html_element), etree.HTMLParser())


if __name__ == '__main__':
    pass

