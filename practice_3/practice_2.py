import requests
from bs4 import BeautifulSoup

class Parser(object):
    main_url = ''
    search_link = ''
    site_name = ''
    area_name = ''
    search_words_name = ''
    vacancies_block_class_name = ''
    vacancy_class_name = ''
    vacancy_title_class_name = ''
    vacancy_salary_tag = ''
    vacancy_salary_tag_name = ''
    next_page_button_class_name = ''
    salary_sep = ''
    page_name = 'page'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 '
               'YaBrowser/20.2.0.1145 Yowser/2.5 Safari/537.36'}

    params = {area_name: '',
              search_words_name: ''}

    def __init__(self):
        self.parsed_html = BeautifulSoup()
        self.block_of_vacancies = BeautifulSoup()
        self.data = list()

    def get_response(self, area='', search_text='', page=1):

        self.params.update({self.search_words_name: search_text,
                            self.area_name: area,
                            self.page_name: page})
        response = requests.get(self.main_url + self.search_link, headers=self.headers, params=self.params)

        return response

    def parse_html(self, response):
        self.parsed_html = BeautifulSoup(response.text, 'lxml')

    def fill_block_of_vacancies(self):
        self.block_of_vacancies = self.parsed_html.find('div', {'class': self.vacancies_block_class_name})

    def get_list_of_vacancies(self):
        return self.block_of_vacancies.find_all('div', {'class': self.vacancy_class_name})

    def get_salary_info(self, salary_html):
        salary = {'min': None,
                  'max': None,
                  'currency_name': None}

        if salary_html:
            salary_str = salary_html.text

            flag = False
            for i in range(10):
                if str(i) in salary_str:
                    flag = True
                    break

            if not flag:
                return salary

            salary_str = salary_str.replace('.', '')


            last_number_index = len(salary_str)
            for char in salary_str[::-1]:
                if '0' <= char <= '9' or char == ' ':
                    break
                last_number_index -= 1

            salary['currency_name'] = salary_str[last_number_index:].replace('\xa0', '')


            salary_str = salary_str.replace(salary_str[last_number_index:], '')

            salary_str = salary_str.replace(' ', '')
            if salary_str.startswith('от'):

                salary_str = salary_str.replace('от', '')
                salary['min'] = int(salary_str)

            elif salary_str.startswith('до'):

                salary_str = salary_str.replace('до', '')
                salary['max'] = int(salary_str)

            else:
                try:
                    salary['min'], salary['max'] = map(int, salary_str.split(self.salary_sep))
                except:
                    salary['min'] = int(salary_str)

        return salary

    def get_vacancy_info(self, vacancy):
        vacancy_info = {}
        vacancy_title = vacancy.find('a', {'class': self.vacancy_title_class_name})

        vacancy_info['name'] = vacancy_title.text
        vacancy_info['href'] = vacancy_title['href']

        vacancy_salary = vacancy.find('span', {self.vacancy_salary_tag: self.vacancy_salary_tag_name})
        vacancy_info.update(self.get_salary_info(vacancy_salary))

        vacancy_info['site_name'] = self.site_name

        return vacancy_info

    def get_vacancies_from_all_pages(self, area='', search_text=''):
        old_data = self.data.copy()
        page = 0

        response = self.get_response(area, search_text)
        self.parse_html(response)
        self.fill_block_of_vacancies()

        list_on_page = self.get_list_of_vacancies()
        for vacancy in list_on_page:
            self.data.append(self.get_vacancy_info(vacancy))

        while self.parsed_html.find('a', {'class': self.next_page_button_class_name}):
            old_data = self.data.copy()
            page += 1
            response = self.get_response(area, search_text, page=page)

            self.parse_html(response)
            self.fill_block_of_vacancies()


            list_on_page = self.get_list_of_vacancies()

            for vacancy in list_on_page:

                self.data.append(self.get_vacancy_info(vacancy))


            if old_data == self.data:
                page -= 1
        return self.data


class Hh_Parser(Parser):
    main_url = 'https://hh.ru'
    search_link = '/search/vacancy?'
    site_name = 'HeadHunter'
    area_name = 'area'
    search_words_name = 'text'
    vacancies_block_class_name = 'vacancy-serp'
    vacancy_class_name = 'vacancy-serp-item'
    vacancy_title_class_name = 'bloko-link HH-LinkModifier'
    vacancy_salary_tag = 'data-qa'
    vacancy_salary_tag_name = 'vacancy-serp__vacancy-compensation'
    next_page_button_class_name = 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'
    salary_sep = '-'


class Sj_Parser(Parser):
    main_url = 'https://www.superjob.ru'
    search_link = '/vacancy/search/?'
    site_name = 'SuperJob'
    area_name = 'geo'
    search_words_name = 'keywords'
    vacancies_block_class_name = '_1ID8B'
    vacancy_class_name = '_3zucV f-test-vacancy-item undefined RwN9e _3tNK- _1I1pc'
    vacancy_title_class_name = '_1UJAN'
    vacancy_salary_tag = 'class'
    vacancy_salary_tag_name = 'f-test-text-company-item-salary'
    next_page_button_class_name = 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'
    salary_sep = '—'

    def get_vacancy_info(self, vacancy):
        vacancy_info = {}
        vacancy_title = vacancy.find('a', {'class': self.vacancy_title_class_name})

        vacancy_info['name'] = vacancy_title.text
        vacancy_info['href'] = self.main_url + vacancy_title['href']

        vacancy_salary = vacancy.find('span', {self.vacancy_salary_tag: self.vacancy_salary_tag_name})
        vacancy_info.update(self.get_salary_info(vacancy_salary))

        vacancy_info['site_name'] = self.site_name

        return vacancy_info

def get_data_from_practice_2():
    hh = Hh_Parser()
    search_vacancy = input('Введите текст для поиска на HH: ')
    print(len(hh.get_vacancies_from_all_pages(search_text=search_vacancy)))


    sj = Sj_Parser()
    search_vacancy = input('Введите текст для поиска на SuperJob: ')
    print(len(sj.get_vacancies_from_all_pages(search_text=search_vacancy)))

    data = list()
    data.extend(hh.data)
    data.extend(sj.data)

    return data


