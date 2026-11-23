/* s24cos: pagina coșului (cos.html) — produsele din coș cu prețurile actuale de pe server, datele de livrare și facturare,
   trimiterea comenzii la /public/order și confirmarea. Prețurile le recalculează serverul; dacă s-au schimbat, coșul se reîncarcă. */
(function () {
  var API = 'https://proxy.supraveghere24h.ro';
  var JUD = ['București', 'Ilfov', 'Alba', 'Arad', 'Argeș', 'Bacău', 'Bihor', 'Bistrița-Năsăud', 'Botoșani', 'Brăila', 'Brașov', 'Buzău', 'Călărași', 'Caraș-Severin', 'Cluj', 'Constanța', 'Covasna', 'Dâmbovița', 'Dolj', 'Galați', 'Giurgiu', 'Gorj', 'Harghita', 'Hunedoara', 'Ialomița', 'Iași', 'Maramureș', 'Mehedinți', 'Mureș', 'Neamț', 'Olt', 'Prahova', 'Sălaj', 'Satu Mare', 'Sibiu', 'Suceava', 'Teleorman', 'Timiș', 'Tulcea', 'Vâlcea', 'Vaslui', 'Vrancea'];
  var FALLBACK = { exterior: 'images/cam-hilook-bullet.svg', interior: 'images/cam-hilook-turret.svg', lift: 'images/cam-hilook-turret.svg' };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function lei(n) { return (Math.round(n * 100) / 100).toLocaleString('ro-RO', { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 }) + ' lei'; }
  function cartGet() { try { var c = JSON.parse(localStorage.getItem('s24cart') || '[]'); return Array.isArray(c) ? c.filter(function (x) { return x && x.id && x.qty > 0; }) : []; } catch (e) { return []; } }
  function cartSet(c) { try { localStorage.setItem('s24cart', JSON.stringify(c)); } catch (e) {} try { window.dispatchEvent(new Event('s24cart')); } catch (e) {} }
  var root, BY = {}, SHOP = null, lines = [], form = { type: 'pf', delivery: 'curier', pay: '' }, sending = false;   // doar livrare prin curier (ridicarea personală scoasă 23.11.2026)
  try { var saved = JSON.parse(sessionStorage.getItem('s24cos') || 'null'); if (saved) form = saved; } catch (e) {}
  form.delivery = 'curier';

  function totals() {
    var sub = lines.reduce(function (t, l) { return t + l.x.price * l.qty; }, 0);
    var ship = form.delivery === 'curier' ? (SHOP.freeOver > 0 && sub >= SHOP.freeOver ? 0 : SHOP.ship) : 0;
    var fee = form.pay === 'ramburs' ? SHOP.codFee || 0 : 0;
    return { sub: sub, ship: ship, fee: fee, total: sub + ship + fee, n: lines.reduce(function (t, l) { return t + l.qty; }, 0) };
  }
  function payOpts() {
    var o = [];
    if (form.delivery === 'curier' && SHOP.cod) o.push(['ramburs', 'Ramburs, la curier', 'Plătești când primești coletul' + (SHOP.codFee ? ' · taxă ' + lei(SHOP.codFee) : '')]);
    if (SHOP.op) o.push(['op', 'Transfer bancar', 'Primești pe e-mail datele de plată; expediem după ce primim banii']);
    return o;
  }
  function sync() { lines = cartGet().map(function (c) { return { x: BY[c.id], qty: c.qty }; }).filter(function (l) { return l.x && l.x.price > 0; }); }
  function save() { try { sessionStorage.setItem('s24cos', JSON.stringify(form)); } catch (e) {} }
  function val(n) { var el = root.querySelector('[name="' + n + '"]'); return el ? (el.type === 'checkbox' ? el.checked : el.value.trim()) : ''; }
  function grab() { ['name', 'phone', 'email', 'company', 'cui', 'regcom', 'county', 'city', 'address', 'zip', 'notes'].forEach(function (k) { var el = root.querySelector('[name="' + k + '"]'); if (el) form[k] = el.value; }); save(); }

  function render() {
    sync();
    if (!lines.length) {
      root.innerHTML = '<div class="s24c-empty"><div class="s24c-ei"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.7 12.4a2 2 0 0 0 2 1.6h8.6a2 2 0 0 0 2-1.5L22 7H6"/></svg></div><h2>Coșul tău este gol</h2><p>Alege camerele, NVR-ul și accesoriile de care ai nevoie din pagina de echipamente.</p><a class="s24x-add s24x-add-l" href="echipamente.html">Vezi echipamentele</a></div>';
      return;
    }
    var po = payOpts(); if (!po.some(function (p) { return p[0] === form.pay; })) form.pay = po.length ? po[0][0] : '';
    var t = totals();
    var radio = function (name, v, title, sub, on, extra) { return '<label class="s24c-opt' + (on ? ' on' : '') + '"><input type="radio" name="' + name + '" value="' + v + '"' + (on ? ' checked' : '') + '><span class="s24c-dot"></span><span class="s24c-ot"><b>' + title + '</b><small>' + sub + '</small></span>' + (extra ? '<span class="s24c-ox">' + extra + '</span>' : '') + '</label>'; };
    var f = function (n, label, type, req, attrs, cls) { return '<div class="s24c-f' + (cls ? ' ' + cls : '') + '"><label for="c-' + n + '">' + label + (req ? '' : ' <i>(opțional)</i>') + '</label><input id="c-' + n + '" name="' + n + '" type="' + (type || 'text') + '"' + (req ? ' required' : '') + ' value="' + esc(form[n] || '') + '"' + (attrs || '') + '></div>'; };
    root.innerHTML = '<div class="s24c-grid"><div class="s24c-main">' +
      '<section class="s24c-card"><h2 class="s24c-h">Produsele tale <span>' + t.n + ' buc.</span></h2>' +
      lines.map(function (l) { var x = l.x; return '<div class="s24c-li" data-id="' + esc(x.id) + '"><img src="' + esc(x.photo || FALLBACK[x.cat] || 'images/kit-hilook-8.svg') + '" alt=""><div class="s24c-lt"><b>' + esc(x.name) + '</b><span>' + esc([x.brand, x.model].filter(Boolean).join(' · ')) + '</span><span class="s24c-up">' + lei(x.price) + ' / buc.</span></div>' +
        '<div class="s24x-qty s24x-qty-s"><button type="button" data-q="-1" aria-label="Mai puține">−</button><output>' + l.qty + '</output><button type="button" data-q="1" aria-label="Mai multe">+</button></div>' +
        '<div class="s24c-lr"><b>' + lei(x.price * l.qty) + '</b><button type="button" data-rm>Șterge</button></div></div>'; }).join('') +
      '<a class="s24c-more" href="echipamente.html">← Adaugă și alte produse</a></section>' +
      '<form class="s24c-card" id="s24c-form" novalidate><h2 class="s24c-h">Date de facturare</h2>' +
      '<div class="s24c-seg" role="radiogroup" aria-label="Tip client"><label class="' + (form.type === 'pf' ? 'on' : '') + '"><input type="radio" name="type" value="pf"' + (form.type === 'pf' ? ' checked' : '') + '>Persoană fizică</label><label class="' + (form.type === 'pj' ? 'on' : '') + '"><input type="radio" name="type" value="pj"' + (form.type === 'pj' ? ' checked' : '') + '>Firmă / asociație</label></div>' +
      '<div class="s24c-row">' + f('name', 'Nume și prenume', 'text', 1, ' autocomplete="name" maxlength="120"') + f('phone', 'Telefon', 'tel', 1, ' autocomplete="tel" inputmode="tel" maxlength="40"') + '</div>' +
      f('email', 'E-mail (aici primești confirmarea comenzii)', 'email', 1, ' autocomplete="email" maxlength="160"') +
      (form.type === 'pj' ? '<div class="s24c-row">' + f('company', 'Denumirea firmei / asociației', 'text', 1, ' autocomplete="organization" maxlength="160"') + f('cui', 'CUI / CIF', 'text', 1, ' maxlength="30"') + '</div>' + f('regcom', 'Nr. Reg. Comerțului', 'text', 0, ' maxlength="40"') : '') +
      '<h2 class="s24c-h s24c-h2">Livrare</h2><div class="s24c-opts">' +
      radio('delivery', 'curier', 'Livrare prin curier', 'La adresa ta, în 1–3 zile lucrătoare după expediere', form.delivery === 'curier', t.ship || form.delivery !== 'curier' ? (SHOP.freeOver && t.sub >= SHOP.freeOver ? 'gratuit' : lei(SHOP.ship)) : 'gratuit') +
      '</div>' +
      (form.delivery === 'curier' ? '<div class="s24c-row">' + '<div class="s24c-f"><label for="c-county">Județ</label><select id="c-county" name="county" required autocomplete="address-level1"><option value="">Alege județul</option>' + JUD.map(function (j) { return '<option' + (form.county === j ? ' selected' : '') + '>' + j + '</option>'; }).join('') + '</select></div>' + f('city', 'Localitate / sector', 'text', 1, ' autocomplete="address-level2" maxlength="80"') + '</div>' +
        '<div class="s24c-row s24c-row-a">' + f('address', 'Strada, număr, bloc, scară, apartament', 'text', 1, ' autocomplete="street-address" maxlength="300"') + f('zip', 'Cod poștal', 'text', 0, ' autocomplete="postal-code" inputmode="numeric" maxlength="12"', 's24c-zip') + '</div>' : '') +
      '<h2 class="s24c-h s24c-h2">Plata</h2><div class="s24c-opts">' + po.map(function (p) { return radio('pay', p[0], p[1], p[2], form.pay === p[0]); }).join('') + '</div>' +
      '<div class="s24c-f"><label for="c-notes">Observații <i>(opțional)</i></label><textarea id="c-notes" name="notes" rows="3" maxlength="1500" placeholder="ex. interval orar pentru livrare, dacă vrei și montaj, alte detalii">' + esc(form.notes || '') + '</textarea></div>' +
      '<input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" class="s24c-hp">' +
      '</form></div>' +
      '<aside class="s24c-side"><div class="s24c-card s24c-sum"><h2 class="s24c-h">Sumar comandă</h2>' +
      '<div class="s24c-sr"><span>Produse (' + t.n + ' buc.)</span><b>' + lei(t.sub) + '</b></div>' +
      (form.delivery === 'curier' ? '<div class="s24c-sr"><span>Transport</span><b>' + (t.ship ? lei(t.ship) : 'gratuit') + '</b></div>' : '<div class="s24c-sr"><span>Ridicare din sediu</span><b>gratuit</b></div>') +
      (t.fee ? '<div class="s24c-sr"><span>Taxă ramburs</span><b>' + lei(t.fee) + '</b></div>' : '') +
      (form.delivery === 'curier' && SHOP.freeOver && t.sub < SHOP.freeOver ? '<div class="s24x-ship">Mai adaugă <b>' + lei(SHOP.freeOver - t.sub) + '</b> pentru transport gratuit<i style="--p:' + Math.round(t.sub / SHOP.freeOver * 100) + '%"></i></div>' : '') +
      '<div class="s24c-tot"><span>Total de plată</span><b>' + lei(t.total) + '</b></div><p class="s24c-vat">Prețuri finale. Firma nu este plătitoare de TVA.</p>' +
      '<label class="s24c-terms"><input type="checkbox" name="terms" form="s24c-form"' + (form.terms ? ' checked' : '') + '><span>Am citit și accept <a href="termeni-si-conditii.html#vanzare" target="_blank">Termenii și condițiile de vânzare</a> și <a href="livrare-si-retur.html" target="_blank">condițiile de livrare și retur</a>. Datele mele sunt folosite pentru comandă conform <a href="politica-de-confidentialitate.html" target="_blank">politicii de confidențialitate</a>.</span></label>' +
      '<div class="s24c-err" role="alert" hidden></div>' +
      '<button type="submit" form="s24c-form" class="s24x-add s24x-add-l s24c-send">Trimite comanda · ' + lei(t.total) + '</button>' +
      '<p class="s24c-after">Te sunăm să confirmăm comanda înainte de expediere. Nu plătești nimic acum.</p>' +
      (SHOP.note ? '<p class="s24c-note">' + esc(SHOP.note) + '</p>' : '') + '</div>' +
      '<ul class="s24c-trust" role="list"><li>Produse originale, garanție 2 ani</li><li>Factură fiscală pentru fiecare comandă</li><li>Retur în 14 zile pentru persoane fizice</li><li>Întrebări? <a href="tel:+40763354355">0763 354 355</a></li></ul></aside></div>';
  }

  function onClick(e) {
    var li = e.target.closest('.s24c-li');
    if (li) { var id = li.getAttribute('data-id'), c = cartGet(), it = c.filter(function (y) { return y.id === id; })[0]; if (!it) return;
      if (e.target.closest('[data-rm]')) c = c.filter(function (y) { return y.id !== id; });
      else { var d = e.target.closest('[data-q]'); if (!d) return; it.qty = Math.max(1, Math.min(99, it.qty + (+d.getAttribute('data-q')))); }
      grab(); cartSet(c); render(); }
  }
  function onChange(e) {
    var n = e.target.name; if (!n) return;
    if (n === 'type' || n === 'delivery' || n === 'pay') { grab(); form[n] = e.target.value; save(); var y = window.scrollY; render(); window.scrollTo(0, y); return; }
    if (n === 'terms') { form.terms = e.target.checked; save(); }
  }
  function err(msg, el) {
    var b = root.querySelector('.s24c-err'); b.textContent = msg; b.hidden = !msg;
    if (el) { el.setAttribute('aria-invalid', 'true'); el.focus(); el.addEventListener('input', function f() { el.removeAttribute('aria-invalid'); el.removeEventListener('input', f); }); }
  }
  function submit(e) {
    e.preventDefault(); if (sending) return; grab(); err('');
    var need = [['name', 'Completează numele.'], ['phone', 'Completează telefonul.'], ['email', 'Completează adresa de e-mail.']];
    if (form.type === 'pj') need.push(['company', 'Completează denumirea firmei.'], ['cui', 'Completează CUI-ul.']);
    if (form.delivery === 'curier') need.push(['county', 'Alege județul.'], ['city', 'Completează localitatea.'], ['address', 'Completează adresa de livrare.']);
    for (var i = 0; i < need.length; i++) { if (!val(need[i][0])) return err(need[i][1], root.querySelector('[name="' + need[i][0] + '"]')); }
    if (val('phone').replace(/\D/g, '').length < 9) return err('Numărul de telefon nu pare complet.', root.querySelector('[name="phone"]'));
    if (!/^[^\s@<>,;]+@[^\s@<>,;]+\.[a-z]{2,}$/i.test(val('email'))) return err('Adresa de e-mail nu pare corectă.', root.querySelector('[name="email"]'));
    if (!form.pay) return err('Alege metoda de plată.');
    if (!root.querySelector('[name="terms"]').checked) return err('Bifează acceptarea termenilor ca să trimiți comanda.', root.querySelector('[name="terms"]'));
    var body = { items: lines.map(function (l) { return { id: l.x.id, qty: l.qty, price: l.x.price }; }), delivery: form.delivery, pay: form.pay, terms: true, website: val('website'),
      c: { type: form.type, name: form.name, phone: form.phone, email: form.email, company: form.type === 'pj' ? form.company : '', cui: form.type === 'pj' ? form.cui : '', regcom: form.type === 'pj' ? form.regcom : '',
        county: form.delivery === 'curier' ? form.county : '', city: form.delivery === 'curier' ? form.city : '', address: form.delivery === 'curier' ? form.address : '', zip: form.delivery === 'curier' ? form.zip : '', notes: form.notes } };
    var btn = root.querySelector('.s24c-send'); sending = true; btn.disabled = true; btn.textContent = 'Se trimite comanda…';
    fetch(API + '/public/order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(function (r) { return r.json().catch(function () { return { error: 'Răspuns neașteptat de la server' }; }).then(function (d) { return { st: r.status, d: d }; }); })
      .then(function (r) {
        sending = false;
        if (r.st === 200 && r.d.ok) return done(r.d);
        if (r.st === 409) { return load(function () { err(r.d.error || 'Coșul s-a schimbat. Verifică-l din nou.'); }); }
        btn.disabled = false; btn.textContent = 'Trimite comanda'; err(r.d.error || 'Comanda nu a putut fi trimisă. Încearcă din nou sau sună-ne la 0763 354 355.');
      }).catch(function () { sending = false; btn.disabled = false; btn.textContent = 'Trimite comanda'; err('Nu am putut trimite comanda (fără conexiune?). Încearcă din nou sau sună-ne la 0763 354 355.'); });
  }
  function done(d) {
    cartSet([]); try { sessionStorage.removeItem('s24cos'); } catch (e) {}
    root.innerHTML = '<div class="s24c-ok"><div class="s24c-oki"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg></div><h2>Mulțumim! Am primit comanda <b>' + esc(d.no) + '</b></h2>' +
      '<p>' + (d.mailed ? 'Ți-am trimis confirmarea pe e-mail, la <b>' + esc(form.email) + '</b>. ' : '') + 'Te sunăm în cel mai scurt timp, în zilele lucrătoare, ca să confirmăm comanda și livrarea.</p>' +
      (d.pay === 'op' ? '<div class="s24c-bank"><b>Date pentru plată</b><span>Beneficiar: YCA SOLUTIONS S.R.L. · CUI 45211628</span><span>IBAN: <b>RO62INGB0000999911979489</b> (ING Bank)</span><span>Suma: <b>' + lei(d.total) + '</b> · Detalii plată: <b>' + esc(d.no) + '</b></span><small>Expediem comanda după ce primim plata.</small></div>' : '<p>Total de plată: <b>' + lei(d.total) + '</b>' + (d.pay === 'ramburs' ? ', la curier.' : ', la ridicare.') + '</p>') +
      '<p class="s24c-okq">Întrebări despre comandă: <a href="tel:+40763354355">0763 354 355</a> · <a href="mailto:contact@supraveghere24h.ro">contact@supraveghere24h.ro</a></p><a class="s24x-add s24x-add-o" href="echipamente.html">Înapoi la echipamente</a></div>';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  function load(after) {
    fetch(API + '/public/catalog', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      SHOP = d && d.shop && d.shop.on ? d.shop : null; BY = {};
      if (!SHOP) { root.innerHTML = '<div class="s24c-empty"><h2>Comenzile online nu sunt disponibile acum</h2><p>Ne poți suna la <a href="tel:+40763354355">0763 354 355</a> sau ne poți scrie la <a href="mailto:contact@supraveghere24h.ro">contact@supraveghere24h.ro</a> și îți facem o ofertă.</p><a class="s24x-add s24x-add-l" href="echipamente.html">Vezi echipamentele</a></div>'; return; }
      (d.items || []).forEach(function (x) { BY[x.id] = x; });
      var c = cartGet(), keep = c.filter(function (x) { return BY[x.id] && BY[x.id].price > 0; });
      if (keep.length !== c.length) cartSet(keep);
      render(); if (after) after();
      if (keep.length !== c.length && keep.length) { var b = root.querySelector('.s24c-err'); if (b) { b.textContent = 'Am scos din coș produsele care nu mai sunt disponibile.'; b.hidden = false; } }
    }).catch(function () { root.innerHTML = '<div class="s24c-empty"><h2>Nu am putut încărca coșul</h2><p>Verifică conexiunea și reîncarcă pagina, sau sună-ne la <a href="tel:+40763354355">0763 354 355</a>.</p></div>'; });
  }
  function init() {
    root = document.getElementById('s24c'); if (!root) return;
    root.addEventListener('click', onClick); root.addEventListener('change', onChange); root.addEventListener('submit', submit);
    root.addEventListener('input', function (e) { if (e.target.name && e.target.name !== 'website') { form[e.target.name] = e.target.value; save(); } });
    if (!window.fetch) { root.innerHTML = '<p>Browserul tău nu poate trimite comanda. Sună-ne la 0763 354 355.</p>'; return; }
    load();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
