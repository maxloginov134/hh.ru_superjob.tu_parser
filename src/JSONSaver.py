import json


class JSONSaver:
    """Универсальный класс для сохранения информации о вакансиях в файл по определённым критериям"""

    def __init__(self, keyword):
        self.__filename = f"{keyword.title()}.json"

    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        """Метод для записи информации о подходящих вакансиях в json файл"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self) -> list:
        pass
