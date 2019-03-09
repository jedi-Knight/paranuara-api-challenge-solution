import pytest, requests

BASE_URL = 'http://0.0.0.0:8080/'

@pytest.mark.parametrize('company_name, expected_response_code, expected_content_type', [
    ('PERMADYNE', 200, 'application/json'),
    ('Non Existant', 200, 'application/json')
])
def test_endpoint_company(company_name, expected_response_code, expected_content_type):
    request = None
    try:
        request = requests.get(BASE_URL + 'company/' + company_name)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    



@pytest.mark.parametrize('person_one, person_two, expected_response_code, expected_content_type', [
    ('Moon Herring','Walter Avery', 200, 'application/json'),
    ('Moon Herring', 'None Existant', 200, 'application/json')
])
def test_endpoint_two_people(person_one, person_two, expected_response_code, expected_content_type):
    request = None
    try:
        request = requests.get(BASE_URL + 'user/' + person_one + '/' + person_two)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    



@pytest.mark.parametrize('person_name, expected_response_code, expected_content_type', [
    ('Moon Herring', 200, 'application/json'),
    ('Non Existant', 200, 'application/json')
])
def test_endpoint_one_person(person_name, expected_response_code, expected_content_type):
    request = None
    try:
        request = requests.get(BASE_URL + 'user/' + person_name)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    



@pytest.mark.parametrize('invalid_endpoint,expected_response_code,expected_content_type', [
    ('Invalid', 404, 'text/html; charset=UTF-8'),
    ('/Invalid', 404, 'text/html; charset=UTF-8'),
    ('/Invalid/Invalid', 404, 'text/html; charset=UTF-8')
])
def test_endpoint_invalid(invalid_endpoint, expected_response_code, expected_content_type):
    request = None
    try:
        request = requests.get(BASE_URL + invalid_endpoint)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
    



@pytest.mark.parametrize('index_page,expected_response_code,expected_content_type', [
    ('', 200, 'text/html; charset=UTF-8'),
])
def test_endpoint_index_page(index_page, expected_response_code, expected_content_type):
    request = None
    try:
        request = requests.get(BASE_URL + index_page)
    except:
        raise AssertionError('App server not running!')

    gotten_response_code = request.status_code
    gotten_content_type = request.headers['Content-Type']

    assert gotten_response_code == expected_response_code
    assert gotten_content_type == expected_content_type
        