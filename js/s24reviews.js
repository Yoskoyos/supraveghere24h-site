/* s24reviews: recenziile reale de pe Google (prin serverul nostru, /public/reviews) în secțiunea .s24-reviews.
   Dacă nu există recenzii sau serverul nu răspunde, rămâne cardul static „Lasă o recenzie”. */
(function () {
  var API = 'https://proxy.supraveghere24h.ro/public/reviews';
  var WRITE = 'https://g.page/r/CQV6InDh9bMwEBM/review';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function stars(n, size) {
    var o = ''; for (var i = 1; i <= 5; i++) o += '<span style="color:' + (n >= i - .25 ? '#F5A100' : 'rgba(255,255,255,.22)') + '">★</span>';
    return '<span aria-label="' + n + ' din 5 stele" style="font-size:' + size + 'px;letter-spacing:2px;line-height:1">' + o + '</span>';
  }
  function initials(n) { return String(n || '?').trim().split(/\s+/).slice(0, 2).map(function (w) { return w.charAt(0); }).join('').toUpperCase(); }
  var css = '.s24rv-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px;margin:30px 0 0;text-align:left}' +
    '.s24rv-c{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:12px}' +
    '.s24rv-a{display:flex;align-items:center;gap:12px}.s24rv-a img,.s24rv-i{width:40px;height:40px;border-radius:50%;flex-shrink:0;object-fit:cover}' +
    '.s24rv-i{background:#1B7AB3;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}' +
    '.s24rv-n{color:#fff;font-weight:700;font-size:15px;text-decoration:none}.s24rv-w{color:#9FB0C3;font-size:13px;margin-top:2px}' +
    '.s24rv-t{color:#D5DEE8;font-size:15px;line-height:1.6;margin:0;display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden}' +
    '.s24rv-m{color:#F5A100;font-size:13px;font-weight:700;text-decoration:none;margin-top:auto}' +
    '.s24rv-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:28px}' +
    '.s24rv-g{display:inline-flex;align-items:center;gap:8px;color:#9FB0C3;font-size:13px;margin-top:18px}';
  var G = '<svg width="16" height="16" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>';
  function card(r) {
    var av = r.photo ? '<img src="' + esc(r.photo) + '" alt="" loading="lazy" referrerpolicy="no-referrer">' : '<span class="s24rv-i" aria-hidden="true">' + esc(initials(r.author)) + '</span>';
    var name = r.authorUrl ? '<a class="s24rv-n" href="' + esc(r.authorUrl) + '" target="_blank" rel="noopener">' + esc(r.author) + '</a>' : '<span class="s24rv-n">' + esc(r.author) + '</span>';
    return '<div class="s24rv-c"><div class="s24rv-a">' + av + '<div>' + name + '<div class="s24rv-w">' + esc(r.when) + '</div></div></div>' + stars(r.rating, 17) +
      (r.text ? '<p class="s24rv-t">' + esc(r.text) + '</p>' : '') + (r.url && r.text && r.text.length > 260 ? '<a class="s24rv-m" href="' + esc(r.url) + '" target="_blank" rel="noopener">Citește pe Google →</a>' : '') + '</div>';
  }
  function run() {
    var secs = document.querySelectorAll('.s24-reviews'); if (!secs.length || !window.fetch) return;
    fetch(API, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.configured || !(d.reviews || []).length) return;
      var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
      var rating = (+d.rating || 0).toFixed(1).replace('.', ',');
      Array.prototype.forEach.call(secs, function (sec) {
        var box = sec.querySelector('.s24-wrap > div'); if (!box) return;
        box.style.maxWidth = '1140px'; box.style.background = 'none'; box.style.border = '0'; box.style.padding = '0';
        box.innerHTML = '<div class="s24-eyebrow" style="color:#F5A100;text-align:center">PĂRERILE CLIENȚILOR</div>' +
          '<h2 class="s24-h2" style="color:#fff;text-align:center;margin:8px auto 0;max-width:none">Ce spun clienții noștri</h2>' +
          '<div style="display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:16px;color:#fff">' +
          '<b style="font-size:30px;line-height:1">' + rating + '</b>' + stars(+d.rating, 24) +
          '<span style="color:#C9D4E0;font-size:15px">' + d.count + (d.count === 1 ? ' recenzie' : ' recenzii') + ' pe Google</span></div>' +
          '<div class="s24rv-grid">' + d.reviews.map(card).join('') + '</div>' +
          '<div class="s24rv-btns"><a href="' + WRITE + '" target="_blank" rel="noopener" class="s24-btn s24-btn-a">Lasă o recenzie pe Google</a>' +
          (d.url ? '<a href="' + esc(d.url) + '" target="_blank" rel="noopener" class="s24-btn s24-btn-o">Vezi toate recenziile</a>' : '') + '</div>' +
          '<div style="text-align:center"><span class="s24rv-g">' + G + 'Recenzii preluate de pe Google</span></div>';
      });
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
