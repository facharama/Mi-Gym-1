from django import forms
from .models import Acceso

class AccesoForm(forms.ModelForm):
    class Meta:
        model = Acceso
        fields = ["socio", "sucursal", "tipo", "fecha_hora"]

