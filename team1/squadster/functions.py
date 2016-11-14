import pytz
from team1.settings import dateformat
from django.utils import timezone
from datetime import datetime, timedelta


def str_to_time(s):
    t = datetime.strptime(s, dateformat)
    utctz = pytz.timezone('UTC')
    t = utctz.localize(t)
    return t

def time_to_str(time):
    time.strftime(settings.dateformat)

def now():
    utctz = pytz.timezone('UTC')
    