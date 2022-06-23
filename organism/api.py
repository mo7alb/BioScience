from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import *
from .models import *

class ProteinDetail(GenericAPIView):
   queryset = Protein.objects.all()
   serializer_class = ProteinSerializer

   def get_object(self, pk):
      try:
         return self.queryset.get(protein_id=pk)
      except models.Protein.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

   def get(self, request, protein_id, format="json"):
      protein = self.get_object(protein_id)
      serializer = ProteinSerializer(protein)
      return Response(serializer.data)


class PfamDetails(GenericAPIView):
   queryset = Pfam.objects.all()
   serializer_class = PfamSerializer

   def get(self, request, pfam_id, format="json"):
      pfam = self.queryset.get(domain_id=pfam_id)
      serializer = PfamSerializer(pfam)
      return Response(serializer.data)

class ProteinList(GenericAPIView):
   queryset = Protein.objects.all()
   serializer_class = ProteinsListSerializer

   def get_object(self, pk):
      return self.queryset.get(id=pk)

   def get(self, request, taxa_id, format="json"):
      tax = Taxonomy.objects.get(taxa_id=taxa_id)

      relationList = ProteinTaxonomyLink.objects.filter(taxonomy=tax)
      proteins = []
      for relation in relationList:
         proteins.append(self.get_object(relation.protein.id))
      serializer = ProteinsListSerializer(proteins, many=True)
      return Response(serializer.data)

class PfamList (GenericAPIView):
   queryset = Domain.objects.all()
   serializer_class = PfamListSerializer

   def get_object(self, pk):
      return self.queryset.get(id=pk)

   def get(self, request, taxa_id, format="json"):
      tax = Taxonomy.objects.get(taxa_id=taxa_id)

      relationList = ProteinTaxonomyLink.objects.filter(taxonomy=tax)

      domains = []

      for relation in relationList:
         protein = Protein.objects.get(id=relation.protein.id)
         protein_domain = ProteinDomainLink.objects.filter(protein=protein)

         for domain in protein_domain:
            domains.append(self.get_object(domain.domain.id))


      serializer = PfamListSerializer(domains, many=True)

      return Response(serializer.data)

class Coverage(GenericAPIView):
   queryset = Domain.objects.all()
   serializer_class = CoverageSerializer

   def get_object(self, pk):
      return self.queryset.get(id=pk)

   def get (self, request, protein_id, format="json"):
      protein = Protein.objects.get(protein_id=protein_id)

      relations = ProteinDomainLink.objects.filter(protein=protein)
      domains = []
      for relation in relations:
         domains.append(self.get_object(relation.domain.id))

      serializer = CoverageSerializer(domains, many=True)
      values = serializer.data

      coverage = 0
      for value in values:
         coverage += value['end_coordinate']
         coverage -= value['start_coordinate']

      coverage /= protein.length

      return Response({ "coverage": coverage  })

@api_view(["POST"])
def new_protein(request):
      serializer = ProteinSerializer(data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)