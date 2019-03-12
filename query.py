'''
The query.py module provides the Query class which has helper methods to perform queries 
on the Model and return results. These methods return query results as record sets 
in the form lists of dictionaries. 

The Query class itself relies on the QueryBuilder class (defined in the same module) 
which provides an interface for building queries for use on a Pandas DataFrame 
such as testing multiple values against multiple columns or multiple values within a column.

'''

from pandas import Series
from model import Model

class QueryBuilder(object):
    '''
    This is a helper class to build queries for the Model instance's in-memory table.
    This class is instantiated by the Query object. 
    Its role is to build database specific queries for the given parameters.
    In the current implementation the database is a Pandas dataframe referenced by `model.df`. 
    Please refer to the Model class to learn mode about `model.df`. 

    '''
    
    model = None
    primitives = None

    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        self.model = model
        self.primitives = (int, float, complex, str, bool)

    def single_value_match_query(self, query_column:str, value:'primitive'):
        '''
        Build a query to match a single row with the value at a given column. 
        Returns a Pandas selector (query) for one row.
        '''
        assert isinstance(query_column, str), 'Type mismatch! query_column must be of type str.'
        assert isinstance(value, self.primitives), 'Type mismatch! value must be of primitive type.'

        return self.model.df[query_column] == value
    

    def multi_value_match_query(self, query_column, values_list):
        '''
        Build a query to match rows for a list of values in a given column. 
        Returns a Pandas selector (query) to select the
        rows matching the values in the values_list in the column given by query_column.
        '''
        assert isinstance(query_column, str), 'Type mismatch! query_column must be of type str.'
        assert isinstance(values_list, list), 'Type mismatch! value must be of type list.'

        return self.model.df[ query_column ].isin( values_list )


    def multi_column_match_query(self, *col_val_tuple):
        '''
        Build a query to match one or more values across multiple columns. 
        Returns a Pandas selector (query) to return the set of 
        rows matching the *col_val_tuple in the following format: 
        (column_name_1, value_1), (column_name_2, [value_1, value_2, ...])...
        The second item in each tupe can either be a list of primitive type values, i.e. [value_1, value_2, ...], 
        or single primitive type values, i.e. value_1 of type number, boolean or string.
        '''
        assert len(col_val_tuple)>0, 'at least one argument required'
        assert False not in [isinstance(item, tuple) for item in col_val_tuple], 'each col_val_tuple must be of type tuple.'
        assert False not in [len(item)==2 for item in col_val_tuple], 'each col_val_tuple must contain exactly 2 items.'
        assert False not in [isinstance(item[0], str) for item in col_val_tuple], 'first item of each col_val_tupe must be a string for the column to be queried.'

        return_series = Series( [ True for x in self.model.df.index ] ) #get a Pandas Series object of size equals to the dataframe size and all True values

        for query_column, value in col_val_tuple:
            
            if isinstance(value, self.primitives):
                return_series &= self.single_value_match_query( query_column, value )
            else:
                return_series &= self.multi_value_match_query( query_column, value )
        
        return return_series





class Query(object):

    '''
    This is a helper class to run queries on the Model object's in-memory table (`self.model.df`),
    and to return the results as record sets, i.e. a list of dictionaries
    of this format: 
    ```
    [
        {
            'Column 1': 'Value at 1st row for column 1',
            'Column 2': 'Value at 1st row for column 2'
            ...and so on for `m` number of columns
        },
        {
            'Column 1': 'Value at 2nd row for column 1',
            'Column 2': 'Value at 2nd row for column 2'
            ...
        },
        .. and so on for for `n` number of row.
    ]
    ```
    To build the specific queries, this class calls methods from a QueryBuilder object (`self.query_builder`).
    The role of the QueryBuilder object is to build database specific queries.
    While the role of the Query object is to pass query parameters to the QueryBuilder, 
    run the query obtained from QueryBuilder on the Model object's database reference (`self.model.df`)
    and return the query results in the above format.
    In the current implementation the queries are specific to Pandas 
    since the database is a Pandas dataframe referenced by `model.df`. 
    Please refer to the Model class to learn mode about `model.df`. 

    '''

    model = None # This gets assegned a value in the class constructor.
    query_builder = None # This gets assegned a value in the class constructor.
    def __init__(self, model:Model):
        '''
        Query object constructor.
        Requires a Model object as a parameter (`model`). 
        The Model object must have a Model.df field that refers to a Pandas Dataframe.
        Please refer to the Model class to learn mode about `Model.df`.
        '''
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        
        self.model = model
        self.query_builder = QueryBuilder(model)



    def single_column_value_match(self, query_column:'Name of the column to query', value:'Value of a primitive type.', return_columns: 'List containing names of the columns to filter the recordset return by.'):
        '''
        Targets one column, takes one value and returns a list containing 
        one dictionar object matching the given value for a given column. 
        Only those columns are included in the dictionary record that are named in the query_columns list.
        Returns the selected records, i.e. list of dictionary records.
        '''

        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'
        
        df = self.model.df
        query = self.query_builder.single_value_match_query( query_column, value )

        return df[ query ].filter( return_columns ).to_dict('records')



    def single_column_list_of_values_match(self, query_column, values_list, return_columns):
        '''
        Targets one column, takes a list of values and returns
        a list contaning the dictionary records for the rows matching the list of values for a given column. 
        Only those columns are included in the dictionary record that are named in the query_columns list.
        Returns the selected records, i.e. list of dictionary records.
        '''
        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'
        
        df = self.model.df
        query = self.query_builder.multi_value_match_query(query_column, values_list)

        return df[ query ].filter( return_columns ).to_dict('records')


    def multi_column_match(self, return_columns, *col_val_tuple):
        '''
        Targets multiple columns, takes a either a single primitive or a list of primitive values and returns
        a list contaning the dictionary records for the rows matching the sing/list-of values for the given columns. 
        Only those columns are included in the dictionary record that are named in the query_columns list.
        
        *col_val_tuple is in the following format: (column_name_1, value_1), (column_name_2, [value_1, value_2, ...])...
        The second item in each tupe can either be a list of primitive type values, i.e. [value_1, value_2, ...], 
        or single primitive type values, i.e. value_1 of type number, boolean or string.
        
        Returns the selected records, i.e. list of dictionary records.
        '''

        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'

        df = self.model.df
        query = self.query_builder.multi_column_match_query(*col_val_tuple)

        return df[ query ].filter( return_columns ).to_dict('records')
