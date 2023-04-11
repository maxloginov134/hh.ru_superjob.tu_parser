import json
from abc import ABC, abstractmethod
import requests


class Engine(ABC):
    def get_requast(self):
        pass


class HeadHunterAPI(Engine):
    def get_requast(self, keyword, page):
        # headers = {
        #   "User-Agent": "TestApp/1.0(test@example.com)"
        # }
        params = {
            "test": keyword,
            "page": page,
            "per_page": 100,
        }
        return requests.get("https://api.hh.ru/vacancies", params=params).json()['items']

    def get_vacancies(self, keyword, count=1000):
        pages = 1
        response = []

        for page in range(pages):
            print(f"Парсинг страницы {page+1}", end=": ")
            values = self.get_requast(keyword, page)
            print(f"Найдено {len(values)} вакансий")
            response.extend(values)

        return response


class Vacancy:
    __slots__ = ('title', 'salary_min', 'salary_max', 'currency', 'employer', 'link')

    def __init__(self, title, salary_min, salary_max, currency, employer, link):
        self.title = title
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.employer = employer
        self.link = link

    def __str__(self):
        salary_min = f'От {self.salary_min}' if self.salary_min else ''
        salary_max = f'До {self.salary_max}' if self.salary_max else ''
        currency = self.currency if self.currency else ''
        if self.salary_min is None and self.salary_max is None:
            salary_min = "Не указано"
        return f"{self.employer}: {self.title} \n{salary_min} {salary_max} {currency}\nURL: {self.link}"


class JSONSaver:
    def __init__(self, keyword):
        self.__filename = f"{keyword.title()}.json"

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []
        for row in data:
            salary_min, salary_max, currency = None, None, None
            if row['salary']:
                salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary']['currency']
            vacancies.append(Vacancy(row['name'], salary_min, salary_max, currency, row['employer']['name'],
                                     row['alternate_url']))
        return vacancies
