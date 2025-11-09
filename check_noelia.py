from aplications.socios.models import Socio
from django.contrib.auth import get_user_model

User = get_user_model()

socio = Socio.objects.get(dni='45678901')
print(f'Socio: {socio.nombre} {socio.apellido}')
print(f'Socio.email: {socio.email}')
print(f'Socio.user_id: {socio.user_id}')

if socio.user:
    print(f'User.id: {socio.user.id}')
    print(f'User.email: {socio.user.email}')
    print(f'User.username: {socio.user.username}')
    
# Buscar otros usuarios con ese email
otros_users = User.objects.filter(email__iexact='noeliasramoss17@gmail.com').exclude(pk=socio.user_id)
print(f'\nOtros usuarios con ese email: {otros_users.count()}')
for u in otros_users:
    print(f'  - User #{u.id}: {u.username} - {u.email}')
