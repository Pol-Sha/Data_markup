# Сценарий Foursquare
# Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
# Используйте API Foursquare для поиска заведений в указанной категории.
# Получите название заведения, его адрес и рейтинг для каждого из них.
# Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.
from typing import List, Dict, Any

import requests
from fake_useragent import UserAgent

ua = UserAgent() #### для указания "браузера"
category = input("Введите название интересующей Вас категории на английском языке (например: Cafe, Fitness, Park, Zoos, Museums и т.п.) : ")
url = "https://api.foursquare.com/v3/places/search"
params = {
    'limit': 10,
    'query': category,
    'fields': 'name,location,rating'}

headers = {
    "User-Agent": ua.firefox,
    "Accept": "application/json",
    "Authorization": "fsq3P6zWw5hrHAp69JoTu+0TFeYEBCEXDIo7+Ivypcz/4Uo="}

response = requests.request("GET", url, params=params, headers=headers)
if response.status_code == 200:
    print("Успешный запрос API по URL: ", response.url)
else:
    print("Запрос API отклонен с кодом состояния:", response.status_code)

data = response.json()
### pprint(data) ### для отображения структуры ответа

facilitys = []
for place in data['results']:
    place_name = place.get('name')
    place_address = place.get('location')['formatted_address']
    place_rating = place.get('rating') if 'rating' in place else "Рейтинг не определялся"
    facilitys.append({'name': place_name, 'address': place_address, 'rating': place_rating})
for facility in facilitys:
        print(f"Название: {facility['name']}")
        print(f"Адрес: {facility['address']}")
        print(f"Рейтинг: {facility['rating']}")
        print()