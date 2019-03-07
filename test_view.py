import pytest

@pytest.fixture(scope='module')
def view():
    from model import Model
    from config import DATA_FILES
    from view import View
    view = View( Model( DATA_FILES['companies'], DATA_FILES['users'] ) )
    return view

@pytest.mark.parametrize('records, testfield, expected_result',[
    ([],'name',[]),
    ([{'name':'Any Name'}], 'name', [{'name':'Any Name'}]),
     ([{'name':'Any Name'},{'name':float('nan')},{'name':'Another Name'}], 'name', [{'name':'Any Name'}, {'name':'Another Name'}])
])
def test_remove_artefacts(view, records, testfield, expected_result):
    assert view.remove_artefacts(records, testfield) == expected_result

@pytest.mark.parametrize('user_data, expected_result',[
    ([{'name': float('nan')}], {'employees': [],'message': 'The company has no employees.','number-of-employees': 0}),
    ([{'name': "Any Name"}, {'name': float('nan')}], {'number-of-employees': 1, 'employees': ["Any Name"]}),
    ([{'name': float('nan')}, {'name': float('nan')}], {'employees': [],'message': 'The company has no employees.','number-of-employees': 0}),
    ([{'name': "Any Name"}, {'name': "Another Name"}], {'number-of-employees': 2, 'employees': ["Any Name", "Another Name"]}),
    ([{'name': "Any Name"}, {'name': "Another Name"}, {'name': "Another Name"}, {'name': float('nan')}], {'number-of-employees': 3, 'employees': ["Any Name", "Another Name", "Another Name"]}),
])
def test_format_users_list(view, user_data, expected_result):
    assert view.format_users_list(user_data) == expected_result



@pytest.mark.parametrize('two_user_data, common_friends, expected_output',[
    ([{'name': 'Whitfield Deleon', 'age': 43.0, 'address': '381 Debevoise Avenue, Whitmer, Minnesota, 2849', 'phone': '+1 (879) 555-3032'}, {'name': 'Decker Mckenzie', 'age': 60.0, 'address': '492 Stockton Street, Lawrence, Guam, 4854', 'phone': '+1 (893) 587-3311'}],
    [{'name': 'Mindy Beasley'}, {'name': 'Whitfield Deleon'}, {'name': 'Goodwin Cook'}, {'name': 'Decker Mckenzie'}],
    {'user-1': {'name': 'Whitfield Deleon', 'age': 43.0, 'address': '381 Debevoise Avenue, Whitmer, Minnesota, 2849', 'phone': '+1 (879) 555-3032'}, 'user-2': {'name': 'Decker Mckenzie', 'age': 60.0, 'address': '492 Stockton Street, Lawrence, Guam, 4854', 'phone': '+1 (893) 587-3311'}, 'friends-in-common': ['Mindy Beasley', 'Goodwin Cook']}),
    ([],[],{"message": "One or more users not found."})
])
def test_format_two_users_data(view, two_user_data, common_friends, expected_output):
    assert view.format_two_users_data(two_user_data, common_friends) == expected_output





@pytest.mark.parametrize('user_data, expected_result', [
    ([{'name': 'Goodwin Cook', 'age': 32.0, 'favouriteFood': ['orange', 'apple', 'carrot', 'strawberry']}], {"username": "Goodwin Cook", "age": 32.0, "fruits": ["apple", "strawberry", "orange"], "vegetables": ["carrot"]}),
    ([{'name': 'Moon Herring', 'age': 40.0, 'favouriteFood': ['orange', 'beetroot', 'carrot', 'celery']}], {"username": "Moon Herring", "age": 40.0, "fruits": ["orange"], "vegetables": ["celery", "beetroot", "carrot"]}),
    ([],{"message": "User not found."})
])
def test_format_user_data(view, user_data, expected_result):

    gotten_result = view.format_user_data(user_data)

    if 'fruits' in gotten_result.keys():
        gotten_result['fruits'] = set(gotten_result['fruits'])
        expected_result['fruits'] = set(expected_result['fruits'])
        gotten_result['vegetables'] = set(gotten_result['vegetables'])
        expected_result['vegetables'] = set(expected_result['vegetables'])
    
    assert gotten_result == expected_result

@pytest.mark.parametrize('company_name, expected_result', [
    ("PERMADYNE", {"number-of-employees": 7, "employees": ["Frost Foley", "Luna Rodgers", "Boyer Raymond", "Solomon Cooke", "Walter Avery", "Hester Malone", "Arlene Erickson"]}),
    ("ZOINAGE", {"number-of-employees": 9, "employees": ["Kathrine Vaughan", "Merritt Park", "Brittney Arnold", "Rhoda Lawrence", "Neal Gould", "Hogan Goodwin", "Laurel Mcintyre", "Griffin Blankenship", "Fitzpatrick Bradford"]}),
    ("MICROLUXE", {"number-of-employees": 10, "employees": ["Wilda Cooley", "Spence Waters", "Hill Mclaughlin", "Gena Strong", "Conley Castaneda", "Lavonne Terry", "May Cardenas", "Silva Navarro", "Marquez Phillips", "Aileen Reynolds"]}),
    ("NETBOOK",{"number-of-employees": 0, "employees": [], "message": "The company has no employees."})
])
def test_company_users(view, company_name, expected_result):
    assert view.company_users(company_name) == expected_result
    

@pytest.mark.parametrize('user_name_1, user_name_2, expected_result', [
    ("Luna Rodgers", "Walter Avery", {"user-1": {"name": "Luna Rodgers", "age": 56, "address": "430 Frank Court, Camino, American Samoa, 2134", "phone": "+1 (889) 544-3275"}, "user-2": {"name": "Walter Avery", "age": 35, "address": "797 Vandervoort Place, Wheaton, Kentucky, 1051", "phone": "+1 (992) 532-3748"}, "friends-in-common": ["Mindy Beasley", "Whitfield Deleon", "Goodwin Cook", "Decker Mckenzie"]}),
    ("Luna Rodgers", "WalterAvery", {"message": "One or more users not found."}),
    ("Lqws", "WalterAvery", {"message": "One or more users not found."}),
    ("Lqws", "Walter Avery", {"message": "One or more users not found."}),
    ("Luna Rodgers", "Luna Rodgers", {"message": "One or more users not found."})
])
def test_two_users(view, user_name_1, user_name_2, expected_result):
    assert view.two_users(user_name_1, user_name_2) == expected_result

@pytest.mark.parametrize('user_name, expected_result', [
    ("Luna Rodgers", {"username": "Luna Rodgers", "age": 56, "fruits": ["banana"], "vegetables": ["beetroot", "celery", "cucumber"]}),
    ("Moon Herring", {"username": "Moon Herring", "age": 40.0, "fruits": ["orange"], "vegetables": ["beetroot", "carrot", "celery"]}),
    ("Goodwin Cook", {"username": "Goodwin Cook", "age": 32, "fruits": ["apple", "strawberry", "orange"], "vegetables": ["carrot"]}),
    ("qeqweqwewqe",{"message": "User not found."})
])
def test_user(view, user_name, expected_result):
    
    gotten_result = view.user(user_name)

    if 'fruits' in gotten_result.keys():
        gotten_result['fruits'] = set(gotten_result['fruits'])
        expected_result['fruits'] = set(expected_result['fruits'])
        gotten_result['vegetables'] = set(gotten_result['vegetables'])
        expected_result['vegetables'] = set(expected_result['vegetables'])
    
    assert gotten_result == expected_result