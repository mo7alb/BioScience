from django.forms import ModelForm

from .models import Protein

class ProteinForm(ModelForm):
    """
    a class used to make a django form to add a new protein to the database
    """
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'length']
