from django import forms
from aplications.socios.models import Plan, Sucursal
from aplications.rutina.models import Ejercicio, Rutina, RutinaDia, RutinaDetalle


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['nombre', 'descripcion', 'duracion_dias', 'precio', 'requiere_certificado', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del plan'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción opcional'}),
            'duracion_dias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Días de duración'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'requiere_certificado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono', 'email', 'aforo_maximo', 'umbral_bajo_pct', 'umbral_medio_pct', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la sucursal'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@ejemplo.com'}),
            'aforo_maximo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad máxima'}),
            'umbral_bajo_pct': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '40'}),
            'umbral_medio_pct': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'descripcion', 'grupo_muscular', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del ejercicio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del ejercicio'}),
            'grupo_muscular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pecho, Espalda, Piernas'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RutinaFormConfig(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre', 'objetivo', 'creada_por', 'activa', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la rutina'}),
            'objetivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objetivo (Ej: Hipertrofia, Fuerza)'}),
            'creada_por': forms.Select(attrs={'class': 'form-select'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones'}),
        }


class RutinaDiaFormConfig(forms.ModelForm):
    class Meta:
        model = RutinaDia
        fields = ['dia_semana', 'observaciones']
        widgets = {
            'dia_semana': forms.Select(
                choices=[
                    (1, 'Lunes'),
                    (2, 'Martes'),
                    (3, 'Miércoles'),
                    (4, 'Jueves'),
                    (5, 'Viernes'),
                    (6, 'Sábado'),
                    (7, 'Domingo'),
                ],
                attrs={'class': 'form-select'}
            ),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones del día'}),
        }


class RutinaDetalleFormConfig(forms.ModelForm):
    class Meta:
        model = RutinaDetalle
        fields = ['ejercicio', 'orden', 'series', 'repeticiones', 'tiempo_seg', 'descanso_seg', 'observaciones']
        widgets = {
            'ejercicio': forms.Select(attrs={'class': 'form-select'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Orden'}),
            'series': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Series'}),
            'repeticiones': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Repeticiones'}),
            'tiempo_seg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo en segundos'}),
            'descanso_seg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Descanso en segundos'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
        }
