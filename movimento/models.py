from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Lancamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_publicacao_banco = models.DateField(default=datetime.now)
    data_transacao_banco = models.DateField(blank=False)

class Movimentos(models.Model):
    ordem_lancamento = models.ForeignKey(Lancamento, on_delete=models.CASCADE)
    banco_origem = models.CharField(max_length=30, blank=False)
    agencia_origem = models.CharField(max_length=30, blank=False)
    conta_origem = models.CharField(max_length=30, blank=False)
    banco_destino = models.CharField(max_length=30, blank=False)
    agencia_destino = models.CharField(max_length=30, blank=False)
    conta_destino = models.CharField(max_length=30, blank=False)
    valor_da_transacao = models.FloatField(max_length=200, blank=False)
    data_e_hora_da_transacao = models.DateField(blank=False)
    data_upload = models.DateField(default=datetime.now)