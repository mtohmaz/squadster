## NOTE: This is tested for Ubuntu 16.04
# any target with apt-get commands must be run on Ubuntu
# the others should on any linux distro

# if postgresql *admin* user is not postgres, set it here
postgresrootuser='postgres'
postgresrootdb='postgres'

# if someone runs the makefile from a different directory than the makefile
export ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

default:
	echo "no default set, please see Makefile and select a target"

# mostly for developers, sets up the app server and db on the same machine
install_all: install_appserver install_dbserver

# installs and sets up everything needed to run the app web server
install_appserver: ubuntu_app_packages setuppython setupwebserver cleanmigrations

# installs and sets up everything needed for the database server
install_dbserver: ubuntu_db_packages setupdb


ubuntu_app_packages:
	sudo apt-get update
	sudo apt-get install -y \
		python3-pip \
		npm nodejs nodejs-legacy \
		nginx

	# install the angular-cli
	sudo npm install -g angular-cli
	sudo npm install -g typings

	# remove pip for python2
	sudo apt-get remove python-pip

ubuntu_db_packages:
	sudo apt-get update
	sudo apt-get install -y \
		postgresql \
		postgresql-contrib \
		postgresql-server-dev-all

	# PostGIS
	sudo add-apt-repository -y ppa:ubuntugis/ppa
	sudo apt-get update
	sudo apt-get install -y postgis

# drops the database and completely recreates it
resetdb:
	psql ${postgresrootdb} ${postgresrootuser} -f sql/reset.sql
	#psql ${postgresrootdb} ${postgresrootuser} -c 'drop database squadsterdb;'
	#psql ${postgresrootdb} ${postgresrootuser} -c 'create database squadsterdb;'
	#psql ${postgresrootdb} ${postgresrootuser} -c 'grant all privileges on database squadsterdb to squadster_admin;'


# wipes main contents of the squasterdb database
cleandb:
	# contents that contain user keys
	psql squadster_admin squadsterdb -c 'delete from squadster_comment;'
	psql squadster_admin squadsterdb -c 'delete from squadster_joinedevents;'
	psql squadster_admin squadsterdb -c 'delete from squadster_event;'

	# user related tables
	psql squadster_admin squadsterdb -c 'delete from authtoken_token;'
	psql squadster_admin squadsterdb -c 'delete from squadster_squadsteruser;'
	psql squadster_admin squadsterdb -c 'delete from auth_user;'


# NOTE: must have already run setuppython to create the virtualenv for django
cleanmigrations: resetdb
	rm -rf team1/squadster/migrations
	bash setup/makemigrations.sh


setupdb:
	# This script is only for commands run as db user 'postgres'
	# if we need to have other setup commands for the team1 user,
	# we should put them in a setupteam1.sql script or something

	# The following two are path dependent based on the version of postgresql
	sudo cp setup/pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf
	sudo chown postgres:postgres /etc/postgresql/9.5/main/pg_hba.conf
	sudo chmod 640 /etc/postgresql/9.5/main/pg_hba.conf
	sudo systemctl restart postgresql

	sudo -u postgres psql -f setup/setup.sql
	sudo -u postgres psql -d squadsterdb -c 'CREATE EXTENSION postgis';

setuppython:
	bash setup/pythonsetup.sh


cleanpython:
	cd team1
	rm -rf bin lib share pip* include

setupwebserver:
	sudo cp nginx.conf /etc/nginx/nginx.conf
	sudo nginx -s reload


# NOTE: this allows you to get around the peer authentication
# by having a local user the same as the db user
# but not using right now
createuser:
	if sudo useradd squadster_admin -s /bin/bash > /dev/null 2>&1; \
		then echo "squadster_admin:mysharedpassword" | sudo chpasswd ; fi
	sudo usermod -a -G sudo squadster_admin
	# you can now connect to postgresql:
	#     sudo -u squadster_admin psql -d squadsterdb
