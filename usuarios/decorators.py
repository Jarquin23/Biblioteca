from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.perfil.rol == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos de administrador.')
                return redirect('dashboard')
        return redirect('login')
    return _wrapped_view

def bibliotecario_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.perfil.rol in ['admin', 'bibliotecario']:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos de bibliotecario.')
                return redirect('dashboard')
        return redirect('login')
    return _wrapped_view