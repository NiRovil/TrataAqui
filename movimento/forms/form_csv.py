from django import forms
from django.core.validators import FileExtensionValidator

class FormValidator(forms.Form):
    arquivo = forms.FileField(validators=[FileExtensionValidator(['csv'])])