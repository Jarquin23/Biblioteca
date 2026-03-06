from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Lector
from .forms import LectorForm
from usuarios.decorators import bibliotecario_required

@login_required
def lista_lectores(request):
    query = request.GET.get('q', '')
    activo = request.GET.get('activo', '')
    
    lectores = Lector.objects.all()
    
    if query:
        lectores = lectores.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(numero_documento__icontains=query) |
            Q(email__icontains=query)
        )
    
    if activo:
        lectores = lectores.filter(activo=(activo == 'true'))
    
    context = {
        'lectores': lectores,
        'query': query,
        'activo_seleccionado': activo,
    }
    return render(request, 'lectores/lista_lectores.html', context)

@login_required
@bibliotecario_required
def crear_lector(request):
    if request.method == 'POST':
        form = LectorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lector registrado exitosamente.')
            return redirect('lista_lectores')
    else:
        form = LectorForm()
    
    context = {
        'form': form,
        'accion': 'Crear'
    }
    return render(request, 'lectores/form_lector.html', context)

@login_required
@bibliotecario_required
def editar_lector(request, pk):
    lector = get_object_or_404(Lector, pk=pk)
    if request.method == 'POST':
        form = LectorForm(request.POST, instance=lector)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lector actualizado exitosamente.')
            return redirect('lista_lectores')
    else:
        form = LectorForm(instance=lector)
    
    context = {
        'form': form,
        'lector': lector,
        'accion': 'Editar'
    }
    return render(request, 'lectores/form_lector.html', context)

@login_required
@bibliotecario_required
def eliminar_lector(request, pk):
    lector = get_object_or_404(Lector, pk=pk)
    if request.method == 'POST':
        lector.delete()
        messages.success(request, 'Lector eliminado exitosamente.')
        return redirect('lista_lectores')
    
    context = {'lector': lector}
    return render(request, 'lectores/eliminar_lector.html', context)

@login_required
def detalle_lector(request, pk):
    lector = get_object_or_404(Lector, pk=pk)
    context = {'lector': lector}
    return render(request, 'lectores/detalle_lector.html', context)

@login_required
@bibliotecario_required
def toggle_lector_activo(request, pk):
    lector = get_object_or_404(Lector, pk=pk)
    lector.activo = not lector.activo
    lector.save()
    messages.success(request, f'Lector {"activado" if lector.activo else "desactivado"} exitosamente.')
    return redirect('lista_lectores')