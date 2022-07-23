from django import forms
from django.core.validators import FileExtensionValidator

#Verifica se a extensão do arquivo upado é CSV.
class FormValidator(forms.Form):
    arquivo = forms.FileField(validators=[FileExtensionValidator(['csv'])])