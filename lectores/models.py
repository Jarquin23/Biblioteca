from django.db import models

class Lector(models.Model):
    TIPO_DOCUMENTO = (
        ('dni', 'DNI'),
        ('pasaporte', 'Pasaporte'),
        ('carnet_extranjeria', 'Carnet de Extranjería'),
    )
    
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO, default='dni')
    numero_documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ['apellidos', 'nombre']
        verbose_name = 'Lector'
        verbose_name_plural = 'Lectores'
    
    def __str__(self):
        return f"{self.apellidos}, {self.nombre}"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"