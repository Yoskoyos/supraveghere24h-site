# Pagina „Supraveghere video pentru firme și case” (pentru campania Google Ads 2) + link în subsol + sitemap.
# Se construiește din despre-noi.html (antet, subsol, cookie-uri, analytics identice). Re-rulabil.
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = 'supraveghere-video-firme.html'
tpl = open(os.path.join(ROOT, 'despre-noi.html')).read()

title = 'Camere supraveghere pentru firme și case, București și Ilfov – SUPRAVEGHERE24h'
desc = ('Proiectăm și montăm sisteme de supraveghere video pentru firme, depozite, magazine, birouri și case din București și Ilfov. '
        'Firmă acreditată IGPR, echipamente Hikvision și Dahua, ofertă personalizată.')
s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', tpl, count=1)
s = re.sub(r'<meta content="[^"]*" name="description">', f'<meta content="{desc}" name="description">', s, count=1)
s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', s, count=1)
s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', s, count=1)
s = s.replace('https://supraveghere24h.ro/despre-noi"', 'https://supraveghere24h.ro/supraveghere-video-firme"')
s = s.replace('<a href="despre-noi.html" aria-current="page" class="s24-link w--current">Despre noi</a>', '<a href="despre-noi.html" class="s24-link">Despre noi</a>')

hero_start = s.find('  <section class="s24-base s24-dark s24-ohero">')
contact_start = s.find('  <section id="contact" class="s24-base s24-contact">')
assert 0 < hero_start < contact_start

def card(n, h, p, dark=False):
    d = ' s24-card-d' if dark else ''
    return (f'        <div class="s24-card{d}">\n          <div class="s24-card-n{" s24-card-n-d" if dark else ""}">{n}</div>\n'
            f'          <h3 class="s24-card-h{" s24-card-h-d" if dark else ""}">{h}</h3>\n          <p class="s24-card-p{" s24-card-p-d" if dark else ""}">{p}</p>\n        </div>\n')

body = f'''  <section class="s24-base s24-dark s24-ohero">
    <div class="s24-wrap s24-ohero-in">
      <div class="s24-ohero-txt"><span class="s24-pill">FIRME ȘI CASE</span>
        <h1 class="s24-h1">Camere de supraveghere pentru <span class="s24-h1-a">firme și case</span></h1>
        <p class="s24-lead">Proiectăm, montăm și configurăm sisteme de supraveghere video pentru firme, depozite, magazine, birouri și case din București și Ilfov. Vezi camerele live și înregistrările de pe telefon, de oriunde.</p>
        <div class="s24-cta">
          <a href="#contact" class="s24-btn s24-btn-a">Cere o ofertă</a>
          <a href="tel:+40763354355" class="s24-btn s24-btn-o">Sună: 0763 354 355</a>
        </div>
      </div>
      <div class="s24-ohero-card">
        <p class="s24-ohero-k">Pe scurt</p>
        <div class="s24-ohero-row"><span>Pentru</span><span class="s24-ohero-val">Firme, depozite, magazine, birouri, case</span></div>
        <div class="s24-ohero-row"><span>Zonă</span><span class="s24-ohero-val">București și Ilfov</span></div>
        <div class="s24-ohero-row"><span>Echipamente</span><span class="s24-ohero-val">Hikvision, Dahua, HiLook · minim 4 MP</span></div>
        <div class="s24-ohero-row"><span>Acreditare</span><span class="s24-ohero-val">Poliția Română (IGPR)</span></div>
        <div class="s24-ohero-row"><span>Preț</span><span class="s24-ohero-val">Ofertă personalizată, după numărul de camere</span></div>
      </div>
    </div>
  </section>
  <section class="s24-base s24-sec">
    <div class="s24-wrap">
      <div class="s24-eyebrow">CE SUPRAVEGHEM</div>
      <h2 class="s24-h2">Un sistem gândit pentru locul tău</h2>
      <p class="s24-sub">Fiecare locație e diferită, așa că nu vindem pachete fixe. Alegem numărul de camere, tipul lor și locul de montaj după ce vrei să vezi: intrările, casa de marcat, rafturile, curtea sau parcarea.</p>
      <div class="s24-grid">
{card('01', 'Firme și birouri', 'Intrări, recepție, holuri și spații de lucru. Acces la imagini doar pentru persoanele desemnate de firmă.')}{card('02', 'Depozite și hale', 'Rampe de încărcare, rafturi, curte și perimetru, cu camere cu infraroșu pentru noapte.')}{card('03', 'Magazine', 'Casa de marcat, raioanele și intrarea, ca să vezi ce se întâmplă și când nu ești acolo.')}{card('04', 'Case și vile', 'Poarta, curtea, garajul și accesele în casă. Primești notificări pe telefon când camera detectează mișcare.')}{card('05', 'Vezi totul pe telefon', 'Configurăm aplicația pe telefonul tău: imagini live și înregistrări, de oriunde ai fi.')}{card('06', 'Garanție și service', 'Montajul îl facem noi, iar dacă apare o problemă tot noi intervenim.', True)}      </div>
    </div>
  </section>
  <section class="s24-base s24-sec" style="background:#F5F7FA">
    <div class="s24-wrap">
      <div class="s24-eyebrow">CUM LUCRĂM</div>
      <h2 class="s24-h2">De la cerere la sistemul funcțional</h2>
      <div class="s24-grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
{card('1', 'Ne spui ce ai nevoie', 'Completezi formularul sau ne suni: ce fel de locație e și ce vrei să supraveghezi.')}{card('2', 'Stabilim soluția', 'Venim la fața locului sau lucrăm pe baza pozelor și a planului, apoi alegem camerele potrivite.')}{card('3', 'Primești oferta', 'Oferta are fiecare echipament și prețul lui, plus montajul. Fără costuri ascunse.')}{card('4', 'Montăm și configurăm', 'Instalăm camerele și înregistratorul (NVR), configurăm aplicația și îți arătăm cum o folosești.')}      </div>
    </div>
  </section>
'''
s = s[:hero_start] + body + s[contact_start:]

# formularul de contact: texte pentru firme și case (rămâne același formular → serverul vede pagina de proveniență)
s = s.replace('<h2 class="s24-contact-h">Siguranța locatarilor începe cu un apel</h2>', '<h2 class="s24-contact-h">Spune-ne ce vrei să supraveghezi</h2>', 1)
s = s.replace('<p class="s24-contact-p">Lasă-ne datele în formular și revenim cu o ofertă adaptată asociației.</p>', '<p class="s24-contact-p">Lasă-ne datele și câteva detalii despre locație, iar noi revenim cu o ofertă personalizată.</p>', 1)
s = s.replace('<label for="" class="s24-lab">Asociația sau adresa blocului</label>', '<label for="" class="s24-lab">Firma sau adresa locației</label>', 1)
s = s.replace('<label for="" class="s24-lab">Mesaj</label><textarea class="s24-inp w-input" maxlength="5000" name="mesaj" data-name="mesaj" rows="3" id="s24-msg">',
              '<label for="" class="s24-lab">Ce vrei să supraveghezi?</label><textarea class="s24-inp w-input" maxlength="5000" name="mesaj" data-name="mesaj" rows="3" id="s24-msg" placeholder="ex. depozit cu 2 intrări și curte, aprox. 8 camere">', 1)
s = s.replace('value="Trimite mesajul">', 'value="Cere oferta">', 1)
s = s.replace('<a class="k" href="calculator-pret.html"><svg viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h8"/></svg>Calculează prețul<',
              '<a class="k" href="#contact"><svg viewBox="0 0 24 24"><path d="M4 4h16v12H5.2L4 17.2z"/><path d="M8 9h8M8 12h5"/></svg>Cere ofertă<', 1)   # bara de jos pe telefon
assert 'FIRME ȘI CASE' in s and 'Ce vrei să supraveghezi?' in s and 'Cere oferta">' in s
open(os.path.join(ROOT, OUT), 'w').write(s)

# link în subsol pe toate paginile (după „Echipamente”)
LINK = '<a href="supraveghere-video-firme.html" class="s24-flink">Firme și case</a><span class="s24-fsep">·</span>'
n = 0
for f in sorted(os.listdir(ROOT)):
    if not f.endswith('.html') or f == '404.html': continue
    p = os.path.join(ROOT, f); t = open(p).read()
    if 'href="supraveghere-video-firme.html" class="s24-flink"' in t: continue
    a = '<a href="echipamente.html" class="s24-flink">Echipamente</a><span class="s24-fsep">·</span>'
    if a not in t: print('fără link Echipamente în subsol:', f); continue
    t = t.replace(a, a + '\n          ' + LINK, 1); open(p, 'w').write(t); n += 1

# sitemap
sm = os.path.join(ROOT, 'sitemap.xml'); x = open(sm).read()
if '/supraveghere-video-firme<' not in x:
    x = x.replace('</urlset>', '  <url><loc>https://supraveghere24h.ro/supraveghere-video-firme</loc><lastmod>2026-11-18</lastmod></url>\n</urlset>')
    open(sm, 'w').write(x)
print(OUT, 'creat; link în subsol pe', n, 'pagini')
