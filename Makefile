## NOTE: This is tested for Ubuntu 16.04

default: setupdb setuppython

setupdb:
	sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-all
	
	# This script is only for commands run as db user 'postgres'
	# if we need to have other setup commands for the team1 user,
	# we should put them in a setupteam1.sql script or something
	psql --username postgres -f setup/setup.sql

setuppython:
	# remove pip for python2
	sudo apt-get remove python-pip
	# set python3 as the default
	sudo rm -f /usr/bin/python
	sudo ln -s /usr/bin/python3 /usr/bin/python
	# install pip for python3
	sudo apt-get install python3-pip
	# install django and rest and postgresql driver
	sudo pip install django djangorestframework psycopg2

compile:

makemigrations:

install:
