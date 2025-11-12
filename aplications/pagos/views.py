from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PagoForm

# Create your views here.

@login_required
def crear_pago(request):
    if request.method == "POST":
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save()
            socio_id = pago.suscripcion.socio_id
            return redirect("socios:detalle", pk=socio_id)
    else:
        # allow prefilling suscripcion via GET param ?suscripcion=<id>
        initial = {}
        sus_id = request.GET.get("suscripcion")
        if sus_id:
            initial["suscripcion"] = sus_id
        form = PagoForm(initial=initial)
    return render(request, "pagos/form_pago.html", {"form": form})

@login_required
def listar_pagos(request):
    from .models import Pago
    from aplications.socios.models import Plan
    pagos = Pago.objects.select_related("suscripcion", "suscripcion__socio", "suscripcion__plan").order_by("-fecha_pago")

    # Filtros avanzados
    socio = request.GET.get("socio", "").strip()
    metodo = request.GET.get("metodo", "")
    plan_id = request.GET.get("plan", "")
    fecha = request.GET.get("fecha", "")

    if socio:
        pagos = pagos.filter(
            models.Q(suscripcion__socio__user__username__icontains=socio) |
            models.Q(suscripcion__socio__nombre__icontains=socio) |
            models.Q(suscripcion__socio__apellido__icontains=socio)
        )
    if metodo:
        pagos = pagos.filter(metodo=metodo)
    if plan_id:
        pagos = pagos.filter(suscripcion__plan__id=plan_id)
    if fecha:
        pagos = pagos.filter(fecha_pago__date=fecha)

    planes = Plan.objects.filter(activo=True).order_by("nombre")
    return render(request, "pagos/lista.html", {"pagos": pagos, "planes": planes})

@login_required
def detalle_pago(request, pk):
    """Vista de detalle de pago - solo lectura"""
    from .models import Pago
    pago = get_object_or_404(Pago, pk=pk)
    
    context = {
        'pago': pago,
        'socio': pago.suscripcion.socio,
        'suscripcion': pago.suscripcion,
        'plan': pago.suscripcion.plan,
    }
    return render(request, "pagos/detalle.html", context)
