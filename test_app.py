'''
`app` module unit tests.
'''
import pytest
from config import INDEX_PAGE_CONTENT, ERROR_404_MESSAGE, INDEX_PAGE_CONTENT

@pytest.fixture(scope='module')
def app():
    from app import App
    try:
        app = App()
        return app
    except:
        raise AssertionError('There was a problem creating the App instance!')


@pytest.mark.parametrize('expected_result', [
    (INDEX_PAGE_CONTENT),
])
def test_index(app, expected_result):
    gotten_result = app.index()
    assert gotten_result==expected_result



@pytest.mark.parametrize('expected_result', [
    (ERROR_404_MESSAGE),
])
def test_error_404(app, expected_result):
    gotten_result = app.error_404(None)
    assert gotten_result==expected_result



@pytest.mark.parametrize('company_name, expected_result', [
    ("PERMADYNE", {"number-of-employees": 7, "employees": ["Frost Foley", "Luna Rodgers", "Boyer Raymond", "Solomon Cooke", "Walter Avery", "Hester Malone", "Arlene Erickson"]}),
    ("ZOINAGE", {"number-of-employees": 9, "employees": ["Kathrine Vaughan", "Merritt Park", "Brittney Arnold", "Rhoda Lawrence", "Neal Gould", "Hogan Goodwin", "Laurel Mcintyre", "Griffin Blankenship", "Fitzpatrick Bradford"]}),
    ("MICROLUXE", {"number-of-employees": 10, "employees": ["Wilda Cooley", "Spence Waters", "Hill Mclaughlin", "Gena Strong", "Conley Castaneda", "Lavonne Terry", "May Cardenas", "Silva Navarro", "Marquez Phillips", "Aileen Reynolds"]}),
    ("NETBOOK",{"number-of-employees": 0, "employees": [], "message": "The company has no employees."})
])
def test_company_users(app, company_name, expected_result):
    assert app.company_users(company_name) == expected_result
    



@pytest.mark.parametrize('user_name_1, user_name_2, expected_result', [
    ("Luna%20Rodgers", "Walter%20Avery", {"user-1": {"name": "Luna Rodgers", "age": 56.0, "address": "430 Frank Court, Camino, American Samoa, 2134", "phone": "+1 (889) 544-3275"}, "user-2": {"name": "Walter Avery", "age": 35.0, "address": "797 Vandervoort Place, Wheaton, Kentucky, 1051", "phone": "+1 (992) 532-3748"}, "friends-in-common": ["Mindy Beasley", "Whitfield Deleon", "Goodwin Cook", "Decker Mckenzie", "Moon Herring"]}),
    ("Luna%20Rodgers", "WalterAvery", {"message": "One or more users not found."}),
    ("Lqws", "WalterAvery", {"message": "One or more users not found."}),
    ("Lqws", "Walter%20Avery", {"message": "One or more users not found."}),
    ("Luna%20Rodgers", "Luna%20Rodgers", {"message": "One or more users not found."})
])
def test_two_users(app, user_name_1, user_name_2, expected_result):
    assert app.two_users(user_name_1, user_name_2) == expected_result




@pytest.mark.parametrize('user_name, expected_result', [
    ("Luna%20Rodgers", {"username": "Luna Rodgers", "age": 56, "fruits": ["banana"], "vegetables": ["beetroot", "celery", "cucumber"]}),
    ("Moon%20Herring", {"username": "Moon Herring", "age": 40.0, "fruits": ["orange"], "vegetables": ["beetroot", "carrot", "celery"]}),
    ("Goodwin%20Cook", {"username": "Goodwin Cook", "age": 32, "fruits": ["apple", "strawberry", "orange"], "vegetables": ["carrot"]}),
    ("qeqweqwewqe",{"message": "User not found."})
])
def test_user(app, user_name, expected_result):
    
    gotten_result = app.user(user_name)

    if 'fruits' in gotten_result.keys():
        gotten_result['fruits'] = set(gotten_result['fruits'])
        expected_result['fruits'] = set(expected_result['fruits'])
    if 'vegetables' in gotten_result.keys():
        gotten_result['vegetables'] = set(gotten_result['vegetables'])
        expected_result['vegetables'] = set(expected_result['vegetables'])
    
    assert gotten_result == expected_result



