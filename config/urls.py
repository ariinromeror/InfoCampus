from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Corregido: .urls en lugar de .center
    path('api/', include('portal.urls')),
]