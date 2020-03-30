# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class VacancySpider(scrapy.Spider):
    name = ''
    site_name = ''
    allowed_domains = ['']
    start_urls = ['']
    next_page_href_xpath = ""
    vacancies_href_xpath = ""
    vacancy_name_xpath = ""
    vacancy_salary_xpath = ""

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(self.next_page_href_xpath).extract_first()
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath(self.vacancies_href_xpath).extract()
        for link in vac_list:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name', self.vacancy_name_xpath)
        loader.add_xpath('salary', self.vacancy_salary_xpath)
        loader.add_xpath('name', self.vacancy_name_xpath)
        loader.add_value('href', response.url)
        loader.add_value('site_name', self.site_name)
        yield loader.load_item()
