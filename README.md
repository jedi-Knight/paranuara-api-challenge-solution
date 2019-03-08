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

## To Run
After completing the build steps above, run this command:

```
$ docker run -p 127.0.0.1:8080:8080 -dit paranuara-challenge-solution

```

#### To test the API endpoints (solutions):

Note: The query and return values of following examples are based on the JSON data included in the challenge GitHub repo. Please change the company and user names to test with different data.

1. API endpoint to get all employees for a given company:
`http://localhost:8080/company/<company name>`

To test this endpoint, click the following links with the API running:
_Example 1.1:_
[http://localhost:8080/company/PERMADYNE](http://localhost:8080/company/NETBOOK)
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
[http://localhost:8080/company/NETBOOK](http://localhost:8080/company/NETBOOK)
Here the company name is NETBOOK. Following is its JSON return:
```
{
    "number-of-employees": 0, 
    "employees": [],
    "message": "The company has no employees."
}
```
If a company has no employees, the `number-of-employees` and `employees` field reflect this fact and a `message` field is included in the JSON which includes a string message.



2. API endpoint to get the Name, Age, Address and phone information about two people, and a list of their friends in common who have brown eyes and are still alive:
`http://localhost:8080/user/<one user name>/<another user name>`
_Example 2.1:_
http://localhost:8080/user/Sharron%20Barker/Moon%20Herring
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

3. API endpoint to get the name and age of one person and the fruits and vegetables they like:
`http://localhost:8080/user/<user name>`
    
    _Example 3.1:_
    http://localhost:8080/user/Leblanc%20Talley

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
$ docker run -p 127.0.0.1:8080:8080 -it --entrypoint /paranuara/api/test.sh paranuara-challenge-solution

```
