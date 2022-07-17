from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('', include('movimento.urls')),
    path('admin/', admin.site.urls),
]
