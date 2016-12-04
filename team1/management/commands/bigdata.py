import os, sys, random
import psycopg2
import pprint
import squadster
from squadster import functions
import django
from django.utils import timezone
import requests
from rest_framework.test import APIRequestFactory
from datetime import datetime, timedelta
#from dateutil.relativedelta import relativedelta
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

dateformat = "%Y-%m-%dT%H:%M:%S%z"

## CONFIG
user_count = 10
events_per_user = 10
comments_per_event = 10

#from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
class Command(BaseCommand):

    def handle(self, *args, **options):
        conn_string = "host='localhost' dbname='squadsterdb' user='squadster_admin' password='mysharedpassword'"
        conn = psycopg2.connect(conn_string)
        sess_key = 'testsesskey'
        #try:
        #    session = Session.objects.get(session_key=sess_key)
        #    session.delete()
        #except Exception as e:
        #    pass

        time = functions.now() + timedelta(hours=2)
        fmt = "%Y-%m-%d %H:%M:%S%z"

        time_str = time.strftime(fmt)


        #payload = {'lat': 35, 'lon': 78, 'radius': 10}
        #req = requests.get('http://localhost/api/events/', cookies=cookie, params=payload)

        # do the data
        self.cleardata(conn)
        ids = self.createusers(conn, user_count)
        sessions = []
        cookies = []
        for id in ids:
            session = self.create_session(id)
            sessions.append(session)
            cookies.append({'sessionid':session.session_key})

        random.seed(time)
        self.create_events(cookies, ids, events_per_user)

        for session in sessions:
            session.delete()


    def cleardata(self, conn):
        cursor = conn.cursor()
        queries = [
            "DELETE FROM squadster_comment",
            "DELETE FROM squadster_event",
            "DELETE FROM authtoken_token",
            "DELETE FROM squadster_credentials",
            "DELETE FROM squadster_squadsteruser",
            "DELETE FROM auth_user",
        ]
        for query in queries:
            cursor.execute(query)
        conn.commit()


    def createusers(self, conn, count):
        users = []

        for i in range(count):
            username = 'user'+str(i)
            u = {'username': username, 'email': username+'@squadster.io'}
            users.append(u)

        cursor = conn.cursor()
        for user in users:
            time = functions.now() + timedelta(hours=2)
            fmt = "%Y-%m-%d %H:%M:%S%z"
            time_str = time.strftime(fmt)

            query = "INSERT INTO auth_user(is_superuser, is_staff, is_active, username, password, email, first_name, last_name, date_joined) " \
                +"VALUES('f', 'f', 't', 'user', '', 'user1@squadster.io', '', '', '"+ time_str +"')"
            cursor.execute(query)

        query = "SELECT id FROM auth_user"
        cursor.execute(query)
        rows = cursor.fetchall()
        ids = []
        for row in rows:
            ids.append(row[0])
        #print(ids)

        conn.commit()
        return ids


    def create_session(self, user_id):
        session = SessionStore()
        session['google_session_timeout'] = 5
        session['google_session_last_auth'] = timezone.now().strftime(dateformat)
        session['google_session_token'] = 'test_id_token_'+str(user_id)
        session['user_id'] = user_id
        session.create()
        sess_key = session.session_key
        self.sess_key = session.session_key
        #cookie = {'sessionid': sess_key}
        return session


    def create_events(self, cookies, ids, events_per_user):
        events = [
            {
                'host_id': ids[0],
                'title': 'dp dough',
                'description': 'description',
                'lat': 35.779,
                'lon': -78.675,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'mission valley'
            },
        ]
        for i in range(events_per_user):
            


        for event in events:

            req = requests.post('http://localhost/api/events/', cookies=cookie, data=event)
            print(req.text)
