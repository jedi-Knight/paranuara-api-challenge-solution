#!/bin/bash

source ../bin/activate

#Install test dependencies from pip
pip install pytest==4.3.0   #For running tests.
pip install requests==2.21.0    #For API endpoints test over HTTP.

#Run unit tests
pytest -vv --ignore test_http.py

#Test API Endpoints
echo "Now starting server at http://0.0.0.0:8080/  .."
python server.py 2>&1 &     # Start the API server to start tests for endpoints.

#Now wait for 5 seconds, giving the server some time to start up before continuing tests..
sleep 5
pytest -vv test_http.py


