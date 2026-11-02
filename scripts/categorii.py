# Categoriile din bara laterală a paginilor de echipamente + paginile NVR-uri / Hard disk / Accesorii. Idempotent.
# Rulează apoi scripts/echipamente.py (pune blocul cu lista din aplicație pe paginile noi).
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = [('camere-ip-interior.html', 'Camere IP interior'), ('camere-ip-exterior.html', 'Camere IP exterior'),
        ('nvr-uri.html', 'NVR-uri'), ('stocare.html', 'Stocare'), ('accesorii.html', 'Accesorii')]
NEW = {  # pagină: (titlu, descriere)
  'nvr-uri.html': ('NVR-uri', 'Recorderele NVR pe care le montăm la blocuri: înregistrare locală, acces de pe telefon, incluse în abonament.'),
  'stocare.html': ('Stocare', 'Hard diskurile de supraveghere pe care se păstrează înregistrările din sistemele noastre, incluse în abonament.'),
  'accesorii.html': ('Accesorii', 'Rack-uri, switch-uri PoE, surse și alte accesorii pentru sistemele de supraveghere ale blocurilor.'),
}
SRC = os.path.join(ROOT, 'camere-ip-interior.html')
for f, (h, d) in NEW.items():
    p = os.path.join(ROOT, f)
    if os.path.exists(p): continue
    s = open(SRC).read()
    slug = f[:-5]
    s = s.replace('<title>Camere IP interior – SUPRAVEGHERE24h</title>', f'<title>{h} – SUPRAVEGHERE24h</title>')
    s = s.replace('Camere IP interior pentru scari, holuri si culoare. Cere oferta.', d)
    s = s.replace('content="Camere IP interior – SUPRAVEGHERE24h"', f'content="{h} – SUPRAVEGHERE24h"')
    s = s.replace('https://supraveghere24h.ro/camere-ip-interior"', f'https://supraveghere24h.ro/{slug}"')
    open(p, 'w').write(s)
side_re = re.compile(r'(<div class="s24-side-h">Categorii</div>)[\s\S]*?(\n\s*</aside>)')
pages = ['echipamente.html', 'camere-ip.html', 'kit-uri-camere.html'] + [c[0] for c in CATS]
for f in pages:
    p = os.path.join(ROOT, f); s = open(p).read()
    links = ''.join(f'\n        <a href="{u}"{" aria-current=\"page\"" if u == f else ""} class="s24-side-sub{" w--current" if u == f else ""}">{t}</a>' for u, t in CATS)
    s2 = side_re.sub(lambda m: m.group(1) + links + m.group(2), s, count=1)
    if s2 != s: open(p, 'w').write(s2)
sm = os.path.join(ROOT, 'sitemap.xml'); s = open(sm).read()
line = re.search(r'\s*<url><loc>https://supraveghere24h.ro/camere-ip-interior</loc>.*?</url>', s).group(0)
for f in NEW:
    u = 'https://supraveghere24h.ro/' + f[:-5]
    if u + '<' not in s: s = s.replace(line, line + line.replace('https://supraveghere24h.ro/camere-ip-interior', u), 1)
open(sm, 'w').write(s)
print('categorii actualizate pe', len(pages), 'pagini')
