#! /bin/bash

# setup environment parameters
export DBHOST="database-2.clbmc2tqyqce.us-east-2.rds.amazonaws.com"
export DBUSER="admin"
export DBPASSWORD="seadogs!"
export FLASK_APP='application.py'

# ready to run actual app
flask run --host=0.0.0.0 --port=5000
