from django.urls import path
from user import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajuda/', views.ajuda, name='ajuda'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('accounts/login/', views.login, name='acclogin'),
    path('logout/', views.logout, name='logout'),
]