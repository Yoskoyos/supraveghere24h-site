/* s24catalog: echipamentele bifate „Pe site” în aplicație (tabul Echipamente) înlocuiesc lista de pe pagina Echipamente.
   Dacă serverul nu răspunde sau lista e goală, rămâne conținutul static al paginii. */
(function () {
  var API = 'https://proxy.supraveghere24h.ro/public/catalog';
  var CAT = { exterior: 'Cameră exterior', interior: 'Cameră interior', lift: 'Cameră lift', nvr: 'Recorder (NVR)', hdd: 'Hard disk', rack: 'Rack și protecție', retea: 'Rețea și alimentare', altele: 'Altele' };
  var FALLBACK = { exterior: 'images/cam-hilook-bullet.svg', interior: 'images/cam-hilook-turret.svg', lift: 'images/cam-hilook-turret.svg' };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function card(x) {
    var img = x.photo || FALLBACK[x.cat] || 'images/kit-hilook-8.svg';
    var title = x.name;
    var meta = [['Marcă', x.brand], ['Cod produs', x.model], ['Tip', CAT[x.cat]], ['Garanție', 'Inclusă pe toată durata abonamentului']].filter(function (r) { return r[1]; });
    return '<div class="s24-pd"><img src="' + esc(img) + '" loading="lazy" alt="' + esc(title) + '" class="s24-pd-img" width="400" height="300" style="object-fit:contain;background:#fff">' +
      '<div class="s24-pd-info"><h3 class="s24-pd-h">' + esc(title) + '</h3>' +
      (x.tagline ? '<p class="s24-pd-lead">' + esc(x.tagline) + '</p>' : '') +
      ((x.specs || []).length ? '<ul role="list" class="s24-pd-list">' + x.specs.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ul>' : '') +
      '<table class="s24-pd-meta"><tbody>' + meta.map(function (r) { return '<tr><td class="s24-pd-k">' + esc(r[0]) + '</td><td class="s24-pd-v">' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody></table>' +
      (x.datasheet ? '<p style="margin:0 0 14px"><a href="' + esc(x.datasheet) + '" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:8px;font-weight:700;color:#0D1F33;text-decoration:underline;text-underline-offset:3px;min-height:44px"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F5A100" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/><path d="M12 18v-6M9 15l3 3 3-3"/></svg>Fișa tehnică (PDF)</a></p>' : '') +
      '<a href="calculator-pret.html" class="s24-pd-cta">Calculează prețul</a>' +
      '<p class="s24-pd-note">Echipamentele sunt incluse în abonamentul lunar, fără investiție inițială.</p></div></div>';
  }
  function bindZoom(root) {
    var lb = document.getElementById('s24-lb'); if (!lb) return;
    root.querySelectorAll('.s24-pd-img').forEach(function (im) {
      im.addEventListener('click', function () { var i = lb.querySelector('img'); i.src = im.src; i.alt = im.alt; lb.classList.add('s24-lb-on'); });
    });
  }
  function run() {
    var box = document.getElementById('camere-ip'); if (!box || !window.fetch) return;
    fetch(API, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.items || !d.items.length) return;
      var h = box.querySelector('.s24-block-h'), p = box.querySelector('.s24-block-p');
      box.innerHTML = (h ? h.outerHTML : '') + (p ? p.outerHTML : '') + d.items.map(card).join('');
      bindZoom(box);
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
