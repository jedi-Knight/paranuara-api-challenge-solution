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
from config import DATA_FILES, DATA_MERGE_KEYS

class App(object):
    
    view = None

    def __init__(self):
        self.view = View( Model( DATA_FILES['companies'], DATA_FILES['users'], DATA_MERGE_KEYS['companies'], DATA_MERGE_KEYS['users'] ) )
        pass

    def index(self):
        return '<!DOCTYPE html><p style="text-align: center;"><b>☼☼☼☼☼ welc☼me! ☼☼☼☼☼ </b>&#10; <br/>Please refer to API docs for available endpoints.</p>'
    
    def company_users(self, company_name):
        return self.view.company_users( unquote(company_name) )
    
    def two_users(self, user_name_1, user_name_2):
        return self.view.two_users( unquote(user_name_1), unquote(user_name_2) )
    
    def user(self, user_name):
        return self.view.user( unquote(user_name) )

    
         

