from jobparser.spiders.VacancySpider import VacancySpider

class HhruSpider(VacancySpider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&text=python']
    next_page_href_xpath = "//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href"
    vacancies_href_xpath = "//a[@class='bloko-link HH-LinkModifier']/@href"
    vacancy_name_xpath = "//h1[@class='bloko-header-1']/text()"
    vacancy_salary_xpath = "//span[@class='bloko-header-2 bloko-header-2_lite']/text()"







