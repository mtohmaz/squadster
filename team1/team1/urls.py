"""team1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from squadster import views, viewsets, urls
#from squadster import viewsets

urlpatterns = [
    # catch these before they go to squadster app
    url(r'^api/admin/', admin.site.urls),
    
    
    # the rest go through to squadster specific urls
    #url(r'^api/auth/', views.login),
    
    
    
    # keep this right before ^api/
    url(r'^api/$', views.root_view),
    # must be last
    url(r'^api/', include('squadster.urls')),
]
