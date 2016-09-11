from django.shortcuts import render
from django.http import HttpResponse
import re

def login(request):
    context = {'user': request.user}
    return render(request, 'login.html', context)

def join_event(request):
    matcher = re.search('events/([0-9]{7})/join_event', request.url)
    event_id = matcher.group(1)
    
