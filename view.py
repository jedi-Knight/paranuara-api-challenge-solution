from model import Model
from query import Query

class View(object):
    query = None
    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        self.query = Query(model)

    def format_people_list(self, people_data):
        assert isinstance(people_data, dict), 'Type mismatch! people_data must be of type dict.'
        formatted_data = {
            'number-of-people': len(people_data['name']),
            'people': people_data['name']
        }

        return formatted_data


    def company_people(self, company_name):
        assert isinstance(company_name, str), 'Type mismatch! company_name must be of type str.'
        people_data = self.query.get_people_in_company(company_name)
        return self.format_people_list(people_data)


        

