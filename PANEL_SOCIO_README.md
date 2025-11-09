# Panel del Socio - Mi Gym

## ✅ Módulo Completo del Socio

Se ha implementado el **Panel del Socio** con todas las funcionalidades solicitadas en la ERS.

### 🎯 Funcionalidades Implementadas:

#### 1. **Dashboard Principal** (`/socios/panel/`)
- Vista general con 3 widgets principales:
  - **Mi Cuota**: Estado de suscripción (al día / vencida)
  - **Rutina de Hoy**: Cantidad de ejercicios programados
  - **Ocupación**: Porcentaje de ocupación en tiempo real
- Vista rápida de los primeros 5 ejercicios del día
- Diseño con cards interactivos y colores según el estado

#### 2. **Consulta de Cuota** (`/socios/panel/cuota/`)
- Estado de la suscripción actual (vigente/vencida)
- Días restantes hasta el vencimiento
- Alertas visuales según el tiempo restante
- Historial completo de suscripciones
- Historial de pagos por cada suscripción
- Diseño con código de colores (verde/amarillo/rojo)

#### 3. **Rutina del Día** (`/socios/panel/rutina/`)
- Muestra la rutina asignada para el día actual (según día de la semana)
- Información de cada ejercicio:
  - Orden de ejecución
  - Grupo muscular
  - Series y repeticiones
  - Tiempo (si aplica)
  - Descanso entre series
  - Observaciones del instructor
- Datos de la rutina (nombre, objetivo, creador)
- Diseño visual con cards para cada ejercicio

#### 4. **Ocupación del Gimnasio** (`/socios/panel/ocupacion/`)
- Visualización en tiempo real de la ocupación
- Círculo grande con porcentaje de ocupación
- Código de colores según nivel:
  - 🟢 Verde (< 40%): Baja ocupación
  - 🟡 Amarillo (40-70%): Media ocupación
  - 🔴 Rojo (> 70%): Alta ocupación
- Estadísticas:
  - Personas actuales
  - Capacidad máxima
  - Lugares disponibles
- Recomendaciones según el nivel de ocupación
- Botón para actualizar datos en tiempo real

### 🎨 Características de Diseño:

- ✅ Mismo estilo Bootstrap 5.3.3 que el resto de la app
- ✅ Sidebar personalizado para el socio con 4 opciones
- ✅ Cards interactivos con hover effects
- ✅ Código de colores intuitivo
- ✅ Responsive design
- ✅ Iconos y emojis para mejor UX
- ✅ Transiciones suaves

### 🔒 Seguridad:

- Todas las vistas requieren `@login_required`
- Validación de que el usuario tenga perfil de socio
- Redirección automática según tipo de usuario (admin/socio)

### 📍 Navegación:

El sistema ahora detecta automáticamente el tipo de usuario:
- **Administradores/Staff**: Ven el sidebar de administración
- **Socios**: Ven el sidebar del panel del socio

### 🛣️ URLs Disponibles:

```
/socios/panel/                  → Dashboard principal del socio
/socios/panel/cuota/            → Consulta de cuota
/socios/panel/rutina/           → Rutina del día
/socios/panel/ocupacion/        → Ocupación en tiempo real
```

### 🔄 Redirección Automática:

Después del login, el sistema redirige:
- **Administradores** → `/dash/admin/`
- **Socios** → `/socios/panel/`

### 📂 Archivos Creados/Modificados:

**Vistas:**
- `aplications/socios/views.py` (agregadas 4 nuevas vistas)

**Templates:**
- `templates/socios/panel/dashboard.html`
- `templates/socios/panel/mi_cuota.html`
- `templates/socios/panel/mi_rutina.html`
- `templates/socios/panel/ocupacion.html`
- `templates/partials/sidebar_socio.html`

**URLs:**
- `aplications/socios/urls.py` (agregadas 4 rutas)

**Configuración:**
- `templates/base_dash.html` (sidebar dinámico según usuario)
- `aplications/usuarios/views.py` (redirección actualizada)

### 💡 Uso:

1. **Como Socio:**
   - Inicia sesión con tu DNI y contraseña
   - Serás redirigido automáticamente al panel del socio
   - Navega por las opciones del menú lateral

2. **Como Administrador:**
   - Inicia sesión normalmente
   - Serás redirigido al dashboard de administración
   - Podés gestionar todo desde el panel admin

### ✨ Características Especiales:

- **Actualización en tiempo real**: La ocupación se puede actualizar con un botón
- **Widgets interactivos**: Los cards son clickeables y te llevan a la vista detallada
- **Alertas inteligentes**: Avisos según días restantes de suscripción
- **Vista rápida**: El dashboard muestra un resumen de la rutina del día

¡Todo listo para que los socios puedan usar el sistema! 🎉
