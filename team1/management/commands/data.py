import os, sys
import psycopg2
import pprint
#import squadster
import django
from rest_framework.test import APIRequestFactory
#from django.core.management.base import NoArgsCommand

#class Command(NoArgsCommand):
#def handle_noargs(self, **options):

conn_string = "host='localhost' dbname='squadsterdb', user='squadster_admin' password='mysharedpassword'"

conn = psycopg2.connect(conn_string)

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute('SELECT * from auth_user')
for row in cursor:
    print(row)

#factory = APIRequestFactory()
#request = factory.post()
