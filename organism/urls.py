from django.urls import path
from . import views
from . import api

urlpatterns= [
   # root url
   path('', views.index, name="index"),

   # api paths
   # server protein api path
   path('api/protein/<str:protein_id>', api.ProteinDetail.as_view(), name="proteins"),
   path('api/pfam/<str:pfam_id>', api.Pfam.as_view(), name="proteins"),
   path('api/proteins/<int:taxa_id>', api.Proteins.as_view(), name="proteins"),
]