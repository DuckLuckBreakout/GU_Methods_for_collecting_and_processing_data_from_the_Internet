# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import hashlib

from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin_photos

    def process_item(self, item, spider):
        item = fix_price(item)
        item = fix_params(item)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeroymerlinParserPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{get_dir_name(request.url)}/{image_guid}'


def get_dir_name(url):
    dir_name = url.rfind('/LMCode/')
    return url[dir_name + len('/LMCode/'): dir_name + len('/LMCode/') + 8]


def fix_price(item):
    item['price'] = int(item['price'].replace(' ', ''))
    return item


def fix_params(item):
    normal_params = []
    param = ''
    for elem in item['params']:
        elem = elem.replace('\n', '')
        while elem.find('  ') != -1:
            elem = elem.replace('  ', ' ')
        if param:
            elem = elem.strip()
            normal_params.append((param, elem))
            param = ''
        else:
            param = elem
    item['params'] = normal_params
    return item