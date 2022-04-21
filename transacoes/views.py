from django.shortcuts import render
import csv
from transacoes.forms import CsvModelForm
from .models import Modelo

def upload(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid:
        form.save()
    else:
        form = CsvModelForm

    for filename, file in request.FILES.items():
        name = request.FILES[filename].name
        size = request.FILES[filename].size


    dados = {'form':form,'name':name, 'size':size}
    
    return render(request, 'upload.html', dados)

def name_file(request):
    for filename, file in request.FILES.items():
        name_files = request.FILES[filename].name
    return name_files

def render_csv(request):
    for filename, file in request.FILES.items():
        name = request.FILES[filename].name
        size = request.FILES[filename].size
    lista = []

    with open(name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for linha in reader:
            lista.append(
                {'Banco Origem':linha[0], 'Agência Origem':linha[1], 'Conta Origem':linha[2],
                'Banco Destino':linha[3], 'Agência Destino':linha[4], 'Conta Destino':linha[5],
                'Valor da Transação':linha[6], 'Data e hora da transção':linha[7]}
                )
    dados = {'name':name_file,'size':size,'lista':lista}
    return render(request,'index.html', dados)