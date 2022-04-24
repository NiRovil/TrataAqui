from django import forms
from .models import Modelo

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ['csv_importer']