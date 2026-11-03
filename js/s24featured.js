/* s24featured: 4 echipamente din aplicație (tabul Echipamente, bifate „Pe site”) pe prima pagină.
   Câte unul din: cameră exterior, cameră interior, NVR, stocare; restul locurilor se completează cu alte camere. */
(function () {
  var API = 'https://proxy.supraveghere24h.ro/public/catalog';
  var CAT = { exterior: 'Cameră exterior', interior: 'Cameră interior', lift: 'Cameră lift', nvr: 'Recorder (NVR)', hdd: 'Stocare', rack: 'Accesorii', retea: 'Accesorii', altele: 'Accesorii' };
  var PAGE = { exterior: 'camere-ip-exterior.html', interior: 'camere-ip-interior.html', lift: 'camere-ip-interior.html', nvr: 'nvr-uri.html', hdd: 'stocare.html' };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pick(items) {
    var out = [], used = {};
    ['exterior', 'interior', 'nvr', 'hdd'].forEach(function (c) { var x = items.filter(function (i) { return i.cat === c && i.photo; })[0]; if (x) { out.push(x); used[x.id] = 1; } });
    items.forEach(function (i) { if (out.length < 4 && !used[i.id] && i.photo && /exterior|interior|lift/.test(i.cat)) { out.push(i); used[i.id] = 1; } });
    return out.slice(0, 4);
  }
  function card(x) {
    var specs = (x.specs || []).slice(0, 3);
    return '<a class="s24f-c" href="' + (PAGE[x.cat] || 'echipamente.html') + '">' +
      '<span class="s24f-img"><img src="' + esc(x.photo) + '" alt="' + esc(x.name) + '" loading="lazy" width="400" height="300"></span>' +
      '<span class="s24f-tag">' + esc(CAT[x.cat] || 'Echipament') + '</span>' +
      '<b class="s24f-n">' + esc(x.name) + '</b>' +
      '<span class="s24f-m">' + esc([x.brand, x.model].filter(Boolean).join(' · ')) + '</span>' +
      (specs.length ? '<ul class="s24f-s">' + specs.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ul>' : '') + '</a>';
  }
  function run() {
    var box = document.getElementById('s24f-grid'); if (!box || !window.fetch) return;
    fetch(API, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      var L = pick((d && d.items) || []); if (!L.length) return;
      box.innerHTML = L.map(card).join(''); box.hidden = false;
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
