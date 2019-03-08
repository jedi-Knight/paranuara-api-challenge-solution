import pytest
from pandas import DataFrame, Series



@pytest.fixture(scope='module')
def model():
    from model import Model
    from config import DATA_FILES, DATA_MERGE_KEYS
    model = Model( DATA_FILES['companies'], DATA_FILES['users'], DATA_MERGE_KEYS['companies'], DATA_MERGE_KEYS['users'] )
    
    model.df = DataFrame({'col1':[1,2,3,4],'col2':['val1','val2','val3','val4']}) #use simpler dataframe for simpler test inputs
    
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










@pytest.fixture(scope='module')
def query(model):
    from query import Query
    query = Query(model)
    return query


@pytest.mark.parametrize('query_column, value, return_columns, expected_result',[
    ('col1', 2, ['col2'], [{'col2': 'val2'}]),
    ('col2', 'val3', ['col2'], [{'col2': 'val3'}])
])
def test_single_column_value_match(query, query_column, value, return_columns, expected_result):
    gotten_result = query.single_column_value_match(query_column, value, return_columns)
    print('gotten_result:\n', gotten_result)
    print('\nexpected_result:\n', expected_result)
    assert gotten_result == expected_result

@pytest.mark.parametrize('query_column, values_list, return_columns, expected_result',[
    ('col1', [2,3], ['col1','col2'], [{'col1':2,'col2':'val2'},{'col1':3,'col2':'val3'}] ),
    ('col2', ['val1','val3','val4'], ['col1'], [{'col1':1},{'col1':3},{'col1':4}] ),
    ('col2', ['val1','val3','val3'], ['col1'], [{'col1':1},{'col1':3}] )
])
def test_single_column_list_of_values_match(query, query_column, values_list, return_columns, expected_result):
    gotten_result = query.single_column_list_of_values_match(query_column, values_list, return_columns)
    print('gotten_result:\n', gotten_result)
    print('\nexpected_result:\n', expected_result)
    assert gotten_result == expected_result

@pytest.mark.parametrize('return_columns, col_val_tuple, expected_result',[
    (['col1','col2'], (('col1', 1),), [{'col1':1,'col2':'val1'}]),
    (['col2'], (('col1', [2,3]),), [{'col2':'val2'},{'col2':'val3'}]),
    (['col1','col2'], (('col2','val1'), ('col1',4)), []),
    (['col1','col2'], (('col2','val1'), ('col1',1)), [{'col1':1, 'col2':'val1'}]),
    (['col1','col2'], (('col2','val1'), ('col1',1), ('col1',2)), [])
])
def test_multi_column_match(query, return_columns, col_val_tuple, expected_result):
    gotten_result = query.multi_column_match(return_columns, *col_val_tuple)
    print('gotten_result:\n', gotten_result)
    print('\nexpected_result:\n', expected_result)
    assert gotten_result == expected_result