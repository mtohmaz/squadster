## NOTE: This is tested for Ubuntu 16.04
# any target with apt-get commands must be run on Ubuntu
# the others work on any linux distro

default:


install_ubuntu: ubuntu_packages setuppython setupdb createuser

ubuntu_packages:
	sudo apt-get update
	sudo apt-get install -y postgresql postgresql-contrib postgresql-server-dev-all
	# remove pip for python2
	sudo apt-get remove python-pip
	# set python3 as the default
	#sudo rm -f /usr/bin/python
	#sudo ln -s /usr/bin/python3 /usr/bin/python
	# install pip for python3
	sudo apt-get install python3-pip

cleanmigrations: cleandb
	rm -rf team1/squadster/migrations

cleandb:
	sudo -u postgres psql "drop database squadsterdb;"

setupdb:
	# This script is only for commands run as db user 'postgres'
	# if we need to have other setup commands for the squadster_admin user,
	# we should put them in a setupsquadster.sql script or something
	sudo -u postgres psql -f setup/setup.sql

setuppython:
	# install django and rest and postgresql driver
	sudo pip3 install django djangorestframework psycopg2 oauth2client


# NOTE: this allows you to get around the peer authentication
# but not using right now
# instead connect with:
#     psql -h 127.0.0.1 squadsterdb squadster_admin
createuser:
	if sudo useradd squadster_admin -s /bin/bash > /dev/null 2>&1; \
		then echo "squadster_admin:mysharedpassword" | sudo chpasswd ; fi
	sudo usermod -a -G sudo squadster_admin
	# you can now connect to postgresql:
	#     sudo -u squadster_admin psql -d squadsterdb

compile:

install:
