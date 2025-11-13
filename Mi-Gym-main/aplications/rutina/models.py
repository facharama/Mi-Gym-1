from django.db import models
from django.db import models
from aplications.socios.models import Socio, Instructor

# Create your models here.

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=300, blank=True)
    grupo_muscular = models.CharField(max_length=60, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Rutina(models.Model):
    nombre = models.CharField(max_length=120)
    objetivo = models.CharField(max_length=120, blank=True)
    creada_por = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, blank=True, related_name="rutinas_creadas"
    )
    activa = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.nombre


class RutinaAsignacion(models.Model):
    ESTADOS = [
        ("Vigente", "Vigente"),
        ("Finalizada", "Finalizada"),
        ("Pausada", "Pausada"),
    ]

    rutina = models.ForeignKey(Rutina, on_delete=models.PROTECT, related_name="asignaciones")
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="asignaciones")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Vigente")

    class Meta:
        indexes = [models.Index(fields=["socio", "fecha_inicio", "fecha_fin"])]
        verbose_name = "Asignación de rutina"
        verbose_name_plural = "Asignaciones de rutina"

    def __str__(self):
        return f"{self.socio} → {self.rutina} ({self.estado})"


class RutinaDia(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name="dias")
    dia_semana = models.PositiveSmallIntegerField()
    observaciones = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("rutina", "dia_semana")
        verbose_name = "Día de rutina"
        verbose_name_plural = "Días de rutina"

    def __str__(self):
        return f"{self.rutina} - Día {self.dia_semana}"


class RutinaDetalle(models.Model):
    rutina_dia = models.ForeignKey(RutinaDia, on_delete=models.CASCADE, related_name="detalles")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT, related_name="en_rutinas")
    orden = models.PositiveIntegerField(default=1)
    series = models.PositiveIntegerField(null=True, blank=True)
    repeticiones = models.PositiveIntegerField(null=True, blank=True)
    tiempo_seg = models.PositiveIntegerField(null=True, blank=True)
    descanso_seg = models.PositiveIntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["orden"]
        verbose_name = "Detalle de rutina"
        verbose_name_plural = "Detalles de rutina"

    def __str__(self):
        return f"{self.rutina_dia} - {self.orden}. {self.ejercicio}"