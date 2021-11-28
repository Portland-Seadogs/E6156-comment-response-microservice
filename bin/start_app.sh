#! /bin/bash

# setup environment parameters
export DBHOST=
export DBUSER=
export DBPASSWORD= 
export FLASK_APP='application.py'

# ready to run actual app
flask run --host=0.0.0.0 --port=5000
