# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class VacancySpider(scrapy.Spider):
    name = ''
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
        name = response.xpath(self.vacancy_name_xpath).extract()[0]
        salary = response.xpath(self.vacancy_salary_xpath).extract()
        href = response.url
        yield JobparserItem(name=name, salary=salary, href=href)