from django.contrib import admin
from .models import Pago

# Register your models here.

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "suscripcion", "monto", "metodo", "fecha_pago")
    search_fields = ("suscripcion_sociodni", "suscripcionsociouser_username")
    list_filter = ("metodo", "fecha_pago")
    ordering = ("-fecha_pago",)