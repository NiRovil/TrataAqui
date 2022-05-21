from django.shortcuts import render
from .validation import validation
from .forms.form_csv import FormValidator
import pandas as pd

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
        print(df)
        for linha in df:
            validation(linha, validacao)
            for x in validacao:
                mensagem = validacao[x]
                dados = {'form':mensagem, 'name':name, 'size':size}
                return render(request, 'erro.html', dados)
    dados = {'form':form, 'name':name, 'size':size}
    return render(request, 'upload.html', dados)