

default: setupdb

setupdb:
	psql --username postgres -f setup.sql

compile:

makemigrations:

install:
