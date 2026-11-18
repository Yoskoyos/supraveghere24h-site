# Ghiduri pentru administratori de bloc (3 articole + pagina /ghiduri) cu formular de abonare la newsletter (dublă confirmare).
# Se construiesc din despre-noi.html (antet, subsol, cookie-uri, analytics identice). Re-rulabil: python3 scripts/ghiduri.py
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, 'despre-noi.html')).read()
TODAY = '2026-11-18'

CSS = '''<style id="s24-art-css">
.s24-art{background:#fff;padding:56px 0 64px}.s24-art .s24-wrap{max-width:780px}
.s24-art h2{font-family:Bricolage Grotesque,Montserrat,sans-serif;color:#14202E;font-size:28px;line-height:1.25;margin:40px 0 12px;letter-spacing:-.2px}
.s24-art h3{color:#14202E;font-size:20px;margin:28px 0 8px}
.s24-art p,.s24-art li{color:#3B4A5C;font-size:18px;line-height:1.65}.s24-art p{margin:0 0 16px}
.s24-art ul,.s24-art ol{margin:0 0 18px;padding-left:24px}.s24-art li{margin:6px 0}
.s24-art a{color:#0D63B8;text-decoration:underline}.s24-art strong{color:#14202E}
.s24-art .s24-box{background:#F5F7FA;border-left:4px solid #F5A100;border-radius:10px;padding:18px 20px;margin:24px 0}
.s24-art .s24-box p:last-child{margin:0}
.s24-art table{width:100%;border-collapse:collapse;margin:8px 0 22px;font-size:16px}
.s24-art th,.s24-art td{border-bottom:1px solid #E1E6EC;padding:10px 12px;text-align:left;color:#14202E}.s24-art th{background:#F5F7FA;font-weight:700}
.s24-art .s24-model{background:#FFFDF6;border:1px dashed #E3C77A;border-radius:12px;padding:20px 22px;font-size:16px}
.s24-art .s24-model p{font-size:16px;margin:0 0 10px}
.s24-art .s24-note{font-size:14px;color:#6B7785;margin-top:32px}
.s24-art .s24-cta2{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px}
.s24-art .s24-cta2 a{text-decoration:none}
.s24-gcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-top:8px}
.s24-gcard{display:block;background:#fff;border:1px solid #E1E6EC;border-radius:14px;padding:22px;text-decoration:none!important;transition:box-shadow .2s,transform .2s}
.s24-gcard:hover{box-shadow:0 10px 30px rgba(13,31,51,.10);transform:translateY(-2px)}
.s24-gcard h3{margin:0 0 8px!important;font-size:19px!important}.s24-gcard p{font-size:16px!important;margin:0!important}
.s24-gcard span{display:inline-block;margin-top:12px;color:#B86E00;font-weight:700;font-size:15px}
.s24-nl{background:#0D1F33;padding:56px 0}.s24-nl .s24-wrap{max-width:780px}
.s24-nl h2{color:#fff;font-family:Bricolage Grotesque,Montserrat,sans-serif;font-size:28px;margin:0 0 8px}
.s24-nl p{color:#C9D3DE;font-size:17px;margin:0 0 18px}
.s24-nl form{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.s24-nl input[type=email],.s24-nl input[type=text]{height:48px;border-radius:10px;border:1px solid #2A3E55;background:#132A44;color:#fff;padding:0 14px;font-size:16px;width:100%;box-sizing:border-box}
.s24-nl input::placeholder{color:#8FA0B3}
.s24-nl .s24-nl-chk{grid-column:1/-1;display:flex;gap:10px;align-items:flex-start;color:#C9D3DE;font-size:14px;line-height:1.5}
.s24-nl .s24-nl-chk input{width:20px;height:20px;margin-top:2px;flex:0 0 auto}
.s24-nl .s24-nl-chk a{color:#FFC54D}
.s24-nl button{grid-column:1/-1;height:50px;border:0;border-radius:10px;background:#F5A100;color:#0D1F33;font-weight:800;font-size:17px;cursor:pointer}
.s24-nl .s24-nl-msg{grid-column:1/-1;border-radius:10px;padding:12px 14px;font-size:15px;display:none}
.s24-nl .s24-nl-msg.ok{display:block;background:#E8F7EE;color:#14532D}.s24-nl .s24-nl-msg.err{display:block;background:#FDECEC;color:#7F1D1D}
@media(max-width:600px){.s24-art{padding:36px 0 44px}.s24-art h2{font-size:23px}.s24-art p,.s24-art li{font-size:17px}.s24-nl form{grid-template-columns:1fr}.s24-art table{font-size:14px}}
</style>'''

NL = '''  <section id="abonare" class="s24-base s24-nl">
    <div class="s24-wrap">
      <h2>Primește noutățile pe e-mail</h2>
      <p>Ghiduri pentru administratori, modificări legislative și ofertele SUPRAVEGHERE24h. Doar când avem ceva util de spus; te poți dezabona oricând.</p>
      <form action="https://proxy.supraveghere24h.ro/nl/subscribe" method="post">
        <input type="email" name="email" required placeholder="Adresa de e-mail" aria-label="Adresa de e-mail">
        <input type="text" name="asociatie" placeholder="Asociația / blocul (opțional)" aria-label="Asociația sau blocul">
        <input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
        <label class="s24-nl-chk"><input type="checkbox" name="acord" required><span>Sunt de acord să primesc pe e-mail oferte și noutăți de la SUPRAVEGHERE24h (Yca Solutions SRL), conform <a href="politica-de-confidentialitate.html" target="_blank">politicii de confidențialitate</a>. Mă pot dezabona oricând.</span></label>
        <div class="s24-nl-msg" id="s24-nl-msg" role="status"></div>
        <button type="submit">Mă abonez</button>
      </form>
    </div>
  </section>
  <script>(function(){try{var q=new URLSearchParams(location.search),a=q.get('abonare'),m=document.getElementById('s24-nl-msg');if(!a||!m)return;
  if(a==='trimis'){m.className='s24-nl-msg ok';m.textContent='Mai ai un pas: ți-am trimis un e-mail. Apasă linkul din el ca să confirmi abonarea.';}
  else{m.className='s24-nl-msg err';m.textContent='Abonarea nu a mers: '+(q.get('motiv')||'încearcă din nou.');}}catch(e){}})();</script>
'''

def page(slug, title, desc, pill, h1, lead, body, kind='article'):
    s = TPL
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1)
    s = re.sub(r'<meta content="[^"]*" name="description">', f'<meta content="{desc}" name="description">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', s, count=1)
    s = s.replace('https://supraveghere24h.ro/despre-noi"', f'https://supraveghere24h.ro/{slug}"')
    s = s.replace('<a href="despre-noi.html" aria-current="page" class="s24-link w--current">Despre noi</a>', '<a href="despre-noi.html" class="s24-link">Despre noi</a>')
    ld = {"@context": "https://schema.org", "@type": "Article" if kind == 'article' else "CollectionPage", "headline": h1, "description": desc,
          "inLanguage": "ro-RO", "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": f"https://supraveghere24h.ro/{slug}",
          "author": {"@type": "Organization", "name": "SUPRAVEGHERE24h"}, "publisher": {"@type": "Organization", "name": "SUPRAVEGHERE24h (Yca Solutions SRL)", "url": "https://supraveghere24h.ro/"}}
    s = s.replace('</head>', CSS + '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    hs = s.find('  <section class="s24-base s24-dark s24-ohero">'); cs = s.find('  <section id="contact" class="s24-base s24-contact">')
    assert 0 < hs < cs
    hero = f'''  <section class="s24-base s24-dark s24-ohero">
    <div class="s24-wrap s24-ohero-in">
      <div class="s24-ohero-txt"><span class="s24-pill">{pill}</span>
        <h1 class="s24-h1">{h1}</h1>
        <p class="s24-lead">{lead}</p>
        <div class="s24-cta">
          <a href="calculator-pret.html" class="s24-btn s24-btn-a">Calculează prețul blocului</a>
          {'<a href="#abonare" class="s24-btn s24-btn-o">Abonează-te la noutăți</a>' if slug == 'ghiduri' else '<a href="ghiduri.html" class="s24-btn s24-btn-o">Toate ghidurile</a>'}
        </div>
      </div>
    </div>
  </section>
'''
    s = s[:hs] + hero + body + NL + s[cs:]
    open(os.path.join(ROOT, slug + '.html'), 'w').write(s)

CTA = '''      <div class="s24-cta2"><a href="calculator-pret.html" class="s24-btn s24-btn-a">Calculează prețul pentru blocul tău</a><a href="#contact" class="s24-btn s24-btn-o" style="color:#14202E;border-color:#14202E">Cere o ofertă</a></div>
'''
NOTE = '      <p class="s24-note">Acest ghid are caracter informativ și nu reprezintă consultanță juridică. Pentru situația concretă a asociației voastre, verificați statutul asociației și, la nevoie, cereți părerea unui avocat. Actualizat la 18 noiembrie 2026.</p>\n'

# ───── Articolul 1 ─────
A1 = f'''  <section class="s24-base s24-art">
    <div class="s24-wrap">
      <div class="s24-box"><p><strong>Pe scurt:</strong> da, asociația de proprietari poate monta camere de supraveghere în spațiile comune ale blocului. Are nevoie de o hotărâre a adunării generale, trebuie să informeze locatarii, să păstreze imaginile doar cât e necesar și să lase accesul la ele numai persoanelor desemnate. Montajul îl face o firmă licențiată.</p></div>

      <h2>1. Decizia o ia adunarea generală a proprietarilor</h2>
      <p>Camerele se montează în spațiile comune ale blocului, care aparțin tuturor proprietarilor. De aceea decizia se ia în adunarea generală a asociației, nu de administrator sau de președinte singuri.</p>
      <p>Legea asociațiilor de proprietari (<strong>Legea nr. 196/2018</strong>) spune că adunarea generală poate lua hotărâri dacă e prezentă majoritatea proprietarilor membri (art. 48), iar hotărârile se iau cu votul majorității celor prezenți (art. 49). Dacă la prima convocare nu se strânge cvorumul, adunarea se reconvoacă și poate decide cu votul majorității celor prezenți, cu condiția ca toți membrii să fi fost anunțați.</p>
      <p><strong>Atenție:</strong> pentru acțiunile de modernizare a condominiului, art. 51 din aceeași lege cere acordul a două treimi din numărul total al proprietarilor. Legea nu spune explicit dacă un sistem de supraveghere intră aici. Ca să nu existe discuții ulterioare, verificați statutul asociației și, dacă e posibil, strângeți acordul a cel puțin două treimi dintre proprietari.</p>
      <p>Cum se pregătește concret adunarea și ce se scrie în hotărâre găsiți în ghidul <a href="ghid-hotarare-aga-camere.html">Hotărârea AGA pentru camere de supraveghere</a>.</p>

      <h2>2. Asociația devine „operator de date” (GDPR)</h2>
      <p>Imaginile în care apar oameni sunt date personale. Asociația care montează camerele devine operator de date, în sensul Regulamentului general privind protecția datelor (GDPR), și are câteva obligații simple.</p>
      <p>Temeiul legal folosit de obicei este <strong>interesul legitim</strong> al proprietarilor de a-și proteja bunurile și siguranța. Curtea de Justiție a Uniunii Europene a analizat chiar un caz dintr-un bloc din București (cauza C-708/18) și a arătat că supravegherea video a părților comune poate fi făcută fără consimțământul fiecărui locatar, dacă sunt îndeplinite condițiile interesului legitim: scopul e real, camerele sunt necesare și nu se filmează mai mult decât trebuie.</p>

      <h2>3. Locatarii trebuie informați</h2>
      <ul>
        <li><strong>Panouri de avertizare</strong> „Zonă supravegheată video”, la intrarea în bloc și în zonele filmate, înainte ca omul să intre în raza camerei.</li>
        <li><strong>O notă de informare</strong> mai detaliată: cine este operatorul, de ce se filmează, cât timp se păstrează imaginile, cine are acces și ce drepturi au oamenii. Poate fi afișată la avizier sau publicată online; un exemplu este <a href="informare-video.html">nota noastră de informare</a>.</li>
      </ul>

      <h2>4. Ce nu aveți voie să filmați</h2>
      <ul>
        <li>interiorul apartamentelor sau ce se vede prin ușile lor;</li>
        <li>camere îndreptate spre ușa unui anumit apartament, ca să urmărească o anumită persoană;</li>
        <li>strada, trotuarul sau proprietatea vecinilor, mai mult decât e strict necesar pentru intrarea în bloc.</li>
      </ul>
      <p>Regula de bază: fiecare cameră trebuie să aibă un motiv clar (intrarea, casa scării, parcarea, liftul) și să filmeze doar zona respectivă.</p>

      <h2>5. Cât timp se păstrează imaginile</h2>
      <p>Imaginile se păstrează doar cât e necesar. În practică, termenul recomandat este de <strong>cel mult 30 de zile</strong>, după care se șterg automat. Sistemele moderne de înregistrare (NVR) se pot seta să suprascrie singure înregistrările vechi.</p>
      <p>Riscul e real: în 2022, Autoritatea Națională de Supraveghere a Prelucrării Datelor cu Caracter Personal (ANSPDCP) a amendat o asociație de proprietari din București cu aproximativ 24.700 de lei pentru că păstrase imaginile camerelor circa un an și jumătate, fără un termen stabilit.</p>

      <h2>6. Cine are acces la imagini</h2>
      <ul>
        <li>Accesul îl au doar persoanele desemnate de adunarea generală, de exemplu președintele sau administratorul.</li>
        <li>Imaginile <strong>nu se publică</strong> pe grupuri de WhatsApp sau pe rețele sociale.</li>
        <li>Se predau poliției sau altor autorități doar la cerere oficială.</li>
        <li>E bine să existe un registru simplu în care se notează cine a cerut imagini, când și de ce.</li>
      </ul>

      <h2>7. Montajul îl face o firmă licențiată</h2>
      <p>Legea nr. 333/2003 privind paza obiectivelor, bunurilor, valorilor și protecția persoanelor stabilește că sistemele de supraveghere video se instalează cu respectarea dreptului la viață intimă, familială și privată, iar lucrările de proiectare și montaj ale sistemelor de securitate se fac de firme licențiate de Poliția Română pentru acest tip de activitate. SUPRAVEGHERE24h are licența IGPR nr. 6310/T.</p>

      <h2>Pe scurt: lista de verificare</h2>
      <ol>
        <li>Hotărârea adunării generale, consemnată în procesul-verbal.</li>
        <li>Camere doar în spațiile comune, fiecare cu un scop clar.</li>
        <li>Panouri „Zonă supravegheată video” și notă de informare.</li>
        <li>Păstrarea imaginilor cel mult 30 de zile, cu ștergere automată.</li>
        <li>Acces doar pentru persoanele desemnate, fără publicarea imaginilor.</li>
        <li>Montaj făcut de o firmă licențiată.</li>
      </ol>
{CTA}{NOTE}      <p class="s24-note">Surse: <a href="https://e-juridic.manager.ro/articole/cjue-camerele-video-din-bloc-nu-incalca-gdpr-26864.html" rel="noopener" target="_blank">CJUE C-708/18 (rezumat e-juridic.manager.ro)</a> · <a href="https://www.stiripesurse.ro/cea-mai-mare-amenda-aplicata-unei-asociatii-de-proprietari-mii-de-euro-pentru-incalcarea-gdpr_2437290.html" rel="noopener" target="_blank">amenda ANSPDCP din 2022 (stiripesurse.ro)</a> · Legea nr. 196/2018 · Legea nr. 333/2003 · Regulamentul (UE) 2016/679.</p>
    </div>
  </section>
'''

# ───── Articolul 2 ─────
A2 = f'''  <section class="s24-base s24-art">
    <div class="s24-wrap">
      <div class="s24-box"><p><strong>Pe scurt:</strong> pregătiți o ofertă, convocați adunarea generală cu supravegherea video pe ordinea de zi, votați, consemnați hotărârea în procesul-verbal, apoi semnați contractul și afișați informarea. Mai jos sunt pașii și un model orientativ de hotărâre.</p></div>

      <h2>Pasul 1. Cereți o ofertă concretă</h2>
      <p>Proprietarii votează mai ușor când știu exact ce primesc și cât costă. Oferta ar trebui să spună câte camere se montează și unde (intrare, casa scării, parcare, lift), cât costă lunar sau ca investiție, ce include (montaj, mentenanță, garanție) și pe ce durată se încheie contractul.</p>
      <p>Pentru blocurile din București și Ilfov puteți afla prețul în <a href="calculator-pret.html">calculatorul nostru</a> și primiți oferta pe e-mail, gata de prezentat în adunare.</p>

      <h2>Pasul 2. Convocați adunarea generală</h2>
      <p>Adunarea se convoacă de președinte, de comitetul executiv sau la cererea proprietarilor, în condițiile din Legea nr. 196/2018 și din statutul asociației. Convocatorul se afișează la avizier și trebuie să cuprindă data, ora, locul și ordinea de zi. Treceți explicit pe ordinea de zi: <em>„Aprobarea montării unui sistem de supraveghere video în spațiile comune”</em>.</p>

      <h2>Pasul 3. Ce discutați și votați în adunare</h2>
      <ul>
        <li><strong>Amplasarea camerelor</strong>: doar spații comune, fiecare cu scopul ei.</li>
        <li><strong>Furnizorul și costul</strong>: oferta aleasă, suma lunară sau investiția și cum se împarte pe apartamente.</li>
        <li><strong>Cine are acces la imagini</strong>: de obicei președintele și/sau administratorul.</li>
        <li><strong>Cât se păstrează imaginile</strong>: recomandat cel mult 30 de zile.</li>
        <li><strong>Cine semnează contractul</strong> în numele asociației.</li>
      </ul>

      <h2>Pasul 4. Cvorumul și votul</h2>
      <p>Potrivit Legii nr. 196/2018, adunarea generală poate lua hotărâri dacă e prezentă majoritatea proprietarilor membri, iar hotărârile se iau cu majoritatea voturilor celor prezenți. Dacă hotărârea e tratată ca acțiune de modernizare a blocului, art. 51 cere acordul a două treimi din numărul total al proprietarilor. Ca hotărârea să nu poată fi contestată ușor, e bine să aveți cel puțin două treimi din proprietari de acord; cei care nu pot veni pot vota prin reprezentant, cu împuternicire scrisă.</p>

      <h2>Pasul 5. Procesul-verbal și hotărârea</h2>
      <p>Hotărârea se consemnează în procesul-verbal al adunării, cu numărul de voturi pentru, împotrivă și abțineri, și se afișează la avizier. Proprietarii care nu au fost de acord o pot contesta în instanță în termenele prevăzute de lege, de aceea e important ca procedura să fie respectată.</p>

      <h2>Model orientativ de hotărâre</h2>
      <div class="s24-model">
        <p><strong>HOTĂRÂREA nr. ___ din __.__.____</strong> a Adunării generale a Asociației de proprietari ___________________</p>
        <p>Adunarea generală, întrunită legal în data de __.__.____, cu participarea a ___ proprietari din totalul de ___, hotărăște:</p>
        <p><strong>Art. 1.</strong> Se aprobă montarea unui sistem de supraveghere video în spațiile comune ale blocului, în următoarele zone: ____________________ (ex.: intrarea principală, casa scării, liftul, parcarea).</p>
        <p><strong>Art. 2.</strong> Scopul sistemului este protejarea persoanelor și a bunurilor și prevenirea vandalismului și a furturilor. Nu se filmează interiorul apartamentelor, ușile acestora sau spațiul public mai mult decât este necesar.</p>
        <p><strong>Art. 3.</strong> Se aprobă oferta furnizorului ____________________, în valoare de ______ lei/lună (sau ______ lei investiție), pe o durată de ___ luni. Costul se repartizează pe apartamente astfel: ____________________.</p>
        <p><strong>Art. 4.</strong> Imaginile se păstrează cel mult ___ zile, după care se șterg automat. Acces la imagini au doar: ____________________. Imaginile se pun la dispoziția autorităților numai la cerere oficială și nu se publică.</p>
        <p><strong>Art. 5.</strong> Se mandatează ____________________ să semneze contractul în numele asociației și să asigure afișarea panourilor de avertizare și a notei de informare.</p>
        <p>Voturi: pentru ___ · împotrivă ___ · abțineri ___. Președinte: __________ · Secretar: __________</p>
      </div>
      <p>Modelul e doar un punct de plecare; adaptați-l la statutul asociației.</p>

      <h2>Pasul 6. După vot</h2>
      <ol>
        <li>Semnați contractul cu furnizorul ales.</li>
        <li>Stabiliți cu firma de montaj amplasarea exactă a camerelor.</li>
        <li>Afișați panourile „Zonă supravegheată video” și nota de informare.</li>
        <li>Țineți un registru al cererilor de acces la imagini.</li>
      </ol>
      <p>Ce spune legea despre camerele din bloc, pe larg, găsiți în ghidul <a href="ghid-camere-supraveghere-bloc-legal.html">Camere de supraveghere în bloc: ce spune legea</a>.</p>
{CTA}{NOTE}    </div>
  </section>
'''

# ───── Articolul 3 ─────
A3 = f'''  <section class="s24-base s24-art">
    <div class="s24-wrap">
      <div class="s24-box"><p><strong>Pe scurt:</strong> o asociație are două variante: cumpără sistemul (plătește tot de la început, plus reparațiile de după) sau plătește un abonament lunar fix, cu montaj, mentenanță și garanție incluse. La SUPRAVEGHERE24h abonamentul pornește de la <strong>189 lei pe lună pentru tot blocul</strong>.</p></div>

      <h2>Varianta 1: asociația cumpără sistemul</h2>
      <p>Asociația plătește de la început camerele, înregistratorul (NVR), hard disk-ul, cablurile și montajul. Suma depinde mult de numărul de camere și de cât cablu trebuie tras, așa că diferă de la un bloc la altul.</p>
      <ul>
        <li><strong>Avantaj:</strong> sistemul e al asociației din prima zi.</li>
        <li><strong>Dezavantaje:</strong> suma mare trebuie strânsă de la toți proprietarii deodată, iar după garanție reparațiile, camerele furate sau vandalizate și hard disk-urile defecte se plătesc separat. De multe ori nimeni nu verifică dacă sistemul chiar înregistrează.</li>
      </ul>

      <h2>Varianta 2: abonament lunar, fără investiție</h2>
      <p>Asociația nu plătește nimic la început. Furnizorul montează sistemul și îl întreține, iar asociația plătește o sumă fixă pe lună, pe durata contractului.</p>
      <h3>Cum se calculează prețul la SUPRAVEGHERE24h</h3>
      <table>
        <tr><th>Ce include</th><th>Preț pe lună</th></tr>
        <tr><td>Pachetul de bază: primele 3 camere (interior sau exterior), înregistratorul video, montajul</td><td>189 lei</td></tr>
        <tr><td>Fiecare cameră în plus (interior sau exterior)</td><td>+50 lei</td></tr>
        <tr><td>Fiecare cameră montată în lift</td><td>+150 lei</td></tr>
      </table>
      <p>Prețurile sunt finale (firma nu este plătitoare de TVA). Contractul este pe 48 de luni, montajul e gratuit, iar mentenanța, service-ul și garanția sunt incluse pe toată durata contractului, inclusiv la furt și vandalism. La final, echipamentele rămân ale asociației.</p>

      <h3>Exemple</h3>
      <table>
        <tr><th>Bloc</th><th>Camere</th><th>Preț pe lună</th><th>Pe apartament</th></tr>
        <tr><td>1 scară, 40 de apartamente</td><td>3 (intrare, casa scării, exterior)</td><td>189 lei</td><td>≈ 4,7 lei</td></tr>
        <tr><td>2 scări, 80 de apartamente</td><td>6, plus 2 în lifturi</td><td>189 + 3 × 50 + 2 × 150 = 639 lei</td><td>≈ 8 lei</td></tr>
        <tr><td>4 scări, 160 de apartamente</td><td>10</td><td>189 + 7 × 50 = 539 lei</td><td>≈ 3,4 lei</td></tr>
      </table>
      <p>Prețul exact pentru blocul vostru îl aflați în <a href="calculator-pret.html">calculator</a>, în mai puțin de un minut, și primiți oferta pe e-mail.</p>

      <h2>Ce influențează prețul</h2>
      <ul>
        <li><strong>Numărul de camere</strong>: câte intrări, scări, parcări și lifturi vreți supravegheate.</li>
        <li><strong>Camerele din lift</strong>: necesită echipamente și montaj speciale, de aceea costă mai mult.</li>
        <li><strong>Calitatea imaginii</strong>: folosim camere de cel puțin 4 MP, pentru imagini clare și ziua, și noaptea.</li>
        <li><strong>Cât timp se păstrează înregistrările</strong>: legea recomandă oricum cel mult 30 de zile, deci nu e nevoie de stocare foarte mare.</li>
      </ul>

      <h2>Ce să verificați înainte să semnați</h2>
      <ol>
        <li>Firma are licență de la Poliția Română pentru montajul sistemelor de supraveghere.</li>
        <li>Prețul lunar e fix pe toată durata contractului și nu există costuri ascunse.</li>
        <li>Garanția acoperă și furtul sau vandalizarea camerelor.</li>
        <li>Cineva verifică permanent că sistemul înregistrează (la noi, platforma de monitorizare verifică non-stop și ne anunță dacă o cameră nu mai merge).</li>
        <li>Ce se întâmplă cu echipamentele la finalul contractului.</li>
      </ol>
      <p>Înainte de semnare e nevoie de hotărârea adunării generale; pașii sunt în ghidul <a href="ghid-hotarare-aga-camere.html">Hotărârea AGA pentru camere de supraveghere</a>.</p>
{CTA}      <p class="s24-note">Prețurile sunt cele din calculatorul SUPRAVEGHERE24h la 18 noiembrie 2026 și se pot modifica; oferta primită pe e-mail este cea valabilă.</p>
    </div>
  </section>
'''

ARTS = [
  ('ghid-camere-supraveghere-bloc-legal', 'Camere de supraveghere în bloc: ce spune legea (2026) – SUPRAVEGHERE24h',
   'Este legal să montezi camere de supraveghere în bloc? Hotărârea adunării generale, GDPR, panouri de informare, cât se păstrează imaginile și cine are acces.',
   'GHID PENTRU ASOCIAȚII', 'Camere de supraveghere în bloc: ce spune legea',
   'Ce trebuie să facă asociația de proprietari ca supravegherea video din spațiile comune să fie legală: hotărârea adunării generale, GDPR, informarea locatarilor și păstrarea imaginilor.', A1,
   'Este legal să montezi camere în bloc? Ce spune Legea 196/2018, GDPR și ce riscă asociația.'),
  ('ghid-hotarare-aga-camere', 'Hotărârea AGA pentru camere de supraveghere: pași și model – SUPRAVEGHERE24h',
   'Cum se aprobă montarea camerelor de supraveghere în bloc: convocarea adunării generale, cvorumul, votul, procesul-verbal și un model orientativ de hotărâre.',
   'GHID PENTRU ASOCIAȚII', 'Hotărârea AGA pentru camere de supraveghere',
   'Pașii prin care adunarea generală aprobă montarea camerelor în bloc, de la ofertă la procesul-verbal, plus un model orientativ de hotărâre.', A2,
   'Convocarea adunării, cvorumul, votul și un model de hotărâre gata de completat.'),
  ('ghid-cost-supraveghere-video-bloc', 'Cât costă supravegherea video la bloc în 2026 – SUPRAVEGHERE24h',
   'Cât costă camerele de supraveghere pentru un bloc: investiție sau abonament lunar, de la 189 lei pe lună pentru tot blocul, cu exemple de calcul pe apartament.',
   'GHID PENTRU ASOCIAȚII', 'Cât costă supravegherea video la bloc',
   'Investiție sau abonament lunar? Cum se calculează prețul, exemple pe apartament și ce să verificați înainte să semnați.', A3,
   'Investiție sau abonament, prețuri de la 189 lei/lună și exemple pe apartament.'),
]
for slug, title, desc, pill, h1, lead, body, _ in ARTS:
    page(slug, title, desc, pill, h1, lead, body)

cards = ''.join(f'        <a class="s24-gcard" href="{slug}.html"><h3>{h1}</h3><p>{short}</p><span>Citește ghidul →</span></a>\n' for slug, _, _, _, h1, _, _, short in ARTS)
IDX = f'''  <section class="s24-base s24-art" style="background:#F5F7FA">
    <div class="s24-wrap" style="max-width:1080px">
      <div class="s24-gcards">
{cards}      </div>
    </div>
  </section>
'''
page('ghiduri', 'Ghiduri pentru asociații de proprietari – supraveghere video la bloc | SUPRAVEGHERE24h',
     'Ghiduri gratuite pentru administratori și președinți de asociații: ce spune legea despre camerele din bloc, hotărârea AGA și cât costă supravegherea video.',
     'GHIDURI', 'Ghiduri pentru asociații de proprietari',
     'Răspunsuri clare la întrebările pe care ni le pun cel mai des administratorii și președinții de asociații despre supravegherea video la bloc.', IDX, kind='index')

# link „Ghiduri” în subsol (după „Firme și case”) pe toate paginile
LINK = '<a href="ghiduri.html" class="s24-flink">Ghiduri</a><span class="s24-fsep">·</span>'
A = '<a href="supraveghere-video-firme.html" class="s24-flink">Firme și case</a><span class="s24-fsep">·</span>'
n = 0
for f in sorted(os.listdir(ROOT)):
    if not f.endswith('.html') or f == '404.html': continue
    p = os.path.join(ROOT, f); t = open(p).read()
    if 'href="ghiduri.html" class="s24-flink"' in t or A not in t: continue
    t = t.replace(A, A + '\n          ' + LINK, 1); open(p, 'w').write(t); n += 1

sm = os.path.join(ROOT, 'sitemap.xml'); x = open(sm).read()
for slug in ['ghiduri'] + [a[0] for a in ARTS]:
    if f'/{slug}<' not in x:
        x = x.replace('</urlset>', f'  <url><loc>https://supraveghere24h.ro/{slug}</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>')
open(sm, 'w').write(x)
print('4 pagini create; link „Ghiduri” în subsol pe', n, 'pagini')
