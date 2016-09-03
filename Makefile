

default: setupdb

setupdb:
	psql --username postgres -f setup/setup.sql

compile:

makemigrations:

install:
