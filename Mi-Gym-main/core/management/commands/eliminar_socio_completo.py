"""
Comando para eliminar completamente un socio por DNI
Uso: python manage.py eliminar_socio_completo <dni>
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from aplications.socios.models import Socio

User = get_user_model()


class Command(BaseCommand):
    help = 'Elimina completamente un socio y su usuario asociado por DNI'

    def add_arguments(self, parser):
        parser.add_argument('dni', type=str, help='DNI del socio a eliminar')

    def handle(self, *args, **options):
        dni = options['dni']
        
        try:
            socio = Socio.objects.get(dni=dni)
            self.stdout.write(f'Encontrado socio: {socio.nombre} {socio.apellido} (DNI: {socio.dni})')
            
            # Guardar referencia al usuario
            usuario = socio.user
            
            # Eliminar socio (CASCADE eliminara suscripciones, pagos, etc)
            socio.delete()
            self.stdout.write(self.style.SUCCESS(f'Socio eliminado correctamente'))
            
            # Eliminar usuario asociado
            if usuario:
                username = usuario.username
                email = usuario.email
                usuario.delete()
                self.stdout.write(self.style.SUCCESS(f'Usuario eliminado: {username} ({email})'))
            
            self.stdout.write(self.style.SUCCESS(f'\nEliminacion completa exitosa!'))
            
        except Socio.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No se encontro el socio con DNI {dni}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
