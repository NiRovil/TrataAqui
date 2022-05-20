from django.shortcuts import render, redirect
from .validation import validation
from .forms.form_csv import FormValidator

def upload(request):
    name, size = '', 0
    for filename, file in request.FILES.items():
        arquivo = request.FILES[filename]
        name = request.FILES[filename].name
        size = request.FILES[filename].size
    form = FormValidator(request.POST, request.FILES)
    validacao = {}
    if request.method == 'POST' and form.is_valid:
        for linha in arquivo:
            validation(linha, validacao)
            for x in validacao:
                mensagem = validacao[x]
                dados = {'form':mensagem, 'name':name, 'size':size}
                return render(request, 'erro.html', dados)
    dados = {'form':form, 'name':name, 'size':size}
    return render(request, 'upload.html', dados)