from django.db import models
import csv



class Modelo(models.Model):
    csv_importer = models.FileField(upload_to='csv', blank=False)
    with open('csv/transacoes-2022-01-01.csv', 'r') as file:
        lista = []
        for linha in file:
            print(linha)