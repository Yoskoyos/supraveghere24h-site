# LANSARE: mută site-ul din folderul de previzualizare în rădăcină (pe supraveghere24h.ro).
# Rulare: python3 scripts/lanseaza.py   apoi commit + push.  NU se rulează automat.
import os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, 'previzualizare-25c472e2')
assert os.path.isdir(PRE), 'Folderul de previzualizare nu există (site-ul e deja lansat?)'

# pagina „în lucru” devine pagina 404
lucru = open(os.path.join(ROOT, 'index.html')).read()
p404 = (lucru.replace('Site-ul nou este <span>în lucru</span>', 'Pagina nu a fost <span>găsită</span>')
             .replace('Pregătim noul site SUPRAVEGHERE24h. Între timp suntem aici pentru oferte și întrebări despre sistemele de supraveghere video pentru asociații de proprietari.',
                      'Pagina căutată nu există sau a fost mutată. <a href="/" style="color:#F5A100;font-weight:700">Mergi la prima pagină</a> sau contactează-ne.'))
p404 = p404.replace('<meta name="robots"', '<meta name="robots-old"')
p404 = p404.replace('<head>', '<head>\n  <meta name="robots" content="noindex">', 1)

for name in os.listdir(PRE):
    src, dst = os.path.join(PRE, name), os.path.join(ROOT, name)
    if os.path.isdir(dst): shutil.rmtree(dst)
    elif os.path.exists(dst): os.remove(dst)
    shutil.move(src, dst)
os.rmdir(PRE)
for f in os.listdir(ROOT):
    if f.endswith('.html') and f != '404.html':
        p = os.path.join(ROOT, f); s = open(p).read()
        s = s.replace('  <meta name="robots" content="noindex, nofollow">\n', '')
        s = s.replace('href="index.html#', 'href="/#').replace('href="index.html"', 'href="/"')
        open(p, 'w').write(s)
open(os.path.join(ROOT, '404.html'), 'w').write(p404)
print('Gata. Verifică local, apoi: git add -A && git commit -m "Lansare site" && git push')
