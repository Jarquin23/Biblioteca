from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Libro, Autor, Categoria
from .forms import LibroForm, AutorForm, CategoriaForm
from usuarios.decorators import bibliotecario_required

@login_required
def lista_libros(request):
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    categoria = request.GET.get('categoria', '')
    
    libros = Libro.objects.all()
    
    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) | 
            Q(isbn__icontains=query) |
            Q(autores__nombre__icontains=query) |
            Q(autores__apellidos__icontains=query)
        ).distinct()
    
    if estado:
        libros = libros.filter(estado=estado)
    
    if categoria:
        libros = libros.filter(categoria_id=categoria)
    
    context = {
        'libros': libros,
        'query': query,
        'estado_seleccionado': estado,
        'categoria_seleccionada': categoria,
        'estados': Libro.ESTADO_CHOICES,
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'libros/lista_libros.html', context)

@login_required
@bibliotecario_required
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro creado exitosamente.')
            return redirect('lista_libros')
    else:
        form = LibroForm()
    
    context = {
        'form': form,
        'accion': 'Crear'
    }
    return render(request, 'libros/form_libro.html', context)

@login_required
@bibliotecario_required
def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro actualizado exitosamente.')
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)
    
    context = {
        'form': form,
        'libro': libro,
        'accion': 'Editar'
    }
    return render(request, 'libros/form_libro.html', context)

@login_required
@bibliotecario_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado exitosamente.')
        return redirect('lista_libros')
    
    context = {'libro': libro}
    return render(request, 'libros/eliminar_libro.html', context)

@login_required
def detalle_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    context = {'libro': libro}
    return render(request, 'libros/detalle_libro.html', context)