from model import Model
from view import View
from config import DATA_FILES

class App(object):
    
    view = View( Model( DATA_FILES['companies'], DATA_FILES['users'] ) )

    def __init__(self):
        pass

    def index(self):
        return "☼"
    
    def company_users(self, company_name):
        return self.view.company_users(company_name)
    
    def user(self, user_name):
        return self.view.user(user_name)
         

