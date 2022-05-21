from .models import ModeloMovimento
from datetime import datetime

def validation(linha, validacao):
    data_inicio = None
    data_transacao = None
    data = datetime.fromisoformat(linha[7])
    if data_inicio is None:
        data_inicio = datetime.fromisoformat(linha[7])
    if data_transacao is None:
        data_transacao = ModeloMovimento.objects.dates('data_e_hora_da_transacao', 'year')
    if data_inicio.date() in data_transacao:
        validacao['index'] = 'Um arquivo com as mesmas datas e horarios já foi usado para upload!'

    banco = ModeloMovimento(
        banco_origem = linha[0],
        agencia_origem = linha[1],
        conta_origem = linha[2],
        banco_destino = linha[3],
        agencia_destino = linha[4],
        conta_destino = linha[5],
        valor_da_transacao = linha[6],
        data_e_hora_da_transacao = data
    )

    if data.date() == data_inicio.date():
        banco.full_clean()
        banco.save()
    else:
        validacao['index'] = 'As datas não coincidem'