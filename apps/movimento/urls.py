from django.urls import path
from movimento import views


urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('importacoes/', views.importacoes, name='importacoes'),
    path('detalhes/<username>', views.detalhes, name='detalhes'),
    path('analise/', views.analise, name='analise')
]