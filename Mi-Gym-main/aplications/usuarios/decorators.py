from functools import wraps
from django.http import HttpResponseForbidden
from .utils import is_admin, is_socio

def role_required(role: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if role == "Administrador" and is_admin(request.user):
                return view_func(request, *args, **kwargs)
            if role == "Socio" and is_socio(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tenés permisos para acceder aquí.")
        return _wrapped
    return decorator
