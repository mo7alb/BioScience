from .models import *
from rest_framework import serializers

class PfamSerializer(serializers.ModelSerializer):
   """
   serializer class for the pfam model allowing the API to
   return a single pfam related data
   """
   class Meta:
      """
      class that describes meta data of the parent class
      
      ...

      Attributes
      ----------
      model: class
         model class from which the data is to be fetched
      
      fields: list
         list of fields that are to be included in the fetch
      """
      model = Pfam
      fields = ['domain_id', 'domain_description']

class DomainSerializer(serializers.ModelSerializer):
   """
   serializer class for the domain model allowing the API to
   return a single domain related data

   ...

   Attributes
   ----------
   pfam: class
      serializer class for the foreign key pfam
   """
   pfam = PfamSerializer()
   class Meta:
      """
      class that describes meta data of the parent class
      
      ...

      Attributes
      ----------
      model: class
         model class from which the data is to be fetched
      
      fields: list
         list of fields that are to be included in the fetch
      """
      model = Domain
      fields = ['id', 'description', 'start_coordinate','end_coordinate', 'pfam']

class TaxonomySerializer(serializers.ModelSerializer):
   """
   serializer class for the Taxonomy model allowing the API to
   return a organism related data
   """
   class Meta:
      """
      class that describes meta data of the parent class
      
      ...

      Attributes
      ----------
      model: class
         model class from which the data is to be fetched
      
      fields: list
         list of fields that are to be included in the fetch
      """
      model = Taxonomy
      fields = '__all__'

class ProteinSerializer(serializers.ModelSerializer):
   """
   serializer class for the Protein model allowing the API to
   return a single protein related data

   ...

   Attributes
   ----------
   domains: class
      serializer class for the many to many relation between Protein and Domains
   taxonomy: class
      serializer class for the many to many relation between Protein and Taxonomy
   
   ... 

   methods
   -------
   create(validated_data):
      method to create a new protein and save it in the database
   """
   domains = DomainSerializer(many=True)
   taxonomy = TaxonomySerializer(many=True)
   class Meta:
      """
      class that describes meta data of the parent class
      
      ...

      Attributes
      ----------
      model: class
         model class from which the data is to be fetched
      
      fields: list
         list of fields that are to be included in the fetch
      """
      model = Protein
      fields = '__all__'
   
   def create(self, validated_data) -> Protein:
      # get list of organisms
      taxonmy_data = self.initial_data.get('taxonomy')
      # get list of domains
      domains_data = self.initial_data.get('domains')
      
      # creates a new protein
      pro = Protein(
         protein_id=validated_data['protein_id'],
         sequence=validated_data['sequence'],
         length=validated_data['length'],
      )
      # saves the protein to the database
      pro.save()

      # iterates over the list of organisms and addes a relation between 
      # them and the protein
      for tax in taxonmy_data:
         pro.taxonomy.add(Taxonomy.objects.get(id=tax['id']))
      
      # iterates over the list of organisms and addes a relation
      # between them and the protein
      for domain in domains_data:
         pro.domains.add(Domain.objects.get(domain_id=domain['id']))

      # return the newly created protein
      return pro

class ProteinsListSerializer(serializers.ModelSerializer):
   """
   serializer class for the Protein model allowing the API to
   return a list of proteins that are related to an organism
   """
   class Meta:
      model = Protein
      fields = ["id", "protein_id"]

class PfamListSerializer (serializers.ModelSerializer):
   """
   serializer class for the Pfam model allowing the API to
   return a list of pfams that are related to an organism
   """
   pfam = PfamSerializer()
   class Meta:
      """
      class that describes meta data of the parent class
      
      ...

      Attributes
      ----------
      model: class
         model class from which the data is to be fetched
      
      fields: list
         list of fields that are to be included in the fetch
      """
      model = Domain
      fields = ['id', 'pfam']

class CoverageSerializer(serializers.ModelSerializer):
   """
   serializer class for the Protein model allowing the API to
   return the coverage of a protein
   """
   class Meta:
      """
      class that describes meta data of the parent class
      
      ...

      Attributes
      ----------
      model: class
         model class from which the data is to be fetched
      
      fields: list
         list of fields that are to be included in the fetch
      """
      model = Domain
      fields = ["start_coordinate", "end_coordinate"]