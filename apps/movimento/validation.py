from .models import Movimentos
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages

def transacoes_suspeitas(request):
    """
    Filtra todos os valores suspeitos que forem acima de R$ 100.000,00.
    """
    transacoes_suspeitas = Movimentos.objects.filter(valor_da_transacao__gte=100_000)
    return transacoes_suspeitas

def contas_suspeitas(request):
    """
    Filtra todas as contas suspeitas que movimentaram mais de R$ 1.000.000,00.
    """
    transacoes = Movimentos.objects.all()

    # Busca o valor de uma caracteristica do objeto com base em 3 outras caracteristicas. 
    # Faz a soma desses valores, e anota em uma variável.
    # Realiza o filto com base na soma, se essa for maior que R$ 1.000.000,00.
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

    # Para cada item do filtro anterior, adiciona a tag 'Saída' ou 'Entrada'.
    for conta in conta_origem:
        conta.update({'movimento':'Saída'})
    
    for conta in conta_destino:
        conta.update({'movimento':'Entrada'})
    
    # Concatena as duas listas resultantes em uma única variável.
    contas_suspeitas = list(conta_origem) + list(conta_destino)

    return contas_suspeitas

def agencias_suspeitas(request):
    """
    Filtra todas as agencias suspeitas que movimentaram mais de R$ 1.000.000.000,00.
    """
    transacoes = Movimentos.objects.all()

    # Busca o valor de uma caracteristica do objeto com base em 3 outras caracteristicas. 
    # Faz a soma desses valores, e anota em uma variável.
    # Realiza o filto com base na soma, se essa for maior que R$ 1.000.000,00.
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

    # Para cada item do filtro anterior, adiciona a tag 'Saída' ou 'Entrada'.
    for conta in agencia_origem:
        conta.update({'movimento':'Saída'})
    
    for conta in agencia_destino:
        conta.update({'movimento':'Entrada'})

    # Concatena as duas listas resultantes em uma única variável.
    agencias_suspeitas = list(agencia_origem) + list(agencia_destino)

    return agencias_suspeitas

def erro(request, validacao):
    for erro in validacao:
        mensagem = validacao[erro]
        messages.error(request, mensagem)
        return redirect('upload')

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