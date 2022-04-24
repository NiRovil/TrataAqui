from django.urls import include, path
from . import views


urlpatterns = [
    path('upload', views.upload, name='upload')
]