from django.urls import path
from movimento import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('importacoes/', views.importacoes, name='importacoes'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('accounts/login/', views.login, name='acclogin'),
    path('detalhes/<username>', views.detalhes, name='detalhes')
]