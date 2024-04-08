import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrap():
    url = 'https://www.converse.com.tr/erkek-tum-ayakkabilar/'
    product_data = []
    p =0
    while True:
        p+=1
        if p >=11:
            break
        page = requests.get(f'{url}?page={p}')
        tree = BeautifulSoup(page.content,'html.parser')
        time.sleep(3)
        lis = tree.find('div',class_='body').find('div',class_='products__items').find('div',class_='js-product-wrapper product-item')
        for li in  lis:

            product = {}

            try:
                product['link'] = 'https://www.converse.com.tr'+li.find('a')['href']
            except:
                product['link'] = ''

            try :
                product['title'] = li.find('h2',class_='product-item__name d-block js-product-anchor fsize-14').get_text()
            except :
                product['title'] = ''

            try:
                product['imageURL'] = li.find('img').get('data-src')
            except :
                product['imageURL'] = ''

            try:
                product['price'] = li.find('div',class_='product-item__price').get_text().strip()
            except:
                product['price'] = ''

            product_data.append(product)

        print(f'page_number: {p} | products_count: {len(product_data)}')

        df = pd.DataFrame([t for t in product_data])
        out_filename = '/Users/mac/Documents/Output_data.csv'
        df.to_csv(out_filename, index=False)

scrap()
