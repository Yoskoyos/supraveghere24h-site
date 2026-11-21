# Antet mai mic (cererea proprietarului, 21.11.2026): mai puțin spațiu sus/jos, logo, telefon și „Cere ofertă” mai compacte.
# Re-rulabil: adaugă/înlocuiește blocul marcat la sfârșitul css/supraveghere24h-ro.webflow.css și versiunea CSS din pagini (?v=).
import os, re, glob, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = '''/* s24-hdr-compact */
@media screen and (min-width: 992px) {
  .s24-nav-in { padding-top: 8px !important; padding-bottom: 8px !important; }
  .s24-header.s24-scrolled .s24-nav-in { padding-top: 5px !important; padding-bottom: 5px !important; }
  .s24-nav-in > .s24-logo-img { width: 196px !important; }
  .s24-nav-in > .s24-links .s24-link { padding-top: 7px !important; padding-bottom: 7px !important; }
  .s24-nav-in > .s24-btn { padding: 11px 22px !important; font-size: 15px !important; }
  .s24-navtel svg { width: 18px; height: 18px; padding: 8px; }
  .s24-navtel b { font-size: 15px; }
  .s24-navtel small { font-size: 11px; }
}
@media screen and (max-width: 991px) {
  .s24-nav-in { padding-top: 8px !important; padding-bottom: 8px !important; }
  .s24-nav-in > .s24-logo-img { width: 150px !important; }
}
/* /s24-hdr-compact */
'''
p = os.path.join(ROOT, 'css', 'supraveghere24h-ro.webflow.css'); s = open(p).read()
s = re.sub(r'/\* s24-hdr-compact \*/.*?/\* /s24-hdr-compact \*/\n?', '', s, flags=re.S)
open(p, 'w').write(s.rstrip('\n') + '\n' + CSS)
v = time.strftime('%Y%m%d%H%M'); n = 0
for f in glob.glob(os.path.join(ROOT, '*.html')):
    h = open(f).read(); o = h
    h = re.sub(r'(css/supraveghere24h-ro\.webflow\.css)(\?v=[\w.-]+)?"', r'\1?v=' + v + '"', h)
    if h != o: open(f, 'w').write(h); n += 1
print('antet compact; versiune CSS în', n, 'pagini')
