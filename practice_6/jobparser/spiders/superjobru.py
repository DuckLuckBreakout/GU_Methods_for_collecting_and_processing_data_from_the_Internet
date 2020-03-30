from jobparser.spiders.VacancySpider import VacancySpider

class SuperjobruSpider(VacancySpider):
    name = 'superjobru'
    site_name = 'superjob.ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']
    next_page_href_xpath = "//a[contains(@class, 'f-test-button-dalshe')]/@href"
    vacancies_href_xpath = "//a[contains(@class, '_2JivQ')]/@href"
    vacancy_name_xpath = "//h1/text()"
    vacancy_salary_xpath = "//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text() | " \
                           "//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/span[last()]/text() "


