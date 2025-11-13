(() => {
  // URLs nombradas (namespace ocupacion)
  const OCC_URL    = "{% url 'ocupacion:occupancy_current' %}";
  const ACCESS_URL = "{% url 'ocupacion:access_event' %}";

  // Si tu API no devuelve capacidad, usá fallback:
  const CAPACITY_FALLBACK = 100;

  // ==== WIDGET OCUPACIÓN ====
  const $id = (x) => document.getElementById(x);
  const elPct   = $id("occ-pct");
  const elFill  = document.getElementById("g-fill");
  const elCount = $id("occ-count");
  const elCap   = $id("occ-capacity");
  const elBadge = $id("occ-badge");

  const getVar = (name, fallback) => {
    const v = getComputedStyle(document.documentElement).getPropertyValue(name);
    return (v && v.trim().length) ? v.trim() : fallback;
  };

  function setBadge(pct){
    elBadge.classList.remove("low","mid","high");
    if (pct < 40){ elBadge.textContent="Baja"; elBadge.classList.add("low"); elFill.style.stroke = getVar('--cyan','#06b6d4'); }
    else if (pct < 70){ elBadge.textContent="Media"; elBadge.classList.add("mid"); elFill.style.stroke = getVar('--orange','#ff6a00'); }
    else { elBadge.textContent="Alta"; elBadge.classList.add("high"); elFill.style.stroke = '#ff4d4d'; }
  }
  const pctToDash = (p) => `${Math.max(0,Math.min(100,Math.round(p)))} 100`;

  async function refreshOcc(){
    try{
      // opcional: filtrar por sucursal si se escribió en el simulador
      const suc = document.getElementById("sim-sucursal")?.value?.trim();
      const url = suc ? `${OCC_URL}?sucursal_id=${encodeURIComponent(suc)}` : OCC_URL;

      const r = await fetch(url, { headers: { Accept: 'application/json' }});
      const data = await r.json();
      const count = Number(data.count ?? 0);
      const capacity = Number(data.capacity ?? CAPACITY_FALLBACK);
      const pct = capacity > 0 ? Math.round((count / capacity) * 100) : 0;

      elCount.textContent = count;
      elCap.textContent   = capacity;
      elPct.textContent   = pct + "%";
      elFill.setAttribute("stroke-dasharray", pctToDash(pct));
      setBadge(pct);
    }catch(e){ console.error(e); }
  }
  // Exponer para que el simulador pueda refrescar
  window.miGymRefreshOcc = refreshOcc;

  refreshOcc();
  setInterval(refreshOcc, 5000);

  // ==== SIMULADOR ====
  const $ = (sel) => document.querySelector(sel);
  const statusEl = $("#sim-status");
  const show = (msg, cls="") => { statusEl.className = "sim-status " + cls; statusEl.textContent = msg; };

  async function registrar(tipo){
    const member  = $("#sim-member").value.trim();
    const device  = $("#sim-device").value.trim() || "kiosk-admin-1";
    const source  = $("#sim-source").value;
    const suc     = $("#sim-sucursal").value.trim() || null;

    if(!member){ show("Ingresá un código de socio / usuario.", "warn"); return; }

    const headers = { "Content-Type":"application/json" }; // csrf no requerido (tu view es csrf_exempt)
    const body = JSON.stringify({
      member_code: member,
      type: tipo,           // "IN" | "OUT"
      source: source,
      device_id: device,
      raw_uid: member,
      sucursal_id: suc
    });

    try{
      const r = await fetch(ACCESS_URL, { method:"POST", headers, body });
      const data = await r.json().catch(()=> ({}));
      if (r.ok){
        show(`✅ ${tipo === "IN" ? "Entrada" : "Salida"} registrada`, "ok");
        if (window.miGymRefreshOcc) window.miGymRefreshOcc();
      }else{
        show(`⚠️ ${data.detail || data.status || "Error en la solicitud"}`, "warn");
      }
    }catch(e){
      console.error(e);
      show("❌ No se pudo conectar con el backend", "err");
    }
  }

  document.querySelectorAll(".sim-actions .btn[data-type]").forEach(btn=>{
    btn.addEventListener("click", () => registrar(btn.dataset.type));
  });
  $("#sim-random").addEventListener("click", () => {
    registrar(Math.random()>.5 ? "IN" : "OUT");
  });
})();
