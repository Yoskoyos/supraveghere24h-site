"""Subsolul tuturor paginilor: sigla NETOPIA Payments (scriptul oficial) + pictograma ANPC SAL. Re-rulabil."""
import glob, re
ROW = ('<div class="s24-wrap s24-foot-pay" data-s24pay>'
       '<span class="s24-pay-t">Plăți securizate prin</span>'
       '<div class="s24-pay-np"><script src="https://mny.ro/npId.js?p=171524" type="text/javascript" data-version="orizontal" data-contrast-color="#091726"></script></div>'
       '<a href="https://reclamatiisal.anpc.ro/" target="_blank" rel="noopener" class="s24-pay-sal" title="ANPC – Soluționarea alternativă a litigiilor">'
       '<img src="images/anpc-sal.png" width="201" height="50" alt="ANPC – Soluționarea alternativă a litigiilor (SAL)" loading="lazy"></a></div>')
n = 0
for f in sorted(glob.glob('*.html')) + sorted(glob.glob('magazin/*.html')):
    s = open(f, encoding='utf-8').read()
    if '<footer class="s24-base s24-foot">' not in s: continue
    s0 = s
    s = re.sub(r'<div class="s24-wrap s24-foot-pay" data-s24pay>.*?</a></div>', '', s, flags=re.S)
    pre = '../' if f.startswith('magazin/') else ''
    s = s.replace('</footer>', ROW.replace('images/', pre + 'images/') + '\n  </footer>', 1)
    s = s.replace('https://anpc.ro/ce-este-sal/', 'https://reclamatiisal.anpc.ro/')
    if s != s0: open(f, 'w', encoding='utf-8').write(s); n += 1
print(n, 'pagini')
