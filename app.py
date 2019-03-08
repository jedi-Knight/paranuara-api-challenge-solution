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

    
         

