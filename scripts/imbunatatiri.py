# Rulat o singură dată (30-31.10.2026): SEO, Open Graph, butoane flotante, pagini pe sectoare, calculator pe prima pagină.
import re, os, json, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, 'previzualizare-25c472e2')
SITE = 'https://supraveghere24h.ro'
OGIMG = SITE + '/og-image.jpg'

BUSINESS = {
  "@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#firma",
  "name": "SUPRAVEGHERE24h", "legalName": "Yca Solutions SRL", "url": SITE + "/",
  "image": OGIMG, "logo": SITE + "/og-image.jpg",
  "telephone": "+40763354355", "email": "contact@supraveghere24h.ro",
  "address": {"@type": "PostalAddress", "streetAddress": "Str. Aviator Mircea Petre nr. 10", "addressLocality": "București",
              "addressRegion": "Sector 1", "addressCountry": "RO"},
  "areaServed": [{"@type": "City", "name": "București"}, {"@type": "AdministrativeArea", "name": "Județul Ilfov"}],
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
  "priceRange": "de la 189 lei / lună",
  "description": "Sisteme de supraveghere video pentru blocuri și asociații de proprietari, cu abonament lunar fix și instalare gratuită."
}

WA = 'https://wa.me/40763354355?text=' + 'Bun%C4%83%20ziua!%20A%C8%99%20dori%20o%20ofert%C4%83%20pentru%20supraveghere%20video%20la%20bloc.'
FLOAT = '''
<!-- s24-float: bară jos pe telefon -->
<style>
.s24f-bar{display:none}
@media(max-width:767px){
  .s24f-bar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:899;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom,0px));background:#0D1F33;box-shadow:0 -8px 24px rgba(13,31,51,.25)}
  .s24f-bar a{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;height:48px;border-radius:12px;font:700 15px/1 Montserrat,'Segoe UI',Arial,sans-serif;text-decoration:none}
  .s24f-bar .c{background:#fff;color:#0D1F33}.s24f-bar .k{background:#F5A100;color:#0D1F33}
  .s24f-bar svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
  body{padding-bottom:calc(70px + env(safe-area-inset-bottom,0px))}
  .s24-ck{bottom:calc(80px + env(safe-area-inset-bottom,0px))!important}
  .s24-up{display:none!important}
}
</style>
<div class="s24f-bar"><a class="c" href="tel:+40763354355"><svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>Sună acum</a><a class="k" href="calculator-pret.html"><svg viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h8"/></svg>Calculează prețul</a></div>
<!-- /s24-float -->
'''

def meta_block(title, desc, slug, ld=None):
    url = SITE + '/' + slug
    t, d = H.escape(title, quote=True), H.escape(desc, quote=True)
    out = f'''  <!-- s24-seo -->
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0D1F33">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="SUPRAVEGHERE24h">
  <meta property="og:locale" content="ro_RO">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OGIMG}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
'''
    if ld: out += '  <script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n'
    return out + '  <!-- /s24-seo -->\n'

def strip_old(s):
    s = re.sub(r'  <!-- s24-seo -->.*?<!-- /s24-seo -->\n', '', s, flags=re.S)
    s = re.sub(r'\n<!-- s24-float:.*?<!-- /s24-float -->\n', '', s, flags=re.S)
    return s

def get_title_desc(s):
    t = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
    m = re.search(r'<meta content="([^"]*)" name="description">', s)
    return H.unescape(t), H.unescape(m.group(1)) if m else ''

# ---------- 1. prima pagină: titlu, descriere, butoane ----------
p = os.path.join(PRE, 'index.html'); s = open(p).read()
s = s.replace('<title>Supraveghere24h.ro</title>',
  '<title>Supraveghere video pentru blocuri, fără investiție – SUPRAVEGHERE24h</title>\n  <meta content="Sisteme de supraveghere video pentru asociații de proprietari din București: camere IP Hikvision de minimum 5 MP, instalare gratuită, abonament lunar fix de la 189 lei. Calculează prețul online." name="description">')
s = s.replace('''          <a href="contact.html" class="s24-btn s24-btn-a">Cere ofertă gratuită</a>
          <a href="#oferta" class="s24-btn s24-btn-o">Vezi ce include</a>''',
'''          <a href="calculator-pret.html" class="s24-btn s24-btn-a">Calculează prețul blocului</a>
          <a href="contact.html" class="s24-btn s24-btn-o">Cere ofertă gratuită</a>''')
open(p, 'w').write(s)

# ---------- 2. pagini pe sectoare ----------
SECT = {
 1: ['Băneasa', 'Aviației', 'Dorobanți', 'Floreasca', 'Primăverii', 'Bucureștii Noi', 'Damaroaia', '1 Mai', 'Pajura', 'Victoriei'],
 2: ['Colentina', 'Tei', 'Pantelimon', 'Iancului', 'Obor', 'Ștefan cel Mare', 'Moșilor', 'Fundeni', 'Andronache', 'Dacia'],
 3: ['Titan', 'Dristor', 'Vitan', 'Balta Albă', 'Unirii', 'Lipscani', 'Dudești', 'Laminorului', 'Ozana', 'Muncii'],
 4: ['Berceni', 'Tineretului', 'Văcărești', 'Olteniței', 'Giurgiului', 'Apărătorii Patriei', 'Timpuri Noi', 'Brâncoveanu', 'Constantin Brâncoveanu', 'Eroii Revoluției'],
 5: ['Rahova', 'Ferentari', '13 Septembrie', 'Cotroceni', 'Sebastian', 'Panduri', 'Antiaeriană', 'Margeanului', 'Salaj', 'Izvor'],
 6: ['Drumul Taberei', 'Militari', 'Crângași', 'Giulești', 'Ghencea', 'Lujerului', 'Gorjului', 'Păcii', 'Grozăvești', 'Politehnica'],
}
SECT[4] = ['Berceni', 'Tineretului', 'Văcărești', 'Olteniței', 'Giurgiului', 'Apărătorii Patriei', 'Timpuri Noi', 'Constantin Brâncoveanu', 'Eroii Revoluției', 'Piața Sudului']
SECT[5] = ['Rahova', 'Ferentari', '13 Septembrie', 'Cotroceni', 'Sebastian', 'Panduri', 'Antiaeriană', 'Margeanului', 'Sălaj', 'Ghencea']
SECT[6] = ['Drumul Taberei', 'Militari', 'Crângași', 'Giulești', 'Lujerului', 'Gorjului', 'Păcii', 'Grozăvești', 'Politehnica', 'Uverturii']

tpl = open(os.path.join(PRE, 'oferta-asociatii.html')).read()
tpl = strip_old(tpl)
def sector_page(n):
    cart = SECT[n]; s = tpl
    title = f'Supraveghere video bloc Sector {n} București – SUPRAVEGHERE24h'
    desc = (f'Supraveghere video pentru blocuri și asociații de proprietari din Sectorul {n} ({", ".join(cart[:4])} și alte cartiere): '
            'camere IP Hikvision de minimum 5 MP, instalare gratuită, abonament de la 189 lei / lună.')
    s = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)}</title>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" name="description">', f'<meta content="{H.escape(desc, quote=True)}" name="description">', s, count=1)
    s = s.replace('<span class="s24-pill">OFERTĂ PENTRU ASOCIAȚII DE PROPRIETARI</span>', f'<span class="s24-pill">SECTORUL {n} · BUCUREȘTI</span>', 1)
    s = s.replace('<h1 class="s24-h1">Supraveghere video pentru blocul tău, <span class="s24-h1-a">fără costuri de investiție</span></h1>',
                  f'<h1 class="s24-h1">Supraveghere video pentru blocuri din Sectorul {n}, <span class="s24-h1-a">fără costuri de investiție</span></h1>', 1)
    s = s.replace('Instalăm, întreținem și garantăm un sistem complet de camere IP Hikvision de minimum 5 MP.',
                  f'Montăm sisteme de supraveghere video pentru asociațiile de proprietari din Sectorul {n}: {", ".join(cart[:3])}, {cart[3]} și nu numai. Instalăm, întreținem și garantăm un sistem complet de camere IP Hikvision de minimum 5 MP.', 1)
    chips = ''.join(f'<span style="display:inline-block;background:#fff;border:1px solid #E1E6EC;border-radius:999px;padding:8px 16px;margin:0 8px 10px 0;font-weight:600;color:#0D1F33">{H.escape(c)}</span>' for c in cart)
    others = ' · '.join(f'<a href="supraveghere-video-bloc-sector-{k}.html" style="color:#0D1F33;font-weight:700">Sectorul {k}</a>' for k in range(1, 7) if k != n)
    zone = f'''  <section class="s24-base s24-sec" style="background:#F5F7FA">
    <div class="s24-wrap">
      <div class="s24-eyebrow">ZONE DIN SECTORUL {n}</div>
      <h2 class="s24-h2">Montăm sisteme de supraveghere în tot Sectorul {n}</h2>
      <p class="s24-sub">Lucrăm cu asociații de proprietari din toate cartierele sectorului, inclusiv:</p>
      <div style="margin-top:22px">{chips}</div>
      <p class="s24-sub" style="margin-top:18px">Venim la bloc pentru evaluare, propunem amplasarea camerelor și vă trimitem oferta. Lucrăm și în {others}, precum și în <a href="supraveghere-video-bloc-ilfov.html" style="color:#0D1F33;font-weight:700">județul Ilfov</a>.</p>
    </div>
  </section>
'''
    s = s.replace('  <section id="pasi" class="s24-base s24-steps">', zone + '  <section id="pasi" class="s24-base s24-steps">', 1)
    s = s.replace('        <h3 class="s24-q-h">Cât durează contractul?</h3>',
                  f'''        <h3 class="s24-q-h">Veniți și în Sectorul {n}?</h3>
        <p class="s24-q-p">Da. Lucrăm cu asociații de proprietari din tot Sectorul {n} și din restul Bucureștiului. Evaluarea la bloc și oferta sunt gratuite.</p>
      </div>
      <div class="s24-q">
        <h3 class="s24-q-h">Cât durează contractul?</h3>''', 1)
    for k in ['SECTORUL', f'Sectorul {n}', 'Veniți și în']: assert k in s, (n, k)
    return s, title, desc

# ---------- 3. secțiunea „Zone deservite” pe prima pagină ----------
p = os.path.join(PRE, 'index.html'); s = open(p).read()
if 's24-zone' not in s:
    cards = ''.join(f'<a href="supraveghere-video-bloc-sector-{k}.html" style="display:block;background:#fff;border:1px solid #E1E6EC;border-radius:14px;padding:18px 20px;text-decoration:none;color:#0D1F33"><b style="font-size:18px">Sectorul {k}</b><br><span style="color:#52606F;font-size:14px">{H.escape(", ".join(SECT[k][:3]))}…</span></a>' for k in range(1, 7))
    zone = f'''  <section class="s24-base s24-sec s24-zone">
    <div class="s24-wrap">
      <div class="s24-eyebrow">ZONE DESERVITE</div>
      <h2 class="s24-h2">Montăm în toate sectoarele Bucureștiului</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:26px">{cards}</div>
    </div>
  </section>
'''
    s = s.replace('  <section id="faq" class="s24-base s24-faq">', zone + '  <section id="faq" class="s24-base s24-faq">', 1)
    open(p, 'w').write(s)

for n in range(1, 7):
    s, _, _ = sector_page(n)
    open(os.path.join(PRE, f'supraveghere-video-bloc-sector-{n}.html'), 'w').write(s)

# ---------- 4. SEO + butoane pe toate paginile ----------
pages = sorted(f for f in os.listdir(PRE) if f.endswith('.html'))
LD_PAGES = {'index.html', 'contact.html'} | {f for f in os.listdir(PRE) if f.startswith('supraveghere-video-bloc-')}
for f in pages:
    p = os.path.join(PRE, f); s = strip_old(open(p).read())
    title, desc = get_title_desc(s)
    slug = '' if f == 'index.html' else f[:-5]
    s = s.replace('</head>', meta_block(title, desc, slug, BUSINESS if f in LD_PAGES else None) + '</head>', 1)
    s = s.replace('</body>', FLOAT + '</body>', 1)
    open(p, 'w').write(s)

# pagina „în lucru” (rădăcina): OG + WhatsApp
for f in ['index.html']:
    p = os.path.join(ROOT, f); s = strip_old(open(p).read())
    s = s.replace('</head>', meta_block('SUPRAVEGHERE24h – supraveghere video pentru blocuri',
        'Sisteme de supraveghere video pentru asociații de proprietari: instalare gratuită, abonament lunar fix de la 189 lei.', '') + '</head>', 1)
    fl = FLOAT.replace('<a class="k" href="calculator-pret.html">', '<a class="k" href="' + WA + '">').replace('Calculează prețul</a></div>', 'WhatsApp</a></div>')
    s = s.replace('</body>', fl + '</body>', 1)
    open(p, 'w').write(s)

# ---------- 5. sitemap + robots (pentru lansare: se mută în rădăcină) ----------
urls = [SITE + '/' + ('' if f == 'index.html' else f[:-5]) for f in pages]
prio = lambda u: '1.0' if u.endswith('/') else '0.9' if ('calculator' in u or 'oferta' in u or 'contact' in u) else '0.7' if 'supraveghere-video-bloc' in u else '0.5'
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url><loc>{u}</loc><lastmod>2026-10-31</lastmod><priority>{prio(u)}</priority></url>\n' for u in urls) + '</urlset>\n'
open(os.path.join(PRE, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(PRE, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nDisallow: /email/\n\nSitemap: ' + SITE + '/sitemap.xml\n')
print('pagini:', len(pages)); print('\n'.join(urls))
