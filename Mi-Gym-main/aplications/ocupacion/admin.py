from django.contrib import admin
from .models import Acceso, ActiveSession

@admin.register(Acceso)
class AccesoAdmin(admin.ModelAdmin):
    list_display = ("socio", "sucursal", "tipo", "fecha_hora")
    list_filter = ("sucursal", "tipo")
    search_fields = ("socio__user__username", "socio__dni")
    ordering = ("-fecha_hora",)

@admin.register(ActiveSession)
class ActiveSessionAdmin(admin.ModelAdmin):
    list_display = ("member", "status", "check_in_at", "check_out_at")
    list_filter = ("status",)
    search_fields = ("member__user__username", "member__dni")
