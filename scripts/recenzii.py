# Recenzii Google: link în subsol (toate paginile) + secțiune pe „Despre noi”.
# Ordine: ilfov.py → despre.py → imbunatatiri.py → animatii.py → recenzii.py   (idempotent)
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, 'previzualizare-25c472e2')
if not os.path.isdir(PRE): PRE = ROOT   # după lansare, paginile sunt în rădăcină
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
    <div class="s24-wrap">
      <div style="max-width:760px;margin:0 auto;text-align:center;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:40px 28px">
        <div style="color:#F5A100;font-size:28px;letter-spacing:6px;line-height:1;margin-bottom:14px" aria-hidden="true">★★★★★</div>
        <div class="s24-eyebrow" style="color:#F5A100;text-align:center">PĂRERILE CLIENȚILOR</div>
        <h2 class="s24-h2" style="color:#fff;text-align:center;margin:8px auto 0;max-width:none">Ai lucrat cu noi? Spune-ne cum a fost</h2>
        <p class="s24-sub" style="color:#C9D4E0;margin:14px auto 0;max-width:560px;text-align:center">Profilul nostru de pe Google este nou. Dacă imobilul vostru are deja sistemul nostru, o recenzie scurtă ne ajută foarte mult și le arată altor asociații la ce să se aștepte.</p>
        <a href="{URL}" target="_blank" rel="noopener" class="s24-btn s24-btn-a" style="margin:26px auto 0;display:inline-flex;align-items:center;gap:10px">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path fill="#0D1F33" d="M21.35 11.1H12v2.9h5.35c-.25 1.4-1.6 4.1-5.35 4.1a5.9 5.9 0 010-11.8c1.8 0 3 .8 3.7 1.4l2.5-2.4A9.4 9.4 0 0012 2.6a9.4 9.4 0 100 18.8c5.4 0 9-3.8 9-9.2 0-.6 0-1-.15-1.1z"/></svg>
          Lasă o recenzie pe Google</a>
      </div>
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
