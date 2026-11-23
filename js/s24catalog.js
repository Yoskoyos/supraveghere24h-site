/* s24catalog: pagina Echipamente (și categoriile ei) din echipamentele bifate „Pe site” în aplicație.
   Magazin pornit → preț, disponibilitate, „Adaugă în coș”, coș lateral, fereastră cu detalii.
   Magazin oprit → aceleași carduri, cu „Preț la cerere” și „Cere ofertă” (formularul de pe pagină).
   Coșul stă în localStorage („s24cart”: [{id, qty}]); prețurile se recitesc mereu de pe server. */
(function () {
  var API = 'https://proxy.supraveghere24h.ro/public/catalog';
  var CAT = { exterior: 'Cameră exterior', interior: 'Cameră interior', lift: 'Cameră lift', nvr: 'Înregistrator (NVR)', hdd: 'Stocare', retea: 'Rețea', alimentare: 'Alimentare', rack: 'Montaj și accesorii', monitor: 'Monitor', altele: 'Accesorii' };
  // categoriile mari (filtre) și tipurile din fiecare (al doilea rând de filtre)
  var GROUPS = [['cam', 'Camere', ['exterior', 'interior', 'lift']], ['nvr', 'NVR', ['nvr']], ['hdd', 'Stocare', ['hdd']], ['net', 'Rețea', ['retea']], ['pwr', 'Alimentare', ['alimentare']], ['acc', 'Montaj și accesorii', ['rack', 'altele']], ['mon', 'Monitoare', ['monitor']]];
  var SUBS = { cam: [['p:exterior', 'Exterior'], ['p:interior', 'Interior'], ['bullet', 'Bullet'], ['dome', 'Dome / turret'], ['ptz', 'Rotative'], ['wifi', 'Wi-Fi'], ['kit', 'Kituri']],
    hdd: [['hdd', 'Hard disk'], ['microsd', 'Card microSD']], net: [['switch', 'Switch PoE'], ['router', 'Router']], pwr: [['sursa', 'Surse'], ['alimentator', 'Alimentatoare'], ['ups', 'UPS']],
    acc: [['doza', 'Doze'], ['rack', 'Rack'], ['cablu', 'Cablu'], ['accesorii', 'Accesorii de montaj']] };
  var SUBN = { bullet: 'Cameră bullet', dome: 'Cameră dome / turret', ptz: 'Cameră rotativă', wifi: 'Cameră Wi-Fi', kit: 'Kit supraveghere', hdd: 'Hard disk', microsd: 'Card microSD', switch: 'Switch PoE', router: 'Router', sursa: 'Sursă de alimentare', alimentator: 'Alimentator', ups: 'UPS', doza: 'Doză de joncțiune', rack: 'Rack', cablu: 'Cablu', accesorii: 'Accesorii de montaj' };
  function catName(x) { var c = ['exterior', 'interior', 'lift'].indexOf(x.cat) >= 0; return SUBN[x.sub] ? SUBN[x.sub] + (c && x.sub !== 'kit' ? ' · ' + (x.cat === 'lift' ? 'lift' : x.cat) : '') : (CAT[x.cat] || ''); }
  var FALLBACK = { exterior: 'images/cam-hilook-bullet.svg', interior: 'images/cam-hilook-turret.svg', lift: 'images/cam-hilook-turret.svg' };
  var AV = { stoc: ['În stoc', 'ok'], furnizor: ['Livrare în 1–3 zile', 'soon'], comanda: ['La comandă', 'ord'] };
  var I = {
    cart: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.7 12.4a2 2 0 0 0 2 1.6h8.6a2 2 0 0 0 2-1.5L22 7H6"/></svg>',
    search: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>',
    x: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    pdf: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/><path d="M12 18v-6M9 15l3 3 3-3"/></svg>',
    shield: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    truck: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M1 4h14v12H1zM15 9h4l3 3v4h-7"/><circle cx="6" cy="18.5" r="2"/><circle cx="18" cy="18.5" r="2"/></svg>',
    doc: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></svg>',
    tool: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg>',
    back: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
    check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>'
  };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function lei(n) { return (Math.round(n * 100) / 100).toLocaleString('ro-RO'); }
  function dmy(d) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || ''); return m ? (+m[3]) + ' ' + ['ian.', 'feb.', 'mar.', 'apr.', 'mai', 'iun.', 'iul.', 'aug.', 'sept.', 'oct.', 'nov.', 'dec.'][+m[2] - 1] : ''; }
  function hasDisc(x) { return priced(x) && x.oldPrice > x.price; }
  // ── coșul (comun cu pagina cos.html și antetul) ──
  function cartGet() { try { var c = JSON.parse(localStorage.getItem('s24cart') || '[]'); return Array.isArray(c) ? c.filter(function (x) { return x && x.id && x.qty > 0; }) : []; } catch (e) { return []; } }
  function cartSet(c) { try { localStorage.setItem('s24cart', JSON.stringify(c)); } catch (e) {} try { window.dispatchEvent(new Event('s24cart')); } catch (e) {} }
  function cartAdd(id, q) { var c = cartGet(), x = c.filter(function (y) { return y.id === id; })[0]; if (x) x.qty = Math.min(99, x.qty + q); else c.push({ id: id, qty: Math.min(99, q) }); cartSet(c); }

  var ALL = [], BYID = {}, SHOP = { on: false }, box, state = { g: '', s: '', p: '', q: '', sort: 'rec' };
  var priced = function (x) { return SHOP.on && x.price > 0; };

  // „Cere ofertă” → formularul de contact de pe pagină, cu produsul trecut în mesaj
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-ofr]'); if (!a) return;
    closeAll(); var m = document.getElementById('s24-msg'); if (!m) return;
    if (!m.value.trim()) m.value = 'Bună ziua, doresc o ofertă pentru ' + a.getAttribute('data-ofr') + '.';
    setTimeout(function () { try { m.focus({ preventScroll: true }); } catch (_) {} }, 600);
  });

  function card(x) {
    var img = x.photo || FALLBACK[x.cat] || 'images/kit-hilook-8.svg', av = AV[x.avail];
    var specs = (x.specs || []).slice(0, 3);
    return '<article class="s24x-card" data-id="' + esc(x.id) + '">' +
      '<button type="button" class="s24x-media" data-open aria-label="Detalii: ' + esc(x.name) + '"><img src="' + esc(img) + '" alt="' + esc(x.name) + '" loading="lazy" width="400" height="300">' +
      (x.brand ? '<span class="s24x-brand">' + esc(x.brand) + '</span>' : '') + (hasDisc(x) ? '<span class="s24x-off">-' + x.disc + '%</span>' : '') + '</button>' +
      '<div class="s24x-body"><div class="s24x-cat">' + esc(catName(x)) + '</div>' +
      '<h3 class="s24x-name"><button type="button" data-open>' + esc(x.name) + '</button></h3>' +
      (x.model ? '<div class="s24x-sku">Cod: ' + esc(x.model) + '</div>' : '') +
      (specs.length ? '<ul class="s24x-spec">' + specs.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ul>' : '') +
      '<div class="s24x-foot">' + (priced(x)
        ? '<div class="s24x-pr">' + (hasDisc(x) ? '<s class="s24x-old">' + lei(x.oldPrice) + ' lei</s>' : '') + '<div class="s24x-price' + (hasDisc(x) ? ' s24x-red' : '') + '">' + lei(x.price) + '<small> lei</small></div>' + (av ? '<span class="s24x-av ' + av[1] + '">' + av[0] + '</span>' : '') + '</div>' +
          '<button type="button" class="s24x-add" data-add aria-label="Adaugă în coș: ' + esc(x.name) + '">' + I.cart + '<span>Adaugă</span></button>'
        : '<div class="s24x-pr"><div class="s24x-ask">Preț la cerere</div><span class="s24x-av ord">Inclus și în abonament</span></div>' +
          '<a href="' + (document.getElementById('contact') ? '#contact' : 'contact.html') + '" class="s24x-add s24x-add-o" data-ofr="' + esc([x.brand, x.model || x.name].filter(Boolean).join(' ')) + '">Cere ofertă</a>') +
      '</div></div></article>';
  }
  function visible() {
    var g = state.g === 'off' ? null : GROUPS.filter(function (r) { return r[0] === state.g; })[0], q = state.q.toLowerCase().trim();
    var L = ALL.filter(function (x) {
      if (state.g === 'off') { if (!hasDisc(x)) return false; } else if (g && g[2].indexOf(x.cat) < 0) return false;
      if (state.s) { if (state.s.indexOf('p:') === 0) { if (x.cat !== state.s.slice(2) && !(state.s === 'p:interior' && x.cat === 'lift')) return false; } else if (x.sub !== state.s) return false; }
      if (state.p && x.cat !== state.p) return false;
      if (q && (x.name + ' ' + x.brand + ' ' + x.model + ' ' + (x.specs || []).join(' ')).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    if (state.sort === 'pa' || state.sort === 'pd') L = L.slice().sort(function (a, b) { var pa = priced(a) ? a.price : 1e9, pb = priced(b) ? b.price : 1e9; return state.sort === 'pa' ? pa - pb : (pb === 1e9 ? -1 : pa === 1e9 ? 1 : pb - pa); });
    if (state.sort === 'nm') L = L.slice().sort(function (a, b) { return a.name.localeCompare(b.name, 'ro'); });
    return L;
  }
  function renderGrid() {
    var L = visible(), grid = box.querySelector('.s24x-grid');
    grid.innerHTML = L.length ? L.map(card).join('') : '<div class="s24x-none">Niciun produs nu se potrivește căutării. <button type="button" data-reset>Arată toate produsele</button></div>';
    box.querySelector('.s24x-count').textContent = L.length + (L.length === 1 ? ' produs' : ' produse');
    [].forEach.call(box.querySelectorAll('.s24x-chip[data-g]'), function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-g') === state.g ? 'true' : 'false'); });
    // al doilea rând: tipurile din categoria aleasă (doar cele care au produse)
    var sb = box.querySelector('.s24x-subs'), grp = GROUPS.filter(function (r) { return r[0] === state.g; })[0];
    var subs = grp && SUBS[state.g] ? SUBS[state.g].filter(function (o) { return ALL.some(function (x) { return grp[2].indexOf(x.cat) >= 0 && (o[0].indexOf('p:') === 0 ? x.cat === o[0].slice(2) || (o[0] === 'p:interior' && x.cat === 'lift') : x.sub === o[0]); }); }) : [];
    sb.hidden = subs.length < 2;
    sb.innerHTML = subs.length < 2 ? '' : '<button type="button" class="s24x-sub" data-s="" aria-pressed="' + (!state.s) + '">Toate</button>' + subs.map(function (o) { return '<button type="button" class="s24x-sub" data-s="' + o[0] + '" aria-pressed="' + (state.s === o[0]) + '">' + o[1] + '</button>'; }).join('');
  }
  /* meniul „Categorii” (ca la magazinele mari): grupe în stânga, subcategorii pe coloane în dreapta; doar ce există în catalog */
  var MEGA_IC = { off: '%', cam: '📷', nvr: '🖥', hdd: '💾', net: '🔌', pwr: '⚡', acc: '🧰', mon: '🖵' };
  function megaCols(g) {   // [[titlu, [[eticheta, g, s, p, n], ...]], ...]
    var inG = function (x) { return g[2].indexOf(x.cat) >= 0; }, cnt = function (f) { return ALL.filter(function (x) { return inG(x) && f(x); }).length; };
    if (g[0] === 'cam') {
      var cols = [];
      [['exterior', 'Camere exterior'], ['interior', 'Camere interior'], ['lift', 'Camere lift']].forEach(function (pl) {
        var items = SUBS.cam.filter(function (o) { return o[0].indexOf('p:') !== 0 && o[0] !== 'kit'; }).map(function (o) { return [SUBN[o[0]].replace('Cameră ', '').replace(/^./, function (c) { return c.toUpperCase(); }), 'cam', o[0], pl[0], cnt(function (x) { return x.cat === pl[0] && x.sub === o[0]; })]; }).filter(function (i) { return i[4]; });
        var tot = cnt(function (x) { return x.cat === pl[0]; }); if (tot) cols.push([pl[1], [['Toate camerele de ' + pl[0], 'cam', '', pl[0], tot]].concat(items)]);
      });
      var kits = cnt(function (x) { return x.sub === 'kit'; }); if (kits) cols.push(['Kituri supraveghere', [['Kituri', 'cam', 'kit', '', kits], ['Kituri complete', 'cam', 'kit', '', kits]]]);
      return cols;
    }
    var items = (SUBS[g[0]] || []).map(function (o) { return [o[1], g[0], o[0], '', cnt(function (x) { return x.sub === o[0]; })]; }).filter(function (i) { return i[4]; });
    return [[g[1], [['Toate (' + cnt(function () { return true; }) + ')', g[0], '', '', -1]].concat(items)]];
  }
  function megaHtml(present) {
    var L = present.map(function (g, i) { var n = g[0] === 'off' ? ALL.filter(hasDisc).length : ALL.filter(function (x) { return g[2].indexOf(x.cat) >= 0; }).length;
      return '<button type="button" class="s24x-mg-g' + (g[0] === 'off' ? ' red' : '') + (i === (present[0] && present[0][0] === 'off' ? 1 : 0) ? ' on' : '') + '" data-mg="' + g[0] + '"><span>' + (MEGA_IC[g[0]] || '•') + '</span>' + esc(g[1]) + '<em>' + n + '</em><b>›</b></button>'; }).join('');
    var R = present.filter(function (g) { return g[0] !== 'off'; }).map(function (g, i) {
      return '<div class="s24x-mg-p" data-mgp="' + g[0] + '"' + (i ? ' hidden' : '') + '><div class="s24x-mg-h">' + esc(g[1]) + '</div><div class="s24x-mg-cols">' + megaCols(g).map(function (c) {
        return '<div class="s24x-mg-c"><a href="#" class="s24x-mg-t" data-go="' + c[1][0].slice(1, 4).join('|') + '">' + esc(c[0]) + '</a>' + c[1].slice(1).map(function (it) {
          return '<a href="#" data-go="' + [it[1], it[2], it[3]].join('|') + '">' + esc(it[0]) + (it[4] > 0 ? ' <small>' + it[4] + '</small>' : '') + '</a>'; }).join('') + '</div>'; }).join('') + '</div></div>'; }).join('');
    return '<div class="s24x-mg-l">' + L + '</div><div class="s24x-mg-r">' + R + '</div>';
  }
  function megaShow(k) {
    [].forEach.call(box.querySelectorAll('[data-mg]'), function (b) { b.classList.toggle('on', b.getAttribute('data-mg') === k); });
    [].forEach.call(box.querySelectorAll('[data-mgp]'), function (p) { p.hidden = p.getAttribute('data-mgp') !== k; });
  }
  function syncChips() { [].forEach.call(box.querySelectorAll('.s24x-chip[data-g]'), function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-g') === state.g ? 'true' : 'false'); }); }
  function megaOpen(on) { var m = box.querySelector('.s24x-mega'), b = box.querySelector('.s24x-catbtn'); if (!m) return; m.hidden = !on; b.setAttribute('aria-expanded', on ? 'true' : 'false'); }
  function build(title) {
    var present = GROUPS.filter(function (g) { return ALL.some(function (x) { return g[2].indexOf(x.cat) >= 0; }); });
    var nDisc = ALL.filter(hasDisc).length;
    if (nDisc) present = [['off', 'Reduceri', []]].concat(present);
    var chips = present.length > 1 ? '<div class="s24x-chips" role="group" aria-label="Filtrează după categorie"><button type="button" class="s24x-chip" data-g="" aria-pressed="true">Toate</button>' +
      present.map(function (g) { return '<button type="button" class="s24x-chip" data-g="' + g[0] + '" aria-pressed="false">' + g[1] + '</button>'; }).join('') + '</div>' : '';
    box.classList.add('s24x');
    box.innerHTML = '<div class="s24x-head"><h2 class="s24-block-h">' + esc(title) + '</h2><span class="s24x-count"></span></div>' +
      (SHOP.on ? '<ul class="s24x-trust" role="list">' +
        '<li>' + I.shield + '<span><b>Produse originale</b>garanție 2 ani</span></li>' +
        '<li>' + I.doc + '<span><b>Factură fiscală</b>pe firmă sau persoană fizică</span></li>' +
        '<li>' + I.truck + '<span><b>Livrare prin curier</b>' + (SHOP.freeOver ? 'gratuită peste ' + lei(SHOP.freeOver) + ' lei' : 'sau ridicare din București') + '</span></li>' +
        '<li>' + I.back + '<span><b>Retur în 14 zile</b>pentru persoane fizice</span></li></ul>' : '') +
      '<div class="s24x-tools"><div class="s24x-r1"><button type="button" class="s24x-catbtn" aria-expanded="false" aria-haspopup="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>Categorii</button>' + chips + '</div><div class="s24x-tr"><label class="s24x-search">' + I.search + '<input type="search" placeholder="Caută model, rezoluție…" aria-label="Caută în echipamente" autocomplete="off"></label>' +
      '<select class="s24x-sort" aria-label="Ordonează">' + '<option value="rec">Recomandate</option>' + (SHOP.on ? '<option value="pa">Preț crescător</option><option value="pd">Preț descrescător</option>' : '') + '<option value="nm">Nume (A–Z)</option></select></div></div>' +
      '<div class="s24x-mega" hidden>' + megaHtml(present) + '</div>' +
      '<div class="s24x-subs" role="group" aria-label="Filtrează după tip" hidden></div><div class="s24x-grid"></div>' +
      (SHOP.on ? '<p class="s24x-legal">Prețuri finale în lei. YCA SOLUTIONS S.R.L. nu este plătitoare de TVA. Prețul tăiat este cel mai mic preț practicat pe site în cele 30 de zile dinaintea reducerii. Pentru blocuri, aceleași echipamente sunt incluse în <a href="oferta-asociatii.html">abonamentul lunar</a>, cu montaj și mentenanță.</p>'
        : '<p class="s24x-legal">Pentru blocuri, echipamentele sunt incluse în <a href="oferta-asociatii.html">abonamentul lunar</a>, fără investiție inițială. Pentru firme și case facem ofertă personalizată.</p>');
    box.addEventListener('click', function (e) {
      if (e.target.closest('.s24x-catbtn')) { megaOpen(box.querySelector('.s24x-mega').hidden); return; }
      var mg = e.target.closest('[data-mg]');
      if (mg) { var k = mg.getAttribute('data-mg');
        if (k === 'off' || window.matchMedia('(hover: none)').matches === false && e.detail) { state.g = k; state.s = ''; state.p = ''; megaOpen(false); renderGrid(); syncChips(); return; }
        megaShow(k); return; }
      var go = e.target.closest('[data-go]');
      if (go) { e.preventDefault(); var v = go.getAttribute('data-go').split('|'); state.g = v[0]; state.s = v[1] || ''; state.p = v[2] || ''; megaOpen(false); renderGrid(); syncChips(); var t = box.querySelector('.s24x-grid'); if (t && t.getBoundingClientRect().top < 0) box.scrollIntoView({ behavior: 'smooth' }); return; }
      var c = e.target.closest('.s24x-chip'); if (c) { state.g = c.getAttribute('data-g'); state.s = ''; state.p = ''; renderGrid(); return; }
      var sbt = e.target.closest('.s24x-sub'); if (sbt) { state.s = sbt.getAttribute('data-s'); state.p = ''; renderGrid(); return; }
      if (e.target.closest('[data-reset]')) { state = { g: '', s: '', p: '', q: '', sort: state.sort }; box.querySelector('.s24x-search input').value = ''; renderGrid(); return; }
      var art = e.target.closest('.s24x-card'); if (!art) return; var x = BYID[art.getAttribute('data-id')];
      if (e.target.closest('[data-add]')) { cartAdd(x.id, 1); openCart(x); return; }
      if (e.target.closest('[data-open]')) openProduct(x);
    });
    box.querySelector('.s24x-search input').addEventListener('input', function (e) { state.q = e.target.value; renderGrid(); });
    box.addEventListener('mouseover', function (e) { var mg = e.target.closest('[data-mg]'); if (mg && mg.getAttribute('data-mg') !== 'off') megaShow(mg.getAttribute('data-mg')); });
    document.addEventListener('click', function (e) { if (!e.target.closest('.s24x-mega') && !e.target.closest('.s24x-catbtn')) megaOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') megaOpen(false); });
    box.querySelector('.s24x-sort').addEventListener('change', function (e) { state.sort = e.target.value; renderGrid(); });
    renderGrid();
  }

  // ── fereastra cu detalii ──
  var pm, cartEl, lastFocus;
  function ensureUi() {
    if (pm) return;
    pm = document.createElement('div'); pm.className = 's24x-ov'; pm.id = 's24x-pm'; pm.hidden = true;
    pm.innerHTML = '<div class="s24x-dlg" role="dialog" aria-modal="true" aria-labelledby="s24x-pm-h"><button type="button" class="s24x-x" data-close aria-label="Închide">' + I.x + '</button><div class="s24x-pm-in"></div></div>';
    document.body.appendChild(pm);
    cartEl = document.createElement('div'); cartEl.className = 's24x-ov s24x-ov-r'; cartEl.id = 's24x-cart'; cartEl.hidden = true;
    cartEl.innerHTML = '<aside class="s24x-drawer" role="dialog" aria-modal="true" aria-labelledby="s24x-cart-h"><div class="s24x-dh"><h2 id="s24x-cart-h">Coșul tău</h2><button type="button" class="s24x-x" data-close aria-label="Închide">' + I.x + '</button></div><div class="s24x-dmsg" aria-live="polite"></div><div class="s24x-dl"></div><div class="s24x-df"></div></aside>';
    document.body.appendChild(cartEl);
    [pm, cartEl].forEach(function (o) { o.addEventListener('click', function (e) { if (e.target === o || e.target.closest('[data-close]')) closeAll(); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });
    pm.addEventListener('click', function (e) {
      var q = pm.querySelector('.s24x-qty input'); if (!q) return;
      var d = e.target.closest('[data-q]'); if (d) { q.value = Math.max(1, Math.min(99, (+q.value || 1) + (+d.getAttribute('data-q')))); return; }
      var a = e.target.closest('[data-padd]'); if (a) { var x = BYID[a.getAttribute('data-padd')]; cartAdd(x.id, Math.max(1, Math.min(99, +q.value || 1))); closeAll(true); openCart(x); }
    });
    cartEl.addEventListener('click', function (e) {
      var r = e.target.closest('[data-cid]'); if (!r) return; var id = r.getAttribute('data-cid'), c = cartGet(), it = c.filter(function (y) { return y.id === id; })[0]; if (!it) return;
      if (e.target.closest('[data-rm]')) c = c.filter(function (y) { return y.id !== id; });
      else { var d = e.target.closest('[data-cq]'); if (!d) return; it.qty = Math.max(1, Math.min(99, it.qty + (+d.getAttribute('data-cq')))); }
      cartSet(c); renderCart();
    });
  }
  function show(o) { lastFocus = document.activeElement; o.hidden = false; document.documentElement.classList.add('s24x-lock'); requestAnimationFrame(function () { o.classList.add('on'); var f = o.querySelector('[data-close]'); if (f) f.focus(); }); }
  function closeAll(keepFocus) {
    [pm, cartEl].forEach(function (o) { if (o && !o.hidden) { o.classList.remove('on'); o.hidden = true; } });
    document.documentElement.classList.remove('s24x-lock'); if (!keepFocus && lastFocus && lastFocus.focus) try { lastFocus.focus(); } catch (e) {}
  }
  function openProduct(x) {
    ensureUi(); var img = x.photo || FALLBACK[x.cat] || 'images/kit-hilook-8.svg', av = AV[x.avail];
    pm.querySelector('.s24x-pm-in').innerHTML = '<div class="s24x-pm-img"><img src="' + esc(img) + '" alt="' + esc(x.name) + '"></div><div class="s24x-pm-txt">' +
      '<div class="s24x-cat">' + esc([x.brand, catName(x)].filter(Boolean).join(' · ')) + '</div><h2 id="s24x-pm-h">' + esc(x.name) + '</h2>' + (x.model ? '<div class="s24x-sku">Cod produs: ' + esc(x.model) + '</div>' : '') +
      (x.tagline ? '<p class="s24x-tag">' + esc(x.tagline) + '</p>' : '') +
      (priced(x) ? '<div class="s24x-pm-buy"><div>' + (hasDisc(x) ? '<div class="s24x-pmd"><s class="s24x-old">' + lei(x.oldPrice) + ' lei</s><span class="s24x-offi">-' + x.disc + '%</span>' + (x.discUntil ? '<span class="s24x-until">până la ' + dmy(x.discUntil) + '</span>' : '') + '</div>' : '') + '<div class="s24x-price s24x-price-l' + (hasDisc(x) ? ' s24x-red' : '') + '">' + lei(x.price) + '<small> lei</small></div>' + (av ? '<span class="s24x-av ' + av[1] + '">' + av[0] + '</span>' : '') + '</div>' +
        '<div class="s24x-pm-act"><div class="s24x-qty"><button type="button" data-q="-1" aria-label="Mai puține">−</button><input type="number" value="1" min="1" max="99" inputmode="numeric" aria-label="Cantitate"><button type="button" data-q="1" aria-label="Mai multe">+</button></div>' +
        '<button type="button" class="s24x-add s24x-add-l" data-padd="' + esc(x.id) + '">' + I.cart + '<span>Adaugă în coș</span></button></div></div>'
        : '<div class="s24x-pm-buy"><div><div class="s24x-ask">Preț la cerere</div></div><a href="' + (document.getElementById('contact') ? '#contact' : 'contact.html') + '" class="s24x-add s24x-add-l" data-ofr="' + esc([x.brand, x.model || x.name].filter(Boolean).join(' ')) + '">Cere ofertă</a></div>') +
      ((x.specs || []).length ? '<h3 class="s24x-pm-h3">Caracteristici</h3><ul class="s24x-spec s24x-spec-l">' + x.specs.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ul>' : '') +
      (x.datasheet ? '<a class="s24x-pdf" href="' + esc(x.datasheet) + '" target="_blank" rel="noopener">' + I.pdf + 'Fișa tehnică (PDF)</a>' : '') +
      '<ul class="s24x-pm-notes" role="list">' + (priced(x) ? '<li>' + I.shield + 'Garanție 2 ani · factură fiscală</li><li>' + I.truck + 'Livrare prin curier' + (SHOP.pickup ? ' sau ridicare din București' : '') + '</li>' : '<li>' + I.shield + 'Inclus în abonamentul pentru blocuri, cu garanție pe toată durata contractului</li>') +
      '<li>' + I.tool + 'Vrei și montaj? <a href="' + (document.getElementById('contact') ? '#contact' : 'contact.html') + '" data-ofr="' + esc('montaj pentru ' + [x.brand, x.model || x.name].filter(Boolean).join(' ')) + '">Cere ofertă cu montaj</a></li></ul></div>';
    show(pm);
  }
  // ── coșul lateral ──
  function renderCart(added) {
    var c = cartGet(), sub = 0, n = 0, rows = c.map(function (it) {
      var x = BYID[it.id]; if (!x || !priced(x)) return '';
      sub += x.price * it.qty; n += it.qty;
      return '<div class="s24x-ci" data-cid="' + esc(x.id) + '"><img src="' + esc(x.photo || FALLBACK[x.cat] || 'images/kit-hilook-8.svg') + '" alt=""><div class="s24x-ci-t"><b>' + esc(x.name) + '</b><span>' + lei(x.price) + ' lei / buc.</span>' +
        '<div class="s24x-qty s24x-qty-s"><button type="button" data-cq="-1" aria-label="Mai puține">−</button><output>' + it.qty + '</output><button type="button" data-cq="1" aria-label="Mai multe">+</button></div></div>' +
        '<div class="s24x-ci-r"><b>' + lei(x.price * it.qty) + ' lei</b><button type="button" data-rm>Șterge</button></div></div>';
    }).join('');
    cartEl.querySelector('.s24x-dmsg').innerHTML = added ? '<div class="s24x-added">' + I.check + '<span><b>' + esc(added.name) + '</b> a fost adăugat în coș</span></div>' : '';
    cartEl.querySelector('.s24x-dl').innerHTML = rows || '<p class="s24x-empty">Coșul este gol.</p>';
    var left = SHOP.freeOver ? SHOP.freeOver - sub : 0;
    cartEl.querySelector('.s24x-df').innerHTML = n ? '<div class="s24x-sum"><span>Subtotal (' + n + ' buc.)</span><b>' + lei(sub) + ' lei</b></div>' +
      (SHOP.freeOver ? '<div class="s24x-ship">' + (left > 0 ? 'Mai adaugă <b>' + lei(left) + ' lei</b> pentru transport gratuit' : '<b>Transport gratuit</b> prin curier') + '<i style="--p:' + Math.min(100, Math.round(sub / SHOP.freeOver * 100)) + '%"></i></div>' : '') +
      '<a class="s24x-add s24x-add-l s24x-go" href="cos.html">Finalizează comanda</a><button type="button" class="s24x-cont" data-close>Continuă cumpărăturile</button>'
      : '<button type="button" class="s24x-cont" data-close>Înapoi la produse</button>';
  }
  function openCart(added) { ensureUi(); renderCart(added); show(cartEl); }
  window.s24openCart = function () { if (SHOP.on) openCart(); else location.href = 'cos.html'; };

  function run() {
    box = document.getElementById('camere-ip'); if (!box) return;
    var slot = box.querySelector('.s24-cat-items') || box, cats = (box.getAttribute('data-cats') || '').split(',').filter(Boolean);
    var title = (box.querySelector('.s24-block-h') || {}).textContent || 'Echipamente';
    if (/Ce montăm/.test(title)) title = 'Toate echipamentele';
    var empty = '<p style="margin:18px 0 0;color:#3D4F63">Lista echipamentelor se actualizează. Pentru detalii despre modelele pe care le montăm, sună-ne la <a href="tel:+40763354355" style="color:#0D1F33;font-weight:700">0763 354 355</a>.</p>';
    if (!window.fetch) { slot.innerHTML = empty; return; }
    fetch(API, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      ALL = (d && d.items || []).filter(function (x) { return !cats.length || cats.indexOf(x.cat) >= 0; });
      if (!ALL.length) { slot.innerHTML = empty; return; }
      SHOP = d.shop && d.shop.on ? d.shop : { on: false }; ALL.forEach(function (x) { BYID[x.id] = x; });
      (d.items || []).forEach(function (x) { BYID[x.id] = x; });
      if (SHOP.on) { document.documentElement.setAttribute('data-shop', 'on'); try { window.dispatchEvent(new Event('s24cart')); } catch (e) {}
        var p = document.querySelector('.s24-shop-p'); if (p) p.textContent = 'Camere IP, NVR-uri, hard disk-uri și accesorii HiLook, Hikvision și Dahua — aceleași echipamente pe care le montăm noi. Le poți cumpăra cu factură și livrare prin curier, iar pentru blocuri sunt incluse în abonament.'; }
      build(title);
    }).catch(function () { slot.innerHTML = empty; });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
