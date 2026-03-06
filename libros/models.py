from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    biografia = models.TextField(blank=True)
    
    class Meta:
        ordering = ['apellidos', 'nombre']
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
    
    def __str__(self):
        return f"{self.apellidos}, {self.nombre}"

class Libro(models.Model):
    ESTADO_CHOICES = (
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('en_reparacion', 'En Reparación'),
        ('perdido', 'Perdido'),
    )
    
    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor, related_name='libros')
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='libros')
    editorial = models.CharField(max_length=200, blank=True)
    anio_publicacion = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    edicion = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    ubicacion = models.CharField('Estante/Ubicación', max_length=50, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['titulo']
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
    
    def __str__(self):
        return f"{self.titulo} ({self.isbn})"
    
    def autores_lista(self):
        return ", ".join([str(autor) for autor in self.autores.all()])
    autores_lista.short_description = "Autores"