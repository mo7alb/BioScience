from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import *
from .models import *

class ProteinDetail(GenericAPIView):
   """
   A class based view used to handle the api route /api/protein/<str:protein_id>
   it returns the details of the protein representing the protein_id

   ...

   Attributes
   ----------
   queryset : list
      the queryset from the protein is to be returned
   serializer_class : str
      the class that seralizes the incoming and outgoing data

   Methods
   -------
   get_object(pk)
      returns a single protein from the dataset
   get(request, protein_id, format='json')
      responds to a get request to the api route
   """
   queryset = Protein.objects.all()
   serializer_class = ProteinSerializer

   def get_object(self, pk) -> Response | Protein:
      # try to retrieve a protein with pk as id
      try:
         return self.queryset.get(protein_id=pk)
      # return an 404 error if it doesn't exist
      except Protein.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

   def get(self, request, protein_id, format="json") -> Response:
      # get the protein from the query set
      protein = self.get_object(protein_id)
      print (protein)
      # serialize it to be returned to the client
      serializer = ProteinSerializer(protein)
      # return the serialized data within a response
      return Response(serializer.data)


class PfamDetails(GenericAPIView):
   """
   A class based view used to handle the api route /api/pfam/<str:pfam_id>
   it returns the details of the pfam representing the pfam_id

   ...

   Attributes
   ----------
   queryset : list
      list of all the pfams in the database
   serializer_class : str
      the class that seralizes the incoming and outgoing data

   Methods
   -------
   get(request, pfam_id, format='json')
      responds to a get request to the api route by returning a pfam
   """
   
   queryset = Pfam.objects.all()
   serializer_class = PfamSerializer

   def get(self, request, pfam_id, format="json"):
      # query the database for the pfam with the id passed to the function
      pfam = self.queryset.get(domain_id=pfam_id)
      # serialize the pfam to be served to the user
      serializer = PfamSerializer(pfam)
      # return a response with the serializer data
      return Response(serializer.data)

class ProteinList(GenericAPIView):
   """
   A class based view used to handle the api route /api/proteins/<int:taxa_id>
   it returns a list of proteins related to an organism

   ...

   Attributes
   
   queryset : list
      list of all the proteins in the database
   serializer_class : str
      the class that seralizes the incoming and outgoing data

   Methods
   -------
   def get_object(pk)
      queries the database to return a single Protein or throws a 404 error
   get(request, pfam_id, format='json')
      responds to a get request to the api route by returning a list of proteins
   """

   queryset = Protein.objects.all()
   serializer_class = ProteinsListSerializer

   def get_object(self, pk) -> Protein | Response:
      # try to retrieve a protein with pk as id
      try:
         return self.queryset.get(id=pk)
      # throws an error in case the Protein does not exists in the database
      except Protein.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

   def get(self, request, taxa_id, format="json") -> Response:
      # get the organism
      tax = Taxonomy.objects.get(taxa_id=taxa_id)

      # get all the relations between the organism and proteins
      relationList = ProteinTaxonomyLink.objects.filter(taxonomy=tax)
      # list to store the proteins that have a relation with the organism
      proteins = []
      # iterate over all the protein organism relation
      for relation in relationList:
         # add the protein to the list of proteins that have a relation with the organims
         proteins.append(self.get_object(relation.protein.id))
      # serialize the list of proteins in order for it to be served to the client
      serializer = ProteinsListSerializer(proteins, many=True)
      # return a response with the serialized data
      return Response(serializer.data)

class PfamList (GenericAPIView):
   """
   A class based view used to handle the api route /api/pfams/<int:taxa_id>
   it returns a list of pfams related to an organism

   ...

   Attributes
   
   queryset : list
      list of all the pfams in the database
   serializer_class : str
      the class that seralizes the incoming and outgoing data

   Methods
   -------
   def get_object(pk)
      queries the database to return a single pfam or throws a 404 error
   get(request, pfam_id, format='json')
      responds to a get request to the api route by returning a list of pfams
   """
   queryset = Domain.objects.all()
   serializer_class = PfamListSerializer

   def get_object(self, pk):
      # try to retrieve a pfam with pk as id
      try:
         return self.queryset.get(id=pk)
      # throws an error in case the pfam does not exists in the database
      except Pfam.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

   def get(self, request, taxa_id, format="json"):
      # organism which is related to all pfams
      tax = Taxonomy.objects.get(taxa_id=taxa_id)

      # list of relations between the organism and proteins 
      relationList = ProteinTaxonomyLink.objects.filter(taxonomy=tax)

      # list to store domains related to the organism
      domains = []

      # iterate over the list of relations between the proteins and the orgnaism
      for relation in relationList:
         # get the protein
         protein = Protein.objects.get(id=relation.protein.id)
         # get list of relations between the protein and domains 
         protein_domain = ProteinDomainLink.objects.filter(protein=protein)

         # iterate over list of domain protein relationships 
         for domain in protein_domain:
            # add the pfam with the same domain id as the domain
            domains.append(self.get_object(domain.domain.id))

      # serialize the data to be sent out
      serializer = PfamListSerializer(domains, many=True)
      
      # response to the client request with the serilized data
      return Response(serializer.data)

class Coverage(GenericAPIView):
   """
   A class based view used to handle the api route /api/coverage/<str:protein_id>
   it returns the coverage of a protein

   ...

   Attributes
   
   queryset : list
      list of all the pfams in the database
   serializer_class : str
      the class that seralizes the incoming and outgoing data

   Methods
   -------
   def get_object(pk)
      queries the database to return a single pfam or throws a 404 error
   get(request, pfam_id, format='json')
      responds to a get request to the api route by returning a list of pfams
   """

   queryset = Domain.objects.all()
   serializer_class = CoverageSerializer

   def get_object(self, pk):
      # try to retrieve a domain with pk as id
      try:
         return self.queryset.get(id=pk)
      # throws an error in case the Domain does not exists in the database
      except Domain.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

   def get (self, request, protein_id, format="json"):
      # get the protein to which the coverage is to be returned
      protein = Protein.objects.get(protein_id=protein_id)

      # get all relations between the protein and domains
      relations = ProteinDomainLink.objects.filter(protein=protein)
      # iterate over each relation and get the domain and add it to a list
      domains = []
      for relation in relations:
         domains.append(self.get_object(relation.domain.id))

      # serialize the data
      serializer = CoverageSerializer(domains, many=True)
      # get the start coordinate value and the end coordinate value
      values = serializer.data

      # calculate the coverage of the protein
      coverage = 0
      for value in values:
         coverage += value['end_coordinate']
         coverage -= value['start_coordinate']

      # divide it with the length of the protein
      coverage /= protein.length

      # response to the client with the coverage value
      return Response({ "coverage": coverage  })

@api_view(["POST"])
def new_protein(request) -> Response:
   """
   view used to add a new protein to the database
   """

   # serialize the data passed through the request
   serializer = ProteinSerializer(data=request.data)

   # check if the value is valid 
   if serializer.is_valid():
      # if the data is valid save it to the database and return it
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

   # if the data is not valid return an error
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)