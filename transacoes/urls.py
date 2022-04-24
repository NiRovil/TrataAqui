<<<<<<< HEAD
from webbrowser import get
from django.urls import path
=======
from django.urls import include, path
>>>>>>> 4b4f33e7db35d09e59aca8602691890e23b6aac1
from . import views


urlpatterns = [
<<<<<<< HEAD
    path('upload', views.upload, name='upload')
=======
    path('upload', views.upload, name='upload'),
    path('csv/csv/transacoes-2022-01-01.csv', views.render_csv, name='object')
>>>>>>> 4b4f33e7db35d09e59aca8602691890e23b6aac1
]