from django.db import models
from django.contrib.auth.models import User
from lectores.models import Lector
from libros.models import Libro
from datetime import date, timedelta

class Prestamo(models.Model):
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
        ('perdido', 'Perdido'),
    )
    
    lector = models.ForeignKey(Lector, on_delete=models.CASCADE, related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prestamos_registrados')
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    fecha_limite = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_prestamo']
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
    
    def __str__(self):
        return f"{self.lector} - {self.libro} ({self.fecha_prestamo})"
    
    def save(self, *args, **kwargs):
        # Si no se especifica fecha límite, establecer 7 días después
        if not self.fecha_limite:
            self.fecha_limite = date.today() + timedelta(days=7)
        
        # Cambiar estado del libro cuando se crea un préstamo
        if not self.pk:  # Solo al crear
            self.libro.estado = 'prestado'
            self.libro.save()
        
        super().save(*args, **kwargs)
    
    def devolver(self):
        self.fecha_devolucion = date.today()
        self.estado = 'devuelto'
        self.libro.estado = 'disponible'
        self.libro.save()
        self.save()
    
    @property
    def dias_restantes(self):
        if self.estado == 'devuelto':
            return 0
        return (self.fecha_limite - date.today()).days
    
    @property
    def esta_vencido(self):
        return self.estado == 'activo' and date.today() > self.fecha_limite