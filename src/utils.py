def sort_by_salary_min(data):
    """Функция для сортировки зарплат по минимальному порогу"""
    data = sorted(data, reverse=True)
    return data


def sort_by_salary_max(data):
    """Функция для сортировки зарплат по максимальному порогу"""
    data = sorted(data, key=lambda x: (x.salary_max is not None, x.salary_max), reverse=True)
    return data
