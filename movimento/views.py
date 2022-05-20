from django.shortcuts import render
from .validation import validation
from .forms.form_csv import FormValidator

def upload(request):
    name, size = '', 0
    for filename, file in request.FILES.items():
        arquivo = request.FILES[filename]
        name = request.FILES[filename].name
        size = request.FILES[filename].size
    form = FormValidator(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid:
        for linha in arquivo:
            validation(linha)
    dados = {'form':form, 'name':name, 'size':size}
    
    return render(request, 'upload.html', dados)