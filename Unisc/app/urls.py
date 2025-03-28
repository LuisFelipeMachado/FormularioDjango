from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contas.urls')),  # 👈 isso liga a app 'contas'
]
