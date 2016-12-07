import os, sys
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
        ids = self.createusers(conn)
        sessions = []
        cookies = []
        for id in ids:
            session = self.create_session(id)
            sessions.append(session)
            cookies.append({'sessionid':session.session_key})

        self.insertdata(cookies[0], ids)

        session.delete()

    def cleardata(self, conn):
        cursor = conn.cursor()
        queries = [
            "DELETE FROM squadster_event_attendees",
            "DELETE FROM squadster_event",
            "DELETE FROM authtoken_token",
            "DELETE FROM squadster_credentials",
            "DELETE FROM squadster_squadstersession",
            "DELETE FROM django_session",
            "DELETE FROM squadster_squadsteruser",
            "DELETE FROM auth_user",
        ]

        for query in queries:
            cursor.execute(query)
            conn.commit()


    def createusers(self, conn):
        users = [
            {'username':'user1', 'email':'email1@squadster.io'},
            #{'username':'user2', 'email':'email2@squadster.io'},
            #{'username':'user3', 'email':'email3@squadster.io'},
        ]
        cursor = conn.cursor()
        for user in users:
            time = functions.now() + timedelta(hours=2)
            fmt = "%Y-%m-%d %H:%M:%S%z"
            time_str = time.strftime(fmt)

            query = "INSERT INTO auth_user(is_superuser, is_staff, is_active, username, password, email, first_name, last_name, date_joined) " \
                +"VALUES('f', 'f', 't', 'user', '', 'user1@squadster.io', '', '', '"+ time_str +"')"
            cursor.execute(query)
            #conn.commit()

        query = "SELECT id FROM auth_user"
        #cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        ids = []
        for row in rows:
            ids.append(row[0])
        print(ids)
        conn.commit()
        return ids

    def create_session(self, user_id):
        session = SessionStore()

        session['google_session_timeout'] = 5
        session['google_session_last_auth'] = timezone.now().strftime(dateformat)
        session['google_session_token'] = 'test_id_token'
        session['user_id'] = user_id
        session.create()
        sess_key = session.session_key
        self.sess_key = session.session_key

        #cookie = {'sessionid': sess_key}
        return session

    def insertdata(self, cookie, ids):
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
            {
                'host_id': ids[0],
                'title': 'swimming at carmichael',
                'description': 'description',
                'lat': 35.783,
                'lon': -78.674,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'carmichael gym'
            },
            {
                'host_id': ids[0],
                'title': 'biking at umstead',
                'description': 'description',
                'lat': 35.890,
                'lon': -78.752,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'umstead'
            },
            {
                'host_id': ids[0],
                'title': 'dr strange movie',
                'description': 'description',
                'lat': 35.904,
                'lon': -78.784,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'regal cinema raleigh'
            },
            {
                'host_id': ids[0],
                'title': 'study group for py208',
                'description': 'description',
                'lat': 35.787,
                'lon': -78.671,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'DH Hill library'
            },
            {
                'host_id': ids[0],
                'title': 'LAN Party for Halo 3',
                'description': 'description',
                'lat': 35.769,
                'lon': -78.678,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'Hunt Library'
            },
            {
                'host_id': ids[0],
                'title': 'Car Meeting',
                'description': 'description',
                'lat': 35.786,
                'lon': -78.703,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'Kmart parking lot'
            },
            {
                'host_id': ids[0],
                'title': 'canoeing at lake johnson',
                'description': 'description',
                'lat': 35.762,
                'lon': -78.716,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'Lake Johnson'
            },
            {
                'host_id': ids[0],
                'title': 'dinner at chipotle',
                'description': 'description',
                'lat': 35.787,
                'lon': -78.669,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'chipotle hillsborough street'
            },
            {
                'host_id': ids[0],
                'title': 'fun at dave and busters',
                'description': 'description',
                'lat': 35.774,
                'lon': -78.763,
                'max_attendees': 5,
                'date': timezone.now().strftime(dateformat),
                'location': 'dave and busters in cary'
            },
        ]

        for event in events:

            req = requests.post('https://localhost/api/events/', cookies=cookie, data=event, verify=False)
            print(req.text)
