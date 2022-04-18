from django.shortcuts import render
from .models import Modelo


def index(request):
    csv_importer = Modelo.objects.all()
    dados = {'csv':csv_importer}
    return render(request, 'index.html', dados)
    