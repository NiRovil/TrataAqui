from django import forms
from django.core.validators import FileExtensionValidator

class FormValidatorXML(forms.Form):
    arquivo = forms.FileField(validators=[FileExtensionValidator(['xml'])])