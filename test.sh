#!/bin/bash

source ../bin/activate

#Install test dependencies from pip
pip install pytest==4.3.0
pip install requests==2.21.0

#Run unit tests
pytest -vv --ignore test_http.py

#Test API Endpoints
echo "Now starting server at http://0.0.0.0:8080/  .."
python server.py 2>&1 &

#Now wait for 5 seconds, giving the server some time to start up before continuing tests..
sleep 5
pytest -vv test_http.py


