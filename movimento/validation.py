from .models import Movimentos
from django.shortcuts import render

def analise_sus(movimentos_suspeitos):
    valor = []
    for x in movimentos_suspeitos:
        valor.append(movimentos_suspeitos[x])
    return valor

def erro(request, validacao):
    for x in validacao:
        mensagem = validacao[x]
        dados = {'form':mensagem}
        return render(request, 'erro.html', dados)

def validation(request, linha, validacao, data, data_inicio, lancamento):
    banco = Movimentos(
        ordem_lancamento = lancamento,
        banco_origem = linha[0],
        agencia_origem = linha[1],
        conta_origem = linha[2],
        banco_destino = linha[3],
        agencia_destino = linha[4],
        conta_destino = linha[5],
        valor_da_transacao = linha[6],
        data_e_hora_da_transacao = data,
    )

    if data.date() == data_inicio.date():
        banco.full_clean()
        banco.save()

    else:
        validacao['index'] = 'As datas não coincidem'
        return erro(request, validacao)