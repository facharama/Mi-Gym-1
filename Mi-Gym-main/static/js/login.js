(function(){
  const form = document.getElementById('loginForm');
  const passToggle = document.querySelector('.toggle-password');
  const passwordInput = document.querySelector('input[type="password"]');
  const submitBtn = document.getElementById('submitBtn');

  if(passToggle && passwordInput){
    passToggle.addEventListener('click', ()=>{
      const t = passwordInput;
      if(t.type === 'password'){ 
        t.type = 'text'; 
        passToggle.textContent = '🙈'; 
        passToggle.setAttribute('aria-label','Ocultar contraseña'); 
      } else { 
        t.type = 'password'; 
        passToggle.textContent = '👁️'; 
        passToggle.setAttribute('aria-label','Mostrar contraseña'); 
      }
    });
  }

  // Feedback simple al enviar (no reemplaza validación en servidor)
  form.addEventListener('submit', (e)=>{
    submitBtn.disabled = true;
    submitBtn.textContent = 'Verificando...';
  });

  // Animación al enfocar inputs
  document.querySelectorAll('.login-form input').forEach(input=>{
    input.addEventListener('focus', ()=> input.style.boxShadow = '0 6px 18px rgba(124,58,237,0.12)');
    input.addEventListener('blur', ()=> input.style.boxShadow = 'none');
  });
})();
