#!/bin/bash
sudo pip3 install virtualenv
virtualenv -p /usr/bin/python3 team1
source team1/bin/activate
pip3 install django djangorestframework psycopg2 oauth2client gunicorn
