from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_lectores, name='lista_lectores'),
    path('crear/', views.crear_lector, name='crear_lector'),
    path('<int:pk>/', views.detalle_lector, name='detalle_lector'),
    path('<int:pk>/editar/', views.editar_lector, name='editar_lector'),
    path('<int:pk>/eliminar/', views.eliminar_lector, name='eliminar_lector'),
    path('<int:pk>/toggle/', views.toggle_lector_activo, name='toggle_lector'),
]