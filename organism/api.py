from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import *
from .models import *

class Protein(GenericAPIView):
   queryset = Protein.objects.all()

   def get(self, request, protein_id, format="json"):
      protein = Protein.objects.filter(protein_id=protein_id)
      serializer = ProteinSerializer(protein, many=True)
      return Response(serializer.data)