from django.contrib import admin
from .models import Ejercicio, Rutina, RutinaAsignacion, RutinaDia, RutinaDetalle

# Register your models here.


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "grupo_muscular", "activo")
    search_fields = ("nombre", "grupo_muscular")
    list_filter = ("activo",)

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "objetivo", "creada_por", "activa")
    search_fields = ("nombre", "objetivo")
    list_filter = ("activa",)

@admin.register(RutinaAsignacion)
class RutinaAsignacionAdmin(admin.ModelAdmin):
    list_display = ("id", "socio", "rutina", "fecha_inicio", "fecha_fin", "estado")
    search_fields = ("socio_userusername", "rutina_nombre")
    list_filter = ("estado", "fecha_inicio")

@admin.register(RutinaDia)
class RutinaDiaAdmin(admin.ModelAdmin):
    list_display = ("id", "rutina", "dia_semana", "observaciones")
    list_filter = ("dia_semana",)

@admin.register(RutinaDetalle)
class RutinaDetalleAdmin(admin.ModelAdmin):
    list_display = ("id", "rutina_dia", "orden", "ejercicio", "series", "repeticiones", "tiempo_seg", "descanso_seg")
    search_fields = ("ejercicio__nombre",)
    list_filter = ("rutina_dia__dia_semana",)
    ordering = ("rutina_dia", "orden")