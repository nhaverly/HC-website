// Haverly Consulting: small site behaviours (no dependencies)
(function () {
  // Services dropdown: toggle on click for touch and keyboard users
  document.querySelectorAll('.drop > button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var drop = btn.parentElement;
      var open = drop.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.drop.open').forEach(function (d) {
      if (!d.contains(e.target)) { d.classList.remove('open'); d.querySelector('button').setAttribute('aria-expanded', 'false'); }
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.drop.open').forEach(function (d) { d.classList.remove('open'); var b = d.querySelector('button'); b.setAttribute('aria-expanded', 'false'); b.focus(); });
      var m = document.querySelector('.menu[open]'); if (m) m.removeAttribute('open');
    }
  });

  // Mobile menu: close after choosing an in-page link
  document.querySelectorAll('.menu-panel a').forEach(function (a) {
    a.addEventListener('click', function () { var m = a.closest('details'); if (m) m.removeAttribute('open'); });
  });

  // Contact form (Formspree)
  var form = document.getElementById('contact-form');
  if (form) {
    var status = document.getElementById('form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var action = form.getAttribute('action') || '';
      if (action.indexOf('YOUR_FORM_ID') !== -1) {
        status.hidden = false; status.className = 'form-status err';
        status.textContent = 'The form is not connected yet. Please email info@haverlyconsulting.co.uk or call 020 8064 1937.';
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) {
          status.hidden = false;
          if (r.ok) {
            form.reset();
            status.className = 'form-status';
            status.textContent = 'Thank you. We have your details and will be in touch within one working day.';
          } else { throw new Error('send failed'); }
        })
        .catch(function () {
          status.hidden = false; status.className = 'form-status err';
          status.textContent = 'Your details could not be sent. Please email info@haverlyconsulting.co.uk or call 020 8064 1937.';
        })
        .finally(function () { btn.disabled = false; btn.textContent = 'Request a call back'; });
    });
  }
})();
