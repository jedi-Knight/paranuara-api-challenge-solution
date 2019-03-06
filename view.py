from model import Model
from query import Query
from config import FOOD_TYPES

class View(object):
    query = None
    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        self.query = Query(model)

    def format_users_list(self, users_data):
        assert isinstance(users_data, list), 'Type mismatch! users_data must be of type list.'
        
        formatted_data = {
            'number-of-users': len(users_data),
            'usernames': [ item['name'] for item in users_data ]
        }

        return formatted_data

    def format_user_data(self, user_data):
        assert isinstance(user_data, list), 'Type mismatch! users_data must be of type list.'
        user_data = user_data[0]
        user_favourite_food = set(user_data['favouriteFood'])
        formatted_data = {
            'username': user_data['name'],
            'age': user_data['age'],
            'fruits': list( user_favourite_food & FOOD_TYPES['fruits'] ),
            'vegetables': list( user_favourite_food & FOOD_TYPES['vegetables'] )
        }

        return formatted_data
        


    def company_users(self, company_name):
        assert isinstance(company_name, str), 'Type mismatch! company_name must be of type str.'
        users_data = self.query.single_column_value_match('company', company_name, ['name'])
        return self.format_users_list(users_data)

    def user(self, user_name):
        assert isinstance(user_name, str), 'Type mismatch! company_name must be of type str.'
        user_data = self.query.single_column_value_match('name',user_name,['name', 'age', 'favouriteFood'])
        return self.format_user_data(user_data)


        

