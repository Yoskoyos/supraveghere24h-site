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
