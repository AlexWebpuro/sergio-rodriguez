// Envía eventos a Google Tag Manager (dataLayer), a GA4 directo si existe, y a Clarity.
window.trackEvent = function (name, params) {
  params = params || {};
  window.dataLayer = window.dataLayer || [];
  var data = { event: name };
  for (var k in params) data[k] = params[k];
  window.dataLayer.push(data);
  if (window.gtag) window.gtag('event', name, params);
  if (window.clarity) window.clarity('event', name);
};

// Menú móvil
(function () {
  var btn = document.querySelector('.menu-toggle');
  var links = document.querySelector('.nav-links');
  if (btn && links) {
    btn.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();

// Formulario de cotización.
// Si hay una clave de Web3Forms configurada, envía por correo.
// Si no, abre WhatsApp con el mensaje ya escrito, para no perder ningún cliente.
(function () {
  var form = document.getElementById('form-cotizacion');
  if (!form) return;
  var status = form.querySelector('.form-status');
  var key = form.getAttribute('data-key') || '';
  var wa = form.getAttribute('data-wa');

  function val(name) {
    var el = form.elements[name];
    return el ? String(el.value || '').trim() : '';
  }

  function whatsappText() {
    var parts = [
      'Hola Sergio, quiero una cotización.',
      'Nombre: ' + val('nombre'),
      val('tipo') ? 'Soy: ' + val('tipo') : '',
      val('equipo') ? 'Equipo: ' + val('equipo') : '',
      val('zona') ? 'Zona: ' + val('zona') : '',
      val('mensaje') ? 'Detalle: ' + val('mensaje') : ''
    ];
    return parts.filter(Boolean).join('\n');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.elements['botcheck'] && form.elements['botcheck'].checked) return;
    if (!form.reportValidity()) return;

    if (!key || key.indexOf('PON_AQUI') === 0) {
      window.trackEvent('generate_lead', { metodo: 'formulario_whatsapp', pagina: location.pathname });
      window.open('https://wa.me/' + wa + '?text=' + encodeURIComponent(whatsappText()), '_blank', 'noopener');
      return;
    }

    status.textContent = 'Enviando…';
    status.className = 'form-status';
    var data = new FormData(form);
    data.append('access_key', key);
    data.append('subject', 'Nueva solicitud de cotización desde la web');
    data.append('from_name', 'Web Ing. Sergio Rodríguez');

    fetch('https://api.web3forms.com/submit', { method: 'POST', body: data })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.success) {
          status.textContent = '¡Listo! Recibí tu solicitud y te contacto pronto.';
          status.className = 'form-status ok';
          form.reset();
          window.trackEvent('generate_lead', { metodo: 'formulario', pagina: location.pathname });
        } else {
          throw new Error(res.message || 'error');
        }
      })
      .catch(function () {
        status.innerHTML = 'No se pudo enviar. Escríbeme directo por <a href="https://wa.me/' + wa + '?text=' + encodeURIComponent(whatsappText()) + '" target="_blank" rel="noopener">WhatsApp</a>.';
        status.className = 'form-status err';
      });
  });
})();

// Medición de contactos: WhatsApp, llamadas y correo (GA4 + Clarity)
(function () {
  var track = window.trackEvent;
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    var where = a.classList.contains('wa-float') ? 'boton_flotante'
      : (a.closest('header') ? 'menu' : (a.closest('.aside-card') ? 'lateral' : (a.closest('.hero, .page-hero') ? 'portada' : 'contenido')));
    var params = { ubicacion: where, pagina: location.pathname };
    if (href.indexOf('wa.me') > -1) track('contacto_whatsapp', params);
    else if (href.indexOf('tel:') === 0) track('contacto_llamada', params);
    else if (href.indexOf('mailto:') === 0) track('contacto_correo', params);
  });
})();

// Aviso de cookies (informativo, se recuerda por navegador)
(function () {
  var note = document.querySelector('.cookie-note');
  if (!note) return;
  var seen = false;
  try { seen = localStorage.getItem('aviso_cookies') === '1'; } catch (e) {}
  if (!seen) note.hidden = false;
  note.querySelector('button').addEventListener('click', function () {
    note.hidden = true;
    try { localStorage.setItem('aviso_cookies', '1'); } catch (e) {}
  });
})();
