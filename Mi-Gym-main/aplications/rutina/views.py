from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import RutinaAsignacion, RutinaDia
from .forms import RutinaAsignacionForm, RutinaForm

# Create your views here.

@login_required
def asignar_rutina(request):
    if request.method == "POST":
        form = RutinaAsignacionForm(request.POST)
        if form.is_valid():
            asig = form.save()
            return redirect("socios:detalle", pk=asig.socio_id)
    else:
        form = RutinaAsignacionForm()
    return render(request, "rutina/form_asignacion.html", {"form": form})

@login_required
def rutina_de_hoy(request, socio_id):
    """Muestra la rutina del día para un socio."""
    hoy = date.today().isoweekday()  # 1=Lun..7=Dom
    asig = (RutinaAsignacion.objects
            .select_related("rutina", "socio")
            .filter(socio_id=socio_id, estado="Vigente")
            .order_by("-fecha_inicio")
            .first())
    dia = None
    if asig:
        dia = (RutinaDia.objects
               .select_related("rutina")
               .prefetch_related("detalles__ejercicio")
               .filter(rutina=asig.rutina, dia_semana=hoy)
               .first())
    return render(request, "rutina/rutina_hoy.html", {"asig": asig, "dia": dia, "hoy": hoy})

@login_required
def crear_rutina(request):
    if request.method == "POST":
        form = RutinaForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("rutina_hoy", socio_id=request.user.socio.id)  # ejemplo
    else:
        form = RutinaForm()
    return render(request, "rutina/form_rutina.html", {"form": form})
