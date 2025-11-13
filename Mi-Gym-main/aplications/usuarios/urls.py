from django.urls import path
from .views import admin_dashboard, socio_dashboard, role_redirect, crear_usuario

urlpatterns = [
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path("dashboard/socio/", socio_dashboard, name="socio_dashboard"),
    path("role-redirect/", role_redirect, name="role_redirect"),
    path("crear/", crear_usuario, name="usuario_crear"),
]
