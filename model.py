from pandas import read_json, merge, DataFrame as df

class Model(object):

    df = None
    def __init__(self, company_json_path, people_json_path):
        assert isinstance(company_json_path, str), 'Type mismatch! company_json_path must be of type str'
        assert isinstance(people_json_path, str), 'Type mismatch! people_json_path must be of type str'
        
        companies_df = read_json(company_json_path)
        people_df = read_json(people_json_path)

        self.df = merge(left=companies_df, right=people_df, left_on='index', right_on='company_id')




