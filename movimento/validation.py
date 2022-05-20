from django.http import HttpResponse
from .models import ModeloMovimento
from datetime import datetime

def validation(linha):
    lista = linha.decode('utf-8')
    lista = lista.strip()
    lista = lista.split(',')
    data_inicio = None
    data_transacao = None
    data = datetime.fromisoformat(lista[7])
    if data_inicio is None:
        data_inicio = datetime.fromisoformat(lista[7])
    if data_transacao is None:
        data_transacao = ModeloMovimento.objects.dates('data_e_hora_da_transacao', 'year')
    if data_inicio.date() in data_transacao:
        print('Teste 1')
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
        print('Teste 2')
        return HttpResponse('<h1>As datas não coincidem<h1>')