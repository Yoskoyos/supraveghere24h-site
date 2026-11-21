# Scoate secțiunea Ghiduri de pe site (cererea proprietarului, 21.11.2026): linkurile din meniu și subsol, din sitemap,
# iar paginile ghid* devin redirecționări spre prima pagină (noindex), ca adresele deja indexate să nu dea 404. Re-rulabil.
import glob, re
GHID = ['ghiduri.html', 'ghid-camere-supraveghere-bloc-legal.html', 'ghid-hotarare-aga-camere.html', 'ghid-cost-supraveghere-video-bloc.html']
RED = '''<!DOCTYPE html>
<html lang="ro"><head><meta charset="utf-8"><title>SUPRAVEGHERE24h</title>
<meta name="robots" content="noindex, follow"><link rel="canonical" href="https://supraveghere24h.ro/">
<meta http-equiv="refresh" content="0; url=/"><script>location.replace('/')</script></head>
<body><p><a href="/">Mergi la prima pagină</a></p></body></html>
'''
n = 0
for f in sorted(glob.glob('*.html')):
    if f in GHID: continue
    s = open(f).read(); o = s
    s = re.sub(r'\n[ \t]*<a href="ghiduri\.html"[^>]*class="s24-link"[^>]*>Ghiduri</a>', '', s)
    s = re.sub(r'\n[ \t]*<a href="ghiduri\.html"[^>]*class="s24-flink"[^>]*>Ghiduri</a><span class="s24-fsep">·</span>', '', s)
    s = re.sub(r'<a href="ghiduri\.html"[^>]*>Ghiduri</a>(<span class="s24-fsep">·</span>)?', '', s)
    if s != o: open(f, 'w').write(s); n += 1
for f in GHID:
    try: open(f, 'w').write(RED)
    except FileNotFoundError: pass
sm = open('sitemap.xml').read()
sm2 = re.sub(r'\n?\s*<url><loc>https://supraveghere24h\.ro/ghid[^<]*</loc>[^\n]*</url>', '', sm)
open('sitemap.xml', 'w').write(sm2)
h = open('scripts/header.py').read()
h = re.sub(r"\n\s*f'          <a href=\"ghiduri\.html\"\{cur\(f == \"ghiduri\.html\" or f\.startswith\(\"ghid-\"\)\)\}>Ghiduri</a>\\n'", '', h)
open('scripts/header.py', 'w').write(h)
print('pagini modificate:', n, '· sitemap ghiduri rămase:', sm2.count('/ghid'), '· header.py:', 'ghiduri' in h)
