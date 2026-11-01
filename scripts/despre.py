# Pagina „Despre noi” + link în subsolul tuturor paginilor. Ordine: ilfov.py → despre.py → imbunatatiri.py
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, 'previzualizare-25c472e2')
if not os.path.isdir(PRE): PRE = ROOT   # după lansare, paginile sunt în rădăcină

tpl = open(os.path.join(PRE, 'oferta-asociatii.html')).read()
tpl = re.sub(r'  <!-- s24-seo -->.*?<!-- /s24-seo -->\n', '', tpl, flags=re.S)
tpl = re.sub(r'\n<!-- s24-float:.*?<!-- /s24-float -->\n', '', tpl, flags=re.S)

title = 'Despre noi – SUPRAVEGHERE24h, Yca Solutions SRL'
desc = ('SUPRAVEGHERE24h este brandul Yca Solutions SRL, firmă din București înființată în 2021. Montăm și întreținem sisteme de '
        'supraveghere video pentru blocuri și asociații de proprietari din București și Ilfov.')
s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', tpl, count=1)
s = re.sub(r'<meta content="[^"]*" name="description">', f'<meta content="{desc}" name="description">', s, count=1)

hero_start = s.find('  <section class="s24-base s24-dark s24-ohero">')
band_start = s.find('  <section class="s24-base s24-band">')
faq_start = s.find('  <section id="faq" class="s24-base s24-faq">')
contact_start = s.find('  <section id="contact" class="s24-base s24-contact">')
assert 0 < hero_start < band_start < faq_start < contact_start

IC = lambda d: f'<svg stroke-linejoin="round" stroke-linecap="round" stroke-width="2.2" stroke="#0D1F33" fill="none" viewBox="0 0 24 24" height="26" width="26">{d}</svg>'
def card(n, h, p, dark=False):
    d = ' s24-card-d' if dark else ''
    return (f'        <div class="s24-card{d}">\n          <div class="s24-card-n{" s24-card-n-d" if dark else ""}">{n}</div>\n'
            f'          <h3 class="s24-card-h{" s24-card-h-d" if dark else ""}">{h}</h3>\n          <p class="s24-card-p{" s24-card-p-d" if dark else ""}">{p}</p>\n        </div>\n')

body = f'''  <section class="s24-base s24-dark s24-ohero">
    <div class="s24-wrap s24-ohero-in">
      <div class="s24-ohero-txt"><span class="s24-pill">DESPRE NOI</span>
        <h1 class="s24-h1">Securitate rezidențială, <span class="s24-h1-a">non-stop</span></h1>
        <p class="s24-lead">SUPRAVEGHERE24h este brandul firmei Yca Solutions SRL din București, înființată în 2021. Ne ocupăm de un singur lucru și îl facem bine: sisteme de supraveghere video pentru blocuri și asociații de proprietari, montate, întreținute și garantate de noi.</p>
        <div class="s24-cta">
          <a href="calculator-pret.html" class="s24-btn s24-btn-a">Calculează prețul</a>
          <a href="contact.html" class="s24-btn s24-btn-o">Contactează-ne</a>
        </div>
      </div>
      <div class="s24-ohero-card">
        <p class="s24-ohero-k">Pe scurt</p>
        <div class="s24-ohero-row"><span>Din</span><span class="s24-ohero-val">2021</span></div>
        <div class="s24-ohero-row"><span>Sediu</span><span class="s24-ohero-val">București, Sector 1</span></div>
        <div class="s24-ohero-row"><span>Zonă</span><span class="s24-ohero-val">București și Ilfov</span></div>
        <div class="s24-ohero-row"><span>Echipamente</span><span class="s24-ohero-val">Hikvision, Dahua, HiLook · minim 4 MP</span></div>
        <div class="s24-ohero-row"><span>Acreditare</span><span class="s24-ohero-val">Poliția Română</span></div>
        <p class="s24-ohero-note">Program: luni–vineri, 9:00–18:00.</p>
      </div>
    </div>
  </section>
  <section class="s24-base s24-sec">
    <div class="s24-wrap">
      <div class="s24-eyebrow">CINE SUNTEM</div>
      <h2 class="s24-h2">O firmă mică, specializată pe blocuri</h2>
      <p class="s24-sub">Am pornit în 2021 cu o idee simplă: o asociație de proprietari ar trebui să poată avea un sistem de supraveghere bun fără să strângă bani pentru investiția inițială. De aceea lucrăm pe bază de abonament lunar fix: noi montăm echipamentele, le întreținem și le garantăm pe toată durata contractului, iar la final ele rămân ale asociației.</p>
      <p class="s24-sub" style="margin-top:14px">Lucrăm direct cu administratorii și cu comitetele asociațiilor, de la evaluarea blocului până la instruirea persoanelor care vor avea acces la imagini.</p>
    </div>
  </section>
  <section class="s24-base s24-sec" style="background:#F5F7FA">
    <div class="s24-wrap">
      <div class="s24-eyebrow">CE NE DEFINEȘTE</div>
      <h2 class="s24-h2">Cum lucrăm</h2>
      <div class="s24-grid">
{card('01', 'Acreditați de Poliția Română', 'Proiectăm și montăm sisteme de supraveghere video conform cerințelor legale, ca firmă acreditată.')}{card('02', 'Echipamente profesionale', 'Folosim camere IP Hikvision, Dahua și HiLook de minimum 4 MP și recordere video (NVR) dedicate, potrivite pentru funcționare non-stop.')}{card('03', 'Monitorizare 24/7', 'Sistemele montate sunt verificate automat, non-stop, de platforma noastră: aflăm imediat dacă un NVR sau o cameră nu mai funcționează și intervenim.')}{card('04', 'Garanție completă', 'Garanția acoperă toată durata contractului, inclusiv furtul și vandalismul. Service-ul și mentenanța sunt incluse.')}{card('05', 'Transparență', 'Prețul se vede direct pe site, în calculator. Abonamentul lunar este fix și nu există costuri ascunse.')}{card('06', 'Datele rămân în bloc', 'Imaginile se păstrează local, în NVR-ul din bloc, iar acces au doar persoanele desemnate de asociație.', True)}      </div>
    </div>
  </section>
  <section class="s24-base s24-sec">
    <div class="s24-wrap">
      <div class="s24-eyebrow">DATE DE IDENTIFICARE</div>
      <h2 class="s24-h2">Datele firmei</h2>
      <div style="margin-top:22px;max-width:640px;border:1px solid #E1E6EC;border-radius:14px;overflow:hidden;background:#fff">
        <table style="width:100%;border-collapse:collapse;font-size:16px">
          <tr><td style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC;width:40%">Denumire</td><td style="padding:14px 18px;border-bottom:1px solid #E1E6EC;font-weight:700;color:#14202E">Yca Solutions SRL</td></tr>
          <tr><td style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC">Brand</td><td style="padding:14px 18px;border-bottom:1px solid #E1E6EC;font-weight:700;color:#14202E">SUPRAVEGHERE24h</td></tr>
          <tr><td style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC">CUI</td><td style="padding:14px 18px;border-bottom:1px solid #E1E6EC;font-weight:700;color:#14202E">45211628</td></tr>
          <tr><td style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC">Nr. Reg. Com.</td><td style="padding:14px 18px;border-bottom:1px solid #E1E6EC;font-weight:700;color:#14202E">J40/19754/2021</td></tr>
          <tr><td style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC">Sediu</td><td style="padding:14px 18px;border-bottom:1px solid #E1E6EC;font-weight:700;color:#14202E">Str. Aviator Mircea Petre nr. 10, Sector 1, București</td></tr>
          <tr><td style="padding:14px 18px;color:#52606F;border-bottom:1px solid #E1E6EC">Telefon</td><td style="padding:14px 18px;border-bottom:1px solid #E1E6EC;font-weight:700"><a href="tel:+40763354355" style="color:#14202E">0763 354 355</a></td></tr>
          <tr><td style="padding:14px 18px;color:#52606F">E-mail</td><td style="padding:14px 18px;font-weight:700"><a href="mailto:contact@supraveghere24h.ro" style="color:#14202E">contact@supraveghere24h.ro</a></td></tr>
        </table>
      </div>
    </div>
  </section>
'''
s = s[:hero_start] + body + s[band_start:faq_start] + s[contact_start:]
assert 'DESPRE NOI' in s and 's24-band' in s and 'id="contact"' in s and 'id="faq"' not in s
open(os.path.join(PRE, 'despre-noi.html'), 'w').write(s)

# link „Despre noi” în subsol, pe toate paginile
LINK = '<a href="despre-noi.html" class="s24-flink">Despre noi</a><span class="s24-fsep">·</span>'
n = 0
for f in sorted(os.listdir(PRE)):
    if not f.endswith('.html'): continue
    p = os.path.join(PRE, f); t = open(p).read()
    if 'href="despre-noi.html" class="s24-flink"' in t: continue
    i = t.find('<footer'); j = t.find('<a href="', t.find('s24-flink', i) - 60) if i > 0 else -1
    j = t.find('<a ', i) if i > 0 else -1
    if i < 0 or j < 0: print('fără subsol:', f); continue
    t = t[:j] + LINK + '\n          ' + t[j:]
    open(p, 'w').write(t); n += 1
print('despre-noi.html creat; link în subsol pe', n, 'pagini')
