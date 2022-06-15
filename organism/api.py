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

   def post (self, request, format="json"):
      serializer = ProteinSerializer(data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)