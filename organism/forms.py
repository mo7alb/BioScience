from django.forms import ModelForm

from .models import Protein

class ProteinForm(ModelForm):
    """
    """
    class Meta:
        model = Protein
        fields = '__all__'