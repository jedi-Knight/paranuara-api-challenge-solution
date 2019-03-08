import pytest
from pandas import DataFrame, Series



@pytest.fixture(scope='module')
def model():
    from model import Model
    from config import DATA_FILES
    model = Model( DATA_FILES['companies'], DATA_FILES['users'] )
    model.df = DataFrame({'col1':[1,2,3,4],'col2':['val1','val2','val3','val4']})
    return model


@pytest.fixture(scope='module')
def query_builder(model):
    from query import QueryBuilder
    query_builder = QueryBuilder(model)
    return query_builder


@pytest.mark.parametrize('query_column, value, expected_result',[
    ('col1', 2, Series([False,True,False,False])),
    ('col2', 'val3', Series([False,False,True,False]))
])
def test_single_value_match_query(query_builder, query_column, value, expected_result):
    gotten_result = query_builder.single_value_match_query(query_column, value)
    print('gotten_result:\n', gotten_result)
    print('\nexpected_result:\n', expected_result)
    assert gotten_result.equals(expected_result)

@pytest.mark.parametrize('query_column, values_list, expected_result',[
    ('col1', [2,3], Series([False,True,True,False])),
    ('col2', ['val1','val3','val4'], Series([True,False,True,True]))
])
def test_multi_value_match_query(query_builder, query_column, values_list, expected_result):
    gotten_result = query_builder.multi_value_match_query(query_column, values_list)
    print('gotten_result:\n', gotten_result)
    print('\nexpected_result:\n', expected_result)
    assert gotten_result.equals(expected_result)

@pytest.mark.parametrize('col_val_tuple, expected_result',[
    ((('col1', 1),), Series([True,False,False,False])),
    ((('col1', [2,3]),), Series([False,True,True,False])),
    ((('col2','val1'), ('col1',4)), Series([False,False,False,False])),
    ((('col2','val1'), ('col1',1)), Series([True,False,False,False])),
    ((('col2','val1'), ('col1',1), ('col1',2)), Series([False,False,False,False]))
])
def test_multi_column_match_query(query_builder, col_val_tuple, expected_result):
    gotten_result = query_builder.multi_column_match_query(*col_val_tuple)
    print('gotten_result:\n', gotten_result)
    print('\nexpected_result:\n', expected_result)
    assert gotten_result.equals(expected_result)