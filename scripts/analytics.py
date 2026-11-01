# Cloudflare Web Analytics (fără cookie-uri) pe toate paginile .html din repo (rădăcină + previzualizare). Idempotent.
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIP = ('<!-- Cloudflare Web Analytics --><script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
        'data-cf-beacon=\'{"token": "6923ad681c1647f7bb30355648c9ea10"}\'></script><!-- End Cloudflare Web Analytics -->\n')
n = 0
for d, _, fs in os.walk(ROOT):
    if '/.git' in d or '/email' in d: continue
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f); t = open(p).read()
        if 'cloudflareinsights.com/beacon' in t or '</body>' not in t: continue
        i = t.rfind('</body>'); t = t[:i] + SNIP + t[i:]
        open(p, 'w').write(t); n += 1
print('Web Analytics adăugat pe', n, 'pagini')
