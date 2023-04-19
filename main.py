from src.SiteParsingHH_RU import HeadHunterAPI, JSONSaverHH
from src.SiteParsingSuperjob import SuperJobAPI, JSONSaverSuper
from src.utils import sort_by_salary_min


def main():

    print("Для начала поищем для вас подходящие вакансии на платформе HeadHunter")

    hh_keyword = input('Введите слово для поиска: ')

    hh_api = HeadHunterAPI()

    hh_vacancies = hh_api.get_vacancies(hh_keyword)

    json_sever_hh = JSONSaverHH(hh_keyword)
    json_sever_hh.add_vacancies(hh_vacancies)
    data_hh = json_sever_hh.select()
    data_hh = sort_by_salary_min(data_hh)

    for row in data_hh:
        print(row, end=f"\n\n{'_'*180}\n\n")

    input(f"Ничего не нашли?\nНажмите: Enter для продолжения поиска на другой платформе.")

    spj_keyword = input("Ведите слово для поиска: ")

    spj_api = SuperJobAPI()

    spj_vacancies = spj_api.get_vacancies_super(spj_keyword)

    json_server_spj = JSONSaverSuper(spj_keyword)
    json_server_spj.add_vacancies(spj_vacancies)
    data_spj = json_server_spj.select()

    for row in data_spj:
        print(row, end=f"\n\n{'_'*180}\n\n")


if __name__ == "__main__":
    main()

