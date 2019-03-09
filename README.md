# Paranuara Challenge Solution

## Dependencies
1. Docker version 18.09.3
2. Connectivity to Docker Hub and PypI


## Build and Run

### To Build

Clone or download this repository, change directory to the repository path, then run this command:

```
$ docker build -t paranuara-challenge-solution -f DOCKER .

```

#### To use different companies.json and people.json files:
Before running the build command, either replace the files in data/ directory of this repo with the new files, or edit the `DATA_FILE` entry in `config.py` to point to their location. Absolute path, relative path and URIs can also be used with the `DATA_FILE` option.

## To Run
After completing the build steps above, run this command:

```
$ docker run -p 127.0.0.1:8383:8080 -dit paranuara-challenge-solution

```

## To test the API endpoints (solutions):


#### Please note:
1. The company/people names and return values used for the following examples are based on the JSON data included in the challenge GitHub repo. Please change the company and user names to test with different data.
2. The API should be running for the below endpoints to be accessible. To run the API, please follow the steps described above.

### API Endpoints
##### 1. API endpoint to get all employees for a given company:
##### `http://localhost:8383/company/<company name>`

To test this endpoint, click the following links with the API running:

_Example 1.1:_

[http://localhost:8383/company/PERMADYNE](http://localhost:8383/company/NETBOOK)

Here the company name is PERMADYNE. Following is its JSON return:
```
{
    "number-of-employees": 7,
    "employees": 
        [
        "Frost Foley", 
        "Luna Rodgers", 
        "Boyer Raymond", 
        "Solomon Cooke", 
        "Walter Avery", 
        "Hester Malone", 
        "Arlene Erickson"
        ]
}
```
The `number-of-employees` field gives the number of employees of the company, the `employees` field gives the names of the employees as an array.

_Example 1.2:_

[http://localhost:8383/company/NETBOOK](http://localhost:8383/company/NETBOOK)

Here the company name is NETBOOK. Following is its JSON return:
```
{
    "number-of-employees": 0, 
    "employees": [],
    "message": "The company has no employees."
}
```
If a company has no employees, the `number-of-employees` and `employees` field reflect this fact and a `message` field is included in the JSON which includes a string message.



#### 2. API endpoint to get the Name, Age, Address and phone information about two people, and a list of their friends in common who have brown eyes and are still alive:
#### `http://localhost:8383/user/<one user name>/<another user name>`
_Example 2.1:_
http://localhost:8383/user/Sharron%20Barker/Moon%20Herring

The following is the JSON return containing information about the two - people Sharron Barker and Moon Herring, and their friends in common who have brown eyes and are alive:

```
{
    "user-1": {
        "name": "Sharron Barker",
        "age": 28.0,
        "address": "598 Polhemus Place, Ogema, Marshall Islands, 3906",
        "phone": "+1 (856) 530-3907"
    },
    "user-2": {
        "name": "Moon Herring",
        "age": 40.0,
        "address": "718 Locust Street, Ernstville, Kentucky, 741",
        "phone": "+1 (947) 466-2999"
    },
    "friends-in-common": [
        "Mindy Beasley",
        "Whitfield Deleon",
        "Goodwin Cook",
        "Decker Mckenzie"
    ]
}

```

#### 3. API endpoint to get the name and age of one person and the fruits and vegetables they like:
#### `http://localhost:8383/user/<user name>`
    
_Example 3.1:_

http://localhost:8383/user/Leblanc%20Talley

Here the company name is NETBOOK. Following is its JSON return:

```
{
    "username": "Leblanc Talley",
    "age": 55,
    "fruits": [
        "orange",
        "apple"
    ],
    "vegetables": [
        "carrot",
        "celery"
    ]
}

```

The JSON return respects the specified interface, i.e.:
` {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## To Run Unit Tests
After completing the build steps above, run this command:
```
$ docker run -p 127.0.0.1:8383:8080 -it --entrypoint /paranuara/api/test.sh paranuara-challenge-solution

```

## Code Overview
All of the application modules are in the repo root. 
1. `server.py` is the entry point which gets invoked on run and starts a web server. It consists of route definitions for HTTP requests. The `bottle.py` package (from PyPI) provides the WSGI interface.

2. The `app.py` module is the middle layer between the route definitions of `server.py` and the output JSON builders of `view.py`. The App object initializes the data model as a Model object, loads the data into the Model object from the file path/URI defined in `config.py`, and binds it to the View object. The App object's methods get invoked by the routing functions of the `server` module. These methods perform the task of unencoding the URL parameters into plain strings and passing them into the View object's corresponding methods.

3. The `view.py` module sends invokes query methods of the data model and passes the parameters received from the `app` module. The View object consists of methods that transform and map the data received from the data model queries into Python dictionary objects of the required output schema and returns them to the App for JSON serialization.

4. `model.py` provides the Model class which loads the JSON files into a Pandas DataFrame object and merges them (using file path/URI and merge keys defined in `config.py` that get passed during Model instantiation by App). The DataFrame object acts like an in-memory single-table database combining both company and people data. It relies on a separate helper class Query defined in `query.py` to provide an interface for running queries on the combined table.

5. The `query.py` module provides the Query class which has helper methods to perform queries on the Model and return results. These methods return query results as record sets in the form lists of dictionaries.
The Query class itself relies on the QueryBuilder class (defined in the same module) which provides an interface for building queries for use on a Pandas DataFrame such as testing multiple values against multiple columns or multiple values within a column.

6. The `test_app.py`, `test_view.py`, `test_model.py` and `test_query.py` modules provide methods for running unit tests on the app, view, model and query modules respectively.

7. Others:
    - `DOCKER`: Dockerfile to build the API container.
    - `setup.sh`: This executed within the API container during build. It creates a virtual environment and installs Python dependencies using pip.
    - `start.sh`: This gets executed within the API container during run. It runs `server.py` within the container.
    - `tesh.sh`: Executable shell script to install pytest and run unit tests when the container is run in test mode using the command described in the "To Run Unit Test" section above.
    - `requirements.txt`: List of dependencies installed by pip running inside the Docker container during build.
    
