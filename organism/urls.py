from django.urls import path
from . import views
from . import api

urlpatterns= [
   # root url
   path('', views.index, name="index"),

   # api paths
   # server protein api path
   path('api/proteins', api.Proteins, name="proteins")
]