from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Crea grupos base"

    def handle(self, *args, **kwargs):
        for name in ["Socio"]:
            Group.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Grupos creados/actualizados"))
