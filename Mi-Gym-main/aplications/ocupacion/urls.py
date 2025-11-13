from django.urls import path
from . import views

app_name = "ocupacion"

urlpatterns = [
    path("registrar/", views.registrar_acceso, name="ocupacion_registrar"),
    path("actual/", views.ocupacion_actual, name="ocupacion_actual"),
    path("simulador/", views.simulador, name="simulador"),
    path("simulador-qr/", views.simulador_qr, name="simulador_qr"),

    # APIs para el simulador
    path("api/access/", views.access_event, name="access_event"),
    path("api/occupancy/current/", views.occupancy_current, name="occupancy_current"),
]
