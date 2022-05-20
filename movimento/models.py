from django.db import models

class ModeloMovimento(models.Model):
    banco_origem = models.CharField(max_length=30, blank=False)
    agencia_origem = models.CharField(max_length=30, blank=False)
    conta_origem = models.CharField(max_length=30, blank=False)
    banco_destino = models.CharField(max_length=30, blank=False)
    agencia_destino = models.CharField(max_length=30, blank=False)
    conta_destino = models.CharField(max_length=30, blank=False)
    valor_da_transacao = models.FloatField(max_length=200, blank=False)
    data_e_hora_da_transacao = models.DateTimeField(blank=False)
