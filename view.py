'''
The view.py module sends invokes query methods of the data model and passes 
the parameters received from the app module. The View object consists of methods 
that transform and map the data received from the data model queries into 
dictionaries of the required output schema and returns them to the App.

'''

from model import Model
from query import Query
from config import FOOD_TYPES

class View(object):
    query = None
    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        self.query = Query(model)

    def remove_artefacts(self, records:'list-of-dictionaries', testfield:str):
        '''
        Takes `records` which is a records format dictionary, i.e. [{col1: val1_1, col2: val_2_1, ...}, {...}, {...}]
        and a `testfield` (for exacmple, "col1") string which is the "column" to check for `nan`
        Removes the dict record (i.e. the "row") if it has `nan`.
        Returns records with the `nan` rows removed.
        '''

        assert isinstance(records, list), 'Type mismatch! records must be of type list.'
        assert isinstance(testfield, str), 'Type mismatch! target_field must be of type str.'

        artefacts_removed = []
        for item in records:
            if not isinstance(item[testfield], float):
                artefacts_removed.append(item)
        
        print(artefacts_removed)
        return artefacts_removed #original list-of-dictionaries but with items filtered out if having `nan` on the target field


    
    def format_users_list(self, users_data:list):
        '''
        Takes the user_data records (i.e. list-of-dictionaries),
        calculates the total number of records and responds ond returns a 
        dictionary in the specified format:
        ```
            {
                'number-of-employees': length of list-of-dictionaries after removing `nan` values,
                'employees': [names of employees obtained from `records`],
            }
        ```

        Or, if there are no non-`nan`items in the records, returns:
        ```
            {
                'number-of-employees': 0,
                'employees': [],
                'message': 'The company has no employees.'
            }
        ```
        '''

        assert isinstance(users_data, list), 'Type mismatch! users_data must be of type list.'
        
        users_data = self.remove_artefacts(users_data, 'name')
        formatted_data = {
            'number-of-employees': len(users_data),
            'employees': [ item['name'] for item in users_data ]
        }

        if len(users_data) == 0:
            formatted_data['message'] = 'The company has no employees.'
        

        return formatted_data #data as a dictinary in specified format for JSON serialization

    def format_two_users_data(self, two_user_data:'list-of-dictionaries', common_friends:'list-of-dictionaries'):
        assert isinstance(two_user_data, list), 'Type mismatch! two_user_data must be of type list.'
        assert isinstance(common_friends, list), 'Type mismatch! friends_in_common must be of type list.'
        
        if len(two_user_data) == 2:
            common_friends_semantic_filtered = []

            for friend in common_friends:
                if friend['name'] != two_user_data[0]['name'] and friend['name'] != two_user_data[1]['name']:
                    common_friends_semantic_filtered.append(friend['name'])

            formatted_data = {
                'user-1': two_user_data[0],
                'user-2': two_user_data[1],
                'friends-in-common': common_friends_semantic_filtered
            }
        else:
            formatted_data = {
                'message': 'One or more users not found.'
            }

        return formatted_data #data as a dictinary in specified format for JSON serialization


    def format_user_data(self, user_data:'list-of-dictionaries, but with a single item'):
        assert isinstance(user_data, list), 'Type mismatch! users_data must be of type list.'
        
        if len(user_data) > 0:
            user_data = user_data[0]
            user_favourite_food = set(user_data['favouriteFood'])
            formatted_data = {
                'username': user_data['name'],
                'age': int(user_data['age']),
                'fruits': list( user_favourite_food & FOOD_TYPES['fruits'] ),
                'vegetables': list( user_favourite_food & FOOD_TYPES['vegetables'] )
            }
        else:
            formatted_data = {
                "message": "User not found."
            }

        return formatted_data #data as a dictinary in specified format for JSON serialization
        


    def company_users(self, company_name):
        '''
        Returns the dictionary for the list of employees at a given company_name.
        '''
        assert isinstance(company_name, str), 'Type mismatch! company_name must be of type str.'
        
        users_data = self.query.single_column_value_match('company', company_name, ['name'])
        return self.format_users_list(users_data) #data as a dictinary in specified format for JSON serialization

    def two_users(self, user_name_1, user_name_2):
        '''
        Gives the information about the two users as per the specified requirements of the API challenge problem statement.
        '''
        assert isinstance(user_name_1, str), 'Type mismatch! user_name_1 must be of type str.'
        assert isinstance(user_name_2, str), 'Type mismatch! user_name_2 must be of type str.'
        
        two_users_data = self.query.single_column_list_of_values_match('name', [user_name_1, user_name_2], ['name', 'age', 'address', 'phone', 'friends'])


        common_friends_ids = set()

        for user in two_users_data:
            
            common_friends_ids = common_friends_ids | set([ user_friend['index'] for user_friend in user['friends'] ])
            del(user['friends'])

        
        common_friends_ids = list(common_friends_ids)

        common_friends = self.query.multi_column_match(['name'], ('index_y', common_friends_ids), ('eyeColor', 'brown'), ('has_died', False))
        
        return self.format_two_users_data(two_users_data, common_friends) #data as a dictinary in specified format for JSON serialization


    def user(self, user_name):
        '''
        Gives the information about user_name as per the specified requirements of the API challenge problem statement.
        '''
        assert isinstance(user_name, str), 'Type mismatch! user_name must be of type str.'
        
        user_data = self.query.single_column_value_match('name',user_name,['name', 'age', 'favouriteFood'])
        return self.format_user_data(user_data) #data as a dictinary in specified format for JSON serialization


        

