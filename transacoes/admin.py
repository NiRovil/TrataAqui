from django.contrib import admin
from .models import Modelo

class ModeloRegistro(admin.ModelAdmin):
    
    list_display = ['id','csv_importer']
    list_display_links = ['id', 'csv_importer']

admin.site.register(Modelo, ModeloRegistro)
