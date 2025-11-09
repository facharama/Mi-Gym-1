from django.contrib.auth import get_user_model
from aplications.socios.models import Socio

User = get_user_model()

# Buscar y eliminar el socio
try:
    socio = Socio.objects.get(dni='45678901')
    print(f'Encontrado socio: {socio.nombre} {socio.apellido} (DNI: {socio.dni})')
    
    # Guardar referencia al usuario antes de eliminar el socio
    usuario = socio.user
    
    # Eliminar el socio (esto eliminará suscripciones, pagos, etc por CASCADE)
    socio.delete()
    print(f'✅ Socio eliminado correctamente')
    
    # Eliminar el usuario asociado
    if usuario:
        username = usuario.username
        usuario.delete()
        print(f'✅ Usuario eliminado: {username}')
    
    print('\n✅ Noelia Ramos Sabio eliminada completamente del sistema')
    
except Socio.DoesNotExist:
    print('❌ No se encontró el socio con DNI 45678901')
except Exception as e:
    print(f'❌ Error: {e}')
