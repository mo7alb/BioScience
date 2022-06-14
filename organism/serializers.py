from .models import *
from rest_framework import serializers

class ProteinSerializer(serializers.ModelSerializer):
   class Meta:
      model = Protein
      fields = '__all__'