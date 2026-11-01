# Pagini pentru județul Ilfov (o pagină generală + orașe și comune mari). Se rulează ÎNAINTE de imbunatatiri.py
# (acela adaugă SEO, butoanele și sitemap-ul pentru toate paginile, inclusiv acestea).
import os, re, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, 'previzualizare-25c472e2')
if not os.path.isdir(PRE): PRE = ROOT   # după lansare, paginile sunt în rădăcină

ORASE = ['Voluntari', 'Pantelimon', 'Popești-Leordeni', 'Bragadiru', 'Buftea', 'Chitila', 'Otopeni', 'Măgurele']
COMUNE_PAG = ['Chiajna', 'Dobroești', 'Berceni', 'Domnești', 'Jilava', 'Tunari', 'Mogoșoaia', 'Ștefăneștii de Jos']
COMUNE_TOATE = ['1 Decembrie', 'Afumați', 'Balotești', 'Berceni', 'Brănești', 'Cernica', 'Chiajna', 'Ciolpani', 'Ciorogârla', 'Clinceni',
                'Copăceni', 'Corbeanca', 'Cornetu', 'Dascălu', 'Dărăști-Ilfov', 'Dobroești', 'Domnești', 'Dragomirești-Vale', 'Găneasa',
                'Glina', 'Grădiștea', 'Gruiu', 'Jilava', 'Moara Vlăsiei', 'Mogoșoaia', 'Nuci', 'Periș', 'Petrăchioaia', 'Snagov',
                'Ștefăneștii de Jos', 'Tunari', 'Vidra']
EXTRA = {  # detalii locale sigure
  'Voluntari': 'inclusiv zona Pipera',
  'Chiajna': 'inclusiv ansamblurile din zona Militari Residence',
  'Ștefăneștii de Jos': 'inclusiv ansamblul Cosmopolis',
}
TR = str.maketrans({'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ş': 's', 'ț': 't', 'ţ': 't', 'Ă': 'a', 'Â': 'a', 'Î': 'i', 'Ș': 's', 'Ț': 't'})
def slug(name): return re.sub(r'[^a-z0-9]+', '-', name.lower().translate(TR)).strip('-')
def link(name):
    return f'supraveghere-video-bloc-{slug(name)}.html' if (name in ORASE or name in COMUNE_PAG) else None

tpl = open(os.path.join(PRE, 'oferta-asociatii.html')).read()
tpl = re.sub(r'  <!-- s24-seo -->.*?<!-- /s24-seo -->\n', '', tpl, flags=re.S)
tpl = re.sub(r'\n<!-- s24-float:.*?<!-- /s24-float -->\n', '', tpl, flags=re.S)

CHIP = 'display:inline-block;background:#fff;border:1px solid #E1E6EC;border-radius:999px;padding:8px 16px;margin:0 8px 10px 0;font-weight:600;color:#0D1F33;text-decoration:none'
def chips(names): return ''.join(f'<a href="{link(n)}" style="{CHIP}">{H.escape(n)}</a>' if link(n) else f'<span style="{CHIP}">{H.escape(n)}</span>' for n in names)

def page(fname, title, desc, pill, h1a, lead, zone_eyebrow, zone_h, zone_sub, zone_html, faq_q, faq_a):
    s = tpl
    s = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)}</title>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" name="description">', f'<meta content="{H.escape(desc, quote=True)}" name="description">', s, count=1)
    s = s.replace('<span class="s24-pill">OFERTĂ PENTRU ASOCIAȚII DE PROPRIETARI</span>', f'<span class="s24-pill">{H.escape(pill)}</span>', 1)
    s = s.replace('<h1 class="s24-h1">Supraveghere video pentru blocul tău, <span class="s24-h1-a">fără costuri de investiție</span></h1>',
                  f'<h1 class="s24-h1">{h1a}, <span class="s24-h1-a">fără costuri de investiție</span></h1>', 1)
    s = s.replace('Instalăm, întreținem și garantăm un sistem complet de camere IP Hikvision, Dahua și HiLook de minimum 4 MP (2560 × 1440).', lead + ' Instalăm, întreținem și garantăm un sistem complet de camere IP Hikvision, Dahua și HiLook de minimum 4 MP (2560 × 1440).', 1)
    zone = f'''  <section class="s24-base s24-sec" style="background:#F5F7FA">
    <div class="s24-wrap">
      <div class="s24-eyebrow">{zone_eyebrow}</div>
      <h2 class="s24-h2">{zone_h}</h2>
      <p class="s24-sub">{zone_sub}</p>
      {zone_html}
    </div>
  </section>
'''
    s = s.replace('  <section id="pasi" class="s24-base s24-steps">', zone + '  <section id="pasi" class="s24-base s24-steps">', 1)
    s = s.replace('        <h3 class="s24-q-h">Cât durează contractul?</h3>', f'''        <h3 class="s24-q-h">{faq_q}</h3>
        <p class="s24-q-p">{faq_a}</p>
      </div>
      <div class="s24-q">
        <h3 class="s24-q-h">Cât durează contractul?</h3>''', 1)
    assert pill in s and zone_h in s
    open(os.path.join(PRE, fname), 'w').write(s)

# pagina generală Ilfov
page('supraveghere-video-bloc-ilfov.html',
     'Supraveghere video bloc Ilfov – orașe și comune – SUPRAVEGHERE24h',
     'Supraveghere video pentru blocuri și ansambluri rezidențiale din județul Ilfov: Voluntari, Popești-Leordeni, Bragadiru, Chiajna, Otopeni și toate comunele. Instalare gratuită, abonament de la 189 lei / lună.',
     'JUDEȚUL ILFOV',
     'Supraveghere video pentru blocuri din județul Ilfov',
     'Montăm sisteme de supraveghere video pentru asociațiile de proprietari și ansamblurile rezidențiale din tot județul Ilfov, în orașe și în comune.',
     'ORAȘE ȘI COMUNE', 'Lucrăm în tot județul Ilfov',
     'Venim la bloc pentru evaluare, propunem amplasarea camerelor și vă trimitem oferta, gratuit.',
     f'<h3 style="margin:22px 0 12px;color:#0D1F33;font-size:18px">Orașe</h3><div>{chips(ORASE)}</div>'
     f'<h3 style="margin:18px 0 12px;color:#0D1F33;font-size:18px">Comune</h3><div>{chips(COMUNE_TOATE)}</div>',
     'Veniți și în comunele din Ilfov?', 'Da. Lucrăm în toate orașele și comunele din județul Ilfov, la blocuri și la ansambluri rezidențiale. Evaluarea și oferta sunt gratuite.')

for name in ORASE + COMUNE_PAG:
    tip = 'orașul' if name in ORASE else 'comuna'
    ex = EXTRA.get(name)
    vecini = [n for n in (ORASE + COMUNE_PAG) if n != name][:6]
    page(link(name),
         f'Supraveghere video bloc {name}, Ilfov – SUPRAVEGHERE24h',
         f'Supraveghere video pentru blocuri și ansambluri rezidențiale din {name}, Ilfov: camere IP Hikvision, Dahua și HiLook de minimum 4 MP (2560 × 1440), instalare gratuită, abonament de la 189 lei / lună.',
         f'{name.upper()} · ILFOV',
         f'Supraveghere video pentru blocuri din {name}',
         f'Montăm sisteme de supraveghere video pentru asociațiile de proprietari și ansamblurile rezidențiale din {tip} {name}{", " + ex if ex else ""}.',
         f'{name.upper()} ȘI ÎMPREJURIMI', f'Supraveghere video în {name} și în tot Ilfovul',
         f'Venim la bloc în {name} pentru evaluare, propunem amplasarea camerelor și vă trimitem oferta, gratuit. Lucrăm și în localitățile din apropiere:',
         f'<div style="margin-top:18px">{chips(vecini)}<a href="supraveghere-video-bloc-ilfov.html" style="{CHIP};background:#0D1F33;color:#fff;border-color:#0D1F33">Toate localitățile din Ilfov →</a></div>',
         f'Veniți și în {name}?', f'Da. Lucrăm cu asociații de proprietari și ansambluri rezidențiale din {name} și din tot județul Ilfov. Evaluarea la bloc și oferta sunt gratuite.')

# card „Județul Ilfov” în secțiunea „Zone deservite” de pe prima pagină
p = os.path.join(PRE, 'index.html'); s = open(p).read()
if 'supraveghere-video-bloc-ilfov.html' not in s:
    card = ('<a href="supraveghere-video-bloc-ilfov.html" style="display:block;background:#0D1F33;border:1px solid #0D1F33;border-radius:14px;padding:18px 20px;text-decoration:none;color:#fff">'
            '<b style="font-size:18px">Județul Ilfov</b><br><span style="color:#C9D4E0;font-size:14px">Voluntari, Popești-Leordeni, Chiajna…</span></a>')
    s = s.replace('<h2 class="s24-h2">Montăm în toate sectoarele Bucureștiului</h2>', '<h2 class="s24-h2">Montăm în tot Bucureștiul și în județul Ilfov</h2>', 1)
    i = s.find('s24-zone'); j = s.find('</div>\n    </div>\n  </section>', i)
    assert i > 0 and j > i
    s = s[:j] + card + s[j:]
    open(p, 'w').write(s)
print('Ilfov:', 1 + len(ORASE) + len(COMUNE_PAG), 'pagini')
