# Magazin online: catalogul cu prețuri (js/s24catalog.js), coșul din antet (js/s24navfx.js), pagina coșului cos.html (js/s24cos.js),
# pagina „Livrare și retur”, secțiunea de vânzare din Termeni, paragraful despre comenzi din Politica de confidențialitate,
# link în subsol, versiunile scripturilor. CSS la finalul css/...webflow.css (marcaj s24-shop2). Re-rulabil: python3 scripts/magazin.py
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ── CSS ──
p = 'css/supraveghere24h-ro.webflow.css'; css = open(p).read()
if 's24-shop2' not in css:
    open(p, 'a').write(open('scripts/magazin_css.txt').read() + open('scripts/magazin_cos_css.txt').read())

def page(tpl_file, out, title, desc, canon, body, noindex=False, scripts=''):
    s = open(tpl_file).read()
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" name="description">', f'<meta content="{desc}" name="description">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*(">)', r'\g<1>https://supraveghere24h.ro/' + canon + r'\2', s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(">)', r'\g<1>https://supraveghere24h.ro/' + canon + r'\2', s, count=1)
    if noindex and 'name="robots"' not in s: s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex">', 1)
    s = re.sub(r' aria-current="page" class="s24-link w--current"', ' class="s24-link"', s)
    i = s.find('</header>') + len('</header>'); j = s.find('  <footer')
    s = s[:i] + '\n' + body + s[j:]
    s = re.sub(r'<script src="js/s24(reviews|formresult)\.js[^"]*"[^>]*></script>\s*', '', s)
    if scripts: s = s.replace('<script src="js/s24navfx.js', scripts + '\n<script src="js/s24navfx.js', 1)
    open(out, 'w').write(s)

# ── cos.html ──
COS = '''  <section class="s24-base s24-shop s24c-page">
    <div class="s24-wrap">
      <div class="s24-crumb"><a href="index.html">Acasă</a> › <a href="echipamente.html">Echipamente</a> › Coș</div>
      <h1 class="s24-shop-h">Coșul tău</h1>
      <ol class="s24c-steps" aria-label="Pașii comenzii"><li class="on">Produse</li><li class="on">Date și livrare</li><li>Confirmare telefonică</li></ol>
      <div id="s24c"><p class="s24c-wait">Se încarcă coșul…</p></div>
      <noscript><p>Pentru a trimite comanda online ai nevoie de JavaScript. Ne poți suna la 0763 354 355.</p></noscript>
    </div>
  </section>
'''
page('despre-noi.html', 'cos.html', 'Coșul tău – SUPRAVEGHERE24h', 'Coșul de cumpărături SUPRAVEGHERE24h: camere IP, NVR-uri și accesorii, cu livrare prin curier.', 'cos', COS, noindex=True,
     scripts='<script src="js/s24cos.js?v=1" defer></script>')

# ── livrare-si-retur.html ──
H = lambda t: f'      <h2 class="s24-pol-s">{t}</h2>\n'
P = lambda t: f'      <p class="s24-pol-t">{t}</p>\n'
RET = ('  <section class="s24-base s24-pol">\n    <div class="s24-pol-w">\n      <h1 class="s24-pol-h">Livrare, retur și garanție</h1>\n      <p class="s24-pol-d">Ultima actualizare: 19 noiembrie 2026</p>\n'
 + P('Această pagină se aplică echipamentelor cumpărate prin magazinul online de pe supraveghere24h.ro. Vânzătorul este Yca Solutions SRL, CUI 45211628, Nr. Reg. Com. J2021019754409, Str. Aviator Mircea Petre nr. 10, Camera 1, Sector 1, București · contact@supraveghere24h.ro · 0763 354 355.')
 + H('1. Confirmarea comenzii')
 + P('După ce trimiți comanda primești un e-mail cu produsele și totalul. Te sunăm în zilele lucrătoare ca să confirmăm disponibilitatea și livrarea. Dacă un produs nu mai este disponibil sau prețul afișat a fost evident greșit, îți spunem înainte de expediere și poți renunța la comandă fără niciun cost.')
 + H('2. Livrarea')
 + P('<strong>Prin curier</strong>, la adresa indicată în comandă. Costul transportului este afișat în coș înainte să trimiți comanda (și poate fi gratuit peste un anumit total). Expediem de regulă în 1–2 zile lucrătoare de la confirmare pentru produsele „În stoc” și în 2–4 zile lucrătoare pentru cele marcate „Livrare în 2–4 zile”; pentru produsele „La comandă” îți comunicăm termenul la telefon. Curierul livrează de obicei în 1–3 zile lucrătoare de la expediere.')
 + P('<strong>Ridicare personală</strong> din sediul nostru din București, Sector 1, după ce te sunăm și stabilim ora. Ridicarea este gratuită.')
 + P('La primire, verifică aspectul coletului în prezența curierului. Dacă ambalajul este deteriorat, poți refuza coletul sau poți întocmi un proces-verbal împreună cu curierul și ne anunți în aceeași zi.')
 + H('3. Plata și factura')
 + P('Poți plăti ramburs (la curier), prin transfer bancar (datele de plată le primești pe e-mail, iar comanda pleacă după ce primim plata) sau la ridicare. Pentru fiecare comandă emitem factură fiscală, pe persoană fizică sau pe firmă. Prețurile afișate sunt prețuri finale, în lei; Yca Solutions SRL nu este plătitoare de TVA.')
 + H('4. Dreptul de retragere (14 zile) – pentru persoane fizice')
 + P('Dacă ai cumpărat ca persoană fizică (consumator), ai dreptul să te retragi din contract în termen de 14 zile, fără să justifici decizia, conform OUG nr. 34/2014. Termenul curge din ziua în care tu (sau o persoană indicată de tine, alta decât curierul) intri în posesia produselor; dacă produsele dintr-o comandă vin în colete separate, termenul curge de la primirea ultimului colet.')
 + P('Pentru a te retrage, trimite-ne o declarație clară înainte de expirarea termenului: un e-mail la <a href="mailto:contact@supraveghere24h.ro">contact@supraveghere24h.ro</a> sau formularul de mai jos (nu este obligatoriu să-l folosești). Îți confirmăm primirea pe e-mail.')
 + P('<strong>Returnarea produselor.</strong> Trimite sau adu produsele, fără întârzieri nejustificate și cel târziu în 14 zile de la data la care ne-ai comunicat retragerea, la adresa sediului de mai sus (îți spunem la telefon unde le poți preda). Costul direct al returnării îl suporți tu.')
 + P('<strong>Banii înapoi.</strong> Îți returnăm toate sumele plătite, inclusiv costul livrării standard, în cel mult 14 zile de la data la care am fost informați despre retragere, prin aceeași metodă de plată (sau prin transfer bancar, dacă ai plătit ramburs ori numerar). Putem amâna rambursarea până primim produsele înapoi sau până ne trimiți dovada că le-ai expediat, oricare dintre aceste date este mai apropiată.')
 + P('Răspunzi doar pentru diminuarea valorii produselor rezultată din manipulări diferite de cele necesare pentru a le verifica natura, caracteristicile și funcționarea (de exemplu, produse montate, găurite sau deteriorate). Te rugăm să returnezi produsele complete, cu accesoriile și, pe cât posibil, în ambalajul original.')
 + P('<strong>Pentru firme și asociații</strong> (cumpărători persoane juridice) dreptul de retragere de 14 zile nu se aplică; un eventual retur se poate face doar cu acordul nostru.')
 + H('5. Formular de retragere')
 + '      <div class="s24-pol-t" style="background:#F5F7FA;border:1px solid #E1E6EC;border-radius:12px;padding:18px 20px">Către: Yca Solutions SRL, Str. Aviator Mircea Petre nr. 10, Camera 1, Sector 1, București, e-mail contact@supraveghere24h.ro<br><br>'
   'Vă informez prin prezenta cu privire la retragerea mea din contractul referitor la vânzarea următoarelor produse: ……………………<br>'
   'Comandate la data: …………… / primite la data: ……………<br>Numărul comenzii: CMD-……………<br>Numele consumatorului: ……………………<br>Adresa consumatorului: ……………………<br>'
   'IBAN pentru rambursare (dacă e cazul): ……………………<br>Semnătura (doar dacă formularul este trimis pe hârtie): ……………<br>Data: ……………</div>\n'
 + H('6. Garanția')
 + P('Produsele noi beneficiază de garanția legală de conformitate de 2 ani de la livrare (OUG nr. 140/2021), pentru cumpărătorii persoane fizice. Dacă un produs nu funcționează corect, scrie-ne sau sună-ne: îți spunem cum ni-l trimiți sau unde îl aduci, iar noi îl reparăm sau îl înlocuim, iar dacă acest lucru nu este posibil, îți returnăm banii. Repararea sau înlocuirea se face în cel mult 15 zile calendaristice de la data la care ne-ai adus la cunoștință lipsa de conformitate și ne-ai pus produsul la dispoziție. Pentru firme, garanția este cea a producătorului, menționată pe factură.')
 + P('Garanția nu acoperă defectele cauzate de montaj sau alimentare necorespunzătoare, loviri, umezeală peste gradul de protecție declarat, intervenții neautorizate sau uzura normală. Dacă montajul l-am făcut noi, garanția acoperă și manopera.')
 + H('7. Reclamații')
 + P('Ne poți scrie oricând la <a href="mailto:contact@supraveghere24h.ro">contact@supraveghere24h.ro</a> sau ne poți suna la 0763 354 355. Îți răspundem în cel mult 30 de zile. Te poți adresa și Autorității Naționale pentru Protecția Consumatorilor (<a href="https://anpc.ro" rel="noopener">anpc.ro</a>) sau poți folosi procedura de soluționare alternativă a litigiilor (<a href="https://anpc.ro/ce-este-sal/" rel="noopener">SAL</a>).')
 + '    </div>\n  </section>\n')
page('termeni-si-conditii.html', 'livrare-si-retur.html', 'Livrare, retur și garanție – SUPRAVEGHERE24h',
     'Cum livrăm echipamentele comandate online, dreptul de retragere în 14 zile, formularul de retragere și garanția de 2 ani.', 'livrare-si-retur', RET)

# ── Termeni: secțiunea de vânzare online ──
t = open('termeni-si-conditii.html').read()
if 'id="vanzare"' not in t:
    sec = (H('11. Vânzarea online de echipamente').replace('<h2 class="s24-pol-s">', '<h2 class="s24-pol-s" id="vanzare">')
      + P('<strong>Comanda.</strong> Prin trimiterea unei comenzi din coșul de pe site faci o ofertă de cumpărare. Contractul se încheie atunci când îți confirmăm comanda, telefonic sau pe e-mail, înainte de expediere. Putem refuza o comandă (de exemplu, dacă produsul nu mai este disponibil, dacă datele de livrare sunt incomplete sau dacă prețul afișat a fost evident greșit); în acest caz te anunțăm, iar dacă ai plătit deja îți returnăm integral banii.')
      + P('<strong>Prețurile</strong> sunt afișate în lei și sunt prețuri finale; Yca Solutions SRL nu este plătitoare de TVA. Costul transportului și, dacă e cazul, taxa de ramburs sunt afișate în coș înainte de trimiterea comenzii. Prețurile de pe site se pot actualiza, dar pentru o comandă trimisă se aplică prețul afișat în momentul trimiterii.')
      + P('<strong>Plata</strong> se face ramburs, prin transfer bancar sau la ridicare, după metoda aleasă în coș. Pentru fiecare comandă emitem factură fiscală.')
      + P('<strong>Livrarea, dreptul de retragere în 14 zile pentru persoane fizice, returul și garanția</strong> sunt descrise pe pagina <a href="livrare-si-retur.html">Livrare, retur și garanție</a>, care face parte din acești termeni.')
      + P('<strong>Montajul</strong> nu este inclus în prețul produselor; îl putem face la cerere, pe baza unei oferte separate, în București și Ilfov.'))
    t = t.replace('      <h2 class="s24-pol-s">10. Modificări</h2>', sec + '      <h2 class="s24-pol-s">10. Modificări</h2>', 1)
    # mutăm „Modificări” la final
    m = re.search(r'      <h2 class="s24-pol-s">10\. Modificări</h2>\n      <p class="s24-pol-t">.*?</p>\n', t)
    if m:
        blk = m.group(0); t = t.replace(blk, '', 1)
        t = t.replace('    </div>\n  </section>\n  <footer', blk.replace('10. Modificări', '12. Modificări') + '    </div>\n  </section>\n  <footer', 1)
    t = t.replace('Descrierile și imaginile echipamentelor au caracter informativ. Modelele exacte pot varia în funcție de disponibilitate, cu performanțe cel puțin echivalente celor prezentate.',
                  'Descrierile și imaginile echipamentelor au caracter informativ. În cadrul abonamentului, modelele exacte pot varia în funcție de disponibilitate, cu performanțe cel puțin echivalente celor prezentate. La produsele cumpărate din magazinul online primești exact modelul (codul de produs) comandat.', 1)
    t = re.sub(r'Ultima actualizare: [^<]*', 'Ultima actualizare: 19 noiembrie 2026', t, count=1)
    open('termeni-si-conditii.html', 'w').write(t)

# ── Politica de confidențialitate: comenzile online ──
c = open('politica-de-confidentialitate.html').read()
if 'Comenzi online' not in c:
    c = c.replace('Dacă răspunzi la o ofertă (acceptare, refuz sau cerere de clarificări), păstrăm și răspunsul tău.</p>',
                  'Dacă răspunzi la o ofertă (acceptare, refuz sau cerere de clarificări), păstrăm și răspunsul tău.</p>\n'
                  '      <p class="s24-pol-t"><strong>Comenzi online.</strong> Când comanzi echipamente din magazinul online: nume, telefon, e-mail, adresa de livrare, datele firmei (dacă ceri factură pe firmă), produsele comandate, observațiile tale, data, ora și adresa IP de la care ai acceptat termenii.</p>', 1)
    c = c.replace('Datele din formularele de contact și de ofertă nu le folosim pentru publicitate și nu le vindem.</p>',
                  'Datele din formularele de contact și de ofertă nu le folosim pentru publicitate și nu le vindem.</p>\n'
                  '      <p class="s24-pol-t"><strong>Comenzi.</strong> Datele din comandă le folosim ca să o confirmăm, să o livrăm, să emitem factura și să rezolvăm retururi sau probleme de garanție. Temeiul este executarea contractului de vânzare și obligațiile legale (contabilitate). Facturile și documentele justificative se păstrează cât cere legea contabilității (de regulă 5 ani, unele documente 10 ani); restul datelor comenzii le păstrăm cel mult 3 ani de la livrare.</p>', 1)
    c = c.replace('Datele sunt văzute doar de echipa noastră, pentru a răspunde cererii.</p>',
                  'Datele sunt văzute doar de echipa noastră, pentru a răspunde cererii. Pentru comenzile livrate prin curier, firma de curierat primește numele, telefonul și adresa de livrare. Confirmarea comenzii o trimitem prin serviciul nostru de e-mail.</p>', 1)
    assert 'Comenzi online' in c and 'firma de curierat' in c
    open('politica-de-confidentialitate.html', 'w').write(c)

# ── toate paginile: link în subsol, versiunile scripturilor; paginile de echipamente: text ──
SHOPP = {'echipamente.html', 'camere-ip.html', 'camere-ip-exterior.html', 'camere-ip-interior.html', 'kit-uri-camere.html', 'nvr-uri.html', 'stocare.html', 'accesorii.html'}
LNK = '<a href="livrare-si-retur.html" class="s24-flink">Livrare și retur</a><span class="s24-fsep">·</span>'
n = 0
for f in sorted(glob.glob('*.html')):
    s = open(f).read(); o = s
    if 'href="livrare-si-retur.html" class="s24-flink"' not in s:
        s = s.replace('<a href="termeni-si-conditii.html" class="s24-flink">Termeni și condiții</a><span class="s24-fsep">·</span>',
                      '<a href="termeni-si-conditii.html" class="s24-flink">Termeni și condiții</a><span class="s24-fsep">·</span>\n          ' + LNK, 1)
    s = re.sub(r'js/s24navfx\.js\?v=\d+', 'js/s24navfx.js?v=3', s)
    s = re.sub(r'js/s24catalog\.js\?v=\d+', 'js/s24catalog.js?v=5', s)
    if f in SHOPP:
        s = s.replace('<p class="s24-shop-p">Camerele IP pe care le montăm: HiLook, Hikvision și Dahua, cu iluminare duală și microfon. Echipamentele sunt incluse în abonament, fără investiție inițială.',
                      '<p class="s24-shop-p">Camere IP, NVR-uri, hard disk-uri și accesorii HiLook, Hikvision și Dahua — aceleași echipamente pe care le montăm noi. Pentru blocuri, sunt incluse în abonament, fără investiție inițială.', 1)
        s = s.replace('<div class="s24-side-h">Categorii</div>\n', '<div class="s24-side-h">Categorii</div>\n        <a href="echipamente.html" class="s24-side-sub' + (' w--current' if f == 'echipamente.html' else '') + '">Toate echipamentele</a>\n', 1) if 'Toate echipamentele</a>' not in s else s
    if s != o: open(f, 'w').write(s); n += 1

sm = 'sitemap.xml'; x = open(sm).read()
if '/livrare-si-retur<' not in x:
    x = x.replace('</urlset>', '  <url><loc>https://supraveghere24h.ro/livrare-si-retur</loc><lastmod>2026-11-19</lastmod></url>\n</urlset>'); open(sm, 'w').write(x)
print('magazin: cos.html, livrare-si-retur.html; actualizate', n, 'pagini')
