from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_alat, name='daftar_alat'),
    path('tambah/', views.tambah_alat, name='tambah_alat'),
]