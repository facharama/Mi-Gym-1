from django.urls import path
from . import views

app_name = "pagos"

urlpatterns = [
    path("", views.listar_pagos, name="pagos_lista"),
    path("nuevo/", views.crear_pago, name="pagos_crear"),
    path("listar/", views.listar_pagos, name="listar"),
    path("<int:pk>/", views.detalle_pago, name="detalle"),
]