import json

class Model(object):
    companies = {}
    people = {}
    def __init__(self):
        with open('../data/companies.json', 'r') as companies_json:
            self.companies = json.loads(companies_json.read())
            companies_json.close()

        with open('../data/people.json', 'r') as people_json:
            self.people = json.loads(companies_json.read())
            people_json.close()
    



