from django.shortcuts import render
import csv
from transacoes.forms import CsvModelForm
from .models import Modelo

def upload(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid:
        form.save()
    return render(request, 'upload.html', {'form':form})


def render_csv(request):

    lista = []

    with open('csv/transacoes-2022-01-01.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for linha in reader:
            lista.append(
                {'Banco Origem':linha[0], 'Agência Origem':linha[1], 'Conta Origem':linha[2],
                'Banco Destino':linha[3], 'Agência Destino':linha[4], 'Conta Destino':linha[5],
                'Valor da Transação':linha[6], 'Data e hora da transção':linha[7]}
                )

    return render(request,'index.html', {'lista':lista})
