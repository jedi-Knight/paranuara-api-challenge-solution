from model import Model

class Query(object):
    model = None
    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model.'
        
        self.model = model



    def single_column_value_match(self, query_column, value, return_columns):
        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'
        
        df = self.model.df

        return df[ df[query_column]==value ].filter( return_columns ).to_dict('records')



    def single_column_list_of_values_match(self, query_column, values_list, return_columns):
        assert isinstance(values_list, list), 'Type mismatch! value must be of type list.'
        assert isinstance(return_columns, list), 'Type mismatch! select_columns must be of type list.'
        
        df = self.model.df

        return df[ df['companies'].isin( values_list ) ].filter( return_columns ).to_dict('records')