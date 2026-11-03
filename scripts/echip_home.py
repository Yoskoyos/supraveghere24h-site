# Prima pagină: secțiunea „Echipamentele pe care le montăm” (din aplicație, js/s24featured.js) + link Echipamente în subsol pe toate paginile.
# Idempotent. Rulează după analytics.py.
import os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEC = '''  <section class="s24-base s24-sec s24-feat" style="background:#F5F7FA">
    <style>.s24f-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:28px}
.s24f-c{display:flex;flex-direction:column;background:#fff;border:1px solid #E1E6EC;border-radius:16px;padding:16px;text-decoration:none;color:#0D1F33;transition:transform .2s,box-shadow .2s}
.s24f-c:hover{transform:translateY(-3px);box-shadow:0 14px 30px -18px rgba(13,31,51,.35)}
.s24f-img{display:flex;align-items:center;justify-content:center;aspect-ratio:4/3;background:#fff;border-radius:10px;margin-bottom:12px;overflow:hidden}
.s24f-img img{width:100%;height:100%;object-fit:contain}
.s24f-tag{align-self:flex-start;font-size:12px;font-weight:700;color:#1B7AB3;background:#E8F3FA;border-radius:999px;padding:4px 10px;margin-bottom:8px}
.s24f-n{font-size:16px;line-height:1.35}.s24f-m{color:#52606F;font-size:13px;margin-top:4px}
.s24f-s{margin:10px 0 0;padding-left:18px;color:#3D4F63;font-size:14px;line-height:1.55}
@media(max-width:991px){.s24f-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:479px){.s24f-grid{gap:10px}.s24f-c{padding:10px;border-radius:12px}.s24f-s{display:none}.s24f-n{font-size:14px}.s24f-m{font-size:12px}.s24f-tag{font-size:11px;padding:3px 8px}}
@media(prefers-reduced-motion:reduce){.s24f-c{transition:none}.s24f-c:hover{transform:none}}</style>
    <div class="s24-wrap">
      <div class="s24-eyebrow">ECHIPAMENTE</div>
      <h2 class="s24-h2">Echipamentele pe care le montăm</h2>
      <p class="s24-sub">Camere IP Hikvision, Dahua și HiLook de minimum 4 MP, recordere și hard disk-uri dedicate supravegherii. Toate sunt incluse în abonament, cu garanție pe toată durata contractului.</p>
      <div class="s24f-grid" id="s24f-grid" hidden></div>
      <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap">
        <a href="echipamente.html" class="s24-btn s24-btn-a">Vezi toate echipamentele</a>
        <a href="camere-ip.html" class="s24-btn s24-btn-o" style="color:#0D1F33;border-color:#0D1F33">Camere IP</a>
      </div>
    </div>
  </section>
'''
p = os.path.join(ROOT, 'index.html'); t = open(p).read()
if 's24-feat' not in t:
    mark = '<section class="s24-base s24-band">'
    i = t.find(mark); assert i > 0
    t = t[:i] + SEC.lstrip() + '  ' + t[i:]
if 's24featured.js' not in t:
    t = t.replace('</body>', '<script src="js/s24featured.js?v=1" defer></script>\n</body>', 1)
open(p, 'w').write(t)
n = 0
FL = '<a href="echipamente.html" class="s24-flink">Echipamente</a><span class="s24-fsep">·</span>'
for f in glob.glob(os.path.join(ROOT, '*.html')):
    t = open(f).read()
    a = '<a href="despre-noi.html" class="s24-flink">Despre noi</a><span class="s24-fsep">·</span>'
    if FL in t or a not in t: continue
    t = t.replace(a, FL + '\n          ' + a, 1); open(f, 'w').write(t); n += 1
print('Echipamente: secțiune pe prima pagină; link în subsol pe', n, 'pagini')
