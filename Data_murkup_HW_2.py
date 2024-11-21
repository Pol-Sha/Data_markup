#Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
#и извлечь информацию о всех книгах на сайте во всех категориях:
#название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import json

ua = UserAgent()
url = "https://books.toscrape.com/"

headers = {'User-Agent': ua.chrome}
params = {'page': 1}
session = requests.session()


all_books =[]
#next_page = 'page-1.html'
while params['page'] <= 50 :
    response = session.get(url, headers=headers, params = params)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all('article', {'class': 'product_pod'})
    #next_page = soup.find('li', {'class': 'next'}).find('a')['href']
    for book in books:
        book_info={}

        # Название
        name_info = book.find('h3').find('a')
        book_info['name'] = name_info.getText().strip()
        book_info['ref'] = url + name_info.get('href')

        #Стоимость
        price_book_info = book.find('div', {'class': 'product_price'}).find('p', {'class': 'price_color'}).getText()
        book_info['price_book'] = float(price_book_info[2:]) # удаляем знак валюты

        # Описание книги
        description_book_info = soup.find('meta', {'name': 'description'})
        book_info['description_book'] = description_book_info['content'].strip() if description_book_info else "Описание отсутствует"

        # наличие
        instock_book_info = soup.find('p', {'class': 'instock availability'})
        book_info['instock_book'] = instock_book_info.getText().strip()


        all_books.append(book_info)
    print(f"Обработка {params['page']} страница")
    params['page']+= 1

pprint(all_books)


