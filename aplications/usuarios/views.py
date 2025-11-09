# aplications/usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .utils import is_admin, is_socio
from .decorators import role_required
from .forms import UserCreateWithRoleForm


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def crear_usuario(request):
    if request.method == "POST":
        form = UserCreateWithRoleForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Si existe el modelo Socio y el rol elegido fue Socio, crear perfil
            try:
                from aplications.socios.models import Socio  # ajustá si tu modelo se llama distinto
                if form.cleaned_data["rol"] == "Socio":
                    Socio.objects.get_or_create(user=user)
            except Exception:
                # Si no existe el modelo Socio, lo ignoramos
                pass

            return redirect("admin_dashboard")  # o a donde prefieras
    else:
        form = UserCreateWithRoleForm()

    return render(request, "usuarios/crear_usuario.html", {"form": form})


@login_required
def role_redirect(request):
    """Decide a qué dashboard ir después del login."""
    if is_admin(request.user):
        return redirect("admin_dashboard")
    if is_socio(request.user):
        return redirect("socios:panel_socio")  # Nueva URL del panel del socio
    return redirect("login")  # o a una vista "sin rol"


@login_required
@role_required("Administrador")
def admin_dashboard(request):
    from django.db.models import OuterRef, Subquery, Count
    from aplications.ocupacion.models import Acceso, Sucursal
    
    # Subconsulta: para cada (socio, sucursal), traemos el TIPO del último movimiento
    ultimo_tipo_subq = (
        Acceso.objects
        .filter(socio_id=OuterRef("socio_id"), sucursal_id=OuterRef("sucursal_id"))
        .order_by("-fecha_hora")
        .values("tipo")[:1]
    )

    # Filtramos solo los casos cuyo último movimiento fue 'Ingreso'
    ultimos_ingreso = (
        Acceso.objects
        .values("socio_id", "sucursal_id")
        .distinct()
        .annotate(ultimo_tipo=Subquery(ultimo_tipo_subq))
        .filter(ultimo_tipo="Ingreso")
    )

    # Conteo por sucursal
    conteo_por_sucursal = (
        ultimos_ingreso
        .values("sucursal_id")
        .annotate(dentro=Count("socio_id"))
    )
    dentro_map = {row["sucursal_id"]: row["dentro"] for row in conteo_por_sucursal}

    # Armamos respuesta para cada sucursal
    sucursales_data = []
    total_ocupacion = 0
    total_capacidad = 0
    
    for s in Sucursal.objects.all():
        occ = dentro_map.get(s.id, 0)
        cap = s.aforo_maximo if s.aforo_maximo else 100
        total_ocupacion += occ
        total_capacidad += cap
        
        # Calcular porcentaje y nivel de ocupación
        pct = (occ * 100.0 / cap) if cap > 0 else 0.0
        
        # Determinar nivel (Baja/Media/Alta)
        if pct <= 33:
            nivel = "baja"
            color = "#10b981"  # Verde
        elif pct <= 66:
            nivel = "media"
            color = "#f59e0b"  # Amarillo/Naranja
        else:
            nivel = "alta"
            color = "#ef4444"  # Rojo
        
        sucursales_data.append({
            "id": s.id,
            "nombre": s.nombre,
            "ocupacion": occ,
            "capacidad": cap,
            "porcentaje": round(pct, 1),
            "nivel": nivel,
            "color": color,
        })
        print(f"Sucursal {s.id} ({s.nombre}): ocupacion={occ}, capacidad={cap}, porcentaje={pct}")
    
    data = {
        "total_socios": 0,
        "cuotas_pendientes": 0,
        "ocupacion_global": total_ocupacion,
        "capacidad_global": total_capacidad,
        "sucursales": sucursales_data,
    }
    # 👉 usa una plantilla NAMESPACEADA para evitar que Django agarre otra
    return render(request, "usuarios/admin_dashboard.html", data)



@login_required
@role_required("Socio")
def socio_dashboard(request):
    data = {
        "estado_cuota": "paga",
        "rutina_hoy": [],
        "ocupacion_actual": 0,
    }
    return render(request, "dash/socio_dashboard.html", data)

