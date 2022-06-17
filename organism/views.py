from django.shortcuts import render
from .models import Taxonomy

def index(request):
   taxonomy = Taxonomy.objects.all()
   return render(request, 'index.html', { "taxonomy": taxonomy})