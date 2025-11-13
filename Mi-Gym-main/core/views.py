from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .utils import in_group

# Create your views here.

def home(request):
    return render(request, "home.html")

class CustomLoginView(LoginView):
    template_name = "login.html"
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        # Autenticar usuario
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            # Verificar si es un socio y si está activo
            try:
                if hasattr(user, 'perfil_socio'):
                    socio = user.perfil_socio
                    if not socio.activo:
                        messages.error(self.request, 
                            'Tu cuenta ha sido desactivada. Contacta al administrador para reactivarla.')
                        return self.form_invalid(form)
            except:
                pass  # Si no es socio, continúa normal
            
            # Si es usuario activo o no es socio, permite login normal
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        from django.urls import reverse
        u = self.request.user
        if u.is_staff:
            return reverse("admin_dashboard")  # Usar la URL del módulo admin de la app      
        if in_group(u, "Socio"):
            return reverse("socios:panel_socio")  # Usar URL name en lugar de hardcode
        return "/"                    

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required
@user_passes_test(lambda u: in_group(u, "Socio"))
def socios_dashboard(request):
    return render(request, "socios_dashboard.html")
