from django.contrib import admin
from .models import Movimentos

class MovimentosRealizados(admin.ModelAdmin):
    
    list_display = ['id', 'banco_origem', 'agencia_origem']
    list_display_links = ['id', 'banco_origem', 'agencia_origem']

admin.site.register(Movimentos, MovimentosRealizados)
