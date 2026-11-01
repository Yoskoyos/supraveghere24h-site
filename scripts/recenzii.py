# Recenzii Google: link în subsol (toate paginile) + secțiune pe „Despre noi”.
# Ordine: ilfov.py → despre.py → imbunatatiri.py → animatii.py → recenzii.py   (idempotent)
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, 'previzualizare-25c472e2')
URL = 'https://g.page/r/CQV6InDh9bMwEBM/review'

FLINK = f'<a href="{URL}" target="_blank" rel="noopener" class="s24-flink">★ Lasă o recenzie pe Google</a><span class="s24-fsep">·</span>'
n = 0
for f in sorted(os.listdir(PRE)):
    if not f.endswith('.html'): continue
    p = os.path.join(PRE, f); t = open(p).read()
    if URL in t and 'class="s24-flink">★' in t: continue
    anchor = '<a href="despre-noi.html" class="s24-flink">Despre noi</a><span class="s24-fsep">·</span>'
    if anchor not in t: print('fără subsol:', f); continue
    t = t.replace(anchor, anchor + '\n          ' + FLINK, 1)
    open(p, 'w').write(t); n += 1

SEC = f'''  <section class="s24-base s24-sec s24-reviews" style="background:#0D1F33">
    <div class="s24-wrap" style="text-align:center">
      <div class="s24-eyebrow" style="color:#F5A100">PĂRERILE CLIENȚILOR</div>
      <h2 class="s24-h2" style="color:#fff">Ai lucrat cu noi? Spune-ne cum a fost</h2>
      <p class="s24-sub" style="color:#C9D4E0;margin:12px auto 0;max-width:620px">Profilul nostru de pe Google este nou. Dacă blocul tău are deja sistemul nostru, o recenzie scurtă ne ajută foarte mult și le arată altor asociații la ce să se aștepte.</p>
      <a href="{URL}" target="_blank" rel="noopener" class="s24-btn s24-btn-a" style="margin-top:24px;display:inline-flex;align-items:center;gap:10px">
        <span style="letter-spacing:2px">★★★★★</span> Lasă o recenzie pe Google</a>
    </div>
  </section>
'''
p = os.path.join(PRE, 'despre-noi.html'); t = open(p).read()
if 's24-reviews' not in t:
    mark = '  <section class="s24-base s24-sec">\n    <div class="s24-wrap">\n      <div class="s24-eyebrow">DATE DE IDENTIFICARE</div>'
    i = t.find(mark); assert i > 0, 'nu găsesc secțiunea Datele firmei'
    t = t[:i] + SEC + t[i:]
    open(p, 'w').write(t)
print('Recenzii: link în subsol pe', n, 'pagini; secțiune pe despre-noi.html')
