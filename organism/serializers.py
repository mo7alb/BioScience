from .models import *
from rest_framework import serializers

class PfamSerializer(serializers.ModelSerializer):
   class Meta:
      model = Pfam
      fields = '__all__'

class DomainSerializer(serializers.ModelSerializer):
   pfam = PfamSerializer()
   class Meta:
      model = Domain
      fields = '__all__'

class TaxonomySerializer(serializers.ModelSerializer):
   class Meta:
      model = Taxonomy
      fields = '__all__'

class ProteinSerializer(serializers.ModelSerializer):
   domains = DomainSerializer(many=True)
   taxonomy = TaxonomySerializer(many=True)
   class Meta:
      model = Protein
      fields = '__all__'