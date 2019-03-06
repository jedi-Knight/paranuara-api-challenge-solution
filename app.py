from model import Model
from view import View
from urllib.parse import unquote
from config import DATA_FILES

class App(object):
    
    view = View( Model( DATA_FILES['companies'], DATA_FILES['users'] ) )

    def __init__(self):
        pass

    def index(self):
        return "☼"
    
    def company_users(self, company_name):
        return self.view.company_users( unquote(company_name) )
    
    def two_users(self, user_name_1, user_name_2):
        return self.view.two_users( unquote(user_name_1), unquote(user_name_2) )
    
    def user(self, user_name):
        return self.view.user( unquote(user_name) )

    
         

