from django.contrib import admin
from .models import Sucursal, Socio, Instructor, Plan, Suscripcion

# Register your models here.

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "direccion", "telefono", "activo")
    search_fields = ("nombre", "direccion")
    list_filter = ("activo",)

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "dni", "sucursal", "estado", "fecha_alta")
    search_fields = ("user_username", "dni", "userfirst_name", "user_last_name")
    list_filter = ("estado", "sucursal")

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "sucursal", "especialidad", "activo")
    search_fields = ("user_username", "userfirst_name", "user_last_name")
    list_filter = ("activo", "sucursal")

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio", "duracion_dias", "requiere_certificado", "activo")
    search_fields = ("nombre",)
    list_filter = ("activo", "requiere_certificado")

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ("id", "socio", "plan", "fecha_inicio", "fecha_fin", "estado", "monto")
    search_fields = ("socio_userusername", "plan_nombre")
    list_filter = ("estado", "plan", "socio__sucursal")