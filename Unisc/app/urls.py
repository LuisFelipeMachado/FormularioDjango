from contas import views
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include

def home(request):
    return HttpResponse("Bem-vindo à API!")

urlpatterns = [
    path('', include('contas.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('contas.urls')),  # 👈 isso liga a app 'contas'
    path('dashboard/', views.dashboard, name='dashboard'),
]
