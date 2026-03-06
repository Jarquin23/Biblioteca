from django.contrib import admin
from .models import Prestamo

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['lector', 'libro', 'fecha_prestamo', 'fecha_limite', 'estado']
    list_filter = ['estado', 'fecha_prestamo']
    search_fields = ['lector__nombre', 'lector__apellidos', 'libro__titulo', 'libro__isbn']
    date_hierarchy = 'fecha_prestamo'
    list_per_page = 25