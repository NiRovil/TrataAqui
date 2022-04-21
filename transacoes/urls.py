from django.urls import include, path
from . import views


urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('csv/csv/transacoes-2022-01-01.csv', views.render_csv, name='object')
]