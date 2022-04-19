from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('csv/transacoes-2022-01-01.csv', views.render_csv, name='object')
]