# aplications/ocupacion/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from aplications.socios.models import Socio, Sucursal

User = settings.AUTH_USER_MODEL

class Acceso(models.Model):
    TIPO_CHOICES = [
        ("Ingreso", "Ingreso"),
        ("Egreso", "Egreso"),
    ]
    socio = models.ForeignKey(Socio, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_hora = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Acceso"
        verbose_name_plural = "Accesos"
        indexes = [
            models.Index(fields=["socio", "sucursal", "fecha_hora"]),
        ]

    def __str__(self):
        return f"{self.socio} - {self.tipo} - {self.fecha_hora:%Y-%m-%d %H:%M}"

class ActiveSession(models.Model):
    member = models.OneToOneField("socios.Socio", on_delete=models.PROTECT)
    check_in_at = models.DateTimeField()
    check_out_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="ACTIVE")  # ACTIVE, CLOSED, AUTO_CLOSED

    def duration(self):
        end = self.check_out_at or timezone.now()
        return end - self.check_in_at
