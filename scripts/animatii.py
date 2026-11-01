# Animații discrete pentru site (re-rulabil). Ordinea completă: ilfov.py → despre.py → imbunatatiri.py → animatii.py
#  1. „Monitor live” pe prima pagină   2. calculator: preț care „rulează” + bloc cu camerele aprinse
#  3. pașii „Cum funcționează” se completează pe rând   4. întrebări frecvente care se deschid   5. efecte la atingere
# Fără biblioteci externe; totul se oprește dacă telefonul are „Reducere mișcare”.
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, 'previzualizare-25c472e2')

CSS = r'''
/* ── 5. efecte la atingere ── */
@media (hover:hover){
  .s24-card,.s24-ic-card,.s24-pasi-card,.s24-sg>div,.s24-zone a,.s24c-in,.s24c-out{transition:transform .25s ease,box-shadow .25s ease}
  .s24-card:hover,.s24-ic-card:hover,.s24-pasi-card:hover,.s24-zone a:hover{transform:translateY(-4px);box-shadow:0 16px 34px -18px rgba(13,31,51,.45)}
  .s24-btn{transition:transform .2s ease,box-shadow .2s ease,filter .2s ease}
  .s24-btn:hover{transform:translateY(-2px);box-shadow:0 12px 24px -12px rgba(13,31,51,.55)}
}
/* ── 3. pașii ── */
.s24a-step{position:relative}
.s24a-step::before{content:"";position:absolute;left:0;top:0;height:4px;width:0;background:#F5A100;border-radius:4px;transition:width .6s ease var(--d,0s)}
.s24a-go .s24a-step::before{width:100%}
.s24a-step .s24-dot,.s24a-step .s24-pasi-num{transition:transform .45s cubic-bezier(.34,1.56,.64,1) var(--d,0s),background .3s ease var(--d,0s),color .3s ease var(--d,0s)}
.s24a-go .s24a-step .s24-dot{transform:scale(1.12)}
.s24a-go .s24a-step .s24-pasi-num{transform:translateY(-2px)}
.s24a-tick{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#22c55e;color:#fff;font-size:13px;font-weight:800;margin-left:8px;vertical-align:middle;transform:scale(0);transition:transform .4s cubic-bezier(.34,1.56,.64,1) calc(var(--d,0s) + .45s)}
.s24a-go .s24a-tick{transform:scale(1)}
/* ── 4. întrebări frecvente ── */
.s24a-faq .s24-q-h{cursor:pointer;position:relative;padding-right:40px;user-select:none}
.s24a-faq .s24-q-h::after{content:"";position:absolute;right:6px;top:50%;width:10px;height:10px;margin-top:-8px;border-right:2.5px solid #0D1F33;border-bottom:2.5px solid #0D1F33;transform:rotate(45deg);transition:transform .25s ease,margin .25s ease}
.s24a-faq .s24-q.s24a-open .s24-q-h::after{transform:rotate(-135deg);margin-top:-3px}
.s24a-faq .s24-q-p{overflow:hidden;max-height:0;opacity:0;margin-top:0!important;transition:max-height .35s ease,opacity .3s ease,margin .3s ease}
.s24a-faq .s24-q.s24a-open .s24-q-p{opacity:1;margin-top:10px!important}
.s24a-faq .s24-q-h:focus-visible{outline:3px solid #F5A100;outline-offset:4px;border-radius:4px}
/* ── 1. monitor live ── */
.s24m{background:#07121F;border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:10px;margin-bottom:18px;box-shadow:0 24px 50px -24px rgba(0,0,0,.7)}
.s24m-top{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:2px 4px 10px;font:600 12px/1.2 Montserrat,'Segoe UI',Arial,sans-serif;color:#9FB3C8}
.s24m-live{display:inline-flex;align-items:center;gap:7px;color:#fff;font-weight:800;letter-spacing:.08em}
.s24m-live i{width:9px;height:9px;border-radius:50%;background:#ef4444;box-shadow:0 0 0 0 rgba(239,68,68,.6);animation:s24m-rec 1.6s infinite}
@keyframes s24m-rec{0%{box-shadow:0 0 0 0 rgba(239,68,68,.6)}70%{box-shadow:0 0 0 8px rgba(239,68,68,0)}100%{box-shadow:0 0 0 0 rgba(239,68,68,0)}}
.s24m-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.s24m-t{position:relative;aspect-ratio:16/10;border-radius:8px;overflow:hidden;background:#0F2236}
.s24m-t svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.s24m-t::after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 1px,transparent 1px 3px);pointer-events:none}
.s24m-scan{position:absolute;left:0;right:0;height:22%;top:-22%;background:linear-gradient(180deg,transparent,rgba(120,190,255,.10),transparent);animation:s24m-scan 4.5s linear infinite;pointer-events:none}
.s24m-t:nth-child(2) .s24m-scan{animation-delay:-1.2s}.s24m-t:nth-child(3) .s24m-scan{animation-delay:-2.4s}.s24m-t:nth-child(4) .s24m-scan{animation-delay:-3.4s}
@keyframes s24m-scan{to{top:100%}}
.s24m-l{position:absolute;left:6px;top:5px;font:700 9px/1 Montserrat,'Segoe UI',Arial,sans-serif;color:#E6EDF4;letter-spacing:.04em;text-shadow:0 1px 2px #000}
.s24m-r{position:absolute;right:6px;top:5px;display:flex;align-items:center;gap:4px;font:800 8.5px/1 Montserrat,'Segoe UI',Arial,sans-serif;color:#fff;text-shadow:0 1px 2px #000}
.s24m-r i{width:6px;height:6px;border-radius:50%;background:#ef4444;animation:s24m-blink 1.2s steps(2,start) infinite}
@keyframes s24m-blink{to{visibility:hidden}}
.s24m-ts{position:absolute;left:6px;bottom:5px;font:600 8.5px/1 'SFMono-Regular',Consolas,monospace;color:#cfe3f7;text-shadow:0 1px 2px #000}
.s24m-bot{display:flex;justify-content:space-between;gap:10px;padding:10px 4px 2px;font:600 11.5px/1.3 Montserrat,'Segoe UI',Arial,sans-serif;color:#9FB3C8}
.s24m-bot b{color:#22c55e}
.s24m-walk{animation:s24m-walk 9s linear infinite}
@keyframes s24m-walk{0%{transform:translateX(-40px)}100%{transform:translateX(190px)}}
.s24m-car{animation:s24m-car 12s ease-in-out infinite}
@keyframes s24m-car{0%,15%{transform:translateX(-90px)}45%,70%{transform:translateX(0)}100%{transform:translateX(200px)}}
.s24m-floor{animation:s24m-floor 8s steps(1) infinite}
.s24m-door{animation:s24m-door 8s ease-in-out infinite}
@keyframes s24m-door{0%,30%,70%,100%{transform:scaleX(1)}40%,60%{transform:scaleX(.15)}}
/* ── 2. calculator: blocul cu camere ── */
.s24b{margin-top:18px;border:1px solid #E1E6EC;border-radius:14px;background:linear-gradient(180deg,#F5F8FC,#fff);padding:12px 12px 8px}
.s24b svg{display:block;width:100%;height:auto}
.s24b-cap{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;font:700 12.5px/1.3 Montserrat,'Segoe UI',Arial,sans-serif;color:#14202E;padding-top:6px}
.s24b-cap span{display:inline-flex;align-items:center;gap:6px}.s24b-cap i{width:10px;height:10px;border-radius:50%}
.s24b-cam{opacity:.18;transition:opacity .35s ease}
.s24b-cam.on{opacity:1}
.s24b-cam .ping{transform-box:fill-box;transform-origin:center;opacity:0}
.s24b-cam.new .ping{animation:s24b-ping .9s ease-out}
@keyframes s24b-ping{0%{opacity:.9;transform:scale(.6)}100%{opacity:0;transform:scale(2.6)}}
.s24c-total.s24a-roll{transition:transform .25s ease}
@media (prefers-reduced-motion: reduce){
  .s24m *,.s24m-live i,.s24b *{animation:none!important}
  .s24a-step::before,.s24a-step .s24-dot,.s24a-tick,.s24a-faq .s24-q-p{transition:none!important}
  .s24-card,.s24-btn,.s24-ic-card,.s24-pasi-card{transition:none!important;transform:none!important}
}
'''

JS = r'''
(function(){
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function ready(f){ if(document.readyState!=='loading') f(); else document.addEventListener('DOMContentLoaded', f); }
  ready(function(){
    /* 3. pașii */
    var secs = document.querySelectorAll('.s24-pasi-row, .s24-sg');
    secs.forEach(function(row){
      var items = row.classList.contains('s24-pasi-row') ? row.querySelectorAll('.s24-pasi-card') : row.children;
      [].forEach.call(items, function(it, i){
        it.classList.add('s24a-step'); it.style.setProperty('--d', (i * 0.35) + 's');
        var t = it.querySelector('.s24-pasi-t, .s24-pasi-t-last, .s24-step-h');
        if (t && !t.querySelector('.s24a-tick')) { var k = document.createElement('span'); k.className = 's24a-tick'; k.textContent = '✓'; k.setAttribute('aria-hidden','true'); t.appendChild(k); }
      });
      if (RM || !('IntersectionObserver' in window)) { row.classList.add('s24a-go'); return; }
      var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { row.classList.add('s24a-go'); io.disconnect(); } }); }, { threshold: .35 });
      io.observe(row);
    });
    /* 4. întrebări frecvente */
    document.querySelectorAll('.s24-faq').forEach(function(f){
      if (f.classList.contains('s24a-faq') || !f.querySelector('.s24-q')) return;
      f.classList.add('s24a-faq');
      f.querySelectorAll('.s24-q').forEach(function(q, i){
        var h = q.querySelector('.s24-q-h'), p = q.querySelector('.s24-q-p'); if (!h || !p) return;
        h.setAttribute('role','button'); h.setAttribute('tabindex','0'); h.setAttribute('aria-expanded','false');
        function toggle(){ var o = !q.classList.contains('s24a-open'); q.classList.toggle('s24a-open', o); h.setAttribute('aria-expanded', o ? 'true' : 'false'); p.style.maxHeight = o ? (p.scrollHeight + 20) + 'px' : '0px'; }
        h.addEventListener('click', toggle);
        h.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
      });
    });
    /* 1. monitor live: ceasul de pe fiecare cameră */
    var ts = document.querySelectorAll('.s24m-ts, .s24m-clock');
    if (ts.length) {
      var fmt = function(){ var d = new Date(); try { return d.toLocaleString('ro-RO', { timeZone:'Europe/Bucharest', day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit', second:'2-digit' }).replace(',', ''); } catch(e){ return d.toLocaleString(); } };
      var tick = function(){ var t = fmt(); ts.forEach(function(el){ el.textContent = el.classList.contains('s24m-clock') ? t.slice(-8) : t; }); };
      tick(); setInterval(tick, 1000);
      var fl = document.querySelector('.s24m-floor'), n = 0;
      if (fl && !RM) setInterval(function(){ n = (n + 1) % 9; fl.textContent = n === 0 ? 'P' : n; }, 1800);
    }
    /* 2. calculator: preț care rulează + blocul cu camere */
    var tot = document.getElementById('s24c-total');
    if (tot) {
      var num = function(t){ return parseInt(String(t || '').replace(/\D/g, ''), 10) || 0; };
      var last = num(tot.textContent), mine = null, raf = 0;
      new MutationObserver(function(){
        var txt = tot.textContent;
        if (txt === mine) return;                       // schimbarea făcută de animația noastră
        var target = num(txt);
        if (RM || target === last) { last = target; return; }
        var from = last, t0 = performance.now(), dur = 550; last = target;
        cancelAnimationFrame(raf);
        var step = function(now){ var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
          mine = Math.round(from + (target - from) * e).toLocaleString('ro-RO') + ' lei / lună'; tot.textContent = mine;
          if (k < 1) raf = requestAnimationFrame(step); };
        raf = requestAnimationFrame(step);
      }).observe(tot, { childList: true, characterData: true, subtree: true });
    }
    var bld = document.querySelector('.s24b');
    if (bld) {
      var v = function(id){ var el = document.getElementById(id); return el ? Math.max(0, parseInt(el.value, 10) || 0) : 0; };
      var prev = {};
      var render = function(){
        var want = { i: v('s24c-int'), e: v('s24c-ext'), l: v('s24c-lift') };
        ['i','e','l'].forEach(function(k){
          var cams = bld.querySelectorAll('.s24b-cam[data-k="' + k + '"]');
          cams.forEach(function(c, idx){ var on = idx < want[k]; if (on && !c.classList.contains('on') && !RM) { c.classList.add('new'); setTimeout(function(){ c.classList.remove('new'); }, 950); } c.classList.toggle('on', on); });
        });
        var cap = bld.querySelector('.s24b-cap');
        if (cap) cap.innerHTML = '<span><i style="background:#F5A100"></i>' + want.i + ' interior</span><span><i style="background:#0B5FB0"></i>' + want.e + ' exterior</span><span><i style="background:#22c55e"></i>' + want.l + ' lift</span>';
        prev = want;
      };
      var sec = document.querySelector('.s24c-sec') || document;
      ['click','input','change','keyup'].forEach(function(ev){ sec.addEventListener(ev, function(){ requestAnimationFrame(render); }); });
      render();
    }
  });
})();
'''

TILE = lambda label, scene: f'<div class="s24m-t">{scene}<div class="s24m-scan"></div><span class="s24m-l">{label}</span><span class="s24m-r"><i></i>REC</span><span class="s24m-ts"></span></div>'
SC_SCARA = '''<svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice"><rect width="160" height="100" fill="#13283F"/><rect x="0" y="0" width="160" height="38" fill="#183150"/>
<g fill="#1F3D60" stroke="#2F5A86" stroke-width=".8"><path d="M20 100 L20 88 L40 88 L40 76 L60 76 L60 64 L80 64 L80 52 L100 52 L100 40 L120 40 L120 100 Z"/></g>
<path d="M18 80 L118 30" stroke="#6E93B8" stroke-width="2"/><g stroke="#4F77A0" stroke-width="1"><path d="M30 75 V86 M50 65 V76 M70 55 V66 M90 45 V56 M110 35 V46"/></g>
<rect x="128" y="22" width="24" height="46" rx="2" fill="#0E2034" stroke="#3B6590"/><circle cx="147" cy="46" r="1.6" fill="#9FC3E6"/><rect x="132" y="8" width="16" height="6" rx="1" fill="#2E7D4F" opacity=".9"/></svg>'''
SC_PARCARE = '''<svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice"><rect width="160" height="100" fill="#14293F"/><rect width="160" height="34" fill="#0F2134"/>
<g stroke="#3D6489" stroke-width="1.2"><path d="M10 100 L40 40 M50 100 L62 40 M90 100 L84 40 M130 100 L106 40 M160 90 L128 40"/></g><path d="M0 40 H160" stroke="#2A4A6C"/>
<rect x="66" y="52" width="26" height="15" rx="4" fill="#2A4F78"/><rect x="69" y="47" width="18" height="8" rx="3" fill="#3A6896"/>
<rect x="104" y="58" width="30" height="17" rx="4" fill="#24476C"/><rect x="108" y="52" width="21" height="9" rx="3" fill="#335E8A"/>
<g class="s24m-car"><rect x="10" y="70" width="34" height="18" rx="5" fill="#C9D8E8"/><rect x="15" y="64" width="23" height="10" rx="3" fill="#E3ECF5"/><circle cx="18" cy="88" r="3.5" fill="#0B1726"/><circle cx="37" cy="88" r="3.5" fill="#0B1726"/><rect x="40" y="75" width="4" height="3" fill="#FFE08A"/></g>
<path d="M148 10 V44" stroke="#557EA6" stroke-width="2"/><circle cx="148" cy="10" r="4" fill="#FFE9A8" opacity=".85"/></svg>'''
SC_LIFT = '''<svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice"><rect width="160" height="100" fill="#152B42"/><rect x="0" y="80" width="160" height="20" fill="#11253A"/>
<rect x="44" y="18" width="72" height="72" rx="2" fill="#1C3A5A" stroke="#4A73A0"/><g class="s24m-door" style="transform-origin:62px 54px"><rect x="47" y="21" width="32" height="69" fill="#2A5179"/></g><g class="s24m-door" style="transform-origin:98px 54px"><rect x="81" y="21" width="32" height="69" fill="#2A5179"/></g>
<rect x="64" y="6" width="32" height="10" rx="2" fill="#081523" stroke="#3B6590"/><text class="s24m-floor" x="80" y="14" fill="#FF6B6B" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">P</text>
<rect x="124" y="44" width="10" height="20" rx="2" fill="#0E2034" stroke="#3B6590"/><circle cx="129" cy="50" r="1.8" fill="#9FC3E6"/><circle cx="129" cy="57" r="1.8" fill="#9FC3E6"/></svg>'''
SC_INTRARE = '''<svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice"><rect width="160" height="100" fill="#14293F"/><rect y="78" width="160" height="22" fill="#1A324D"/>
<rect x="56" y="20" width="48" height="58" fill="#0D1E31" stroke="#4A73A0"/><path d="M80 20 V78" stroke="#4A73A0"/><rect x="50" y="12" width="60" height="8" fill="#22436A"/>
<rect x="110" y="40" width="9" height="14" rx="1.5" fill="#2B527A"/><g fill="#7FA6CC"><circle cx="114.5" cy="44" r="1"/><circle cx="114.5" cy="48" r="1"/></g>
<rect x="10" y="30" width="30" height="22" fill="#1C3A5A" stroke="#2F5A86"/><rect x="124" y="30" width="28" height="22" fill="#1C3A5A" stroke="#2F5A86"/>
<g class="s24m-walk"><g fill="#B9CCE0"><circle cx="20" cy="56" r="4"/><path d="M15 61 h10 l2 12 h-3 l-1 9 h-3 l-1 -9 h-1 l-1 9 h-3 l-1 -9 h-3 z"/></g><rect x="9" y="49" width="22" height="35" fill="none" stroke="#22c55e" stroke-width="1.4"/><rect x="9" y="44" width="22" height="5" fill="#22c55e"/><text x="20" y="47.8" fill="#04210F" font-size="4" font-family="Arial" font-weight="700" text-anchor="middle">PERSOANĂ</text></g></svg>'''

MONITOR = ('<!-- s24-mon --><div class="s24m" aria-hidden="true"><div class="s24m-top"><span class="s24m-live"><i></i>LIVE</span><span>Monitorizare bloc · 4 camere</span><span class="s24m-clock"></span></div>'
           '<div class="s24m-grid">' + TILE('CAM 1 · SCARĂ', SC_SCARA) + TILE('CAM 2 · PARCARE', SC_PARCARE) + TILE('CAM 3 · LIFT', SC_LIFT) + TILE('CAM 4 · INTRARE', SC_INTRARE) + '</div>'
           '<div class="s24m-bot"><span><b>●</b> Toate camerele online</span><span>Înregistrare 24/7 · 21 de zile</span></div></div><!-- /s24-mon -->')

def cam(x, y, k, col):
    return (f'<g class="s24b-cam" data-k="{k}"><circle class="ping" cx="{x}" cy="{y}" r="6" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="6.5" fill="{col}" stroke="#fff" stroke-width="1.5"/><path d="M{x-3} {y-1.6} h4.2 l2 -1.3 v5.8 l-2 -1.3 h-4.2 z" fill="#fff"/></g>')
def building():
    g = []
    g.append('<rect x="70" y="20" width="160" height="150" rx="3" fill="#E8EEF5" stroke="#9FB0C3" stroke-width="1.5"/>')
    g.append('<rect x="62" y="12" width="176" height="10" rx="2" fill="#C7D3E0"/>')
    for fy in range(0, 5):
        y = 32 + fy * 27
        for wx in (80, 104, 176, 200):
            g.append(f'<rect x="{wx}" y="{y}" width="16" height="13" rx="1.5" fill="#BFD0E3"/>')
    g.append('<rect x="128" y="24" width="22" height="146" fill="#D3DEEA" stroke="#9FB0C3"/>')     # casa scării
    g.append('<rect x="154" y="24" width="14" height="146" fill="#C9D6E4" stroke="#9FB0C3"/>')     # puțul liftului
    g.append('<rect x="132" y="146" width="14" height="24" rx="1" fill="#6F8399"/>')                # ușa de intrare
    g.append('<rect x="0" y="170" width="300" height="10" fill="#B9C6D4"/><rect x="0" y="180" width="300" height="30" fill="#D8E1EA"/>')
    g.append('<g stroke="#fff" stroke-width="2"><path d="M14 196 h22 M50 196 h22"/></g>')          # parcare
    g.append('<rect x="250" y="186" width="34" height="18" rx="9" fill="none" stroke="#9FB0C3" stroke-width="2"/>')  # loc de joacă
    g.append('<text x="150" y="207" font-family="Montserrat,Arial" font-size="9" fill="#5B6B7C" text-anchor="middle">bloc</text>')
    ints = [(139, 38), (139, 65), (139, 92), (139, 119), (139, 146), (122, 38), (122, 92), (122, 146)]
    exts = [(30, 186), (60, 186), (139, 186), (240, 160), (268, 186), (52, 160)]
    lifts = [(161, 40), (161, 80), (161, 120), (161, 158)]
    g += [cam(x, y, 'i', '#F5A100') for x, y in ints] + [cam(x, y, 'e', '#0B5FB0') for x, y in exts] + [cam(x, y, 'l', '#22c55e') for x, y in lifts]
    return ('<!-- s24-bld --><div class="s24b" aria-hidden="true"><svg viewBox="0 0 300 212">' + ''.join(g) +
            '</svg><div class="s24b-cap"></div></div><!-- /s24-bld -->')

BLOCK = '<!-- s24-anim --><style>' + CSS + '</style><script>' + JS + '</script><!-- /s24-anim -->\n'

def strip(s):
    for a, b in [('<!-- s24-anim -->', '<!-- /s24-anim -->\n'), ('<!-- s24-mon -->', '<!-- /s24-mon -->'), ('<!-- s24-bld -->', '<!-- /s24-bld -->')]:
        while a in s:
            i = s.find(a); j = s.find(b, i); assert j > i, a
            s = s[:i] + s[j + len(b):]
    return s

n = 0
for f in sorted(os.listdir(PRE)):
    if not f.endswith('.html'): continue
    p = os.path.join(PRE, f); s = strip(open(p).read())
    if f == 'index.html':
        k = s.find('<div class="s24-ic-col">'); assert k > 0
        k += len('<div class="s24-ic-col">'); s = s[:k] + MONITOR + s[k:]
    if f == 'calculator-pret.html':
        k = s.find('<p class="s24c-min">'); assert k > 0
        k = s.find('</p>', k) + 4; s = s[:k] + building() + s[k:]
    s = s.replace('</body>', BLOCK + '</body>', 1)
    open(p, 'w').write(s); n += 1
print('animații pe', n, 'pagini')
