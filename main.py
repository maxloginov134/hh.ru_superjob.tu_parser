from src.SiteParsingHH_RU import HeadHunterAPI, JSONSaver
from src.SiteParsingSuperjob import SuperJobAPI, JSONSaver
from src.utils import sort_by_salary_min


def main():

    hh_keyword = input('Введите слово для поиска: ')
    # super_keyword = input('Введите слово для поиска: ')

    hh_api = HeadHunterAPI()
    # superjob_api = SuperJobAPI

    hh_vacancies = hh_api.get_vacancies(hh_keyword)
    # super_vacancies = superjob_api.get_vacancies_super

    json_sever_hh = JSONSaver(hh_keyword)
    # json_server_super = JSONSaver(super_keyword)
    # json_server_super.add_vacancies(super_vacancies)
    json_sever_hh.add_vacancies(hh_vacancies)
    data_hh = json_sever_hh.select()
    data_hh = sort_by_salary_min(data_hh)

    for row in data_hh:
        print(row, end=f"\n\n{'_'*180}\n\n")


if __name__ == "__main__":
    main()

