from model import Model
from view import View
from config import DATA_FILES

class App(object):
    
    view = View( Model( DATA_FILES['companies'], DATA_FILES['people'] ) )

    def __init__(self):
        pass

    def index(self):
        return "☼"
    
    def company_people(self, company_name):
        return self.view.company_people(company_name)
         

