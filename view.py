from model import Model
from query import Query
from config import FOOD_TYPES

class View(object):
    query = None
    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        self.query = Query(model)

    def remove_artefacts(self, records, testfield):
        assert isinstance(records, list), 'Type mismatch! records must be of type list.'
        assert isinstance(testfield, str), 'Type mismatch! target_field must be of type str.'

        artefacts_removed = []
        for item in records:
            if not isinstance(item[testfield], float):
                artefacts_removed.append(item)
        
        print(artefacts_removed)
        return artefacts_removed


    
    def format_users_list(self, users_data):
        assert isinstance(users_data, list), 'Type mismatch! users_data must be of type list.'
        
        users_data = self.remove_artefacts(users_data, 'name')
        formatted_data = {
            'number-of-employees': len(users_data),
            'employees': [ item['name'] for item in users_data ]
        }

        if len(users_data) == 0:
            formatted_data['message'] = 'The company has no employees.'
        

        return formatted_data

    def format_two_users_data(self, two_user_data, common_friends):
        assert isinstance(two_user_data, list), 'Type mismatch! two_user_data must be of type list.'
        assert isinstance(common_friends, list), 'Type mismatch! friends_in_common must be of type list.'
        
        if len(two_user_data) == 2:
            formatted_data = {
                'user-1': two_user_data[0],
                'user-2': two_user_data[1],
                'friends-in-common': common_friends
            }
        else:
            formatted_data = {
                'message': 'One or more users not found.'
            }

        return formatted_data


    def format_user_data(self, user_data):
        assert isinstance(user_data, list), 'Type mismatch! users_data must be of type list.'
        
        if len(user_data) > 0:
            user_data = user_data[0]
            user_favourite_food = set(user_data['favouriteFood'])
            formatted_data = {
                'username': user_data['name'],
                'age': user_data['age'],
                'fruits': list( user_favourite_food & FOOD_TYPES['fruits'] ),
                'vegetables': list( user_favourite_food & FOOD_TYPES['vegetables'] )
            }
        else:
            formatted_data = {
                "message": "User not found."
            }

        return formatted_data
        


    def company_users(self, company_name):
        assert isinstance(company_name, str), 'Type mismatch! company_name must be of type str.'
        
        users_data = self.query.single_column_value_match('company', company_name, ['name'])
        return self.format_users_list(users_data)

    def two_users(self, user_name_1, user_name_2):
        assert isinstance(user_name_1, str), 'Type mismatch! user_name_1 must be of type str.'
        assert isinstance(user_name_2, str), 'Type mismatch! user_name_2 must be of type str.'
        
        two_users_data = self.query.single_column_list_of_values_match('name', [user_name_1, user_name_2], ['name', 'age', 'address', 'phone', 'friends'])


        common_friends_ids = set()

        for user in two_users_data:
            
            common_friends_ids = common_friends_ids | set([ user_friend['index'] for user_friend in user['friends'] ])
            del(user['friends'])

        
        common_friends_ids = list(common_friends_ids)

        common_friends = self.query.multi_column_match(['name'], ('index_y', common_friends_ids), ('eyeColor', 'brown'), ('has_died', False))
        
        return self.format_two_users_data(two_users_data, common_friends)


    def user(self, user_name):
        assert isinstance(user_name, str), 'Type mismatch! user_name must be of type str.'
        
        user_data = self.query.single_column_value_match('name',user_name,['name', 'age', 'favouriteFood'])
        return self.format_user_data(user_data)


        

