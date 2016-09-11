## NOTE: This is tested for Ubuntu 16.04
# any target with apt-get commands must be run on Ubuntu
# the others work on any linux distro

default:
	

install_ubuntu: ubuntu_packages setuppython setupdb

ubuntu_packages:
	sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-all
	# remove pip for python2
	sudo apt-get remove python-pip
	# set python3 as the default
	sudo rm -f /usr/bin/python
	sudo ln -s /usr/bin/python3 /usr/bin/python
	# install pip for python3
	sudo apt-get install python3-pip


cleanmigrations:
	rm -rf 

cleandb:
	psql --username postgres "drop database squadsterdb;"

setupdb:
	# This script is only for commands run as db user 'postgres'
	# if we need to have other setup commands for the team1 user,
	# we should put them in a setupteam1.sql script or something
	psql --username postgres -f setup/setup.sql

setuppython:
	# install django and rest and postgresql driver
	sudo pip install django djangorestframework psycopg2

compile:

makemigrations:

install:
