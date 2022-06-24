from django.shortcuts import render
from .models import Taxonomy
from django.core.paginator import Paginator
from . import forms

def index(request):
   taxonomy_list = Taxonomy.objects.all().order_by('taxa_id')
   paginator = Paginator(taxonomy_list, 50)
   
   page = request.GET.get('page')
   taxonomy = paginator.get_page(page)

   return render(request, 'index.html', { "taxonomy": taxonomy })

def new_protein(request):
   """
      a view that handles serving a template that has a form to 
      add a new protein and adding a new protein to the database
   """
   if request.method == "POST":
      form = forms.ProteinForm(request.POST)
      print(form.cleaned_data)
      taxonomy = form.cleaned_data['taxonomy']
      domains = form.cleaned_data['domains']
      print("tax & domains")
      print(taxonomy, domains)

   form = forms.ProteinForm()
   return render(request, 'newProtein.html', {'form': form})