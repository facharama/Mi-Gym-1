from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Socio, Suscripcion, Plan
from .utils import can_access
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import SocioForm, SuscripcionForm
from django.db import transaction
from django.db.models import ProtectedError

# Create your views here.

@login_required
def eliminar_socio(request, pk):
    """Desactivar socio (soft-delete) marcando activo=False"""
    if request.method == 'POST':
        socio = get_object_or_404(Socio, pk=pk)
        nombre = socio.user.get_full_name() or socio.user.username
        
        try:
            # Soft-delete: marcar como inactivo en lugar de eliminar
            socio.activo = False
            socio.estado = "Inactivo"
            socio.save(update_fields=['activo', 'estado'])
            
            # También desactivar el usuario asociado para que no pueda hacer login
            socio.user.is_active = False
            socio.user.save(update_fields=['is_active'])

            messages.success(request, f"Se desactivó el socio {nombre} correctamente.")
        except Exception as e:
            messages.error(request, f"Error al desactivar el socio: {str(e)}")
            
        return redirect("socios:lista")
    else:
        # Si no es POST, redirigir a la lista
        return redirect("socios:lista")


@login_required
def reactivar_socio(request, pk):
    """Reactivar socio marcando activo=True y permitiendo acceso inmediato"""
    if request.method == 'POST':
        socio = get_object_or_404(Socio, pk=pk, activo=False)
        nombre = socio.user.get_full_name() or socio.user.username
        
        try:
            # Reactivar socio completamente
            socio.activo = True
            socio.estado = "Activo"
            socio.save(update_fields=['activo', 'estado'])
            
            # Reactivar el usuario asociado para que pueda hacer login
            socio.user.is_active = True
            socio.user.save(update_fields=['is_active'])

            messages.success(request, f"Se reactivó el socio {nombre} correctamente. Puede acceder al sistema inmediatamente.")
                
        except Exception as e:
            messages.error(request, f"Error al reactivar el socio: {str(e)}")
            
        return redirect("socios:lista")
    else:
        return redirect("socios:lista")

@login_required
def lista_socios(request):
    from django.core.paginator import Paginator
    
    qs = Socio.objects.select_related("user", "sucursal")
    
    # Filtro por apellido
    ape = request.GET.get("apellido", "").strip()
    if ape:
        qs = qs.filter(user__last_name__icontains=ape)
    
    # Filtro por estado activo/inactivo
    estado_filtro = request.GET.get("estado_activo", "")
    if estado_filtro == "activos":
        qs = qs.filter(activo=True)
    elif estado_filtro == "inactivos":
        qs = qs.filter(activo=False)
    # Si no se especifica filtro, mostrar todos (activos e inactivos)
    
    # Paginación: 10 por página para pantallas grandes
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "socios/lista.html", {
        "socios": page_obj,
        "page_obj": page_obj,
        "estado_filtro": estado_filtro
    })

@login_required
def detalle_socio(request, pk):
    socio = get_object_or_404(Socio.objects.select_related("user", "sucursal"), pk=pk)
    suscripciones = Suscripcion.objects.filter(socio=socio).select_related("plan").order_by("-fecha_fin")
    # planes activos para el modal de 'Registrar pago'
    planes = Plan.objects.filter(activo=True).order_by("nombre")
    # si el socio tiene al menos una suscripción vigente
    activo = can_access(socio)
    return render(request, "socios/detalle.html", {"socio": socio, "suscripciones": suscripciones, "planes": planes, "has_active": activo})

@login_required
def crear_socio(request):
    if request.method == "POST":
        form = SocioForm(request.POST)
        if form.is_valid():
            socio = form.save()
            messages.success(request, "El socio se creó correctamente.")
            return redirect(f"{reverse('socios:detalle', args=[socio.pk])}?created=1")
        else:
            messages.error(request, "El socio ya se encuentra registrado.")
    else:
        form = SocioForm()
    return render(request, "socios/socio_form.html", {"form": form})

@login_required
def editar_socio(request, pk):
    from .forms import SocioEditForm  # importá el nuevo form

    socio = get_object_or_404(Socio, pk=pk)

    if request.method == "POST":
        form = SocioEditForm(request.POST, instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Datos del socio actualizados correctamente.")
            return redirect("socios:detalle", pk=socio.pk)
        else:
            # Mostrar los errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = SocioEditForm(instance=socio)

    return render(request, "socios/editar.html", {"form": form, "socio": socio})


@login_required
def crear_suscripcion(request, socio_id=None):
    initial = {"socio": socio_id} if socio_id else None
    if request.method == "POST":
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            sus = form.save()
            # Si venimos con ?to_pagos=1 redirigimos al formulario de Pago
            if request.GET.get("to_pagos") == "1":
                return redirect(f"{reverse('pagos:pagos_crear')}?suscripcion={sus.pk}")

            return redirect("socios:detalle", pk=form.cleaned_data["socio"].pk)
    else:
        form = SuscripcionForm(initial=initial)
    planes = Plan.objects.filter(activo=True).order_by("nombre")
    return render(request, "socios/form_suscripcion.html", {"form": form, "planes": planes})


@login_required
def suscripciones_pendientes(request):
    """Lista todas las suscripciones en estado 'Pendiente' (pendientes de pago)."""
    qs = Suscripcion.objects.filter(estado="Pendiente").select_related("socio", "plan").order_by("socio__apellido", "socio__nombre")
    return render(request, "socios/suscripciones_pendientes.html", {"suscripciones": qs})


@login_required
def crear_suscripcion_rapida(request):
    """Crea una Suscripcion en estado 'Pendiente' a partir de un POST desde el modal.

    Espera campos POST: socio_id, plan_id, monto (opcional).
    Redirige a la vista de crear pago con ?suscripcion=<id>.
    """
    if request.method != "POST":
        return redirect("socios:lista")

    socio_id = request.POST.get("socio_id")
    plan_id = request.POST.get("plan_id")
    monto = request.POST.get("monto")

    # validaciones mínimas
    try:
        socio = Socio.objects.get(pk=int(socio_id))
    except Exception:
        messages.error(request, "Socio inválido")
        return redirect("socios:detalle", pk=socio_id)

    try:
        plan = Plan.objects.get(pk=int(plan_id))
    except Exception:
        messages.error(request, "Plan inválido")
        return redirect("socios:detalle", pk=socio_id)

    # monto por defecto desde el plan si no se provee
    if not monto:
        monto_value = plan.precio
    else:
        try:
            from decimal import Decimal
            monto_value = Decimal(monto)
        except Exception:
            monto_value = plan.precio

    # Antes de crear, comprobamos que no exista ya una suscripción vigente
    from django.utils import timezone
    hoy = timezone.localdate()
    existe_vigente = Suscripcion.objects.filter(socio=socio, estado="Vigente", fecha_inicio__lte=hoy, fecha_fin__gte=hoy).exists()
    if existe_vigente:
        from django.contrib import messages
        messages.error(request, "El socio ya tiene una suscripción vigente. No se creó una nueva suscripción.")
        return redirect("socios:detalle", pk=socio.pk)

    sus = Suscripcion.objects.create(
        socio=socio,
        plan=plan,
        monto=monto_value,
        estado="Pendiente",
    )

    return redirect(f"{reverse('pagos:pagos_crear')}?suscripcion={sus.pk}")


# ============= PANEL DEL SOCIO =============

@login_required
def panel_socio(request):
    """Dashboard principal del socio con resumen de información"""
    try:
        socio = request.user.perfil_socio
    except:
        messages.error(request, "No tienes un perfil de socio asociado.")
        return redirect('home')
    
    from django.utils import timezone
    from aplications.rutina.models import RutinaAsignacion, RutinaDia
    from aplications.ocupacion.models import Acceso
    
    hoy = timezone.localdate()
    
    # Estado de la cuota - buscar suscripción vigente
    suscripcion_vigente = Suscripcion.objects.filter(
        socio=socio,
        estado='Vigente',
        fecha_inicio__lte=hoy,
        fecha_fin__gte=hoy
    ).select_related('plan').first()
    
    # Rutina del día
    asignacion_vigente = RutinaAsignacion.objects.filter(
        socio=socio,
        estado='Vigente'
    ).select_related('rutina').first()
    
    dia_semana = hoy.isoweekday()  # 1=Lunes, 7=Domingo
    rutina_hoy = None
    if asignacion_vigente:
        rutina_hoy = RutinaDia.objects.filter(
            rutina=asignacion_vigente.rutina,
            dia_semana=dia_semana
        ).prefetch_related('detalles__ejercicio').first()
    
    # Ocupación actual - usar el mismo método que el admin
    # Para cada socio en la sucursal, verificar si su último movimiento fue "Ingreso"
    from django.db.models import OuterRef, Subquery, Count
    
    ultimo_tipo_subq = (
        Acceso.objects
        .filter(socio_id=OuterRef("socio_id"), sucursal_id=socio.sucursal.id)
        .order_by("-fecha_hora")
        .values("tipo")[:1]
    )

    # Contamos socios cuyo último movimiento fue 'Ingreso' en esta sucursal
    ocupacion_actual = (
        Acceso.objects
        .filter(sucursal_id=socio.sucursal.id)
        .values("socio_id")
        .distinct()
        .annotate(ultimo_tipo=Subquery(ultimo_tipo_subq))
        .filter(ultimo_tipo="Ingreso")
        .count()
    )
    aforo_maximo = socio.sucursal.aforo_maximo
    porcentaje_ocupacion = int((ocupacion_actual / aforo_maximo) * 100) if aforo_maximo > 0 else 0
    
    # Verificar si el socio actual está registrado (dentro del gym)
    ultimo_acceso = Acceso.objects.filter(socio=socio).order_by('-fecha_hora').first()
    esta_en_gym = ultimo_acceso and ultimo_acceso.tipo == 'Ingreso'
    
    # Si está en el gym, calcular tiempo de entrenamiento
    tiempo_entrenando = None
    if esta_en_gym and ultimo_acceso:
        from datetime import datetime
        tiempo_delta = timezone.now() - ultimo_acceso.fecha_hora
        minutos = int(tiempo_delta.total_seconds() / 60)
        if minutos < 60:
            tiempo_entrenando = f"{minutos} minutos"
        else:
            horas = minutos // 60
            mins_restantes = minutos % 60
            tiempo_entrenando = f"{horas}h {mins_restantes}m"
    
    context = {
        'socio': socio,
        'suscripcion_vigente': suscripcion_vigente,
        'asignacion_vigente': asignacion_vigente,
        'rutina_hoy': rutina_hoy,
        'dia_semana': dia_semana,
        'ocupacion_actual': ocupacion_actual,
        'aforo_maximo': aforo_maximo,
        'porcentaje_ocupacion': porcentaje_ocupacion,
        'esta_en_gym': esta_en_gym,
        'tiempo_entrenando': tiempo_entrenando,
    }
    
    return render(request, 'socios/panel/dashboard.html', context)


@login_required
def mi_cuota(request):
    """Vista de consulta de cuota del socio"""
    try:
        socio = request.user.perfil_socio
    except:
        messages.error(request, "No tienes un perfil de socio asociado.")
        return redirect('home')
    
    from django.utils import timezone
    hoy = timezone.localdate()
    
    # Suscripción actual
    suscripcion_actual = Suscripcion.objects.filter(
        socio=socio,
        estado='Vigente'
    ).select_related('plan').order_by('-fecha_inicio').first()
    
    # Todas las suscripciones con sus pagos
    suscripciones = Suscripcion.objects.filter(
        socio=socio
    ).select_related('plan').prefetch_related('pagos').order_by('-fecha_inicio')
    
    # Calcular si está al día
    al_dia = False
    dias_restantes = None
    dias_vencido = None
    if suscripcion_actual and suscripcion_actual.fecha_fin:
        dias_restantes = (suscripcion_actual.fecha_fin - hoy).days
        al_dia = dias_restantes >= 0
        if not al_dia:
            dias_vencido = abs(dias_restantes + 1)
    
    context = {
        'socio': socio,
        'suscripcion_actual': suscripcion_actual,
        'suscripciones': suscripciones,
        'al_dia': al_dia,
        'dias_restantes': dias_restantes,
        'dias_vencido': dias_vencido,
    }
    
    return render(request, 'socios/panel/mi_cuota.html', context)


@login_required
def mi_rutina(request):
    """Vista de la rutina del día del socio"""
    try:
        socio = request.user.perfil_socio
    except:
        messages.error(request, "No tienes un perfil de socio asociado.")
        return redirect('home')
    
    from django.utils import timezone
    from aplications.rutina.models import RutinaAsignacion, RutinaDia
    
    hoy = timezone.localdate()
    dia_semana = hoy.isoweekday()
    
    # Buscar asignación vigente
    asignacion = RutinaAsignacion.objects.filter(
        socio=socio,
        estado='Vigente'
    ).select_related('rutina__creada_por__user').first()
    
    rutina_dia = None
    if asignacion:
        rutina_dia = RutinaDia.objects.filter(
            rutina=asignacion.rutina,
            dia_semana=dia_semana
        ).prefetch_related('detalles__ejercicio').first()
    
    context = {
        'socio': socio,
        'asignacion': asignacion,
        'rutina_dia': rutina_dia,
        'dia_semana': dia_semana,
        'hoy': hoy,
    }
    
    return render(request, 'socios/panel/mi_rutina.html', context)


@login_required
def ocupacion_gimnasio(request):
    """Vista de ocupación en tiempo real del gimnasio"""
    try:
        socio = request.user.perfil_socio
    except:
        messages.error(request, "No tienes un perfil de socio asociado.")
        return redirect('home')
    
    from django.utils import timezone
    from aplications.ocupacion.models import Acceso
    from django.db.models import OuterRef, Subquery, Count
    
    # Ocupación actual de la sucursal del socio - usar el mismo método que el admin
    ultimo_tipo_subq = (
        Acceso.objects
        .filter(socio_id=OuterRef("socio_id"), sucursal_id=socio.sucursal.id)
        .order_by("-fecha_hora")
        .values("tipo")[:1]
    )

    # Contamos socios cuyo último movimiento fue 'Ingreso' en esta sucursal
    ocupacion_actual = (
        Acceso.objects
        .filter(sucursal_id=socio.sucursal.id)
        .values("socio_id")
        .distinct()
        .annotate(ultimo_tipo=Subquery(ultimo_tipo_subq))
        .filter(ultimo_tipo="Ingreso")
        .count()
    )
    aforo_maximo = socio.sucursal.aforo_maximo
    porcentaje = int((ocupacion_actual / aforo_maximo) * 100) if aforo_maximo > 0 else 0
    
    # Determinar nivel de ocupación
    umbral_bajo = socio.sucursal.umbral_bajo_pct
    umbral_medio = socio.sucursal.umbral_medio_pct
    
    if porcentaje < umbral_bajo:
        nivel = 'bajo'
        nivel_texto = 'Baja'
        nivel_color = 'success'
    elif porcentaje < umbral_medio:
        nivel = 'medio'
        nivel_texto = 'Media'
        nivel_color = 'warning'
    else:
        nivel = 'alto'
        nivel_texto = 'Alta'
        nivel_color = 'danger'
    
    context = {
        'socio': socio,
        'ocupacion_actual': ocupacion_actual,
        'aforo_maximo': aforo_maximo,
        'porcentaje': porcentaje,
        'nivel': nivel,
        'nivel_texto': nivel_texto,
        'nivel_color': nivel_color,
    }
    
    return render(request, 'socios/panel/ocupacion.html', context)


@login_required
def mi_qr(request):
    """Genera y muestra el código QR del socio para acceso al gimnasio"""
    try:
        socio = request.user.perfil_socio
    except:
        messages.error(request, "No tienes un perfil de socio asociado.")
        return redirect('home')
    
    import qrcode
    from io import BytesIO
    import base64
    
    # Generar código QR con el email del socio (el simulador usará esto)
    qr_data = socio.user.email
    
    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Generar imagen
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir a base64 para mostrar en HTML
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'socio': socio,
        'qr_image': img_str,
        'qr_data': qr_data,
    }
    
    return render(request, 'socios/panel/mi_qr.html', context)