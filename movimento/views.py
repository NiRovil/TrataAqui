from django.shortcuts import render
from .validation import *
from .forms.form_csv import FormValidator
import pandas as pd
from datetime import datetime
from .models import *
from django.contrib.auth.decorators import login_required

@login_required
def upload(request):
    name, size = '', 0
    for filename, file in request.FILES.items():
        arquivo = request.FILES[filename]
        name = request.FILES[filename].name
        size = request.FILES[filename].size
    form = FormValidator(request.POST, request.FILES)
    validacao = {}
    
    if request.method == 'POST' and form.is_valid:
        col = 'banco_origem agencia_origem conta_origem banco_destino agencia_destino conta_destino valor_da_transacao data_e_hora_da_transacao'.split()
        df = pd.read_csv(arquivo, names=col)
        df = df.dropna()
        df = df.values.tolist()

        if len(df) == 0:
            validacao['index'] = 'O arquivo está em branco!'
            return erro(request, validacao)

        data_inicio = None
        data_transacao = None
        data = datetime.fromisoformat(df[0][7])
        
        if data_inicio is None:
            data_inicio = datetime.fromisoformat(df[0][7])
        if data_transacao is None:
            data_transacao = Movimentos.objects.dates('data_e_hora_da_transacao', 'year')
        if data_inicio.date() in data_transacao:
            validacao['index'] = 'Um arquivo com as mesmas datas e horarios já foi usado para upload!'
            return erro(request, validacao)
        user = request.user
        lancamento = Lancamento.objects.create(
                usuario = user,
                data_transacao_banco = data_inicio
            )
        
        for linha in df:
            validation(request, linha, validacao, data, data_inicio, lancamento)
        
        lancamento.save()

    dados = {'form':form, 'name':name, 'size':size}
    return render(request, 'upload.html', dados)

def importacoes(request):
    datas = Lancamento.objects.all()
    dados = {'datas':datas}
    return render(request, 'importacoes.html', dados)

def detalhes(request, username):
    if request.method == 'GET':
        arquivo_importado = Movimentos.objects.order_by('data_e_hora_da_transacao').filter(ordem_lancamento_id=username)
        dados = {
            'arquivo':arquivo_importado,
        }

        return render(request, 'detalhes.html', dados)

def analise(request):
    dados = {
        'transacoes_suspeitas':transacoes_suspeitas(request),
        'contas_suspeitas':contas_suspeitas(request),
        'agencias_suspeitas':agencias_suspeitas(request)
    }
    return render(request, 'analise.html', dados)