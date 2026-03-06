from django.contrib import admin
from .models import Lector

@admin.register(Lector)
class LectorAdmin(admin.ModelAdmin):
    list_display = ['apellidos', 'nombre', 'tipo_documento', 'numero_documento', 'email', 'telefono', 'activo']
    list_filter = ['activo', 'tipo_documento']
    search_fields = ['nombre', 'apellidos', 'numero_documento', 'email']
    list_per_page = 25