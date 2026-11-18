// Campo de teléfono con selector de país (bandera + buscador + indicativo).
// Uso: <div class="phone-field" data-phone-input data-name="telefono" data-label="Teléfono o WhatsApp" data-required></div>
(function () {
  var BASE = document.documentElement.getAttribute('data-base') || '/';
  var COUNTRIES = [
    ['co', 'Colombia', '57'], ['de', 'Alemania', '49'], ['ar', 'Argentina', '54'], ['bo', 'Bolivia', '591'],
    ['br', 'Brasil', '55'], ['ca', 'Canadá', '1'], ['cl', 'Chile', '56'], ['cr', 'Costa Rica', '506'],
    ['cu', 'Cuba', '53'], ['ec', 'Ecuador', '593'], ['sv', 'El Salvador', '503'], ['es', 'España', '34'],
    ['us', 'Estados Unidos', '1'], ['fr', 'Francia', '33'], ['gt', 'Guatemala', '502'], ['hn', 'Honduras', '504'],
    ['it', 'Italia', '39'], ['mx', 'México', '52'], ['ni', 'Nicaragua', '505'], ['pa', 'Panamá', '507'],
    ['py', 'Paraguay', '595'], ['pe', 'Perú', '51'], ['pt', 'Portugal', '351'], ['pr', 'Puerto Rico', '1'],
    ['gb', 'Reino Unido', '44'], ['do', 'República Dominicana', '1'], ['uy', 'Uruguay', '598'], ['ve', 'Venezuela', '58']
  ];
  var CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>';
  var CHEVRON = '<svg class="pf-chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
  var SEARCH = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>';
  var uid = 0;

  function norm(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
  function flag(code) { return '<img class="pf-flag" src="' + BASE + 'assets/flags/' + code + '.svg" alt="" width="22" height="16" loading="lazy">'; }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function highlight(name, q) {
    if (!q) return esc(name);
    var i = norm(name).indexOf(norm(q));
    if (i < 0) return esc(name);
    return esc(name.slice(0, i)) + '<strong>' + esc(name.slice(i, i + q.length)) + '</strong>' + esc(name.slice(i + q.length));
  }

  function init(root) {
    var id = 'pf' + (++uid);
    var name = root.getAttribute('data-name') || 'telefono';
    var label = root.getAttribute('data-label') || 'Teléfono';
    var required = root.hasAttribute('data-required');
    var selected = COUNTRIES[0];
    var active = -1;
    var filtered = COUNTRIES.slice();

    root.innerHTML =
      '<div class="pf-box">' +
        '<button type="button" class="pf-country" aria-haspopup="listbox" aria-expanded="false" aria-controls="' + id + '-list" aria-label="Seleccionar país"></button>' +
        '<label class="pf-main" for="' + id + '-num">' +
          '<span class="pf-label">' + esc(label) + (required ? '*' : '') + '</span>' +
          '<span class="pf-line"><span class="pf-dial"></span><input id="' + id + '-num" type="tel" inputmode="tel" autocomplete="tel-national" placeholder="300 123 4567"' + (required ? ' required' : '') + '></span>' +
        '</label>' +
      '</div>' +
      '<input type="hidden" name="' + name + '">' +
      '<div class="pf-panel" hidden>' +
        '<div class="pf-search">' + SEARCH + '<input type="text" placeholder="Buscar país" aria-label="Buscar país" autocomplete="off"></div>' +
        '<ul class="pf-list" role="listbox" id="' + id + '-list" aria-label="Países"></ul>' +
      '</div>';

    var btn = root.querySelector('.pf-country');
    var dial = root.querySelector('.pf-dial');
    var num = root.querySelector('.pf-main input');
    var hidden = root.querySelector('input[type=hidden]');
    var panel = root.querySelector('.pf-panel');
    var search = root.querySelector('.pf-search input');
    var list = root.querySelector('.pf-list');

    function sync() {
      btn.innerHTML = flag(selected[0]) + CHEVRON;
      dial.textContent = '+' + selected[2];
      var digits = num.value.replace(/\D/g, '');
      hidden.value = digits ? '+' + selected[2] + ' ' + num.value.trim() : '';
    }

    function render() {
      var q = search.value.trim();
      var nq = norm(q).replace(/^\+/, '');
      filtered = COUNTRIES.filter(function (c) { return !nq || norm(c[1]).indexOf(nq) >= 0 || c[2].indexOf(nq) === 0; });
      if (!filtered.length) { list.innerHTML = '<li class="pf-empty">Sin resultados</li>'; return; }
      list.innerHTML = filtered.map(function (c, i) {
        var sel = c === selected;
        return '<li role="option" id="' + id + '-o' + i + '" data-i="' + i + '" aria-selected="' + sel + '" class="pf-opt' + (i === active ? ' is-active' : '') + '">' +
          flag(c[0]) + '<span class="pf-name">' + highlight(c[1], q) + ' (+' + c[2] + ')</span>' + (sel ? '<span class="pf-check">' + CHECK + '</span>' : '') + '</li>';
      }).join('');
    }

    function open() {
      panel.hidden = false;
      root.classList.add('is-open');
      btn.setAttribute('aria-expanded', 'true');
      search.value = '';
      active = -1;
      render();
      var cur = list.querySelector('[aria-selected="true"]');
      if (cur) cur.scrollIntoView({ block: 'nearest' });
      search.focus();
    }
    function close(focusBtn) {
      panel.hidden = true;
      root.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
      if (focusBtn) btn.focus();
    }
    function choose(i) {
      if (!filtered[i]) return;
      selected = filtered[i];
      sync();
      close(false);
      num.focus();
    }
    function move(d) {
      if (!filtered.length) return;
      active = (active + d + filtered.length) % filtered.length;
      render();
      var el = document.getElementById(id + '-o' + active);
      if (el) { el.scrollIntoView({ block: 'nearest' }); search.setAttribute('aria-activedescendant', el.id); }
    }

    btn.addEventListener('click', function () { panel.hidden ? open() : close(true); });
    search.addEventListener('input', function () { active = 0; render(); });
    search.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Enter') { e.preventDefault(); choose(active < 0 ? 0 : active); }
      else if (e.key === 'Escape') { close(true); }
    });
    list.addEventListener('mousedown', function (e) { e.preventDefault(); });
    list.addEventListener('click', function (e) {
      var li = e.target.closest('.pf-opt');
      if (li) choose(+li.getAttribute('data-i'));
    });
    document.addEventListener('click', function (e) { if (!root.contains(e.target) && !panel.hidden) close(false); });
    num.addEventListener('input', function () {
      num.value = num.value.replace(/[^\d\s-]/g, '');
      sync();
    });
    num.addEventListener('focus', function () { root.classList.add('is-focus'); });
    num.addEventListener('blur', function () { root.classList.remove('is-focus'); });

    root.phoneValue = function () { return hidden.value; };
    sync();
  }

  document.querySelectorAll('[data-phone-input]').forEach(init);
})();
