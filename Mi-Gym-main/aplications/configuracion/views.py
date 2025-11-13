from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from aplications.socios.models import Plan, Sucursal
from aplications.rutina.models import Ejercicio, Rutina, RutinaDia, RutinaDetalle
from .forms import (
    PlanForm, SucursalForm, EjercicioForm, 
    RutinaFormConfig, RutinaDiaFormConfig, RutinaDetalleFormConfig
)


# ============= PLANES =============

@login_required
def planes_lista(request):
    """Lista todos los planes"""
    planes = Plan.objects.all().order_by('-activo', 'nombre')
    return render(request, 'configuracion/planes/lista.html', {'planes': planes})


@login_required
def plan_crear(request):
    """Crear un nuevo plan"""
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save()
            messages.success(request, f'Plan "{plan.nombre}" creado correctamente.')
            return redirect('configuracion:planes_lista')
    else:
        form = PlanForm()
    return render(request, 'configuracion/planes/form.html', {'form': form, 'titulo': 'Nuevo Plan'})


@login_required
def plan_editar(request, pk):
    """Editar un plan existente"""
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, f'Plan "{plan.nombre}" actualizado correctamente.')
            return redirect('configuracion:planes_lista')
    else:
        form = PlanForm(instance=plan)
    return render(request, 'configuracion/planes/form.html', {'form': form, 'titulo': 'Editar Plan', 'plan': plan})


@login_required
def plan_eliminar(request, pk):
    """Eliminar un plan"""
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        nombre = plan.nombre
        plan.delete()
        messages.success(request, f'Plan "{nombre}" eliminado correctamente.')
    return redirect('configuracion:planes_lista')


# ============= SUCURSALES =============

@login_required
def sucursales_lista(request):
    """Lista todas las sucursales"""
    sucursales = Sucursal.objects.all().order_by('-activo', 'nombre')
    return render(request, 'configuracion/sucursales/lista.html', {'sucursales': sucursales})


@login_required
def sucursal_crear(request):
    """Crear una nueva sucursal"""
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            sucursal = form.save()
            messages.success(request, f'Sucursal "{sucursal.nombre}" creada correctamente.')
            return redirect('configuracion:sucursales_lista')
    else:
        form = SucursalForm()
    return render(request, 'configuracion/sucursales/form.html', {'form': form, 'titulo': 'Nueva Sucursal'})


@login_required
def sucursal_editar(request, pk):
    """Editar una sucursal existente"""
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sucursal "{sucursal.nombre}" actualizada correctamente.')
            return redirect('configuracion:sucursales_lista')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'configuracion/sucursales/form.html', {'form': form, 'titulo': 'Editar Sucursal', 'sucursal': sucursal})


@login_required
def sucursal_eliminar(request, pk):
    """Eliminar una sucursal"""
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        nombre = sucursal.nombre
        try:
            sucursal.delete()
            messages.success(request, f'Sucursal "{nombre}" eliminada correctamente.')
        except Exception as e:
            messages.error(request, f'No se puede eliminar la sucursal porque tiene socios asociados.')
    return redirect('configuracion:sucursales_lista')


# ============= EJERCICIOS =============

@login_required
def ejercicios_lista(request):
    """Lista todos los ejercicios"""
    grupo = request.GET.get('grupo', '').strip()
    ejercicios = Ejercicio.objects.all()
    if grupo:
        ejercicios = ejercicios.filter(grupo_muscular__icontains=grupo)
    ejercicios = ejercicios.order_by('-activo', 'nombre')
    return render(request, 'configuracion/ejercicios/lista.html', {'ejercicios': ejercicios})


@login_required
def ejercicio_crear(request):
    """Crear un nuevo ejercicio"""
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            ejercicio = form.save()
            messages.success(request, f'Ejercicio "{ejercicio.nombre}" creado correctamente.')
            return redirect('configuracion:ejercicios_lista')
    else:
        form = EjercicioForm()
    return render(request, 'configuracion/ejercicios/form.html', {'form': form, 'titulo': 'Nuevo Ejercicio'})


@login_required
def ejercicio_editar(request, pk):
    """Editar un ejercicio existente"""
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=ejercicio)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ejercicio "{ejercicio.nombre}" actualizado correctamente.')
            return redirect('configuracion:ejercicios_lista')
    else:
        form = EjercicioForm(instance=ejercicio)
    return render(request, 'configuracion/ejercicios/form.html', {'form': form, 'titulo': 'Editar Ejercicio', 'ejercicio': ejercicio})


@login_required
def ejercicio_eliminar(request, pk):
    """Eliminar un ejercicio"""
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        nombre = ejercicio.nombre
        try:
            ejercicio.delete()
            messages.success(request, f'Ejercicio "{nombre}" eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'No se puede eliminar el ejercicio porque está siendo usado en rutinas.')
    return redirect('configuracion:ejercicios_lista')


# ============= RUTINAS =============

@login_required
def rutinas_lista(request):
    """Lista todas las rutinas"""
    rutinas = Rutina.objects.select_related('creada_por__user').prefetch_related('dias').order_by('-activa', 'nombre')
    return render(request, 'configuracion/rutinas/lista.html', {'rutinas': rutinas})


@login_required
def rutina_crear(request):
    """Crear una nueva rutina"""
    if request.method == 'POST':
        form = RutinaFormConfig(request.POST)
        if form.is_valid():
            rutina = form.save()
            messages.success(request, f'Rutina "{rutina.nombre}" creada correctamente.')
            return redirect('configuracion:rutina_detalle', pk=rutina.pk)
    else:
        form = RutinaFormConfig()
    return render(request, 'configuracion/rutinas/form.html', {'form': form, 'titulo': 'Nueva Rutina'})


@login_required
def rutina_editar(request, pk):
    """Editar una rutina existente"""
    rutina = get_object_or_404(Rutina, pk=pk)
    if request.method == 'POST':
        form = RutinaFormConfig(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, f'Rutina "{rutina.nombre}" actualizada correctamente.')
            return redirect('configuracion:rutina_detalle', pk=rutina.pk)
    else:
        form = RutinaFormConfig(instance=rutina)
    return render(request, 'configuracion/rutinas/form.html', {'form': form, 'titulo': 'Editar Rutina', 'rutina': rutina})


@login_required
def rutina_eliminar(request, pk):
    """Eliminar una rutina"""
    rutina = get_object_or_404(Rutina, pk=pk)
    if request.method == 'POST':
        nombre = rutina.nombre
        try:
            rutina.delete()
            messages.success(request, f'Rutina "{nombre}" eliminada correctamente.')
        except Exception as e:
            messages.error(request, f'No se puede eliminar la rutina porque está asignada a socios.')
    return redirect('configuracion:rutinas_lista')


@login_required
def rutina_detalle(request, pk):
    """Ver detalle de una rutina con sus días y ejercicios"""
    rutina = get_object_or_404(
        Rutina.objects.select_related('creada_por__user')
        .prefetch_related('dias__detalles__ejercicio'),
        pk=pk
    )
    dias = rutina.dias.all().order_by('dia_semana')
    
    dias_semana = {
        1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 
        4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: 'Domingo'
    }
    
    return render(request, 'configuracion/rutinas/detalle.html', {
        'rutina': rutina, 
        'dias': dias,
        'dias_semana': dias_semana
    })


# ============= RUTINA DIAS =============

@login_required
def rutina_dia_agregar(request, rutina_pk):
    """Agregar un día a una rutina"""
    rutina = get_object_or_404(Rutina, pk=rutina_pk)
    if request.method == 'POST':
        form = RutinaDiaFormConfig(request.POST)
        if form.is_valid():
            dia = form.save(commit=False)
            dia.rutina = rutina
            dia.save()
            messages.success(request, 'Día agregado correctamente.')
            return redirect('configuracion:rutina_detalle', pk=rutina.pk)
    else:
        form = RutinaDiaFormConfig()
    return render(request, 'configuracion/rutinas/dia_form.html', {
        'form': form, 
        'rutina': rutina, 
        'titulo': 'Agregar Día'
    })


@login_required
def rutina_dia_eliminar(request, pk):
    """Eliminar un día de rutina"""
    dia = get_object_or_404(RutinaDia, pk=pk)
    rutina_pk = dia.rutina.pk
    if request.method == 'POST':
        dia.delete()
        messages.success(request, 'Día eliminado correctamente.')
    return redirect('configuracion:rutina_detalle', pk=rutina_pk)


# ============= RUTINA DETALLES (EJERCICIOS DEL DÍA) =============

@login_required
def rutina_detalle_agregar(request, dia_pk):
    """Agregar un ejercicio a un día de rutina"""
    dia = get_object_or_404(RutinaDia.objects.select_related('rutina'), pk=dia_pk)
    if request.method == 'POST':
        form = RutinaDetalleFormConfig(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.rutina_dia = dia
            detalle.save()
            messages.success(request, 'Ejercicio agregado correctamente.')
            return redirect('configuracion:rutina_detalle', pk=dia.rutina.pk)
    else:
        # Establecer el próximo orden automáticamente
        ultimo_orden = dia.detalles.count()
        form = RutinaDetalleFormConfig(initial={'orden': ultimo_orden + 1})
    return render(request, 'configuracion/rutinas/detalle_form.html', {
        'form': form, 
        'dia': dia, 
        'titulo': 'Agregar Ejercicio'
    })


@login_required
def rutina_detalle_editar(request, pk):
    """Editar un ejercicio de un día de rutina"""
    detalle = get_object_or_404(RutinaDetalle.objects.select_related('rutina_dia__rutina'), pk=pk)
    if request.method == 'POST':
        form = RutinaDetalleFormConfig(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio actualizado correctamente.')
            return redirect('configuracion:rutina_detalle', pk=detalle.rutina_dia.rutina.pk)
    else:
        form = RutinaDetalleFormConfig(instance=detalle)
    return render(request, 'configuracion/rutinas/detalle_form.html', {
        'form': form, 
        'dia': detalle.rutina_dia, 
        'titulo': 'Editar Ejercicio',
        'detalle': detalle
    })


@login_required
def rutina_detalle_eliminar(request, pk):
    """Eliminar un ejercicio de un día de rutina"""
    detalle = get_object_or_404(RutinaDetalle.objects.select_related('rutina_dia__rutina'), pk=pk)
    rutina_pk = detalle.rutina_dia.rutina.pk
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Ejercicio eliminado correctamente.')
    return redirect('configuracion:rutina_detalle', pk=rutina_pk)
