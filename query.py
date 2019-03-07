from model import Model

class QueryBuilder(object):
    model = None
    primitives = None

    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        self.model = model
        self.primitives = (int, float, complex, str, bool)

    def single_value_match_query(self, query_column, value):
        assert isinstance(query_column, str), 'Type mismatch! query_column must be of type str.'
        assert isinstance(value, self.primitives), 'Type mismatch! value must be of primitive type.'

        return self.model.df[query_column] == value
    

    def multi_value_match_query(self, query_column, values_list):
        assert isinstance(query_column, str), 'Type mismatch! query_column must be of type str.'
        assert isinstance(values_list, list), 'Type mismatch! value must be of type list.'

        return self.model.df[ query_column ].isin( values_list )


    def multi_column_match_query(self, *col_val_tuple):
        assert len(col_val_tuple)>0, 'at least one argument required'
        assert False not in [isinstance(item, tuple) for item in col_val_tuple], 'each col_val_tuple must be of type tuple.'
        assert False not in [len(item)==2 for item in col_val_tuple], 'each col_val_tuple must contain exactly 2 items.'
        assert False not in [isinstance(item[0], str) for item in col_val_tuple], 'first item of each col_val_tupe must be a string for the column to be queried.'

        return_series = ( self.model.df['index_x'] >= 0 )    #get a Pandas Series object of size equals to the dataframe size and all True values

        for query_column, value in col_val_tuple:
            
            if isinstance(value, self.primitives):
                return_series &= self.single_value_match_query( query_column, value )
            else:
                return_series &= self.multi_value_match_query( query_column, value )
        
        return return_series





class Query(object):
    model = None
    query_builder = None
    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        
        self.model = model
        self.query_builder = QueryBuilder(model)



    def single_column_value_match(self, query_column, value, return_columns):
        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'
        
        df = self.model.df
        query = self.query_builder.single_value_match_query( query_column, value )

        return df[ query ].filter( return_columns ).to_dict('records')



    def single_column_list_of_values_match(self, query_column, values_list, return_columns):
        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'
        
        df = self.model.df
        query = self.query_builder.multi_value_match_query(query_column, values_list)

        return df[ query ].filter( return_columns ).to_dict('records')


    def multi_column_match(self, return_columns, *col_val_tuple):
        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'

        df = self.model.df
        query = self.query_builder.multi_column_match_query(*col_val_tuple)

        return df[ query ].filter( return_columns ).to_dict('records')
