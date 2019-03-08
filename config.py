'''
Consists of config parameters for the app.

'''

DATA_FILES = {      # Required to import the data.
        'companies': 'data/companies.json',     # File path or URI to companies JSON data
        'users': 'data/people.json'             # File path or URI to people JSON data
    }

DATA_MERGE_KEYS = {                 # Required to match companies and people.
        "companies": "index",       # A unique-value field in the companies records that is referred by the people records
        "users": "company_id"       # Connects people to their companies as described above
    }

FOOD_TYPES = {      # Required to differentiate fruits from vegetables.
        'fruits': {'strawberry', 'orange', 'banana', 'apple'},          # Set of fruits
        'vegetables': {'cucumber', 'celery', 'carrot', 'beetroot'}      # Set of vegetables
    }