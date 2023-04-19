import json
import requests
from abc import ABC
from src.SiteParsingHH_RU import Engine


class SuperJobAPI(Engine):
    """Класс для работы с API сайтом SuperJob.ru"""
    URL = "https://api.superjob.ru/2.0/vacancies/?"

    def __init__(self):
        self.__vacancies_list = []

    def __get_request(self, vacancy_for_search: str, pages_for_parse=1) -> list:
        """
        Метод для финальной реализации парсинга,
        в качестве аргументов принимаются ключевое слово и кол-во страниц для парсинга,
        после передачи всех необходимых аргументов происходит парсинг,
        метод скрыт и используется в качестве финального шага.
        """

        header = {
            'X-Api-App-Id':
                "v3.r.137491480.efc206e4525fb50a0bc91e6c0ecff6cec64b1fdb.20452df5d70be14cfb657a43773b962c328135b5"
        }

        params = {
            'test': vacancy_for_search.title(),
            'count': 100,
            'page': pages_for_parse,
        }

        return requests.get(self.URL, headers=header, params=params).json()['objects']

    def get_vacancies_super(self, vacancy_for_search: str):
        """Метод для отображения найденных вакансий"""
        pages = 1
        response = []

        for page in range(pages):
            print(f"Парсинг страницы {page+1}", end=": ")
            values = self.__get_request(vacancy_for_search)
            print(f"Найдено {len(values)} вакансий")
            response.extend(values)

        return response


class Vacancy:
    """Класс для работы с подходящими вакансиями"""
    __slots__ = ('title', 'payment_from', 'payment_to', 'currency', 'employer', 'link')

    def __init__(self, title, payment_from, payment_to, currency, employer, link):
        self.title = title
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.currency = currency
        self.employer = employer
        self.link = link

    def __str__(self):
        """Метод для корректного отображения по минимальной и максимальной зарплате"""
        payment_from = f'От {self.payment_from}' if self.payment_from else ''
        payment_to = f'До {self.payment_to}' if self.payment_to else ''
        currency = self.currency if self.currency else ''
        if self.payment_from is None and self.payment_to is None:
            payment_from = "Не указано"
        return f"{self.title}: {self.employer} \n{payment_from} {payment_to} {currency}\nURL: {self.link}"

    def __gt__(self, other):
        """Метод за счёт которого осуществляется сравнение"""
        if not other.payment_from:
            return True
        if not self.payment_from:
            return False
        return self.payment_from >= other.payment_from


class JSONSaverSuper:
    """Класс для сохранения информации о вакансиях в файл по определённым критериям"""
    def __init__(self, keyword):
        self.__filename = f"{keyword.title()}.json"

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        """Метод для записи информации о подходящих вакансиях в json файл"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        """Метод для чтения информации о вакансиях из json файла"""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []
        for row in data:
            payment_from, payment_to, currency = None, None, None
            if row['payment_from']:
                payment_from, payment_to, currency = row['payment_from'], row['payment_to'], row['currency']
            vacancies.append(Vacancy(row['firm_name'], payment_from, payment_to, currency, row['profession'],
                                     row['link']))
        return vacancies
