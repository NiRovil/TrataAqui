import os
from django.http import HttpResponse
from django.shortcuts import render
import csv
from transacoes.models import Modelo
from transacoes.forms import CsvModelForm
from movimento.models import ModeloMovimento

def upload(request):

    name = ''
    size = 0
    
    for filename, file in request.FILES.items():
        name = request.FILES[filename].name
        size = request.FILES[filename].size
    
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid:
        form.save()
        if render_csv(name):
            form = CsvModelForm()
        else:
            form = CsvModelForm()
            return HttpResponse('<h1>Arquivo em branco<h1>')
    dados = {'form':form, 'name':name, 'size':size}
    
    return render(request, 'upload.html', dados)

def walk(dirname):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            return path
        else:
            return walk(path)

def render_csv(name):
    # name = Modelo.objects.get()
    # name = walk('csv/csv')

    with open('csv/csv/transacoes-2022-01-01.csv', 'r') as file: 
        reader = csv.reader(file, delimiter=',')
        for linha in reader:
            ModeloMovimento.objects.create(
               banco_origem = linha[0],
               agencia_origem = linha[1],
               conta_origem = linha[2],
               banco_destino = linha[3],
               agencia_destino = linha[4],
               conta_destino = linha[5],
               valor_da_transacao = linha[6],
               data_e_hora_da_transacao = linha[7]
           )
            formulario = True
            
    return formulario
