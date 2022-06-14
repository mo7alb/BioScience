from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .models import *

class ProteinList(APIView):
   def get(self, request, format="json"):
      proteins = Protein.objects.all()
      serializer = ProteinSerializer(proteins, many=True)
      return Response(serializer.data)