'''
This module provides the Model class which loads the JSON files 
into a Pandas DataFrame object and merges them using file path/URI 
and merge keys defined in config.py that get passed during Model instantiation by App). 

The DataFrame object acts like an in-memory single-table database combining both company 
and people data. It relies on a separate helper class Query defined in query.py to provide 
an interface for running queries on the combined table.
'''

from pandas import read_json, merge

class Model(object):

    df = None
    def __init__(self, left_table_json, right_table_json, left_key, right_key):
        assert isinstance(left_table_json, str), 'Type mismatch! left_table_json must be of type str'
        assert isinstance(right_table_json, str), 'Type mismatch! right_table_json must be of type str'
        
        try:
            companies_df = read_json(left_table_json)
            users_df = read_json(right_table_json)
        except FileNotFoundError:
            raise AssertionError('People and companies data not found at the given URI!')
        except:
            raise AssertionError('There was a problem reading the data!')

        self.df = merge(left=companies_df, right=users_df, left_on=left_key, right_on=right_key, how='outer')




