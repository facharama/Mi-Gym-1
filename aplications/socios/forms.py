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

    def clean(self):
        data  = super().clean()
        dni   = (data.get("dni") or "").strip()
        email = (data.get("email") or "").strip()

        qs = Socio.objects.exclude(pk=self.instance.pk)
        if dni and qs.filter(dni__iexact=dni).exists():
            self.add_error("dni", "Este DNI ya está registrado como socio.")
        if email and qs.filter(email__iexact=email).exists():
            self.add_error("email", "Este email ya está registrado como socio.")

        # Si existiera otro User con ese DNI/email:
        if User.objects.filter(Q(username__iexact=dni) | Q(email__iexact=email)).exclude(pk=getattr(self.instance.user, "pk", None)).exists():
            if dni:   self.add_error("dni", "Ya existe un usuario con este DNI.")
            if email: self.add_error("email", "Ya existe un usuario con este email.")

        if self.errors:
            raise forms.ValidationError("No se pudo guardar: hay datos duplicados.")
        return data

    def save(self, commit=True):
        socio = super().save(commit=False)
        socio.estado = "Activo" if self.cleaned_data.get("activo") else "Inactivo"
        if commit:
            socio.save()
        if socio.user_id:
            u = socio.user
            u.first_name = self.cleaned_data.get("first_name", u.first_name)
            u.last_name  = self.cleaned_data.get("last_name",  u.last_name)
            u.email      = self.cleaned_data.get("email",      u.email)
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