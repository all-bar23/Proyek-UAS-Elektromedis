from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_alat, name='daftar_alat'),
    path('tambah/', views.tambah_alat, name='tambah_alat'),
    path('<str:pk>/', views.detail_alat, name='detail_alat'),
    path('<str:pk>/edit/', views.edit_alat, name='edit_alat'),
    path('<str:pk>/hapus/', views.hapus_alat, name='hapus_alat'),
]