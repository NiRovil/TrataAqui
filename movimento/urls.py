from django.urls import path
from movimento import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tabela/', views.tabela, name='tabela'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login')
]