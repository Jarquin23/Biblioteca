from django.contrib import admin
from .models import Libro, Autor, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['apellidos', 'nombre', 'nacionalidad']
    list_filter = ['nacionalidad']
    search_fields = ['nombre', 'apellidos']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'isbn', 'categoria', 'estado', 'ubicacion']
    list_filter = ['estado', 'categoria', 'autores']
    search_fields = ['titulo', 'isbn', 'autores__nombre', 'autores__apellidos']
    filter_horizontal = ['autores']
    list_per_page = 25