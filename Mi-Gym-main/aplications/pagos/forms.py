from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["suscripcion", "monto", "metodo", "comprobante", "observaciones"]
