from django.shortcuts import render
from .models import Taxonomy
from django.core.paginator import Paginator

def index(request):
   taxonomy_list = Taxonomy.objects.all().order_by('taxa_id')
   paginator = Paginator(taxonomy_list, 50)
   
   page = request.GET.get('page')
   taxonomy = paginator.get_page(page)

   return render(request, 'index.html', { "taxonomy": taxonomy})