## NOTE: This is tested for Ubuntu 16.04
# any target with apt-get commands must be run on Ubuntu
# the others work on any linux distro

default:

install_ubuntu: ubuntu_packages setuppython

ubuntu_packages:
	sudo apt-get update
	sudo apt-get install -y \
		python3-pip \
		postgresql postgresql-contrib postgresql-server-dev-all \
		npm nodejs \
		nginx

	# remove pip for python2
	sudo apt-get remove python-pip

cleanmigrations: cleandb
	rm -rf team1/squadster/migrations

cleandb:
	sudo -u postgres psql "drop database squadsterdb;"

setupdb:
	# This script is only for commands run as db user 'postgres'
	# if we need to have other setup commands for the team1 user,
	# we should put them in a setupteam1.sql script or something
	sudo cp setup/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
	sudo chown root:root /etc/postgresql/9.3/main/pg_hba.conf
	psql --username postgres -f setup/setup.sql

setuppython:
	bash setup/pythonsetup.sh

cleanpython:
	cd team1
	rm -rf bin lib share pip* include

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
