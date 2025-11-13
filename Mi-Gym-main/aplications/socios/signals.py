from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Socio

def _send_set_password_email(user, *, domain=None):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    base = domain or getattr(settings, "SITE_DOMAIN", "http://localhost:8000")
    path = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
    url = f"{base}{path}"

    subject = "Bienvenido/a a MiGym – Activá tu cuenta"
    text = f"""Hola {user.first_name or user.username},

Te creamos un usuario en MiGym. Establecé tu contraseña acá:
{url}
"""
    html = f"""
    <p>Hola {user.first_name or user.username},</p>
    <p>Tu usuario en <strong>MiGym</strong> está listo. Para ingresar por primera vez, establecé tu contraseña:</p>
    <p><a href="{url}">{url}</a></p>
    """

    msg = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html, "text/html")
    msg.send()

@receiver(post_save, sender=Socio)
def crear_user_y_enviar_mail(sender, instance: Socio, created, **kwargs):
    if not created:
        return

    socio = instance

   
    if socio.user:
        _send_set_password_email(socio.user)
        return

    user, user_created = User.objects.get_or_create(
        username=socio.email,
        defaults={
            "email": socio.email,
            "first_name": socio.nombre,
            "last_name": socio.apellido,
            "is_active": True,
        },
    )
    if user_created:
        user.set_unusable_password()
        user.save()


    group, _ = Group.objects.get_or_create(name="Socio")
    user.groups.add(group)

    socio.user = user
    socio.save(update_fields=["user"])

    _send_set_password_email(user)
