from django.urls import path
from . import views

app_name = "rutina"

urlpatterns = [

    path("asignar/", views.asignar_rutina, name="rutina_asignar"),
    path("hoy/<int:socio_id>/", views.rutina_de_hoy, name="rutina_hoy"),
    path("nueva/", views.crear_rutina, name="rutina_crear"),
]