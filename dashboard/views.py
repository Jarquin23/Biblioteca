from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    context = {
        'total_libros': 0,
        'libros_disponibles': 0,
        'libros_prestados': 0,
        'total_lectores': 0,
        'lectores_activos': 0,
        'prestamos_activos': 0,
        'prestamos_vencidos': 0,
        'prestamos_hoy': 0,
        'proximos_vencer': 0,
        'ultimos_prestamos': [],
        'lectores_recientes': [],
        'libros_recientes': [],
    }
    return render(request, 'dashboard/dashboard.html', context)