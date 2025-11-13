"""
Comando para cargar datos de demostración en el sistema Mi-Gym.
Uso: python manage.py cargar_datos_demo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import random

from aplications.socios.models import Sucursal, Socio, Instructor, Plan, Suscripcion
from aplications.rutina.models import Ejercicio, Rutina, RutinaAsignacion, RutinaDia, RutinaDetalle
from aplications.pagos.models import Pago
from aplications.ocupacion.models import Acceso, ActiveSession

User = get_user_model()


class Command(BaseCommand):
    help = 'Carga datos de demostración: socios, planes, suscripciones, rutinas, pagos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--socios',
            type=int,
            default=20,
            help='Número de socios a crear (default: 20)'
        )
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Eliminar datos existentes antes de crear nuevos'
        )

    def handle(self, *args, **options):
        num_socios = options['socios']
        limpiar = options['limpiar']

        if limpiar:
            self.stdout.write(self.style.WARNING('Limpiando datos existentes...'))
            self.limpiar_datos()

        self.stdout.write(self.style.SUCCESS('Iniciando carga de datos de demostración...'))
        
        # Crear sucursales
        sucursales = self.crear_sucursales()
        
        # Crear planes
        planes = self.crear_planes()
        
        # Crear instructores
        instructores = self.crear_instructores(sucursales)
        
        # Crear ejercicios
        ejercicios = self.crear_ejercicios()
        
        # Crear rutinas
        rutinas = self.crear_rutinas(instructores, ejercicios)
        
        # Crear socios
        socios = self.crear_socios(sucursales, num_socios)
        
        # Crear suscripciones y pagos
        self.crear_suscripciones_y_pagos(socios, planes)
        
        # Asignar rutinas a socios
        self.asignar_rutinas(socios, rutinas)
        
        # Crear registros de ocupación
        self.crear_registros_ocupacion(socios, sucursales)
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Datos de demostración cargados exitosamente!\n'
            f'   - {len(sucursales)} sucursales\n'
            f'   - {len(planes)} planes\n'
            f'   - {len(instructores)} instructores\n'
            f'   - {len(ejercicios)} ejercicios\n'
            f'   - {len(rutinas)} rutinas\n'
            f'   - {len(socios)} socios\n'
        ))

    def limpiar_datos(self):
        """Elimina datos existentes (opcional)"""
        ActiveSession.objects.all().delete()
        Acceso.objects.all().delete()
        RutinaDetalle.objects.all().delete()
        RutinaDia.objects.all().delete()
        RutinaAsignacion.objects.all().delete()
        Rutina.objects.all().delete()
        Ejercicio.objects.all().delete()
        Pago.objects.all().delete()
        Suscripcion.objects.all().delete()
        Socio.objects.all().delete()
        Instructor.objects.all().delete()
        Plan.objects.all().delete()
        # No eliminamos sucursales para mantener las configuradas

    def crear_sucursales(self):
        """Crea sucursales de ejemplo"""
        self.stdout.write('📍 Creando sucursales...')
        sucursales_data = [
            {
                'nombre': 'Mi-Gym Centro',
                'direccion': 'Av. Principal 123',
                'telefono': '0351-4567890',
                'email': 'centro@migym.com',
                'aforo_maximo': 80,
            },
            {
                'nombre': 'Mi-Gym Norte',
                'direccion': 'Calle Norte 456',
                'telefono': '0351-4567891',
                'email': 'norte@migym.com',
                'aforo_maximo': 100,
            },
        ]
        
        sucursales = []
        for data in sucursales_data:
            sucursal, created = Sucursal.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            sucursales.append(sucursal)
            if created:
                self.stdout.write(f'  ✓ {sucursal.nombre}')
        
        return sucursales

    def crear_planes(self):
        """Crea planes de suscripción"""
        self.stdout.write('💳 Creando planes...')
        planes_data = [
            {
                'nombre': 'Plan Mensual',
                'descripcion': 'Acceso completo por 1 mes',
                'duracion_dias': 30,
                'precio': Decimal('5000.00'),
                'requiere_certificado': False,
            },
            {
                'nombre': 'Plan Trimestral',
                'descripcion': 'Acceso completo por 3 meses',
                'duracion_dias': 90,
                'precio': Decimal('13500.00'),
                'requiere_certificado': False,
            },
            {
                'nombre': 'Plan Semestral',
                'descripcion': 'Acceso completo por 6 meses',
                'duracion_dias': 180,
                'precio': Decimal('25000.00'),
                'requiere_certificado': False,
            },
            {
                'nombre': 'Plan Anual',
                'descripcion': 'Acceso completo por 12 meses',
                'duracion_dias': 365,
                'precio': Decimal('45000.00'),
                'requiere_certificado': True,
            },
        ]
        
        planes = []
        for data in planes_data:
            plan, created = Plan.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            planes.append(plan)
            if created:
                self.stdout.write(f'  ✓ {plan.nombre} - ${plan.precio}')
        
        return planes

    def crear_instructores(self, sucursales):
        """Crea instructores"""
        self.stdout.write('👨‍🏫 Creando instructores...')
        instructores_data = [
            {'username': 'instructor1', 'first_name': 'Carlos', 'last_name': 'Pérez', 'especialidad': 'Musculación'},
            {'username': 'instructor2', 'first_name': 'María', 'last_name': 'González', 'especialidad': 'Funcional'},
            {'username': 'instructor3', 'first_name': 'Juan', 'last_name': 'Martínez', 'especialidad': 'Cardio'},
        ]
        
        instructores = []
        for i, data in enumerate(instructores_data):
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': f"{data['username']}@migym.com",
                }
            )
            if created:
                user.set_password('instructor123')
                user.save()
            
            instructor, created = Instructor.objects.get_or_create(
                user=user,
                defaults={
                    'sucursal': sucursales[i % len(sucursales)],
                    'especialidad': data['especialidad'],
                }
            )
            instructores.append(instructor)
            if created:
                self.stdout.write(f'  ✓ {instructor}')
        
        return instructores

    def crear_ejercicios(self):
        """Crea ejercicios básicos"""
        self.stdout.write('💪 Creando ejercicios...')
        ejercicios_data = [
            {'nombre': 'Press de Banca', 'grupo_muscular': 'Pecho'},
            {'nombre': 'Sentadillas', 'grupo_muscular': 'Piernas'},
            {'nombre': 'Peso Muerto', 'grupo_muscular': 'Espalda'},
            {'nombre': 'Press Militar', 'grupo_muscular': 'Hombros'},
            {'nombre': 'Dominadas', 'grupo_muscular': 'Espalda'},
            {'nombre': 'Curl de Bíceps', 'grupo_muscular': 'Brazos'},
            {'nombre': 'Extensión de Tríceps', 'grupo_muscular': 'Brazos'},
            {'nombre': 'Fondos en Paralelas', 'grupo_muscular': 'Pecho'},
            {'nombre': 'Remo con Barra', 'grupo_muscular': 'Espalda'},
            {'nombre': 'Prensa de Piernas', 'grupo_muscular': 'Piernas'},
            {'nombre': 'Elevaciones Laterales', 'grupo_muscular': 'Hombros'},
            {'nombre': 'Abdominales', 'grupo_muscular': 'Core'},
            {'nombre': 'Plancha', 'grupo_muscular': 'Core'},
            {'nombre': 'Burpees', 'grupo_muscular': 'Cardio'},
            {'nombre': 'Jumping Jacks', 'grupo_muscular': 'Cardio'},
        ]
        
        ejercicios = []
        for data in ejercicios_data:
            ejercicio, created = Ejercicio.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            ejercicios.append(ejercicio)
        
        self.stdout.write(f'  ✓ {len(ejercicios)} ejercicios creados')
        return ejercicios

    def crear_rutinas(self, instructores, ejercicios):
        """Crea rutinas de ejemplo"""
        self.stdout.write('📋 Creando rutinas...')
        rutinas_data = [
            {
                'nombre': 'Rutina Principiante Full Body',
                'objetivo': 'Acondicionamiento general',
                'dias': [
                    {'dia': 1, 'ejercicios': [0, 1, 5, 11]},
                    {'dia': 3, 'ejercicios': [2, 3, 6, 12]},
                    {'dia': 5, 'ejercicios': [4, 9, 10, 13]},
                ]
            },
            {
                'nombre': 'Rutina Hipertrofia',
                'objetivo': 'Ganancia muscular',
                'dias': [
                    {'dia': 1, 'ejercicios': [0, 7, 5]},
                    {'dia': 2, 'ejercicios': [1, 9, 11]},
                    {'dia': 4, 'ejercicios': [2, 8, 4]},
                    {'dia': 5, 'ejercicios': [3, 10, 6]},
                ]
            },
            {
                'nombre': 'Rutina Funcional',
                'objetivo': 'Resistencia y funcionalidad',
                'dias': [
                    {'dia': 1, 'ejercicios': [13, 14, 12, 11]},
                    {'dia': 3, 'ejercicios': [1, 4, 0, 12]},
                    {'dia': 5, 'ejercicios': [14, 13, 11, 9]},
                ]
            },
        ]
        
        rutinas = []
        for i, rutina_data in enumerate(rutinas_data):
            rutina, created = Rutina.objects.get_or_create(
                nombre=rutina_data['nombre'],
                defaults={
                    'objetivo': rutina_data['objetivo'],
                    'creada_por': instructores[i % len(instructores)],
                }
            )
            
            if created:
                # Crear días y detalles
                for dia_info in rutina_data['dias']:
                    dia = RutinaDia.objects.create(
                        rutina=rutina,
                        dia_semana=dia_info['dia']
                    )
                    
                    for orden, ejercicio_idx in enumerate(dia_info['ejercicios'], 1):
                        RutinaDetalle.objects.create(
                            rutina_dia=dia,
                            ejercicio=ejercicios[ejercicio_idx],
                            orden=orden,
                            series=random.randint(3, 4),
                            repeticiones=random.randint(8, 12),
                            descanso_seg=random.randint(60, 90),
                        )
                
                self.stdout.write(f'  ✓ {rutina.nombre}')
            
            rutinas.append(rutina)
        
        return rutinas

    def crear_socios(self, sucursales, num_socios):
        """Crea socios de ejemplo"""
        self.stdout.write(f'👥 Creando {num_socios} socios...')
        
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Pedro', 'Laura', 'Diego', 'Sofia', 
                   'Miguel', 'Valentina', 'Luis', 'Camila', 'Jorge', 'Lucía', 'Fernando',
                   'Gabriela', 'Roberto', 'Martina', 'Pablo', 'Julia', 'Andrés', 'Carolina']
        apellidos = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez',
                     'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez',
                     'Díaz', 'Cruz', 'Morales', 'Jiménez', 'Ruiz', 'Hernández']
        
        socios = []
        for i in range(num_socios):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            dni = f"{20000000 + i:08d}"
            
            socio, created = Socio.objects.get_or_create(
                dni=dni,
                defaults={
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': f'{nombre.lower()}.{apellido.lower()}{i}@email.com',
                    'sucursal': random.choice(sucursales),
                    'estado': 'Activo',
                }
            )
            
            if created:
                socios.append(socio)
        
        self.stdout.write(f'  ✓ {len(socios)} socios creados')
        return socios

    def crear_suscripciones_y_pagos(self, socios, planes):
        """Crea suscripciones y pagos para los socios"""
        self.stdout.write('💰 Creando suscripciones y pagos...')
        
        metodos_pago = ['Efectivo', 'Debito', 'Credito', 'Transferencia', 'MP']
        hoy = timezone.localdate()
        
        for socio in socios:
            # 80% tienen suscripción vigente, 15% vencida, 5% pendiente
            rand = random.random()
            
            if rand < 0.80:  # Vigente
                plan = random.choice(planes)
                dias_atras = random.randint(1, 60)
                fecha_inicio = hoy - timedelta(days=dias_atras)
                
                suscripcion = Suscripcion.objects.create(
                    socio=socio,
                    plan=plan,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_inicio + timedelta(days=plan.duracion_dias - 1),
                    monto=plan.precio,
                    estado='Vigente',
                )
                
                # Crear pago
                Pago.objects.create(
                    suscripcion=suscripcion,
                    monto=plan.precio,
                    metodo=random.choice(metodos_pago),
                    comprobante=f'COMP-{random.randint(10000, 99999)}',
                )
                
            elif rand < 0.95:  # Vencida
                plan = random.choice(planes[:2])  # Planes más cortos
                dias_atras = random.randint(plan.duracion_dias + 5, plan.duracion_dias + 60)
                fecha_inicio = hoy - timedelta(days=dias_atras)
                
                suscripcion = Suscripcion.objects.create(
                    socio=socio,
                    plan=plan,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_inicio + timedelta(days=plan.duracion_dias - 1),
                    monto=plan.precio,
                    estado='Vencida',
                )
                
                Pago.objects.create(
                    suscripcion=suscripcion,
                    monto=plan.precio,
                    metodo=random.choice(metodos_pago),
                )
            else:  # Pendiente (sin pago)
                plan = random.choice(planes)
                Suscripcion.objects.create(
                    socio=socio,
                    plan=plan,
                    monto=plan.precio,
                    estado='Pendiente',
                )
        
        total_suscripciones = Suscripcion.objects.count()
        total_pagos = Pago.objects.count()
        self.stdout.write(f'  ✓ {total_suscripciones} suscripciones y {total_pagos} pagos creados')

    def asignar_rutinas(self, socios, rutinas):
        """Asigna rutinas a socios"""
        self.stdout.write('📊 Asignando rutinas a socios...')
        
        hoy = timezone.localdate()
        asignaciones = 0
        
        for socio in socios:
            # 70% de los socios tienen rutina asignada
            if random.random() < 0.70:
                rutina = random.choice(rutinas)
                dias_atras = random.randint(5, 30)
                fecha_inicio = hoy - timedelta(days=dias_atras)
                
                RutinaAsignacion.objects.create(
                    rutina=rutina,
                    socio=socio,
                    fecha_inicio=fecha_inicio,
                    estado='Vigente',
                )
                asignaciones += 1
        
        self.stdout.write(f'  ✓ {asignaciones} rutinas asignadas')

    def crear_registros_ocupacion(self, socios, sucursales):
        """Crea registros de acceso (ingresos y egresos) y sesiones activas"""
        self.stdout.write('🚪 Creando registros de ocupación...')
        
        ahora = timezone.now()
        hoy = ahora.date()
        
        # Crear accesos históricos (últimos 7 días)
        accesos_historicos = 0
        for dia in range(7, 0, -1):
            fecha = ahora - timedelta(days=dia)
            # Simular entre 15-30 accesos por día
            num_accesos = random.randint(15, 30)
            socios_del_dia = random.sample(socios, min(num_accesos, len(socios)))
            
            for socio in socios_del_dia:
                sucursal = socio.sucursal
                # Hora de ingreso (entre 6:00 y 21:00)
                hora_ingreso = fecha.replace(
                    hour=random.randint(6, 21),
                    minute=random.randint(0, 59),
                    second=0,
                    microsecond=0
                )
                
                # Crear ingreso
                Acceso.objects.create(
                    socio=socio,
                    sucursal=sucursal,
                    tipo='Ingreso',
                    fecha_hora=hora_ingreso
                )
                accesos_historicos += 1
                
                # Duración de estadía (60-120 minutos)
                duracion = random.randint(60, 120)
                hora_egreso = hora_ingreso + timedelta(minutes=duracion)
                
                # Crear egreso
                Acceso.objects.create(
                    socio=socio,
                    sucursal=sucursal,
                    tipo='Egreso',
                    fecha_hora=hora_egreso
                )
                accesos_historicos += 1
        
        # Crear accesos del día actual con diferentes estados
        # 1. Personas que ya ingresaron y egresaron hoy (completados)
        socios_completados = random.sample(socios, random.randint(5, 10))
        for socio in socios_completados:
            sucursal = socio.sucursal
            hora_ingreso = ahora.replace(
                hour=random.randint(6, max(6, ahora.hour - 2)),
                minute=random.randint(0, 59),
                second=0,
                microsecond=0
            )
            
            Acceso.objects.create(
                socio=socio,
                sucursal=sucursal,
                tipo='Ingreso',
                fecha_hora=hora_ingreso
            )
            
            duracion = random.randint(60, 120)
            hora_egreso = hora_ingreso + timedelta(minutes=duracion)
            
            Acceso.objects.create(
                socio=socio,
                sucursal=sucursal,
                tipo='Egreso',
                fecha_hora=hora_egreso
            )
        
        # 2. Personas actualmente dentro (con sesiones activas)
        socios_activos = [s for s in socios if s not in socios_completados]
        num_activos = random.randint(8, 15)
        socios_dentro = random.sample(socios_activos, min(num_activos, len(socios_activos)))
        
        sesiones_activas = 0
        for socio in socios_dentro:
            sucursal = socio.sucursal
            # Ingresaron hace 15-90 minutos
            minutos_dentro = random.randint(15, 90)
            hora_ingreso = ahora - timedelta(minutes=minutos_dentro)
            
            # Crear acceso de ingreso
            Acceso.objects.create(
                socio=socio,
                sucursal=sucursal,
                tipo='Ingreso',
                fecha_hora=hora_ingreso
            )
            
            # Crear sesión activa
            ActiveSession.objects.create(
                member=socio,
                check_in_at=hora_ingreso,
                status='ACTIVE'
            )
            sesiones_activas += 1
        
        total_accesos = Acceso.objects.count()
        
        self.stdout.write(f'  ✓ {accesos_historicos} accesos históricos (últimos 7 días)')
        self.stdout.write(f'  ✓ {len(socios_completados)} socios con sesión completada hoy')
        self.stdout.write(f'  ✓ {sesiones_activas} socios actualmente dentro del gimnasio')
        self.stdout.write(f'  ✓ Total de registros de acceso: {total_accesos}')
