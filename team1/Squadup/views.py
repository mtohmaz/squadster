from django.shortcuts import render
from django.http import HttpResponse


def login(request):
   context = {'user': request.user}
   return render(request, 'login.html', context)
