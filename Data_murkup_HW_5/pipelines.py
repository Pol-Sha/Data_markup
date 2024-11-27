# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookparserPipeline:
    def __init__(self):
        # Настраиваем клиент MongoDB (IP, порт)
        client = MongoClient('localhost', 27017)
        # Задаём название базы данных
        self.mongo_base = client.books_labirint


    def process_item(self, item, spider):
        # коллекция в БД (имя паука)
        collection = self.mongo_base[spider.name]

        # id
        try:
            *_, id, _ = item['link'].split('/')
            item['_id'] = id
        except ValueError:
            item['_id'] = None

        # название
        _, title = item.get('title').split(':')
        item['title'] = title.strip()

        # авторы
        item['author'] = ', '.join(item['author'])

        # издательство
        item['publishing'] = ', '.join(item['publishing'])

        # коллекция
        item['collection'] = ', '.join(item['collection'])

        # цена
        try:
            item['price'] = float(item['price'])
        except ValueError:
            item['price'] = None

        try:
            # Добавляем запись в базу данных
            collection.insert_one(item)
        except ValueError:
            print('Ошибка при загрузке документа')

        return item