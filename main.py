import json
import pprint
import hh


print("===================== Выборка по базе данных HeadHunter =======================")
keywords = input('Введите ключевые слова для поиска в базе HH -> ')
area = input('Введите город для поиска вакансий (по умолчанию - Москва) -> ')
area = "Москва" if len(area) == 0 else area
filename = input('Имя файла для сохранения результатов поиска (по умолчанию - result.json) -> ')
filename = "result.json" if len(filename) == 0 else filename + ".json"
print(f"Поисковая строка: {keywords}; Регион поиска вакансий: {area}; Результаты будут сохранены в файл: {filename}")
hh_obj = hh.HH()
# python developer
# Казань Москва Санкт-Петербург
hh_obj.find_vacancies(keywords, area)
hh_obj.save_json(filename)
print("Результаты поиска:")
print(hh_obj.to_json())
print("===============================================================================")

