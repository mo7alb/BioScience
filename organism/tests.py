# import important packages
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json

# import model factories
from .model_factories import * 

# import serializers
from .serializers import *

class TestProteinDetailRoute (APITestCase):
   """
      test API route api/protein/<str:protein_id>
   """
   # protein to be used in the test
   protein = None
   # a good url to request data from
   good_url = ''
   # a bad url to throw an error
   bad_url = ''

   def setUp(self) -> None:
      """
         function to set up the test enviornment and avoid repetition of code
      """

      # create two new proteins
      self.protein = ProteinFactory.create(pk=1, protein_id="A0A016S8J7")
      # construct a good url based on the api route named protein_details
      self.good_url = reverse('protein_details', kwargs={'protein_id': self.protein.protein_id})
      # construct a bad url
      self.bad_url = "/api/protien/A1B2"

   def tearDown(self) -> None:
      """
         function to set the test enviornment as it was before running the tests
      """
      Protein.objects.all().delete()
      ProteinFactory.reset_sequence(0)

   def test_protein_details_return_success(self) -> None:
      """
         test api route /api/protein/<str:protein_id> to return a status code of 200
      """
      # send a get request to the url set above
      response = self.client.get(self.good_url)

      # assert if the status code of the response is 200
      self.assertEqual(response.status_code, status.HTTP_200_OK) 
   
   def test_protein_details_return_fail(self) -> None:
      """
         test api route /api/protein/<str:protein_id> to return a status code of 
         404 upon a bad request
      """
      # send a get request to the url set above
      response = self.client.get(self.bad_url)

      # assert if the status code of the response is 404
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   
   def test_protein_details_return_correct_data(self) -> None:
      """
         test api route /api/protein/<str:protein_id> to return the correct protein sequence 
      """
      # send a get request to the url set above
      response = self.client.get(self.good_url)

      # load the json data from the response
      data = json.loads(response.content)

      # assert if the status code of the response is 200
      self.assertEqual(data['sequence'], self.protein.sequence)

class TestPfamDetailRoute (APITestCase):
   """
      test API route api/pfam/<str:pfam_id>
   """

   # pfam attribute to store a Pfam class instance 
   pfam = None
   # a good api route to request data from
   good_url = ""
   # a bad api route that is to throw an error
   bad_url = ""

   def setUp(self) -> None:
      """
         function to set up the test enviornment and avoid repetition of code
      """
      # create a new pfam
      self.pfam = PfamFactory.create(pk=1, domain_id="PF01650")
      # create a good url
      self.good_url = reverse('pfam_details', kwargs={'pfam_id': self.pfam.domain_id})
      # create a bad url
      self.bad_url = 'api/pfam/A1B2C3'

   def tearDown(self) -> None:
      """
         function to set the test enviornment as it was before running the tests
      """

      Pfam.objects.all().delete()
      PfamFactory.reset_sequence(0)

   def test_pfam_details_return_fails(self) -> None:
      """
         test if api route returns a 404 status code on passing a wrong id
      """
      
      # send a get request to the bad url set in the set up function
      response = self.client.get(self.bad_url)

      # assert if status code of the response is 404
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_pfam_details_return_success(self) -> None:
      """
         test if api route returns a 200 status code on passing a 
         working id
      """
      
      # send a get request to the bad url set in the set up function
      response = self.client.get(self.good_url)

      # assert if status code of the response is 200
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   
   def test_pfam_details_return_correct_data(self) -> None:
      """
         test api route to return the correct pfam description 
      """
      # send a get request to the url set above
      response = self.client.get(self.good_url)

      # load the json data from the response
      data = json.loads(response.content)

      # assert if the status code of the response is 200
      self.assertEqual(data['domain_description'], self.pfam.domain_description)

class TestProteinListRoute (APITestCase):
   """
      test API route api/proteins/<ind:taxa_id>
   """

   # organism to which all proteins are to be related
   taxonomy = None
   # proteins to be returned by the api route
   protein1 = None
   protein2 = None
   # a url to request the data from
   good_url = ""
   # a url that is throw an error
   bad_url = ""

   def setUp(self) -> None:
      """
         function to set up the test enviornment and avoid repetition of code
      """
      # create a new organism
      self.taxonomy = TaxonomyFactory.create(pk=1, taxa_id=55661)

      # create 2 new proteins
      self.protein1 = ProteinFactory.create(pk=1, protein_id="A0A016S8J7")
      self.protein2 = ProteinFactory.create(pk=2, protein_id="A0A016S8J8")

      # add a relation between the proteins and the organism
      self.protein1.taxonomy.add(self.taxonomy)
      self.protein2.taxonomy.add(self.taxonomy)

      self.good_url = reverse("protein_list", kwargs={ 'taxa_id': self.taxonomy.taxa_id })
      self.bad_url = "/api/proteins/12255"

   def tearDown(self) -> None:
      """
         function to set the test enviornment as it was before running the tests
      """
      Taxonomy.objects.all().delete()
      Protein.objects.all().delete()
      ProteinFactory.reset_sequence(0)
      TaxonomyFactory.reset_sequence(0)

   def test_proteins_list_return_success(self) -> None:
      """
         test api route /api/proteins/<int:taxa_id> to return a status code of 
         200 upon a good request
      """
      # send a get request
      response = self.client.get(self.good_url)

      # assert if the status code is 200 
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_protein_list_return_correct_data(self) -> None:
      """
         test api route /api/proteins/<int:taxa_id> to return the correct data 
      """
      # send a get request to the good url
      response = self.client.get(self.good_url)

      # load the json data from the response
      data = json.loads(response.content)

      # assert if the status code of the response is 200
      self.assertEqual(data, [ 
         {'id': self.protein1.id, 'protein_id': self.protein1.protein_id },
         {'id': self.protein2.id, 'protein_id': self.protein2.protein_id },
      ])
   
   def test_protein_list_return_fails(self) -> None:
      """
         test api route to return a status code of 404 upon a bad request
      """
      # send a get request to the bad url
      response = self.client.get(self.bad_url)

      # assert if the status code is  404
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestPfamListRoute (APITestCase):
   """
      test API route api/pfams/<ind:taxa_id>
   """

   # organism to which all proteins are to be related
   taxonomy = None
   
   # proteins to be returned by the api route
   protein1 = None
   protein2 = None

   # create domains to be linked to the proteins
   domain1 = None
   domain2 = None
   
   # create pfams to be returned
   pfam1 = None
   pfam2 = None

   # a url to request the data from
   good_url = ""
   # a url that is throw an error
   bad_url = ""

   def setUp(self) -> None:
      """
         function to set up the test enviornment and avoid repetition of code
      """
      # create a new organism
      self.taxonomy = TaxonomyFactory.create(pk=1, taxa_id=55661)

      # create 2 new proteins
      self.protein1 = ProteinFactory.create(pk=1, protein_id="A0A016S8J7")
      self.protein2 = ProteinFactory.create(pk=2, protein_id="A0A016S8J8")

      # add a relation between the proteins and the organism
      self.protein1.taxonomy.add(self.taxonomy)
      self.protein2.taxonomy.add(self.taxonomy)

      # create 2 fams 
      self.pfam1 = PfamFactory.create(pk=1)
      self.pfam2 = PfamFactory.create(pk=2)

      # create 2 new domains
      self.domain1 = DomainFactory(pk=1, domain_id="PF00307")
      self.domain2 = DomainFactory(pk=2, domain_id="PF00308")

      # link pfams to the domains
      self.domain1.pfam = self.pfam2
      self.domain2.pfam = self.pfam1

      # link domains to the proteins
      self.protein1.domains.add(self.domain2)
      self.protein2.domains.add(self.domain1)

      self.good_url = reverse("pfam_list", kwargs={ 'taxa_id': self.taxonomy.taxa_id })
      self.bad_url = "/api/proteins/12255"

   def tearDown(self) -> None:
      """
         function to set the test enviornment as it was before running the tests
      """
      Pfam.objects.all().delete()
      Domain.objects.all().delete()
      Taxonomy.objects.all().delete()
      Protein.objects.all().delete()
      ProteinFactory.reset_sequence(0)
      TaxonomyFactory.reset_sequence(0)
      DomainFactory.reset_sequence(0)
      PfamFactory.reset_sequence(0)

   def test_pfams_list_return_success(self) -> None:
      """
         test api route /api/pfams/<int:taxa_id> to return a status code of 
         200 upon a good request
      """
      # send a get request
      response = self.client.get(self.good_url)

      # assert if the status code is 200 
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_pfams_list_return_correct_data(self) -> None:
      """
         test api route /api/pfams/<int:taxa_id> to return the correct data 
      """
      # send a get request to the good url
      response = self.client.get(self.good_url)

      # load the json data from the response
      data = json.loads(response.content)

      # the data to compare the response data to
      test_data = [
         {
            'id': self.protein2.pk,
            'pfam': {
               # this domain id is the set in model_factories.py file
               'domain_id': "PF01650",
               # this domain description is the set in model_factories.py file
               'domain_description': "PeptidaseC13family"
            }
         },
         {
            'id': self.protein1.pk,
            'pfam': {
               # this domain id is the set in model_factories.py file
               'domain_id': "PF01650",
               # this domain description is the set in model_factories.py file
               'domain_description': "PeptidaseC13family"
            }
         }
      ]

      # # assert if the status code of the response is 200
      self.assertEqual(data, test_data)
   
   def test_pfam_list_return_fails(self) -> None:
      """
         test api route to return a status code of 404 upon a bad request
      """
      # send a get request to the bad url
      response = self.client.get(self.bad_url)

      # assert if the status code is  404
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestCoverageRoute (APITestCase):
   """
      test API route api/coverage/<str:protein_id>
   """

   # organism to which all proteins are to be related
   taxonomy = None
   
   # proteins to be returned by the api route
   protein = None

   # create domains to be linked to the proteins
   domain = None
   
   # create pfams to be returned
   pfam = None

   # a url to request the data from
   good_url = ""
   # a url that is throw an error
   bad_url = ""

   def setUp(self) -> None:
      """
         function to set up the test enviornment and avoid repetition of code
      """
      # create a new organism
      self.taxonomy = TaxonomyFactory.create(pk=1, taxa_id=55661)
      
      # create a new fams 
      self.pfam = PfamFactory.create(pk=1)

      # create a new domain
      self.domain = DomainFactory(pk=1, domain_id="PF00307")
      # link pfam to the domain
      self.domain.pfam = self.pfam

      # create a new protein
      self.protein = ProteinFactory.create(pk=1, protein_id="A0A016S8J7")
      # add a relation between the protein and the organism
      self.protein.taxonomy.add(self.taxonomy)
      # link domains to the proteins
      self.protein.domains.add(self.domain)

      self.good_url = reverse("protein_coverage", kwargs={"protein_id": self.protein.protein_id})
      self.bad_url = "/api/coverge/A1B2"

   def tearDown(self) -> None:
      """
         function to set the test enviornment as it was before running the tests
      """
      Pfam.objects.all().delete()
      Domain.objects.all().delete()
      Taxonomy.objects.all().delete()
      Protein.objects.all().delete()
      ProteinFactory.reset_sequence(0)
      TaxonomyFactory.reset_sequence(0)
      DomainFactory.reset_sequence(0)
      PfamFactory.reset_sequence(0)

   def test_coverage_returns_success(self) -> None:
      """
         test if the api route returns a 200 status code for
         a good url path
      """
      # make a get request
      response = self.client.get(self.good_url)

      # assert for the status code
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_coverage_returns_fail(self) -> None:
      """
         test if the api route returns a 404 error if 
         a bad url is requested
      """
      # make a get request
      response = self.client.get(self.bad_url)

      # assert for the status code
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   
   def test_coverage_returns_correct_data(self) -> None:
      """
         test if the coverage returned has a correct value
      """
      # make a get request to the good url
      response = self.client.get(self.good_url)

      # load the json response 
      data = json.loads(response.content)

      # coverage to be compared against
      test_coverage = (self.domain.end_coordinate - self.domain.start_coordinate) / self.protein.length

      self.assertEqual(data['coverage'], test_coverage)

class TestNewProteinRoute (APITestCase):
   """
      testing adding new protein route 
      api route: /api/protein 
      method: GET
   """
   url = ""
   data = None
   bad_data = None

   def setUp(self) -> None:
      """
         function to set up the test enviornment and avoid repetition of code
      """
      # url to perform the post request to
      self.url = reverse('new_protein')

      # define a dictionary holding valid protein data
      self.data = {
         "protein_id": "A0A016S8J7",
         "sequence": "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA",
         "length": 101,
         "taxonomy": [],
         "domains": []
      }
      
      # define a dictionary holding invalid protein data
      self.bad_data = {
         "protein_id": "A0A016S8J7",
         "sequence": "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA",
         "domains": []
      }

   def tearDown(self) -> None:
      """
         function to set the test enviornment as it was before running the tests
      """
      Protein.objects.all().delete()

   def test_adding_new_protein(self) -> None:
      """
         test if adding adding a new protein returns a status code 
         of 201
      """
      # make a post request
      response = self.client.post(self.url, data=self.data, format="json")
      
      # check if status code return is 201
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_adding_new_protein_return_correct_data(self) -> None:
      """
         test if adding a new protein returns the correct data
      """
      # make a post request
      response = self.client.post(self.url, data=self.data, format="json")
      
      # load the json data from the response
      response_data = json.loads(response.content)

      # assert if the returned data contains the same sequence as the data
      self.assertEqual(response_data['sequence'], self.data['sequence'])
   
   def test_adding_new_protein_fails_with_bad_data(self) -> None:
      """
         check if the api route returns a 400 error if invalid data is passed to it
      """
      # make a post request
      response = self.client.post(self.url, data=self.bad_data)

      # check if the response status code is 400
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestProteinSerializer(APITestCase):
   """
      test the protein serializer
   """
   protein = None
   protein_serializer = None
   
   def setUp(self) -> None:
      """
         set up common variables used by tests to reduce code repition
      """
      # create a new protein
      self.protein = ProteinFactory.create(pk=1, protein_id="A0A016S8J7")
      # pass the protein to the serializer
      self.protein_serializer = ProteinSerializer(self.protein)
   
   def tearDown(self) -> None:
      """
         rest the testing enviornment back to the orignal state
      """
      Protein.objects.all().delete()
      ProteinFactory.reset_sequence(0)
   
   def test_protein_serializer_returns_keys(self) -> None:
      """
         check if the protein serializer returns the correct keys
      """
      data = self.protein_serializer.data
      keys_expected = ['id', 'domains', 'taxonomy', 'protein_id', 'sequence', 'length']

      self.assertEqual(set(data.keys()), set(keys_expected))

   def test_protein_serializer_returns_correct_data(self) -> None:
      """
         check if the data returned from the protein serializer is correct
      """
      # create a variable for the serializer data
      data = self.protein_serializer.data

      # assert if both have same protein sequence
      self.assertEqual(data['sequence'], self.protein.sequence)

class TestPfamSerializer(APITestCase):
   """
      test the pfam serializer
   """
   pfam = None
   pfam_serializer = None

   def setUp(self) -> None:
      """
         set up common variables used by tests to reduce code repition
      """
      # create a new pfam
      self.pfam = PfamFactory.create(pk=1)
      # pass the pfam to the pfam serializer
      self.pfam_serializer = PfamSerializer(self.pfam)
   
   def tearDown(self) -> None:
      """
         rest the testing enviornment back to the orignal state
      """
      Pfam.objects.all().delete()
      PfamFactory.reset_sequence(0)

   def test_pfam_serializer_returns_keys(self) -> None:
      """
         test if the serializer returns the correct keys
      """
      # get the serializer data
      data = self.pfam_serializer.data

      # list of keys expected
      expected_keys = ['domain_id', 'domain_description']

      # assert if keys are equal to expected keys
      self.assertEqual(set(data.keys()), set(expected_keys))

   def test_pfam_serializer_returns_correct_data(self) -> None:
      """
         test if the pfam serializer returns the correct data
      """
      # get the serializer data
      data = self.pfam_serializer.data

      # assert if data and pfam have the same description
      self.assertEqual(data['domain_description'], self.pfam.domain_description)

class TestProteinsListSerializer(APITestCase):
   """
      test the ProteinsList serializer
   """
   protein = None
   protein_serializer = None
   
   def setUp(self) -> None:
      """
         set up common variables used by tests to reduce code repition
      """
      # create a new protein
      self.protein = ProteinFactory.create(pk=1, protein_id="A0A016S8J7")
      # pass the protein to the serializer
      self.protein_serializer = ProteinsListSerializer(self.protein)

   def tearDown(self) -> None:
      """
         rest the testing enviornment back to the orignal state
      """
      Protein.objects.all().delete()
      ProteinFactory.reset_sequence(0)

   def test_protein_list_serializer_returns_keys(self) -> None:
      """
         check if the protein list serializer returns the correct keys
      """
      data = self.protein_serializer.data
      keys_expected = ['id', 'protein_id']

      self.assertEqual(set(data.keys()), set(keys_expected))

   def test_protein_list_serializer_returns_correct_data(self) -> None:
      """
         check if the data returned from the protein list serializer is correct
      """
      # create a variable for the serializer data
      data = self.protein_serializer.data

      # assert if both have same protein sequence
      self.assertEqual(data['protein_id'], self.protein.protein_id)

class TestPfamListSerializer(APITestCase):
   """
      test the PfamList serializer
   """
   pfam = None
   pfam_serializer = None

   def setUp(self) -> None:
      """
         set up common variables used by tests to reduce code repition
      """
      # create a new pfam
      self.pfam = PfamFactory.create(pk=1)
      # pass the pfam to the pfam serializer
      self.pfam_serializer = PfamSerializer(self.pfam)
   
   def tearDown(self) -> None:
      """
         reset the testing enviornment back to the orignal state
      """
      Pfam.objects.all().delete()
      PfamFactory.reset_sequence(0)
   
   def test_pfam_list_serializer_returns_keys(self) -> None:
      """
         test if the pfam list serializer returns the correct keys
      """
      # get the serializer data
      data = self.pfam_serializer.data

      # list of keys expected
      expected_keys = ['domain_id', 'domain_description']

      # assert if keys are equal to expected keys
      self.assertEqual(set(data.keys()), set(expected_keys))

   def test_pfam_list_serializer_returns_correct_data(self) -> None:
      """
         test if the pfam serializer returns the correct data
      """
      # get the serializer data
      data = self.pfam_serializer.data

      # assert if data and pfam have the same description
      self.assertEqual(data['domain_description'], self.pfam.domain_description)

class TestCoverageListSerializer(APITestCase):
   """
      test the PfamList serializer
   """
   domain = None
   domain_serializer = None

   def setUp(self) -> None:
      """
         set up common variables used by tests to reduce code repition
      """
      # create a new domain
      self.domain = DomainFactory.create(pk=1)
      # pass the domain the coverage serializer
      self.domain_serializer = CoverageSerializer(self.domain)
   
   def tearDown(self) -> None:
      """
         reset the testing enviornment back to the orignal state
      """
      Domain.objects.all().delete()
      DomainFactory.reset_sequence(0)

   def test_coverage_serializer_returns_keys(self) -> None:
      """
         test if the coverage serializer returns right keys
      """
      # serializer returned data
      data = self.domain_serializer.data

      # expected keys
      expected_keys = ['start_coordinate', 'end_coordinate']

      # assert to check if all the keys are the same
      self.assertEqual(set(data.keys()), set(expected_keys))

   def test_coverage_serializer_returns_correct_start(self) -> None:
      """
         test if the start coordinate value returned from the 
         serializer is accurate
      """

      # serializer returned data
      data = self.domain_serializer.data

      # assert to check if the start coordinates are equal
      self.assertEqual(data['start_coordinate'], self.domain.start_coordinate)
   
   def test_coverage_serializer_returns_correct_end(self) -> None:
      """
         test if the start coordinate value returned from the 
         serializer is accurate
      """
      # serializer returned data
      data = self.domain_serializer.data

      # assert to check if the end coordinates are equal
      self.assertEqual(data['end_coordinate'], self.domain.end_coordinate)
