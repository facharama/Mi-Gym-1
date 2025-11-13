(function () {
  const form = document.getElementById("loginForm");
  const passToggle = document.querySelector(".toggle-password");
  const passwordInput =
    (form && form.querySelector('input[type="password"]')) ||
    document.querySelector('input[type="password"]');
  const submitBtn =
    document.getElementById("submitBtn") || document.querySelector(".neon-cta");

  // íconos ojo abierto/cerrado
  const eyeSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>';
  const eyeOffSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 20c-7 0-11-8-11-8a21.74 21.74 0 0 1 4.1-4.88"/><path d="M1 1l22 22"/></svg>';

  function setToggleState(hidden) {
    if (!passToggle) return;
    passToggle.innerHTML = hidden ? eyeSVG : eyeOffSVG;
  }

  if (passToggle && passwordInput) {
    setToggleState(true); // arranca oculto

    passToggle.addEventListener("click", () => {
      if (passwordInput.type === "password") {
        passwordInput.type = "text";
        setToggleState(false);
      } else {
        passwordInput.type = "password";
        setToggleState(true);
      }
      passwordInput.focus();
    });
  }

  if (form && submitBtn) {
    form.addEventListener("submit", () => {
      submitBtn.disabled = true;
      submitBtn.textContent = "Verificando...";
    });
  }
})();
