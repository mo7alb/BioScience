# import important packages
import factory

# import models 
from .models import *

class PfamFactory(factory.django.DjangoModelFactory):
   """
      fixture to the Pfam table
   """
   domain_id = "PF01650"
   domain_description = "PeptidaseC13family"

   class Meta:
      """
         specify which model the Pfam factory is attached to
      """
      model = Pfam

class DomainFactory(factory.django.DjangoModelFactory):
   """
      fixture to the Domain table
   """
   domain_id = "PF01650"
   description = "Peptidase C13 legumain"
   start_coordinate = 40
   end_coordinate = 94
   pfam = factory.SubFactory(PfamFactory)

   class Meta:
      """
         specify which model the Domain fixture is attached to
      """
      model = Domain


class TaxonomyFactory(factory.django.DjangoModelFactory):
   """
      fixture to the Taxonomy table
   """
   taxa_id = 53326
   clade = "E"
   genus = "Ancylostoma"
   species = "ceylanicum"

   class Meta:
      """
         specify which model the Taxonomy fixture is attached to
      """
      model = Taxonomy

class ProteinFactory(factory.django.DjangoModelFactory):
   """
      fixture to the Protein table
   """
   protein_id = "A0A016S8J7"
   sequence = "VLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA"
   length = 100

   class Meta:
      """
      determine which model the Protein factory is attached to 
      """
      model = Protein