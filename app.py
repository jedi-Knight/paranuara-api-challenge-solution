'''
This module is the middle layer between the route definitions of server.py 
and the output JSON builders of view.py. The App object initializes the data model 
as a Model object, loads the data into the Model object from the file path/URI 
defined in config.py, and binds it to the View object. 

The App object's methods get invoked by the routing functions of the server module. 
These methods perform the task of unencoding the URL parameters into plain strings 
and passing them into the View object's corresponding methods.

'''
from urllib.parse import unquote
from model import Model
from view import View
from config import DATA_FILES, DATA_MERGE_KEYS, INDEX_PAGE_CONTENT, ERROR_404_MESSAGE

class App(object):
    
    view = None

    def __init__(self):
        '''
        The App object constructor creates a Model instance 
        giving the filepaths/URIs (defined in DATA_FILES of config.py)
        of the two datasets to load and combine
        into its Model.df DataFrame, 
        and binds it to an instance of the View object. 
        '''
        try:
            self.view = View( 
                            Model( 
                                DATA_FILES['companies'], 
                                DATA_FILES['users'], 
                                DATA_MERGE_KEYS['companies'], 
                                DATA_MERGE_KEYS['users'] 
                                ) 
                            )
        except:
            raise AssertionError('There was a problem creating the Model instance!')
        

    def index(self):
        '''
        Returns INDEX_PAGE_CONTENT defined in config.py.
        '''
        return INDEX_PAGE_CONTENT


    def error_404(self, error):
        '''
        Returns ERROR_404_MESSAGE defined in config.py.
        '''
        return ERROR_404_MESSAGE
    

    def company_users(self, company_name):
        '''
        Returns the dictionary for the list of employees at a given company_name.
        '''
        return self.view.company_users( unquote(company_name) )
    

    def two_users(self, user_name_1, user_name_2):
        '''
        Gives the information about the two users as per the specified requirements of the API challenge problem statement.
        '''
        return self.view.two_users( unquote(user_name_1), unquote(user_name_2) )
    
    def user(self, user_name):
        '''
        Gives the information about user_name as per the specified requirements of the API challenge problem statement.
        '''
        return self.view.user( unquote(user_name) )

    
         

