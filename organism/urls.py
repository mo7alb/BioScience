from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from . import api

urlpatterns= [
   # root url
   path('', views.index, name="index"),

   # api paths
   # server protein api path
   path('api/protein/<str:protein_id>', api.ProteinDetail.as_view(), name="protein_details"),
   path('api/pfam/<str:pfam_id>', api.PfamDetails.as_view(), name="pfam_details"),
   path('api/proteins/<int:taxa_id>', api.ProteinList.as_view(), name="protein_list"),
   path('api/pfams/<int:taxa_id>', api.PfamList.as_view(), name="pfam_list"),
   path('api/coverage/<str:protein_id>', api.Coverage.as_view(), name="domain_coverage")
]