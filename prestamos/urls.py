from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_prestamos, name='lista_prestamos'),
    path('crear/', views.crear_prestamo, name='crear_prestamo'),
    path('vencidos/', views.prestamos_vencidos, name='prestamos_vencidos'),
    path('activos/', views.prestamos_activos, name='prestamos_activos'),
    path('<int:pk>/', views.detalle_prestamo, name='detalle_prestamo'),
    path('<int:pk>/devolver/', views.devolver_prestamo, name='devolver_prestamo'),
]