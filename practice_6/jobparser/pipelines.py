# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Item
from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies

    def process_item(self, item: Item, spider):
        collection = self.mongobase[spider.name]
        item = fix_salary(item, spider.name)
        collection.insert_one(item)
        return item


def fix_salary(item: Item, spider_name):
    salary = item['salary']

    if spider_name == 'superjobru':
        if len(salary) == 1:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None

        elif len(salary) == 4:
            item['salary_min'] = int(salary[0].replace('\xa0', ''))
            item['salary_max'] = int(salary[1].replace('\xa0', ''))
            item['salary_currency'] = salary[-1]

        elif len(salary) == 5:
            if salary[0].startswith('от'):
                item['salary_min'] = int(salary[2].replace('\xa0', ''))
                item['salary_max'] = None
            elif salary[0].startswith('до'):
                item['salary_min'] = None
                item['salary_max'] = int(salary[2].replace('\xa0', ''))
            item['salary_currency'] = salary[-1]

    elif spider_name == 'hhru':
        if len(salary) == 1:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None

        elif len(salary) == 7:
            item['salary_min'] = int(salary[1].replace('\xa0', ''))
            item['salary_max'] = int(salary[3].replace('\xa0', ''))
            item['salary_currency'] = salary[-2][:3]

        elif len(salary) == 5:
            if salary[0].startswith('от'):
                item['salary_min'] = int(salary[1].replace('\xa0', ''))
                item['salary_max'] = None
            elif salary[0].startswith('до'):
                item['salary_min'] = None
                item['salary_max'] = int(salary[1].replace('\xa0', ''))
            item['salary_currency'] = salary[-2][:3]



    item.pop('salary')

    return item


