'''
Functional test of API endpoints for the API challenge problem statement specs.
'''

import pytest, requests
from json import loads
from config import INDEX_PAGE_CONTENT, ERROR_404_MESSAGE

BASE_URL = 'http://127.0.0.1:8080/'

@pytest.mark.parametrize('index_page, expected_response_code, expected_content_type, expected_content', [
    ('', 200, 'text/html; charset=UTF-8', INDEX_PAGE_CONTENT),
])
def test_endpoint_index_page(index_page, expected_response_code, expected_content_type, expected_content):
    request = None
    try:
        request = requests.get(BASE_URL + index_page)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']
    gotten_content = request.text

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    assert gotten_content == expected_content


@pytest.mark.parametrize('invalid_endpoint, expected_response_code, expected_content_type, expected_content', [
    ('Invalid', 404, 'text/html; charset=UTF-8', ERROR_404_MESSAGE),
    ('/Invalid', 404, 'text/html; charset=UTF-8', ERROR_404_MESSAGE),
    ('/Invalid/Invalid', 404, 'text/html; charset=UTF-8', ERROR_404_MESSAGE)
])
def test_endpoint_invalid(invalid_endpoint, expected_response_code, expected_content_type, expected_content):
    request = None
    try:
        request = requests.get(BASE_URL + invalid_endpoint)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']
    gotten_content = request.text

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    assert gotten_content == expected_content


@pytest.mark.parametrize('company_name, expected_response_code, expected_content_type, expected_content', [
    ('PERMADYNE', 200, 'application/json', '{"number-of-employees": 7, "employees": ["Frost Foley", "Luna Rodgers", "Boyer Raymond", "Solomon Cooke", "Walter Avery", "Hester Malone", "Arlene Erickson"]}'),
    ('Non Existant', 200, 'application/json', '{"number-of-employees": 0, "employees": [], "message": "The company has no employees."}')
])
def test_endpoint_company(company_name, expected_response_code, expected_content_type, expected_content):
    request = None
    try:
        request = requests.get(BASE_URL + 'company/' + company_name)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']
    gotten_content = request.text

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    assert gotten_content == expected_content
    

@pytest.mark.parametrize('person_one, person_two, expected_response_code, expected_content_type, expected_content', [
    ('Moon Herring','Walter Avery', 200, 'application/json','{"user-1": {"name": "Walter Avery", "age": 35.0, "address": "797 Vandervoort Place, Wheaton, Kentucky, 1051", "phone": "+1 (992) 532-3748"}, "user-2": {"name": "Moon Herring", "age": 40.0, "address": "718 Locust Street, Ernstville, Kentucky, 741", "phone": "+1 (947) 466-2999"}, "friends-in-common": ["Mindy Beasley", "Whitfield Deleon", "Goodwin Cook", "Decker Mckenzie"]}'),
    ('Moon Herring', 'None Existant', 200, 'application/json', '{"message": "One or more users not found."}')
])
def test_endpoint_two_people(person_one, person_two, expected_response_code, expected_content_type, expected_content):
    request = None
    try:
        request = requests.get(BASE_URL + 'user/' + person_one + '/' + person_two)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']
    gotten_content = request.text

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    assert gotten_content == expected_content
    

@pytest.mark.parametrize('person_name, expected_response_code, expected_content_type, expected_content', [
    ('Moon Herring', 200, 'application/json', {"username": "Moon Herring", "age": 40, "fruits": ["orange"], "vegetables": ["carrot", "beetroot", "celery"]}),
    ('Non Existant', 200, 'application/json', {"message": "User not found."})
])
def test_endpoint_one_person(person_name, expected_response_code, expected_content_type, expected_content):
    request = None
    try:
        request = requests.get(BASE_URL + 'user/' + person_name)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']
    gotten_content = request.text
    
    try:
        gotten_content = loads(gotten_content)
    except:
        raise AssertionError('This endpoint must return a valid JSON string!')


    if 'fruits' in gotten_content.keys():
        gotten_content['fruits'] = set(gotten_content['fruits'])
        expected_content['fruits'] = set(expected_content['fruits'])
        
    if 'vegetables' in gotten_content.keys():
        gotten_content['vegetables'] = set(gotten_content['vegetables'])
        expected_content['vegetables'] = set(expected_content['vegetables'])

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    assert gotten_content == expected_content
