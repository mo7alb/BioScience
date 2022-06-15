from .models import *
from rest_framework import serializers

class PfamSerializer(serializers.ModelSerializer):
   class Meta:
      model = Pfam
      fields = ['domain_id', 'domain_description']

class DomainSerializer(serializers.ModelSerializer):
   pfam = PfamSerializer()
   class Meta:
      model = Domain
      fields = ['description', 'start_coordinate','end_coordinate', 'pfam']

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