import codecs

import requests
import csv


def parse_vacancy(id):
    try:
        r = requests.get('https://api.hh.ru/vacancies/' + str(id))
        if r.status_code != 200:
            print("id = " + str(id) + ' status_code = ' + str(r.status_code))
            return -1
        r_json = r.json()
        if not (r_json['salary']) or (r_json['salary']['from'] == None):
            return -1
        spec = ""
        f = 1
        for it in r_json['specializations']:
            if f != 1:
                spec += " "
            spec += str(float(it['id']))

            f = 0
        f = 1
        key_skills = ""
        for it in r_json['key_skills']:
            if f != 1:
                key_skills += " | "
            key_skills += it['name'].encode('utf-8')
            f = 0

        res = [{
            'city': r_json['address']['city'] if r_json['address'] else "unknown",
            'company_id': int(r_json['employer']['id']) if r_json['employer'] else 0,
            'salary_from': r_json['salary']['from'] if r_json['salary'] else 0,
            'employment': r_json['employment']['id'] if r_json['employment'] else 0,
            'schedule': r_json['schedule']['id'] if r_json['schedule'] else 0,
            'experience': r_json['experience']['id'] if r_json['experience'] else 0,
            'key_skills': key_skills,
            'specializations': spec
        }]
        return res
    except Exception:
        return -1


def to_csv(start, end):
    with codecs.open('base-f-v2.csv', 'w', "utf-8-sig") as csvfile:
        fieldnames = ['city', 'company_id', 'salary_from', 'employment', 'schedule', 'experience', 'key_skills',
                      'specializations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(start, end, 1):
            ans = parse_vacancy(i)
            if ans != -1:
                writer.writerows(ans)
            else:
                print("id = " + str(i) + " failed!")
                # most probably page doesn't exists


start = 36800001
end = 36850000

to_csv(start, end)
