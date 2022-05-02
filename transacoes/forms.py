from msilib.schema import File
from django import forms
from .models import Modelo
from django.core.validators import FileExtensionValidator

class FormValidator(forms.Form):

    arquivo = forms.FileField(validators=[FileExtensionValidator(['csv'])])

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ['csv_importer']