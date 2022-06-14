from django.http import HttpResponse
from django.shortcuts import render, redirect
from .validation import *
from .forms.form_csv import FormValidator
import pandas as pd
from datetime import datetime
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from random import randint
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

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
            data_transacao = Movimentos.objects.dates('data_e_hora_da_transacao', 'day')
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

def login(request):
    if request.method == 'POST':
        email = request.POST['email_login']
        senha = request.POST['senha_login']
        if User.objects.filter(email=email).exists():
            usuario = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = authenticate(request, username=usuario, password=senha)
            if user is not None:
                login_auth(request, user)
                return redirect('index')
    return render(request, 'login.html')

def logout(request):
    logout_auth(request)
    return redirect('index')

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
        send_mail('Senha da sua conta Tratamento CSV!', 'Guarde bem a sua senha: {}'.format(senha), 'sendemailtratamentocsv@gmail.com', [email], fail_silently=False)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'cadastro.html')

def analise(request):
    dados = None
    movimentos_suspeitos = []
    transacao = 100000
    movimentacao = 1000000
    movimentacao_bancaria = 1000000000
    arquivo = Movimentos.objects.all()
    for item in arquivo:
        valor = item.valor_da_transacao
        if transacao <= valor < movimentacao:
            movimentos_suspeitos = movimentos_suspeitos
            retorno = transacao_suspeita(request, movimentos_suspeitos)
            return retorno
        """ if movimentacao <= valor < movimentacao_bancaria:
            movimentos_suspeitos[1] = valor
        if valor >= movimentacao_bancaria:
            movimentos_suspeitos[2] = valor """
    
    dados = {'transacao':retorno.dados}