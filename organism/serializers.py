from pyexpat import model
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
      fields = ['id', 'description', 'start_coordinate','end_coordinate', 'pfam']

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
   
   def create(self, validated_data):
      taxonmy_data = self.initial_data.get('taxonomy')
      domains_data = self.initial_data.get('domains')
      
      pro = Protein(
         protein_id=validated_data['protein_id'],
         sequence=validated_data['sequence'],
         length=validated_data['length'],
      )

      pro.save()

      for tax in taxonmy_data:
         pro.taxonomy.add(Taxonomy.objects.get(id=tax['id']))
      
      for domain in domains_data:
         pro.domains.add(Domain.objects.get(id=domain['id']))

      return pro

class ProteinsListSerializer(serializers.ModelSerializer):
   class Meta:
      model = Protein
      fields = ["id", "protein_id"]

class PfamListSerializer (serializers.ModelSerializer):
   pfam = PfamSerializer()
   class Meta:
      model = Domain
      fields = ['id', 'pfam']

class CoverageSerializer(serializers.ModelSerializer):
   class Meta:
      model = Domain
      fields = ["start_coordinate", "end_coordinate"]