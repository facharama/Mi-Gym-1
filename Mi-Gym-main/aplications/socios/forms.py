from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Socio, Suscripcion

User = get_user_model()

# =======================
# Crear socio
# =======================
class SocioForm(forms.ModelForm):
    # datos de usuario
    first_name = forms.CharField(label="Nombre",  max_length=150, required=True)
    last_name  = forms.CharField(label="Apellido", max_length=150, required=True)
    email      = forms.EmailField(label="Email", required=True)

    # checkbox visible en el form (mapea a estado)
    activo = forms.BooleanField(label="Activo", required=False, initial=True)

    class Meta:
        model = Socio
        # SIN 'estado' para que no salga el select
        fields = ["dni", "sucursal", "first_name", "last_name", "email", "activo"]
        widgets = {
            "dni": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "DNI",
                "inputmode": "numeric",
                "pattern": r"[0-9]*",
                "required": "required",
            }),
            "sucursal": forms.Select(attrs={"class": "form-select", "required": "required"}),
        }
        labels = {"dni": "DNI", "sucursal": "Sucursal"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # estilos
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Nombre", "required": "required"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Apellido", "required": "required"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Email", "required": "required"})
        # inicial del switch según estado (si viniera instancia)
        if self.instance and self.instance.pk:
            self.fields["activo"].initial = (self.instance.estado or "").strip().lower() != "inactivo"

    def clean_dni(self):
        dni = str(self.cleaned_data.get("dni", "")).strip()
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números.")
        if not (7 <= len(dni) <= 10):
            raise forms.ValidationError("El DNI debe tener entre 7 y 10 dígitos.")
        return dni

    def clean(self):
        data = super().clean()
        dni   = (data.get("dni") or "").strip()
        email = (data.get("email") or "").strip()

        # Duplicados en Socio (case-insensitive)
        qs = Socio.objects.all()
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if dni and qs.filter(dni__iexact=dni).exists():
            self.add_error("dni", "Este DNI ya está registrado como socio.")
        if email and qs.filter(email__iexact=email).exists():
            self.add_error("email", "Este email ya está registrado como socio.")

        # Duplicados en User (username = DNI o email)
        if User.objects.filter(Q(username__iexact=dni) | Q(email__iexact=email)).exists():
            if dni:
                self.add_error("dni", "Ya existe un usuario con este DNI.")
            if email:
                self.add_error("email", "Ya existe un usuario con este email.")

        if self.errors:
            raise forms.ValidationError("No se pudo guardar: hay datos duplicados.")
        return data

    def save(self, commit=True):
        socio = super().save(commit=False)
        # mapear checkbox -> string del modelo
        socio.estado = "Activo" if self.cleaned_data.get("activo") else "Inactivo"

        if commit:
            socio.save()

        # si ya tiene user vinculado, sincroniza
        if socio.user_id:
            u = socio.user
            u.first_name = self.cleaned_data.get("first_name", u.first_name)
            u.last_name  = self.cleaned_data.get("last_name",  u.last_name)
            u.email      = self.cleaned_data.get("email",      u.email)
            u.save()
        return socio


# =======================
# Editar socio
# =======================
class SocioEditForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre",  max_length=150, required=True)
    last_name  = forms.CharField(label="Apellido", max_length=150, required=True)
    email      = forms.EmailField(label="Email", required=True)
    # usamos el mismo switch que en alta
    activo     = forms.BooleanField(label="Activo", required=False, initial=True)

    class Meta:
        model = Socio
        # SIN 'estado' para no renderizar select
        fields = ["dni", "sucursal", "first_name", "last_name", "email", "activo"]
        widgets = {
            "dni": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "DNI",
                "inputmode": "numeric",
                "pattern": r"[0-9]*",
                "required": "required",
            }),
            "sucursal": forms.Select(attrs={"class": "form-select", "required": "required"}),
        }
        labels = {"dni": "DNI", "sucursal": "Sucursal"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial  = self.instance.user.last_name
            self.fields["email"].initial      = self.instance.user.email
            self.fields["activo"].initial     = (self.instance.estado or "").strip().lower() != "inactivo"

        self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})

    def clean_dni(self):
        dni = str(self.cleaned_data.get("dni", "")).strip()
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números.")
        if not (7 <= len(dni) <= 10):
            raise forms.ValidationError("El DNI debe tener entre 7 y 10 dígitos.")
        return dni

    def clean(self):
        data  = super().clean()
        dni   = (data.get("dni") or "").strip()
        email = (data.get("email") or "").strip()

        # Obtener valores originales para comparar
        dni_original = self.instance.dni if self.instance else None
        email_original = self.instance.email if self.instance else None
        
        # Solo validar DNI si cambió
        if dni and dni != dni_original:
            # Validar que no exista otro SOCIO con el mismo DNI
            if Socio.objects.exclude(pk=self.instance.pk).filter(dni__iexact=dni).exists():
                self.add_error("dni", "Este DNI ya está registrado en otro socio.")
            # Validar que no exista otro USER con ese DNI como username
            user_qs = User.objects.all()
            if self.instance and self.instance.user_id:
                user_qs = user_qs.exclude(pk=self.instance.user_id)
            if user_qs.filter(username__iexact=dni).exists():
                self.add_error("dni", "Ya existe otro usuario con este DNI.")
        
        # Solo validar email si cambió
        if email and email.lower() != (email_original or "").lower():
            # Validar que no exista otro SOCIO con el mismo email
            if Socio.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
                self.add_error("email", "Este email ya está registrado en otro socio.")
            # Validar que no exista otro USER con ese email
            user_qs = User.objects.all()
            if self.instance and self.instance.user_id:
                user_qs = user_qs.exclude(pk=self.instance.user_id)
            if user_qs.filter(email__iexact=email).exists():
                self.add_error("email", "Ya existe otro usuario con este email.")

        return data

    def save(self, commit=True):
        socio = super().save(commit=False)
        
        # Actualizar estado basado en el checkbox
        socio.estado = "Activo" if self.cleaned_data.get("activo") else "Inactivo"
        socio.activo = self.cleaned_data.get("activo", True)
        
        # Sincronizar campos de nombre y email en el modelo Socio
        socio.nombre = self.cleaned_data.get("first_name", "")
        socio.apellido = self.cleaned_data.get("last_name", "")
        socio.email = self.cleaned_data.get("email", "")
        
        if commit:
            socio.save()
        
        # Sincronizar con el User asociado si existe
        if socio.user_id:
            u = socio.user
            u.first_name = self.cleaned_data.get("first_name", u.first_name)
            u.last_name  = self.cleaned_data.get("last_name",  u.last_name)
            u.email      = self.cleaned_data.get("email",      u.email)
            u.username   = socio.dni  # Asegurar que el username sea el DNI
            u.is_active  = socio.activo  # Sincronizar estado activo
            u.save()
        
        return socio


# =======================
# Suscripción
# =======================
class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ["socio", "plan", "fecha_inicio", "fecha_fin", "monto", "estado", "auto_renovacion"]
        widgets = {
            # ✅ “almanaque” nativo
            "fecha_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_fin":    forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "monto":        forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "socio":        forms.Select(attrs={"class": "form-select"}),
            "plan":         forms.Select(attrs={"class": "form-select"}),
            "estado":       forms.Select(attrs={"class": "form-select"}),
            # auto_renovacion viene como checkbox (OK)
        }