from .models import ModeloMovimento
from datetime import datetime
import pandas as pd

def validation(linha, validacao):
    linha = linha.decode('utf-8')
    linha = linha.strip()
    linha = linha.split(',')
    data_inicio = None
    data_transacao = None
    col = 'banco_origem agencia_origem conta_origem banco_destino agencia_destino conta_destino valor_da_transacao data_e_hora_da_transacao'.split()
    df = pd.DataFrame([linha], columns=col)
    df = df.dropna()
    linha_limpa = df.values.tolist()

    data = datetime.fromisoformat(linha_limpa[7])
    if data_inicio is None:
        data_inicio = datetime.fromisoformat(linha_limpa[7])
    if data_transacao is None:
        data_transacao = ModeloMovimento.objects.dates('data_e_hora_da_transacao', 'year')
    if data_inicio.date() in data_transacao:
        validacao['index'] = 'Um arquivo com as mesmas datas e horarios já foi usado para upload!'

    banco = ModeloMovimento(
        banco_origem = linha_limpa[0],
        agencia_origem = linha_limpa[1],
        conta_origem = linha_limpa[2],
        banco_destino = linha_limpa[3],
        agencia_destino = linha_limpa[4],
        conta_destino = linha_limpa[5],
        valor_da_transacao = linha_limpa[6],
        data_e_hora_da_transacao = data
    )

    if data.date() == data_inicio.date():
        banco.full_clean()
        banco.save()
    else:
        validacao['index'] = 'As datas não coincidem'