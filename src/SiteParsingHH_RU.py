import json
from abc import ABC
import requests

from src.Engine import Engine
from src.JSONSaver import JSONSaver


class HeadHunterAPI(Engine):
    """Класс для работы с API сайтом hh.ru"""
    def get_request(self, keyword, page):

        params = {
            "text": keyword,
            "page": page,
            "per_page": 100,
        }
        try:
            return requests.get("https://api.hh.ru/vacancies", params=params).json()['items']

        except Exception as err:
            raise err

    def get_vacancies(self, keyword):
        """Метод для отображения найденных вакансий"""
        pages = 1
        response = []

        for page in range(pages):
            print(f"Парсинг страницы {page+1}", end=": ")
            try:
                values = self.get_request(keyword, page)
                print(f"Найдено {len(values)} вакансий")
                response.extend(values)
            except Exception as err:
                print(f"Произошла ошибка при получении вакансий: {err}")

        return response


class Vacancy:
    """Класс для работы с подходящими вакансиями"""
    __slots__ = ('title', 'salary_min', 'salary_max', 'currency', 'employer', 'link')

    def __init__(self, title, salary_min, salary_max, currency, employer, link):
        self.title = title
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.employer = employer
        self.link = link

    def __str__(self):
        """Метод для корректного отображения по минимальной и максимальной зарплате"""
        salary_min = f'От {self.salary_min}' if self.salary_min else ''
        salary_max = f'До {self.salary_max}' if self.salary_max else ''
        currency = self.currency if self.currency else ''
        if self.salary_min is None and self.salary_max is None:
            salary_min = "Не указано"
        return f"{self.employer}: {self.title} \n{salary_min} {salary_max} {currency}\nURL: {self.link}"

    def __gt__(self, other):
        """Метод за счёт которого осуществляется сравнение"""
        if not other.salary_min:
            return True
        if not self.salary_min:
            return False
        return self.salary_min >= other.salary_min


class JSONSaverHH(JSONSaver):
    """Класс для сохранения информации о вакансиях в файл по определённым критериям"""
    def __init__(self, keyword):
        super().__init__(keyword)

    def select(self):
        """Метод для чтения информации о вакансиях из json файла"""
        with open(self.filename(), 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []
        for row in data:
            salary_min, salary_max, currency = None, None, None
            if row['salary']:
                salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary']['currency']
            vacancies.append(Vacancy(row['name'], salary_min, salary_max, currency, row['employer']['name'],
                                     row['alternate_url']))
        return vacancies
