from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import date
from .models import Prestamo
from .forms import PrestamoForm, DevolucionForm
from usuarios.decorators import bibliotecario_required

@login_required
def lista_prestamos(request):
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    
    prestamos = Prestamo.objects.all()
    
    if query:
        prestamos = prestamos.filter(
            Q(lector__nombre__icontains=query) |
            Q(lector__apellidos__icontains=query) |
            Q(lector__numero_documento__icontains=query) |
            Q(libro__titulo__icontains=query) |
            Q(libro__isbn__icontains=query)
        )
    
    if estado:
        prestamos = prestamos.filter(estado=estado)
    
    context = {
        'prestamos': prestamos,
        'query': query,
        'estado_seleccionado': estado,
        'estados': Prestamo.ESTADO_CHOICES,
        'hoy': date.today(),
    }
    return render(request, 'prestamos/lista_prestamos.html', context)

@login_required
@bibliotecario_required
def crear_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.usuario_registro = request.user
            prestamo.save()
            messages.success(request, 'Préstamo registrado exitosamente.')
            return redirect('lista_prestamos')
    else:
        form = PrestamoForm()
    
    context = {
        'form': form,
        'accion': 'Nuevo Préstamo'
    }
    return render(request, 'prestamos/form_prestamo.html', context)

@login_required
@bibliotecario_required
def devolver_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk, estado='activo')
    
    if request.method == 'POST':
        form = DevolucionForm(request.POST)
        if form.is_valid():
            prestamo.devolver()
            if form.cleaned_data['observaciones']:
                prestamo.observaciones += f"\nDevolución: {form.cleaned_data['observaciones']}"
                prestamo.save()
            messages.success(request, 'Devolución registrada exitosamente.')
            return redirect('lista_prestamos')
    else:
        form = DevolucionForm()
    
    context = {
        'prestamo': prestamo,
        'form': form,
    }
    return render(request, 'prestamos/devolver_prestamo.html', context)

@login_required
def detalle_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    context = {'prestamo': prestamo}
    return render(request, 'prestamos/detalle_prestamo.html', context)

@login_required
def prestamos_vencidos(request):
    prestamos = Prestamo.objects.filter(
        estado='activo',
        fecha_limite__lt=date.today()
    )
    
    context = {
        'prestamos': prestamos,
        'titulo': 'Préstamos Vencidos',
        'estados': Prestamo.ESTADO_CHOICES,
        'hoy': date.today(),
    }
    return render(request, 'prestamos/lista_prestamos.html', context)

@login_required
def prestamos_activos(request):
    prestamos = Prestamo.objects.filter(estado='activo')
    
    context = {
        'prestamos': prestamos,
        'titulo': 'Préstamos Activos',
        'estados': Prestamo.ESTADO_CHOICES,
        'hoy': date.today(),
    }
    return render(request, 'prestamos/lista_prestamos.html', context)