from .models import Movimentos
from django.shortcuts import render
from django.db.models import Sum

def transacoes_suspeitas(request):
    transacoes_suspeitas = Movimentos.objects.filter(valor_da_transacao__gte=100_000)
    return transacoes_suspeitas

def contas_suspeitas(request):
    transacoes = Movimentos.objects.all()

    conta_origem = (transacoes.values(
        'banco_origem', 'agencia_origem', 'conta_origem'
    ).annotate(
        valor_movimentado=Sum('valor_da_transacao'),
    ).filter(valor_movimentado__gt=1_000_000))

    conta_destino = (transacoes.values(
        'banco_destino', 'agencia_destino', 'conta_destino'
    ).annotate(
        valor_movimentado=Sum('valor_da_transacao')
    ).filter(valor_movimentado__gt=1_000_000))

    for conta in conta_origem:
        conta.update({'movimento':'Saída'})
    
    for conta in conta_destino:
        conta.update({'movimento':'Entrada'})
    
    contas_suspeitas = list(conta_origem) + list(conta_destino)

    return contas_suspeitas

def agencias_suspeitas(request):
    transacoes = Movimentos.objects.all()

    agencia_origem = (transacoes.values(
        'banco_origem', 'agencia_origem'
    ).annotate(
        valor_movimentado=Sum('valor_da_transacao')
    ).filter(valor_movimentado__gt=1_000_000_000))

    agencia_destino = (transacoes.values(
        'banco_destino', 'agencia_destino'
    ).annotate(
        valor_movimentado=Sum('valor_da_transacao')
    ).filter(valor_movimentado__gt=1_000_000_000))

    for conta in agencia_origem:
        conta.update({'movimento':'Saída'})
    
    for conta in agencia_destino:
        conta.update({'movimento':'Entrada'})

    agencias_suspeitas = list(agencia_origem) + list(agencia_destino)

    return agencias_suspeitas

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