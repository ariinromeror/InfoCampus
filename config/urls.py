from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Redirección automática: al entrar a http://127.0.0.1:8000/ te lleva al admin
    path('', lambda request: redirect('admin/', permanent=False)),
    
    path('admin/', admin.site.urls),
    path('api/', include('portal.urls')),
]