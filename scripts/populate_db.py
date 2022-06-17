from itertools import count
import os
import sys
from typing import Dict
import django
import csv
from collections import defaultdict

sys.path.append('/Users/mohammadmahboob/Studies/Adv Web dev/bioscience/bioscience')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioscience.settings')
django.setup()

from organism.models import *

# list of csv files that contain protein data
data_files = [
   "/Users/mohammadmahboob/Studies/Adv Web dev/bioscience/assignment_data_sequences.csv",
   "/Users/mohammadmahboob/Studies/Adv Web dev/bioscience/assignment_data_set.csv",
   "/Users/mohammadmahboob/Studies/Adv Web dev/bioscience/pfam_descriptions.csv"
]

"""
   a set to store pfam data
   data within the set is of the format 
   {(domain_id, pfam_description), (domain_id, pfam_description)}
"""
pfams = set()

"""
   a dict containing domains and their related data
   data is of the format 
   {'domain_id': ['description', 'start_coordinate', 'end_coordinate']}
"""
domains = defaultdict(list)

"""
   a set to store protein sequences
   data within the set is of the format 
   {(protein_id, sequence), (protein_id, sequence)}
"""
sequences = set()

"""
   a dict containing proteins and their length
   data is of the format {'protein_id': 'length', 'protein_id': 'length'}
"""
proteins = {}

"""
   a dict containing organisms and their related data
   data is of the format {'taxa_id': ['clade_idenitifier', 'scientific_name']}
"""
taxonomy = defaultdict(list)

"""
   a set that describes the relationship between Domain and Protein
   data is of the format {(protein_id, domain_id)}
"""
protein_domain = set()

"""
   a set that describes the relationship between Taxonomy and Protein
   data is of the format {(protein_id, taxa_id)}
"""
protein_taxonomy = set()


# open assignment_data_sequence.csv file
with open(data_files[0]) as protein_sequence:
   csv_reader = csv.reader(protein_sequence, delimiter=",")
   # iterate over the lines of the csv file 
   for row in csv_reader:
      if row[1] == '':
         print("Invalid row data")
         continue

      # save instance of each row to the sequence set
      sequences.add((row[0],  row[1]))

# open assignment_data_set.csv file
with open(data_files[1]) as data_set:
   csv_reader = csv.reader(data_set)
   # iterate over the lines of the csv file 
   for row in csv_reader:
      # add data to specific data set
      proteins[row[0]] = row[-1]
      
      domain = []
      for index in [4, 6, 7]:
         domain.append(row[index])
      
      domains[row[5]] = domain

      taxonomy[row[1]] = row[2:4]

      protein_taxonomy.add((row[0], row[1]))
      protein_domain.add((row[0], row[5]))

# open pfam_descriptions.csv file 
with open(data_files[2]) as pfam_data:
   csv_reader = csv.reader(pfam_data, delimiter=",")
   # iterate over the lines of the csv file 
   for row in csv_reader:
      # add each row to the pfams set
      pfams.add((row[0], row[1]))

print("successfully retrived data from the csv files")

Pfam.objects.all().delete()
Domain.objects.all().delete()
ProteinTaxonomyLink.objects.all().delete()
ProteinDomainLink.objects.all().delete()
Protein.objects.all().delete()
Taxonomy.objects.all().delete()

print("successfully cleared data from the database")

pfam_rows = {}
domain_rows = {}
protein_rows = {}
taxonomy_rows = {}

"""
   add pfam data from the csv data file to the database
"""
for data in pfams:
   row = Pfam.objects.create(domain_id=data[0],domain_description=data[1])
   row.save()
   pfam_rows[data[0]] = row
print("Successfully added data to the Pfam table")

"""
   add domain data from the csv data file to the database
"""
for (domain_id, domain_data) in domains.items():
   row = Domain.objects.create(
      domain_id=domain_id, 
      description=domain_data[0], 
      start_coordinate=domain_data[1],
      end_coordinate=domain_data[2],
      pfam=pfam_rows[domain_id]
   )
   row.save()

   domain_rows[domain_id] = row
print("Successfully added data to the domain table")

# add all proteins to the db
for (protein_id, sequence) in sequences:
   row = Protein.objects.create(
      protein_id = protein_id,
      sequence = sequence,
      length = proteins[protein_id],
   )

   row.save()
   protein_rows[protein_id] = row

print("successfully added protein data to the database")

# add all Taxonomy to the db
for (taxa_id, organism_data) in taxonomy.items():
   scientific_name = organism_data[1].split(" ")

   if len(scientific_name) == 2:
      genus = scientific_name[0]
      species = scientific_name[1]
   else:
      contains_period = False
      for string in scientific_name:
         if string.endswith("."):
            contains_period = True
            index = scientific_name.index(string)
            genus = " ".join(scientific_name[0: index + 1])
            species = " ".join(scientific_name[index + 1:])
            break
      
      if contains_period == False:
         genus = scientific_name[0]
         species = " ".join(scientific_name[1:])
      
   row = Taxonomy.objects.create(
      taxa_id=taxa_id,
      clade = organism_data[0],
      genus=genus,
      species=species,
   )

   row.save()

   taxonomy_rows[taxa_id] = row
print("successfully added taxonomy data to the database")


# add all protein and domain links to the db
for (protein_id, domain_id) in protein_domain:
   if not protein_id in protein_rows:
      continue
   
   if not domain_id in domain_rows:
      continue

   relation = ProteinDomainLink.objects.create(
      protein=protein_rows[protein_id],
      domain=domain_rows[domain_id]
   )
   
   relation.save()

for (protein_id, taxa_id) in protein_taxonomy:
   if not protein_id in protein_rows:
      continue
   
   if not taxa_id in taxonomy_rows:
      continue

   relation = ProteinTaxonomyLink.objects.create(
      taxonomy=taxonomy_rows[taxa_id],
      protein=protein_rows[protein_id]
   )
   relation.save()

print("successfully added relations to the database")