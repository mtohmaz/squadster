import os, sys, random
import json
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
user_count = 20
events_per_user = 50
comments_per_event = 5


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

        time = functions.now() + timedelta(hours=48)
        fmt = "%Y-%m-%d %H:%M:%S%z"

        time_str = time.strftime(fmt)

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
        eventids = self.create_events(cookies, ids)
        commentids = self.create_comments(cookies, eventids, ids)

        for session in sessions:
            session.delete()


    def cleardata(self, conn):
        cursor = conn.cursor()
        queries = [
            "DELETE FROM squadster_comment",
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
                +"VALUES('f', 'f', 't', '"+user['username']+"', '', '"+user['email']+"', '', '', '"+ time_str +"')"
            cursor.execute(query)

        query = "SELECT id FROM auth_user"
        cursor.execute(query)
        rows = cursor.fetchall()
        ids = []
        for row in rows:
            ids.append(row[0])

        conn.commit()
        return ids


    def create_session(self, user_id):
        session = SessionStore()
        session['google_session_timeout'] = 60*60*48 # 48 hours
        session['google_session_last_auth'] = timezone.now().strftime(dateformat)
        session['google_session_token'] = 'test_id_token_'+str(user_id)
        session['user_id'] = user_id
        session.create()
        sess_key = session.session_key
        self.sess_key = session.session_key
        return session


    def create_events(self, cookies, ids):
        eventids = []
        for i in range(len(ids)):
            for j in range(events_per_user):
                eventname = 'event-{}-{}'.format(i, j)
                # get a time within the next two weeks (20160 minutes)
                deltaminutes = random.randint(0, 20160)
                eventtime = timezone.now() + timedelta(minutes=deltaminutes)
                event = {
                    'host_id': ids[i],
                    'title': '{}, number {} for userid {}'.format(eventname, j, i),
                    'description': 'description for {}'.format(eventname),
                    'lat': round(random.uniform(35,36), 6),
                    'lon': round(random.uniform(-79,-78), 6),
                    'max_attendees': random.randint(5, 500),
                    'date': eventtime.strftime(dateformat),
                    'location': 'location for ' + eventname
                }
                resp = requests.post('http://localhost/api/events/', cookies=cookies[i], data=event)
                respobj = json.loads(resp.text)
                eventids.append(respobj['event_id'])
        return eventids

    def create_comments(self, cookies, eventids, userids):
        commentids = []
        for eventid in eventids:
            for j in range(comments_per_event):
                commenttext = 'comment-'+str(eventid)+'-'+str(j)
                useridx = random.randint(0, len(userids)-1)
                userid = userids[useridx]
                comment = {
                    'parent_event': eventid,
                    'author': userid,
                    'text': commenttext,
                    #'parent_comment': ''
                }
                resp = requests.post(
                    'http://localhost/api/events/'+str(eventid)+'/comments/',
                    cookies = cookies[useridx],
                    data=comment)
                #print(resp.text)
                respobj = json.loads(resp.text)
                commentids.append(respobj['comment_id'])
        return commentids
