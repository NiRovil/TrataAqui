from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from movimento.models import ModeloMovimento
from transacoes.forms import CsvModelForm, FormValidator

def upload(request):
    name, size = '', 0
    for filename, file in request.FILES.items():
        file_a = request.FILES[filename]
        name = request.FILES[filename].name
        size = request.FILES[filename].size
    data_inicio = None
    data_transacao = None
    form = FormValidator(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid:
        #form.save()
        #form = CsvModelForm()
        #with open(f'csv/csv/{name}', 'r') as file:
        for linha in file_a:
            lista = linha.decode('utf-8')
            lista = lista.strip()
            lista = lista.split(',')
            data = datetime.fromisoformat(lista[7])

            if data_inicio is None:
                data_inicio = datetime.fromisoformat(lista[7])
            if data_transacao is None:
                data_transacao = ModeloMovimento.objects.dates('data_e_hora_da_transacao', 'year')
            if data_inicio.date() in data_transacao:
                return HttpResponse('<h1>As informações dessa data já foram enviadas<h1>')
            
            banco = ModeloMovimento(
                banco_origem = lista[0],
                agencia_origem = lista[1],
                conta_origem = lista[2],
                banco_destino = lista[3],
                agencia_destino = lista[4],
                conta_destino = lista[5],
                valor_da_transacao = lista[6],
                data_e_hora_da_transacao = data
            )

            if data.date() == data_inicio.date():
                banco.full_clean()
                banco.save()
            else:
                return HttpResponse('<h1>As datas não coincidem<h1>')
            #return formulario == True

        #if formulario:
            #pass
        #else:
            #form = CsvModelForm()
            #return HttpResponse('<h1>Arquivo em branco<h1>')
    dados = {'form':form, 'name':name, 'size':size}
    
    return render(request, 'upload.html', dados)