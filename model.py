from pandas import read_json, merge, DataFrame as df

class Model(object):

    df = None
    def __init__(self, left_table_json, right_table_json, left_key, right_key):
        assert isinstance(left_table_json, str), 'Type mismatch! left_table_json must be of type str'
        assert isinstance(right_table_json, str), 'Type mismatch! right_table_json must be of type str'
        
        companies_df = read_json(left_table_json)
        users_df = read_json(right_table_json)

        self.df = merge(left=companies_df, right=users_df, left_on=left_key, right_on=right_key, how='outer')




