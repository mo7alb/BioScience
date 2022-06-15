from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

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

   def post (self, request, format="json"):
      serializer = ProteinSerializer(data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Pfam(GenericAPIView):
   queryset = Pfam.objects.all()
   serializer_class = PfamSerializer

   def get(self, request, pfam_id, format="json"):
      pfam = self.queryset.get(domain_id=pfam_id)
      serializer = PfamSerializer(pfam)
      return Response(serializer.data)

class Proteins(GenericAPIView):
   queryset = Protein.objects.all()
   serializer_class = ProteinsSerializer

   def get_object(self, pk):
      return self.queryset.get(id=pk)

   def get(self, request, taxa_id, format="json"):
      tax = Taxonomy.objects.get(taxa_id=taxa_id)

      relationList = ProteinTaxonomyLink.objects.filter(taxonomy=tax)
      proteins = []
      for relation in relationList:
         proteins.append(self.get_object(relation.protein.id))
      serializer = ProteinsSerializer(proteins, many=True)
      return Response(serializer.data)
