from datetime import date

import requests
import xlsxwriter
from bs4 import BeautifulSoup as bs

URL = 'https://coffee-craft.com.ua/svezheobzharennyiy-kofe-v-zernah/'


def get_data(url):
    response = requests.get(url).content
    return response


def parse_data(response):
    soup = bs(response, 'lxml')
    cards = soup.findAll('div', class_='product-thumb')
    result = {}
    for product in cards:
        title = product.find('div', class_='caption').text.split('(')[0].strip().split(' ', 1)[1]
        prices = product.findAll('p', class_='listItem1')
        result[title] = {}
        for price in prices:
            weight = int(price.find('span', class_='itemean').text.strip().split()[0])
            try:
                hprice = float(price.find('span', class_='hprice').text.strip().split()[0])
            except AttributeError:
                hprice = float(price.find('span', class_='hprice-new').text.strip().split()[0])
            result[title].update({weight: hprice})

    return result

def parse_data_ucc(response):
    pass
def write_to_excel(products):
    day = date.today().strftime("%d_%m_%Y")
    workbook = xlsxwriter.Workbook(f'coffee_price_{day}.xlsx')
    worksheet = workbook.add_worksheet(f'{day}')
    headers = ['Название', '100 г', '250 г', '1 кг']
    column = 0
    for head in headers:
        worksheet.write(0, column, head)
        column += 1
    row = 1
    columns = {100: 1, 250: 2, 1: 3}
    for product in products.items():
        title, data = product
        worksheet.write(row, 0, title)
        for weight, price in data.items():
            worksheet.write(row, columns.get(weight), price)
        row += 1
    worksheet.autofit()
    workbook.close()


def main():
    response = get_data(URL)
    result = parse_data(response)
    write_to_excel(result)


if __name__ == '__main__':
    main()
