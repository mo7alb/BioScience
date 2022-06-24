from django.db import models

class Pfam(models.Model):
   """
   model class that represents as a table for the pfam data in the database

   ... 

   Attributes
   ----------
   domain_id: str
      represents the id of the domain
   
   domain_description: str
      represents a breif description of the domain
   
   ...

   methods
   -------
   __str__() 
      returns the domain description as a string
   """

   domain_id = models.CharField(null=False, max_length=15, default="")
   domain_description = models.CharField(blank=False, null=False, max_length=200)
   
   def __str__(self) -> str:
      return self.pfam_description

class Domain(models.Model):
   """
   model class that represents as a table for the domain data in the database

   ... 

   Attributes
   ----------
   domain_id: str
      represents the id of the domain
   
   description: str
      represents a breif description of the domain
   
   start_coordinate: int
      a integer that represents when the domain starts
   
   end_coordinate: int
      a integer that represents when the domain ends
   
   pfam: class
      represents a foreign key relation between Domain table and Pfam table

   ...

   methods
   -------
   __str__() 
      returns the domain description as a string
   """
   domain_id = models.CharField(null=False, max_length=10, default="")
   description = models.CharField(null=False, blank=False, max_length=200)
   start_coordinate = models.IntegerField(null=False, blank=False)
   end_coordinate = models.IntegerField(null=False, blank=False)
   pfam = models.ForeignKey(Pfam, on_delete=models.CASCADE)

   def __str__(self) -> str: 
      return self.description

class Taxonomy(models.Model):
   """
   model class that represents as a table for the organism data in the database

   ... 

   Attributes
   ----------
   taxa_id: int
      represents the id of the organism
   
   clade: str
      represents organims clade
   
   genus: str
      represents organism genus
   
   species: str
      represents organism species
   
   ...

   methods
   -------
   __str__() 
      returns the organism genus and species as a string
   """
   taxa_id = models.IntegerField(blank=False, null=False, default="")
   clade = models.CharField(max_length=1, null=False, blank=False, default='E')
   genus = models.CharField(max_length=40, null=False, blank=False)
   species = models.CharField(max_length=40, null=False, blank=False)

   def __str__(self) -> str:
      return "{0} : {1}".format(self.genus, self.species)

class Protein(models.Model):
   """
   model class that represents as a table for the protein data in the database

   ... 

   Attributes
   ----------
   protein_id: str
      represents the id of the protein
   
   sequence: str
      represents sequence of the protein
   
   length: int
      represents the length of the protein
   
   domains: 
      represents a many to many relation between the protein and the domain
   
   taxonomy: 
      represents a many to many relation between the protein and the organisms
   
   ...

   methods
   -------
   __str__() 
      returns the protein id as a string
   """
   protein_id = models.CharField(max_length=11, null=False, blank=False, default="")
   sequence = models.CharField(null=False, blank=False, max_length=32760)
   length = models.IntegerField(null=False, blank=False)
   domains = models.ManyToManyField(Domain, through="ProteinDomainLink")
   taxonomy = models.ManyToManyField(Taxonomy, through='ProteinTaxonomyLink')
   
   def __str__(self) -> str:
      return self.protein_id

class ProteinDomainLink(models.Model):
   """
   model class that represents as a table for the protein and domain relation in the database

   ... 

   Attributes
   ----------
   protein: 
      the protein that relationship represents
   
   domain: 
      the domain that relationship represents
   """
   domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
   protein = models.ForeignKey(Protein, on_delete=models.CASCADE)

class ProteinTaxonomyLink(models.Model):
   """
   model class that represents as a table for the protein and organism relation in the database

   ... 

   Attributes
   ----------
   protein: 
      the protein that relationship represents
   
   taxonomy: 
      the organism that relationship represents
   """
   taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE)
   protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
