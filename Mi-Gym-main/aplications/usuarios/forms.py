from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class UserCreateWithRoleForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = (("Socio", "Socio"), ("Administrador", "Administrador"))
    rol = forms.ChoiceField(choices=ROLE_CHOICES, label="Rol")
    superuser = forms.BooleanField(required=False, label="Dar permisos de superusuario (admin de Django)")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "rol", "superuser")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        rol = self.cleaned_data["rol"]

        if rol == "Administrador":
            user.is_staff = True
            if self.cleaned_data.get("superuser"):
                user.is_superuser = True

        if commit:
            user.save()
            g, _ = Group.objects.get_or_create(name=rol)
            user.groups.add(g)
        return user
