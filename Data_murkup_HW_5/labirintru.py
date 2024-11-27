
from gc import callbacks

import requests
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = "labirintru" # Имя паука
    allowed_domains = ["labirint.ru"] # Домен
    start_urls = ["https://www.labirint.ru/search/гарри%20поттер/"] # точка входа

    def parse(self, response: HtmlResponse):
        # Получаем ссылку на следующую страницу, если она есть
        next_page = response.xpath("//div[@class = 'pagination-next']/a/@href").get()
        if next_page:
            # рекурсивный вызов функции со ссылкой на следующую страницу
            yield response.follow(next_page, callback=self.parse)

        # Собираем ссылки со всех книг на странице
        links = response.xpath(
            "//div[contains(@class,'catalog-responsive')]//a[@class='product-title-link']/@href").getall()
        for link in links:
            # Делаем запросы для каждой ссылке, ответы от запросов будут направлятся в метод book_parse
            yield response.follow(link, callback=self.book_parse)

        # метод парсит страницу

    def book_parse(self, response: HtmlResponse):
        author = response.xpath(".//div[@class='product-card__author']/text()").getall()  # автор
        title = response.xpath("//a[@class='product-card__name']/text()").getall() # название
        price = response.xpath(".//div[@class='product-card__price-current']/text()").getall()  # цена
        publishing = response.xpath(".//a[@class='product-card__info-item']/text()").getall()  # издательство
        collection = response.xpath(
            ".//a[@class='product-card__info-item product-card__info-series']/text()").getall()  # коллекция
        link = response.url  # url

        # Отправляем данные в Pipeline
        yield BookparserItem(title=title,
                             author=author,
                             publishing=publishing,
                             collection=collection,
                             price=price,
                             link=link)

