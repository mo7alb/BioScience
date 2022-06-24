from django.shortcuts import render
from .models import Taxonomy
from django.core.paginator import Paginator
from .forms import ProteinForm

def index(request) -> render:
   """
   a function based view used to server the index single page template
   """
   # get list of organism ordered by their id
   taxonomy_list = Taxonomy.objects.all().order_by('taxa_id')
   # add the data to a paginator display 50 rows each time
   # there is a lot of data this needs to be done
   paginator = Paginator(taxonomy_list, 50)
   
   # get the page of the pagination
   page = request.GET.get('page')
   # get data from the paginator based on the page
   taxonomy = paginator.get_page(page)

   # render the template with the organism data
   return render(request, 'index.html', { "taxonomy": taxonomy })

def new_protein(request) -> render:
   """
      a view that handles serving a template that has a form to 
      add a new protein and adding a new protein to the database
   """

   # check if it is a POST request
   if request.method == "POST":
      
      form = ProteinForm(request.POST)

      if form.is_valid():
         
         form.save()

   # if the request is a GET request
   # create a form
   form = ProteinForm()
   # render the template
   return render(request, 'newProtein.html', {'form': form})