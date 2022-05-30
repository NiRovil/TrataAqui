from django.shortcuts import render, redirect
from .validation import validation, erro
from .forms.form_csv import FormValidator
import pandas as pd
from datetime import datetime
from .models import ModeloMovimento, Arquivo
from django.contrib import messages
from django.contrib.auth.models import User
from random import randint

def index(request):
    return render(request, 'index.html')

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
            data_transacao = ModeloMovimento.objects.dates('data_e_hora_da_transacao', 'year')
        if data_inicio.date() in data_transacao:
            validacao['index'] = 'Um arquivo com as mesmas datas e horarios já foi usado para upload!'
            return erro(request, validacao)
        else:
            banco = Arquivo(
                data_transacao_banco = data_inicio
            )
            banco.save()
        

        for linha in df:
            validation(request, linha, validacao, data, data_inicio)
    dados = {'form':form, 'name':name, 'size':size}
    return render(request, 'upload.html', dados)

def tabela(request):
    datas = Arquivo.objects.all()
    dados = {'datas':datas}
    return render(request, 'tabela.html', dados)

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha_gerada = [randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9)]
        senha = ''.join([str(i) for i in senha_gerada])
        if not nome.strip():
            messages.error(request, 'O nome não pode estar em branco!')
            return redirect('cadastro')
        if not email.strip():
            messages.error(request, 'O email não pode estar em branco!')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado!')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        print(senha)
        messages.success(request, 'Usuário cadastrado com sucesso! Sua senha é {}'.format(senha))
        return redirect('login')
    else:
        return render(request, 'cadastro.html')