from pyexpat import model
from django.db import models

class Pfam(models.Model):
   domain_id = models.CharField(primary_key=True, blank=False, null=False, max_length=8)
   domain_description = models.CharField(blank=False, null=False, max_length=200)

class Domain(models.Model):
   description = models.CharField(null=False, blank=False, max_length=200)
   start_coordinate = models.IntegerField(null=False, blank=False)
   end_coordinate = models.IntegerField(null=False, blank=False)
   pfam = models.ForeignKey(Pfam, on_delete=models.CASCADE)

   def __str__(self) -> str: 
      return self.description

class Taxonomy(models.Model):
   taxa_id = models.IntegerField(blank=False, null=False)
   clade = models.CharField(max_length=1, null=False, blank=False, default='E')
   genus = models.CharField(max_length=40, null=False, blank=False)
   species = models.CharField(max_length=40, null=False, blank=False)

   def __str__(self) -> str:
      return "{0} : {1}".format(self.genus, self.species)

class Protein(models.Model):
   protein_id = models.CharField(max_length=11, primary_key=True, null=False, blank=False)
   sequence = models.CharField(null=False, blank=False, max_length=32760)
   length = models.IntegerField(null=False, blank=False)
   domains = models.ManyToManyField(Domain, through="ProteinDomainLink")
   taxonomy = models.ManyToManyField(Taxonomy, through='ProteinTaxonomyLink')
   def __str__(self) -> str:
      return self.protein_id

class ProteinDomainLink(models.Model):
   domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
   protein = models.ForeignKey(Protein, on_delete=models.CASCADE)

class ProteinTaxonomyLink(models.Model):
   taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE)
   protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
