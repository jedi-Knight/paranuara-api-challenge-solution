# Paranuara Challenge Solution

#### Table of Contents
* [Dependencies](#dependencies)
* [To Build and Run on Jenkins](#to-build-and-run-on-jenkins)
* [To Build and Run On Localhost](#to-build-and-run-on-localhost)
    * [To Build](#to-build)
        * [To use different companies.json and people.json files during build](#to-use-different-companiesjson-and-peoplejson-files)
    * [To Run](#to-run)
* [To test the API endpoints (ie. the challenge solutions)](#to-test-the-api-endpoints-solutions)
    * [API Endpoints](#api-endpoints)
        * [1. API endpoint to get all employees for a given company](#1-api-endpoint-to-get-all-employees-for-a-given-company)
        * [2. API endpoint to get the Name, Age, Address and phone information about two people, and a list of their friends in common who have brown eyes and are still alive](#2-api-endpoint-to-get-the-name-age-address-and-phone-information-about-two-people-and-a-list-of-their-friends-in-common-who-have-brown-eyes-and-are-still-alive)
        * [3. API endpoint to get the name and age of one person and the fruits and vegetables they like](#3-api-endpoint-to-get-the-name-and-age-of-one-person-and-the-fruits-and-vegetables-they-like)
* [To Run Tests](#to-run-tests)
* [Code Overview](#code-overview)

## Dependencies
1. Docker version 18.09.3.
2. Jenkins 2.150.3.
3. Docker plugin installed on Jenkins.
4. Jenkins pipeline access to the `docker` command.
5. Connectivity to Docker Hub and PypI.

## To Build and Run on Jenkins

The Jenkins pipeline definition is in the `Jenkinsfile` of this repo. 

To use it with Jenkins, create a new SCM or GitHub based pipeline on Jenkins and enter this repository url as the source. Then Use `Jenkinsfile` as the script path (this is the default setting if using Jenkin's Blue Ocean UI). 

Start the pipeline build. Jenkin runs the pipeline Build, Run and Test tasks. 

On Sucessful execution of the Run task, the API is accessible at port `8383` of the Jenkins-Docker host machine. 
`http://<Jenkins server address>:8383/`

The API endpoints are described in the _To test the API endpoints (solutions)_ section below. Please replace _localhost_ with the Jenkins-Docker host address to test the examples on the CI server.

## To Build and Run On Localhost

### To Build

Clone or download this repository, change directory to the repository path, then run this command:

```
$ docker build -t paranuara-challenge-solution -f DOCKER .

```

#### To use different companies.json and people.json files
Before running the build command, either replace the files in data/ directory of this repo with the new files, or edit the `DATA_FILE` entry in `config.py` to point to their location. Absolute path, relative path and URIs can also be used with the `DATA_FILE` option.

##### IMPORTANT:
When using a different dataset, the tests in `test_app`, `test_view` and `test_http` modules that test the return values using parameters sampled from the included companies.json and people.json data may fail if the new data does not include the records used for the tests. In such event, please comment out or delete the test parameters that rely on the included data. Alternatively, the test parameters can be modified using records sampled from the new dataset.

## To Run
After completing the build steps above, run this command:

```
$ docker run -p 127.0.0.1:8383:8080 -dit --rm paranuara-challenge-solution

```

## To test the API endpoints (solutions)


#### Please note:
1. The company/people names and return values used for the following examples are based on the JSON data included in the challenge GitHub repo. Please change the company and user names to test with different data.
2. The API should be running for the below endpoints to be accessible. To run the API, please follow the steps described above.

### API Endpoints
##### 1. API endpoint to get all employees for a given company
##### `http://localhost:8383/company/<company name>`

To test this endpoint, click the following links with the API running locally:

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



#### 2. API endpoint to get the Name, Age, Address and phone information about two people, and a list of their friends in common who have brown eyes and are still alive
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

#### 3. API endpoint to get the name and age of one person and the fruits and vegetables they like
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

## To Run Tests
The following command runs unit tests within the container using pytest:
```
$ docker run -t --entrypoint /paranuara/api/test.sh --rm paranuara-challenge-solution

``` 
As described in the _Code Overview_ section below (#6), these tests cover unit tests as well as the API endpoint functional tests. `Pytest` is used for the tests, the PyPI package gets installed by the `test.sh` script along with the `requests` package to test the API endpoints over HTTP.

## Code Overview
All of the application modules are in the repo root. 
1. `server.py` is the entry point which gets invoked on run and starts a web server. It consists of route definitions for HTTP requests. The `bottle.py` package (from PyPI) provides the WSGI interface.

2. The `app.py` module is the middle layer between the route definitions of `server.py` and the output JSON builders of `view.py`. The App object initializes the data model as a Model object, loads the data into the Model object from the file path/URI defined in `config.py`, and binds it to the View object. The App object's methods get invoked by the routing functions of the `server` module. These methods perform the task of unencoding the URL parameters into plain strings and passing them into the View object's corresponding methods.

3. The `view.py` module sends invokes query methods of the data model and passes the parameters received from the `app` module. The View object consists of methods that transform and map the data received from the data model queries into Python dictionary objects of the required output schema and returns them to the App for JSON serialization.

4. `model.py` provides the Model class which loads the JSON files into a Pandas DataFrame object and merges them (using file path/URI and merge keys defined in `config.py` that get passed during Model instantiation by App). The DataFrame object acts like an in-memory single-table database combining both company and people data. It relies on a separate helper class Query defined in `query.py` to provide an interface for running queries on the combined table.

5. The `query.py` module provides the Query class which has helper methods to perform queries on the Model and return results. These methods return query results as record sets in the form lists of dictionaries.
The Query class itself relies on the QueryBuilder class (defined in the same module) which provides an interface for building queries for use on a Pandas DataFrame such as testing multiple values against multiple columns or multiple values within a column.

6. __The `test_app.py`, `test_view.py`, `test_model.py` and `test_query.py` modules provide unit tests for the app, view, model and query modules respectively. The `test_http.py` module provides functional tests for the endpoint interfaces specified by the challenge problem statement.__

7. Others:
    - `Jenkinsfile`: Jenkins task pipeline is defined here.
    - `DOCKER`: Dockerfile to build the API container.
    - `setup.sh`: This executed within the API container during build. It creates a virtual environment and installs Python dependencies using pip.
    - `start.sh`: This gets executed within the API container during run. It runs `server.py` within the container.
    - `tesh.sh`: Executable shell script to install `pytest` and `requests` packages fro PyPI and run tests when the container is run in test mode using the command described in the "To Run Unit Test" section above.
    - `requirements.txt`: List of dependencies installed by pip running inside the Docker container during build.
    - `.travis.yml` Required only if using the Travis-CI pipeline.
    