from django.urls import path
from . import views

app_name = 'configuracion'

urlpatterns = [
    # Planes
    path('planes/', views.planes_lista, name='planes_lista'),
    path('planes/crear/', views.plan_crear, name='plan_crear'),
    path('planes/<int:pk>/editar/', views.plan_editar, name='plan_editar'),
    path('planes/<int:pk>/eliminar/', views.plan_eliminar, name='plan_eliminar'),
    
    # Sucursales
    path('sucursales/', views.sucursales_lista, name='sucursales_lista'),
    path('sucursales/crear/', views.sucursal_crear, name='sucursal_crear'),
    path('sucursales/<int:pk>/editar/', views.sucursal_editar, name='sucursal_editar'),
    path('sucursales/<int:pk>/eliminar/', views.sucursal_eliminar, name='sucursal_eliminar'),
    
    # Ejercicios
    path('ejercicios/', views.ejercicios_lista, name='ejercicios_lista'),
    path('ejercicios/crear/', views.ejercicio_crear, name='ejercicio_crear'),
    path('ejercicios/<int:pk>/editar/', views.ejercicio_editar, name='ejercicio_editar'),
    path('ejercicios/<int:pk>/eliminar/', views.ejercicio_eliminar, name='ejercicio_eliminar'),
    
    # Rutinas
    path('rutinas/', views.rutinas_lista, name='rutinas_lista'),
    path('rutinas/crear/', views.rutina_crear, name='rutina_crear'),
    path('rutinas/<int:pk>/', views.rutina_detalle, name='rutina_detalle'),
    path('rutinas/<int:pk>/editar/', views.rutina_editar, name='rutina_editar'),
    path('rutinas/<int:pk>/eliminar/', views.rutina_eliminar, name='rutina_eliminar'),
    
    # Días de rutina
    path('rutinas/<int:rutina_pk>/dia/agregar/', views.rutina_dia_agregar, name='rutina_dia_agregar'),
    path('rutinas/dia/<int:pk>/eliminar/', views.rutina_dia_eliminar, name='rutina_dia_eliminar'),
    
    # Detalles de rutina (ejercicios)
    path('rutinas/dia/<int:dia_pk>/ejercicio/agregar/', views.rutina_detalle_agregar, name='rutina_detalle_agregar'),
    path('rutinas/ejercicio/<int:pk>/editar/', views.rutina_detalle_editar, name='rutina_detalle_editar'),
    path('rutinas/ejercicio/<int:pk>/eliminar/', views.rutina_detalle_eliminar, name='rutina_detalle_eliminar'),
]
