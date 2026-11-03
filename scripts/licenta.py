# Licența IGPR pe „Despre noi”: rând în tabelul cu datele firmei + secțiune cu copia licenței (cu filigran). Idempotent.
# Ordine: ... → despre.py → recenzii.py → licenta.py
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'despre-noi.html'); t = open(p).read()
TD = 'style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC"'
TV = 'style="padding:14px 18px;border-bottom:1px solid #E1E6EC;font-weight:700;color:#14202E"'
ROW = f'<tr><td {TD}>Licență Poliția Română</td><td {TV}>Nr. 6310/T din 14.06.2022, valabilă până la 13.06.2028</td></tr>\n          '
if 'Licență Poliția Română' not in t:
    i = t.index('<tr><td style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC">Telefon</td>')
    t = t[:i] + ROW + t[i:]
SEC = '''  <section class="s24-base s24-sec s24-licenta" id="licenta">
    <div class="s24-wrap">
      <div class="s24-eyebrow">AUTORIZARE</div>
      <h2 class="s24-h2">Licența de funcționare de la Poliția Română</h2>
      <p class="s24-sub" style="max-width:720px">Inspectoratul General al Poliției Române ne-a acordat licența nr. 6310/T din 14.06.2022, conform Legii nr. 333/2003. Licența ne permite „instalare, modificare sau întreținere a componentelor sau sistemelor de alarmare împotriva efracției” și este valabilă până la 13.06.2028.</p>
      <a href="images/licenta-igpr.jpg" target="_blank" rel="noopener" style="display:block;max-width:720px;margin-top:24px;border:1px solid #E1E6EC;border-radius:14px;overflow:hidden;background:#fff">
        <picture><source srcset="images/licenta-igpr-720.webp 720w, images/licenta-igpr.webp 1800w" sizes="(max-width: 767px) 100vw, 720px" type="image/webp"><img src="images/licenta-igpr-720.jpg" loading="lazy" width="720" height="499" alt="Licența de funcționare nr. 6310/T din 14.06.2022, emisă de Inspectoratul General al Poliției Române pentru Yca Solutions SRL" style="display:block;width:100%;height:auto"></picture>
      </a>
      <p style="margin:10px 0 0;font-size:14px;color:#52606F">Apasă pe imagine ca s-o vezi mare. Copie pentru informare, cu filigran.</p>
    </div>
  </section>
'''
if 's24-licenta' not in t:
    mark = '  <section class="s24-base s24-sec">\n    <div class="s24-wrap">\n      <div class="s24-eyebrow">DATE DE IDENTIFICARE</div>'
    i = t.index(mark); t = t[:i] + SEC + t[i:]
open(p, 'w').write(t)
print('licența pe despre-noi.html')
