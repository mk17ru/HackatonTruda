import json
import csv
import grequests
import datetime
import requests

def parse_vacancy(r_json):
    # r = requests.get('https://api.hh.ru/vacancies/' + str(id))
    # r_json = r.json()

    if not r_json:
        return 0

    res = {
        'city' : r_json['address']['city'] if ('address' in r_json and r_json['address'] and 'city' in r_json['address']) else "unknown", # Город в виде строки
        'company_id' : r_json['employer']['id'] if ('employer' in r_json and r_json['employer'] and 'id' in r_json['employer']) else "", # id компании
        'salary_from' : r_json['salary']['from'] if ('salary' in r_json and r_json['salary'] and 'from' in r_json['salary']) else 0, # Зарплата снизу в рублях
        'employment' : r_json['employment']['id'] if ('employment' in r_json and r_json['employment'] and 'id' in r_json['employment']) else "", # Тип в виде строки
        'schedule' : r_json['schedule']['id'] if ('schedule' in r_json and r_json['schedule'] and 'id' in r_json['schedule']) else "", # Тип в виде строки
        'experience' : r_json['experience']['id'] if ('experience' in r_json and r_json['experience'] and 'id' in r_json['experience']) else "", # Тип в виде строки
        'key_skills' : [it['name'] for it in r_json.get('key_skills')] if ('key_skills' in r_json and r_json['key_skills']) else [], # Список названий скиллов в виде строк
        'specializations' : [it['id'] for it in r_json.get('specializations')] if ('specializations' in r_json and r_json['specializations']) else [], # Список специализаций в виде id
    }

    if res['salary_from'] == 0:
        return 0

    return res;

start_time = datetime.datetime.now()

data = []

start = '2020-07-'

days = []
start_day = 11
finish_day = 11
for i in range(start_day, finish_day + 1):
    days.append(i)


urls = []
for day in days:
    temp = ''
    if day < 10:
        temp = '0' + str(day)
    else:
        temp = str(day)
    cur = start + temp
    for i in range(2):
        r = 0
        if i == 0:
            r = requests.get('https://api.hh.ru/vacancies?per_page=100&date_from=' + cur + 'T00:00:00&date_to=' + cur + 'T11:59:59')
        else:
            r = requests.get('https://api.hh.ru/vacancies?per_page=100&date_from=' + cur + 'T12:00:00&date_to=' + cur + 'T23:59:59')
        r_json = r.json()
        if not 'pages' in r_json:
            continue
        pages = []
        if i == 0:
            for j in range(r_json['pages']):
                pages.append('https://api.hh.ru/vacancies?per_page=100&page=' + str(j) + '&date_from=' + cur + 'T00:00:00&date_to=' + cur + 'T11:59:59')
        else:
            for j in range(r_json['pages']):
                pages.append('https://api.hh.ru/vacancies?per_page=100&page=' + str(j) + '&date_from=' + cur + 'T12:00:00&date_to=' + cur + 'T23:59:59')
        cs = (grequests.get(p) for p in pages)
        c = grequests.map(cs)
        for j in range(len(c)):
            c_json = c[j].json()
            if not 'items' in c_json:
                continue
            for element in c_json['items']:
                urls.append('https://api.hh.ru/vacancies/' + element['id'])

print('LETS GO')

rs1 = (grequests.get(u) for u in urls[:2000])
r1 = grequests.map(rs1)

rs2 = (grequests.get(u) for u in urls[2000:])
r2 = grequests.map(rs2)

r = r1 + r2

for element in r:
    if not element:
        cnt += 1
        continue
    temp = parse_vacancy(element.json())
    if temp == 0:
        continue
    data.append(temp)

csv_file = 'TrainVacancies11.csv'
csv_columns = data[0].keys()

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        writer.writeheader()
        for element in data:
            writer.writerow(element)
except IOError:
    print('I/O error')

print(datetime.datetime.now() - start_time)