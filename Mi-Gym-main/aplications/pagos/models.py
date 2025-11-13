from django.db import models
from django.db import models
from aplications.socios.models import Suscripcion

# Create your models here.

class Pago(models.Model):
    METODOS = [
        ("Efectivo", "Efectivo"),
        ("Debito", "Débito"),
        ("Credito", "Crédito"),
        ("Transferencia", "Transferencia"),
        ("MP", "Mercado Pago"),
    ]

    suscripcion = models.ForeignKey(Suscripcion, on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=30, choices=METODOS)
    comprobante = models.CharField(max_length=60, blank=True, null=True)
    observaciones = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ["-fecha_pago"]
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.id} - {self.monto} ({self.metodo})"

