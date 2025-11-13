// SCRIPT DESHABILITADO TEMPORALMENTE PARA DEBUGGING DEL SIDEBAR
/*
document.addEventListener('DOMContentLoaded', () => {
  // Solo aplicar el estado si no está ya establecido
  const sidebarState = localStorage.getItem('sidebarCollapsed');
  if (sidebarState === null) {
    // Primera visita, colapsar por defecto
    document.body.classList.add('sidebar-collapsed');
    localStorage.setItem('sidebarCollapsed', 'true');
  } else if (sidebarState === 'true') {
    document.body.classList.add('sidebar-collapsed');
  } else {
    document.body.classList.remove('sidebar-collapsed');
  }

  // DESHABILITADO: comportamiento de hover para evitar apertura automática
  // const leftSidebar = document.querySelector('.left-sidebar');
  // if (leftSidebar) {
  //   leftSidebar.addEventListener('mouseover', () => {
  //     if (document.body.classList.contains('sidebar-collapsed')) {
  //       document.body.classList.add('sidebar-hover');
  //     }
  //   });
  //   leftSidebar.addEventListener('mouseout', () => {
  //     document.body.classList.remove('sidebar-hover');
  //   });
  // }
});
*/