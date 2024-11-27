# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    title = scrapy.Field()  # название
    author = scrapy.Field()  # автор
    publishing = scrapy.Field()  # издательство
    collection = scrapy.Field()  # коллекция
    price = scrapy.Field()  # цена
    link = scrapy.Field()  # url
    _id = scrapy.Field()  # id в базе данных
