/* Meniul de sus: „pastilă” portocalie care alunecă între linkuri la hover și stă pe pagina curentă (doar pe desktop) */
(function () {
  function init() {
    var box = document.querySelector('.s24-nav-in > .s24-links'); if (!box || box.querySelector('.s24-ind')) return;
    var ind = document.createElement('span'); ind.className = 's24-ind'; ind.setAttribute('aria-hidden', 'true'); box.insertBefore(ind, box.firstChild);
    var links = [].slice.call(box.querySelectorAll('.s24-link'));
    var cur = links.filter(function (a) { return a.classList.contains('w--current'); })[0] || null;
    function place(a, instant) {
      if (!a || getComputedStyle(box).display === 'none' || window.innerWidth < 992) { ind.classList.remove('on'); return; }
      var b = box.getBoundingClientRect(), r = a.getBoundingClientRect();
      if (instant) ind.style.transition = 'none';
      ind.style.width = r.width + 'px'; ind.style.height = r.height + 'px';
      ind.style.transform = 'translate(' + (r.left - b.left) + 'px,' + (r.top - b.top) + 'px)';
      ind.classList.add('on');
      if (instant) { ind.offsetWidth; ind.style.transition = ''; }
    }
    links.forEach(function (a) {
      a.addEventListener('mouseenter', function () { place(a); });
      a.addEventListener('focus', function () { place(a); });
    });
    box.addEventListener('mouseleave', function () { cur ? place(cur) : ind.classList.remove('on'); });
    window.addEventListener('resize', function () { cur ? place(cur, true) : ind.classList.remove('on'); });
    if (cur) setTimeout(function () { place(cur, true); }, 650);   // după animația de intrare a linkurilor
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
/* Antet: rămâne sus la derulare (bara de sus iese din ecran), umbră după derulare; „Servicii” ▾ pe ecrane tactile; nota Google în bara de sus */
(function () {
  function init() {
    var h = document.querySelector('.s24-header'); if (!h || h.getAttribute('data-hdr')) return; h.setAttribute('data-hdr', '1');
    var top = h.querySelector('.s24-top');
    function fit() { var t = top && top.offsetParent !== null ? top.offsetHeight : 0; h.style.top = (-t) + 'px'; }
    function onScroll() { h.classList.toggle('s24-scrolled', (window.scrollY || window.pageYOffset) > 12); }
    fit(); onScroll(); window.addEventListener('resize', fit); window.addEventListener('scroll', onScroll, { passive: true });
    // „Servicii”: pe ecran tactil, prima atingere deschide meniul, a doua merge la pagină
    var dd = h.querySelector('.s24-dd'), t = dd && dd.querySelector('.s24-dd-t');
    if (dd && t) {
      var touch = window.matchMedia && window.matchMedia('(hover: none)').matches;
      t.addEventListener('click', function (e) {
        if (window.innerWidth < 768) return;
        if (touch && !dd.classList.contains('s24-dd-open')) { e.preventDefault(); dd.classList.add('s24-dd-open'); t.setAttribute('aria-expanded', 'true'); }
      });
      document.addEventListener('click', function (e) { if (!dd.contains(e.target)) { dd.classList.remove('s24-dd-open'); t.setAttribute('aria-expanded', 'false'); } });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { dd.classList.remove('s24-dd-open'); t.setAttribute('aria-expanded', 'false'); } });
    }
    // nota reală din Google (prin serverul nostru); apare doar dacă sunt cel puțin 3 recenzii
    var g = document.getElementById('s24-grate');
    if (g && window.fetch) fetch('https://proxy.supraveghere24h.ro/public/reviews', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.configured || !(d.count >= 3) || !(d.rating > 0)) return;
      if (String(d.name || '').toLowerCase().replace(/[^a-z0-9]/g, '').indexOf('supraveghere24h') < 0) return;
      var r = Math.round(d.rating * 10) / 10;
      g.innerHTML = '<span class="s24-stars" aria-hidden="true">★★★★★</span>' + String(r.toFixed(1)).replace('.', ',') + ' pe Google · ' + d.count + ' recenzii';
      if (d.url) g.href = d.url; g.setAttribute('aria-label', 'Nota ' + r + ' din 5 pe Google, ' + d.count + ' recenzii'); g.hidden = false;
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
/* Coșul din antet: apare când ai ceva în coș sau pe paginile magazinului (cu magazinul pornit) */
(function () {
  var SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.7 12.4a2 2 0 0 0 2 1.6h8.6a2 2 0 0 0 2-1.5L22 7H6"/></svg>';
  function count() { try { return (JSON.parse(localStorage.getItem('s24cart') || '[]') || []).reduce(function (t, x) { return t + (x && x.qty > 0 ? +x.qty : 0); }, 0); } catch (e) { return 0; } }
  function mk(cls) { var a = document.createElement('a'); a.href = 'cos.html'; a.className = cls; a.hidden = true; a.innerHTML = SVG + '<i class="s24-cartn"></i>';
    a.addEventListener('click', function (e) { if (window.s24openCart) { e.preventDefault(); window.s24openCart(); } }); return a; }
  var d, m;
  function upd() {
    var n = count(), on = n > 0 || document.documentElement.getAttribute('data-shop') === 'on' || /\/cos(\.html)?$/.test(location.pathname);
    var nav = document.querySelector('.s24-nav-in'); if (!nav) return;
    if (!d) { d = mk('s24-cartbtn'); var t = nav.querySelector('.s24-navtel') || nav.querySelector('.s24-nav-in > .s24-btn'); nav.insertBefore(d, t || null); }
    var mob = nav.querySelector('.s24-mob'); if (mob && !m) { m = mk('s24-cartbtn s24-cartbtn-m'); mob.insertBefore(m, mob.firstChild); }
    [d, m].forEach(function (a) { if (!a) return; a.hidden = !on; a.querySelector('.s24-cartn').textContent = n || ''; a.querySelector('.s24-cartn').hidden = !n; a.setAttribute('aria-label', n ? 'Coșul tău: ' + n + ' produse' : 'Coșul tău'); });
  }
  window.addEventListener('s24cart', function () { upd(); [d, m].forEach(function (a) { if (a && !a.hidden) { a.classList.remove('s24-bump'); a.offsetWidth; a.classList.add('s24-bump'); } }); });
  window.addEventListener('storage', function (e) { if (e.key === 's24cart') upd(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', upd); else upd();
  window.addEventListener('load', upd);
})();
