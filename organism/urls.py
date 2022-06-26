from django.urls import path
from . import views
from . import api

urlpatterns = [
   # root url
   # displays a single page application
   path('', views.index, name="index"),
   # route that displays a form to add a new protein
   path('new', views.new_protein, name="new_protein"),

   # api routes
   # route to add a new protein 
   path (
      'api/protein',
      api.new_protein,
      name="new_protein"
   ),

   # route  to return details of a protein
   path(
      'api/protein/<str:protein_id>', 
      api.ProteinDetail.as_view(), 
      name="protein_details"
   ),
   
   # route to return the domain and its description of a pfam - pass the pfam id
   path(
      'api/pfam/<str:pfam_id>', 
      api.PfamDetails.as_view(), 
      name="pfam_details"
   ),
   
   # route to return list of proteins for a given organism
   path(
      'api/proteins/<int:taxa_id>', 
      api.ProteinList.as_view(), 
      name="protein_list"
   ),
   
   # route to return list of pfams for a given organism
   path(
      'api/pfams/<int:taxa_id>', 
      api.PfamList.as_view(), 
      name="pfam_list"
   ),
   
   # route to return the coverage of a given protein
   path(
      'api/coverage/<str:protein_id>', 
      api.Coverage.as_view(), 
      name="protein_coverage"
   )
]