# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_parser.items import LeroymerlinParserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/vhodnye-dveri/']

    def parse(self, response: HtmlResponse):
        products_links = response.xpath("//div[@class='product-name']/a/@href").extract()
        for link in products_links:
            yield response.follow(link, callback=self.parse_products)

    def parse_products(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinParserItem(), response=response)
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('params', "//dt[@class='def-list__term']/text() | //dd[@class='def-list__definition']/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        yield loader.load_item()