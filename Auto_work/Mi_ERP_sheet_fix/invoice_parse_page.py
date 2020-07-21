from order_info import info
import re


def search_in_text(item: str, txt: str):
    pattern = re.compile(f'(?<={item}_:_).+?(?=_Item total)')
    return re.search(pattern, txt)


def parse_page_lxml(self, sheet_info: dict):
    html = self.get_html_etree()
    shipping_raw_info = '_'.join(html.xpath(self.xpath['quantity']+'//text()'))

    elements_buyer_info = html.xpath(self.xpath['buyer_info']+'//text()')
    elements_product_name = html.xpath(self.xpath['product_name']+'//text()')[0]
    elements_sku = html.xpath(self.xpath['SKU']+'//text()')[-1][2:].strip()
    elements_order_num = html.xpath(self.xpath['order_id'] + '//text()')[0]
    elements_date = html.xpath(self.xpath['date']+'//text()')[0]
    elements_price = html.xpath(self.xpath['price']+'//text()')[-1]
    elements_quantity = html.xpath(self.xpath['quantity']+'//text()')[22]
    elements_sub_total = html.xpath(self.xpath['sub_total']+'//text()')[0]
    elements_signature = html.xpath(self.xpath['signature']+'//text()')[0]
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


if __name__ == '__main__':
    pass

