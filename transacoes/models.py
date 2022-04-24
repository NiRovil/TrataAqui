from django.db import models

class Modelo(models.Model):
    csv_importer = models.FileField(upload_to='csv', blank=False)   
