from django.shortcuts import render
from .validation import validation, erro
from .forms.form_csv import FormValidator
import pandas as pd
from datetime import datetime
from .models import ModeloMovimento

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
        else:
            data_inicio = None
            data_transacao = None
            data = datetime.fromisoformat(df[0][7])
            
            if data_inicio is None:
                data_inicio = datetime.fromisoformat(df[0][7])
            if data_transacao is None:
                data_transacao = ModeloMovimento.objects.dates('data_e_hora_da_transacao', 'year')
            if data_inicio.date() in data_transacao:
                validacao['index'] = 'Um arquivo com as mesmas datas e horarios já foi usado para upload!'

            print(df)
            for linha in df:
                validation(request, linha, validacao, data, data_inicio)
    dados = {'form':form, 'name':name, 'size':size}
    return render(request, 'upload.html', dados)