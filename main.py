from src.classes import HeadHunterAPI, JSONSaver


def main():

    # keyword = input('Введите слово для поиска: ')
    keyword = "python"

    hh_api = HeadHunterAPI()

    hh_vacancies = hh_api.get_vacancies(keyword)

    json_sever = JSONSaver(keyword)
    json_sever.add_vacancies(hh_vacancies)
    data = json_sever.select()

    for row in data:
        print(row, end=f"\n\n{'_'*180}\n\n")


if __name__ == "__main__":
    main()

