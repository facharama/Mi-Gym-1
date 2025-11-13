from django import forms
from .models import Ejercicio, Rutina, RutinaDia, RutinaDetalle, RutinaAsignacion

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ["nombre", "descripcion", "grupo_muscular", "activo"]

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ["nombre", "objetivo", "creada_por", "activa", "observaciones"]

class RutinaDiaForm(forms.ModelForm):
    class Meta:
        model = RutinaDia
        fields = ["rutina", "dia_semana", "observaciones"]

class RutinaDetalleForm(forms.ModelForm):
    class Meta:
        model = RutinaDetalle
        fields = ["rutina_dia", "ejercicio", "orden", "series", "repeticiones", "tiempo_seg", "descanso_seg", "observaciones"]

class RutinaAsignacionForm(forms.ModelForm):
    class Meta:
        model = RutinaAsignacion
        fields = ["rutina", "socio", "fecha_inicio", "fecha_fin", "estado"]
