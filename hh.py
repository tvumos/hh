import requests
import time
import pprint
import json

class City:
    URL = 'https://api.hh.ru/areas/'

    def find_area(self, area_name):
        items = requests.get(self.URL).json()
        # pprint.pprint(items)
        return items

class HH:
    URL = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.keywords = ''
        self.area = ''
        self.count = 0
        self.salary_avg = 0
        self.requirements = []

    def vacancy_salary(self, salary):
        """
        Возвращает чистую сумму предлагаемой зарплаты, без налогов и в рублях
        :param salary: Словарь: {'currency': 'RUR', 'from': 120000, 'gross': False, 'to': None},
        :return:
        """
        sum_salary = 0
        if salary["currency"] == "RUR":
            if salary["gross"]:  # Грязная зарплата, вычитаем налог 13 %
                if salary["from"] is not None and salary["to"] is not None:
                    sum_salary = abs(salary["to"] - salary["from"]) / 2 * 0.87
                else:
                    if salary["from"] is not None:
                        sum_salary = salary["from"] * 0.87
                    elif salary["to"] is not None:
                        sum_salary = salary["to"] * 0.87
            else:               # Чистая зарплата без налога
                if salary["from"] is not None and salary["to"] is not None:
                    sum_salary = abs(salary["to"] - salary["from"]) / 2
                else:
                    if salary["from"] is not None:
                        sum_salary = salary["from"]
                    elif salary["to"] is not None:
                        sum_salary = salary["to"]
        elif salary["currency"] == "USD":       # Считаем курс доллара = 62 рубля
            if salary["gross"]:  # Грязная зарплата, вычитаем налог 13 %
                if salary["from"] is not None and salary["to"] is not None:
                    sum_salary = abs(salary["to"] - salary["from"]) / 2 * 0.87 * 62
                else:
                    if salary["from"] is not None:
                        sum_salary = salary["from"] * 0.87 * 62
                    elif salary["to"] is not None:
                        sum_salary = salary["to"] * 0.87 * 62
            else:               # Чистая зарплата без налога
                if salary["from"] is not None and salary["to"] is not None:
                    sum_salary = abs(salary["to"] - salary["from"]) / 2 * 62
                else:
                    if salary["from"] is not None:
                        sum_salary = salary["from"] * 62
                    elif salary["to"] is not None:
                        sum_salary = salary["to"] * 62
        elif salary["currency"] == "EUR":       # Считаем курс евро = 69 рубля
            if salary["gross"]:  # Грязная зарплата, вычитаем налог 13 %
                if salary["from"] is not None and salary["to"] is not None:
                    sum_salary = abs(salary["to"] - salary["from"]) / 2 * 0.87 * 69
                else:
                    if salary["from"] is not None:
                        sum_salary = salary["from"] * 0.87 * 69
                    elif salary["to"] is not None:
                        sum_salary = salary["to"] * 0.87 * 69
            else:               # Чистая зарплата без налога
                if salary["from"] is not None and salary["to"] is not None:
                    sum_salary = abs(salary["to"] - salary["from"]) / 2 * 69
                else:
                    if salary["from"] is not None:
                        sum_salary = salary["from"] * 69
                    elif salary["to"] is not None:
                        sum_salary = salary["to"] * 69
        return sum_salary

    def find_vacancies(self, keys, area_name):
        skills = []
        count_salary = 0
        salary_avg = 0
        for page in range(100):
            params = {
                'text': keys,
                'page': page
            }
            items = requests.get(self.URL, params=params).json()["items"]
            for item in items:
                if len(item["area"]) > 0:
                    if item["area"]["name"].upper() == area_name.upper():
                        url_vacancy = item['url']
                        vacancy = requests.get(url_vacancy).json()
                        # Получение списка требуемых навыков
                        if vacancy["key_skills"] is not None:
                            for skill in vacancy["key_skills"]:
                                skills.append(skill["name"])
                                self.count += 1
                        # Расчет средней зарплаты
                        # salary': {'currency': 'RUR', 'from': 120000, 'gross': False, 'to': None},
                        if vacancy["salary"] is not None:
                            salary = self.vacancy_salary(vacancy["salary"])
                            if salary > 0:
                                count_salary +=1
                                salary_avg += salary
            time.sleep(0.1)
        self.keywords = keys
        if count_salary > 0:
            self.salary_avg = round(salary_avg / count_salary, 2)
        else:
            self.salary_avg = round(salary_avg, 2)
        self.area = area_name
        self.init_skills(skills)

    def init_skills(self, skills_list):
        key_skills = {}
        for item in skills_list:
            if item in key_skills:
                key_skills[item] += 1
            else:
                key_skills[item] = 1
        result = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)
        for key, value in result:
            skill = {"name": key, "count": value, 'percent': f'{round(value * 100 / len(skills_list), 2)} %'}
            self.requirements.append(skill)
        return result

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4, separators=(',', ': '))

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4, separators=(',', ': '))


if __name__ == '__main__':

    # hh = HH()
    # hh.find_vacancies('python developer', "Москва")
    # print(hh.to_json())
    # hh.save_json('test.json')

    sity = City()
    items = sity.find_area("Москва")
    ls = items["areas"]
    print(ls)
    # pprint.pprint(items)


