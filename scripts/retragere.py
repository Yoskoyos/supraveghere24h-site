#!/usr/bin/env python3
# Funcția online de retragere din contract (art. 11^1 OUG 34/2014) + anularea comenzii + rolul vânzătorului în Termeni.
# Re-rulabil: creează retragere.html, pune linkul „Retragere din contract” în subsol, completează Termeni și Livrare și retur.
import re, glob, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
API = 'https://proxy.supraveghere24h.ro'
src = open('livrare-si-retur.html', encoding='utf-8').read()

FORM = r'''  <section class="s24-base s24-pol" id="s24-rtr">
    <div class="s24-pol-w">
      <h1 class="s24-pol-h">Retragere din contract sau anularea comenzii</h1>
      <p class="s24-pol-d">Pentru produsele cumpărate din magazinul online supraveghere24h.ro</p>
      <p class="s24-pol-t">Dacă ai cumpărat ca persoană fizică, te poți retrage din contract în 14 zile de la primirea produselor, fără să justifici decizia (OUG nr. 34/2014). O comandă care nu a plecat încă o poți anula oricând, gratuit. Completează formularul de mai jos: îți trimitem imediat pe e-mail confirmarea, cu data și ora la care am primit declarația.</p>
      <form class="s24-rtr" id="s24-rtr-f" novalidate>
        <div class="s24-rtr-k"><label><input type="radio" name="kind" value="retragere" checked> <span><b>Mă retrag din contract</b><small>am primit produsele și vreau să le returnez</small></span></label>
          <label><input type="radio" name="kind" value="anulare"> <span><b>Anulez comanda</b><small>comanda nu a fost încă expediată</small></span></label></div>
        <div class="s24-rtr-g">
          <label>Nume și prenume *<input name="name" autocomplete="name" required maxlength="120"></label>
          <label>E-mail * <small>(aici primești confirmarea)</small><input name="email" type="email" autocomplete="email" required maxlength="160"></label>
          <label>Număr comandă *<input name="order" placeholder="ex. CMD-1004" required maxlength="20"></label>
          <label>Telefon<input name="phone" type="tel" autocomplete="tel" maxlength="40"></label>
          <label class="s24-rtr-w">Produsele <small>(lasă gol dacă e vorba de toată comanda)</small><input name="items" maxlength="600" placeholder="ex. 1 × cameră IPC-B140HA-LU"></label>
          <label class="s24-rtr-r">Data primirii produselor<input name="received" type="date"></label>
          <label class="s24-rtr-w">Motivul <small>(opțional, nu e obligatoriu)</small><textarea name="reason" rows="2" maxlength="1000"></textarea></label>
        </div>
        <input name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
        <button type="submit" class="s24-rtr-b">Retrage-te din contract aici</button>
        <div class="s24-rtr-e" role="alert"></div>
      </form>
      <div class="s24-rtr-c" id="s24-rtr-c" hidden></div>
      <div class="s24-rtr-ok" id="s24-rtr-ok" hidden></div>
      <p class="s24-pol-t" style="margin-top:22px">Poți folosi și orice altă declarație clară: un e-mail la <a href="mailto:contact@supraveghere24h.ro">contact@supraveghere24h.ro</a> sau o scrisoare la sediul nostru. Detalii despre returnarea produselor și rambursare: <a href="livrare-si-retur.html">Livrare, retur și garanție</a>.</p>
    </div>
  </section>
<style id="s24-rtr-css">
.s24-rtr{margin-top:18px;background:#fff;border:1px solid #E1E6EC;border-radius:16px;padding:20px;box-shadow:0 10px 30px -18px rgba(13,31,51,.25)}
.s24-rtr-k{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
.s24-rtr-k label{display:flex;gap:10px;align-items:flex-start;border:1.5px solid #E1E6EC;border-radius:12px;padding:12px;cursor:pointer}
.s24-rtr-k label:has(input:checked){border-color:#F5A100;background:#FFF8E8}.s24-rtr-k input{margin-top:4px;accent-color:#F5A100}
.s24-rtr-k b{display:block;color:#0D1F33}.s24-rtr-k small{color:#5B6B7C;font-size:13px}
.s24-rtr-g{display:grid;grid-template-columns:1fr 1fr;gap:12px}.s24-rtr-g label{display:flex;flex-direction:column;gap:6px;font-weight:700;font-size:14px;color:#0D1F33}
.s24-rtr-g small{font-weight:500;color:#5B6B7C}.s24-rtr-w{grid-column:1/-1}
.s24-rtr-g input,.s24-rtr-g textarea{font:inherit;font-weight:500;border:1.5px solid #DCE3EC;border-radius:10px;padding:11px 12px;background:#F7F9FC;width:100%;box-sizing:border-box}
.s24-rtr-g input:focus,.s24-rtr-g textarea:focus{outline:0;border-color:#0B5FB0;background:#fff}
.s24-rtr-b{margin-top:16px;width:100%;border:0;border-radius:12px;background:#F5A100;color:#0D1F33;font-weight:800;font-size:16px;font-family:inherit;padding:16px;cursor:pointer}
.s24-rtr-b:disabled{opacity:.6;cursor:default}.s24-rtr-e{color:#B42318;font-size:14px;margin-top:10px;min-height:1em}
.s24-rtr-c,.s24-rtr-ok{margin-top:18px;background:#fff;border:1px solid #E1E6EC;border-radius:16px;padding:20px}
.s24-rtr-c dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:12px 0}.s24-rtr-c dt{color:#5B6B7C}.s24-rtr-c dd{margin:0;font-weight:700;color:#0D1F33}
.s24-rtr-c .s24-rtr-b2{display:flex;gap:10px;flex-wrap:wrap}.s24-rtr-c button{flex:1;min-width:160px;border-radius:12px;padding:14px;font-weight:800;font-size:15px;font-family:inherit;cursor:pointer}
.s24-rtr-c .go{background:#F5A100;border:0;color:#0D1F33}.s24-rtr-c .back{background:#fff;border:1.5px solid #DCE3EC;color:#0D1F33}
.s24-rtr-ok{border-color:#ABEFC6;background:#ECFDF3}.s24-rtr-ok h2{margin:0 0 6px;font-size:20px;color:#067647}
@media(max-width:620px){.s24-rtr-k,.s24-rtr-g{grid-template-columns:1fr}.s24-rtr{padding:16px}}
</style>
<script id="s24-rtr-js">(function(){var API="''' + API + r'''",f=document.getElementById("s24-rtr-f");if(!f)return;var c=document.getElementById("s24-rtr-c"),ok=document.getElementById("s24-rtr-ok"),er=f.querySelector(".s24-rtr-e");
var q=new URLSearchParams(location.search);if(q.get("comanda"))f.order.value=q.get("comanda");if(q.get("email"))f.email.value=q.get("email");
function esc(s){return String(s).replace(/[&<>"]/g,function(x){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[x]})}
function data(){var d={};["name","email","order","phone","items","received","reason","website"].forEach(function(k){d[k]=(f[k].value||"").trim()});d.kind=f.querySelector("[name=kind]:checked").value;return d}
f.addEventListener("submit",function(e){e.preventDefault();er.textContent="";var d=data();
 if(!d.name||!d.email||!d.order){er.textContent="Completează numele, e-mailul și numărul comenzii.";return}
 if(!/^\S+@\S+\.\S+$/.test(d.email)){er.textContent="Adresa de e-mail nu pare corectă.";return}
 c.innerHTML="<b style=\"font-size:18px;color:#0D1F33\">Verifică și confirmă</b><dl><dt>Declarație</dt><dd>"+(d.kind==="anulare"?"Anulez comanda":"Mă retrag din contract")+"</dd><dt>Comanda</dt><dd>"+esc(d.order)+"</dd><dt>Nume</dt><dd>"+esc(d.name)+"</dd><dt>E-mail</dt><dd>"+esc(d.email)+"</dd>"+(d.items?"<dt>Produse</dt><dd>"+esc(d.items)+"</dd>":"<dt>Produse</dt><dd>toată comanda</dd>")+(d.received?"<dt>Primite la</dt><dd>"+esc(d.received)+"</dd>":"")+"</dl><div class=\"s24-rtr-b2\"><button type=\"button\" class=\"back\">Modifică</button><button type=\"button\" class=\"go\">Confirmă "+(d.kind==="anulare"?"anularea":"retragerea")+"</button></div><div class=\"s24-rtr-e\" role=\"alert\"></div>";
 f.hidden=true;c.hidden=false;c.scrollIntoView({behavior:"smooth",block:"center"});
 c.querySelector(".back").onclick=function(){c.hidden=true;f.hidden=false};
 c.querySelector(".go").onclick=function(){var b=this,e2=c.querySelector(".s24-rtr-e");b.disabled=true;b.textContent="Se trimite…";
  fetch(API+"/public/retragere",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)}).then(function(r){return r.json().then(function(j){return{st:r.status,j:j}})}).then(function(r){
   if(r.st!==200||!r.j.ok){b.disabled=false;b.textContent="Confirmă";e2.textContent=r.j.error||"Nu am putut trimite. Scrie-ne la contact@supraveghere24h.ro.";return}
   c.hidden=true;ok.hidden=false;ok.innerHTML="<h2>Am primit declarația ta</h2><p class=\"s24-pol-t\" style=\"margin:0\">Înregistrată la <b>"+esc(r.j.at)+"</b> (nr. "+esc(r.j.ref)+"). "+(r.j.mailed?"Ți-am trimis confirmarea pe e-mail, la <b>"+esc(d.email)+"</b>. ":"")+(d.kind==="anulare"?"Te anunțăm dacă comanda fusese deja expediată.":"Te contactăm cu instrucțiunile de retur. Banii îi returnăm în cel mult 14 zile.")+"</p>";ok.scrollIntoView({behavior:"smooth",block:"center"})
  }).catch(function(){b.disabled=false;b.textContent="Confirmă";e2.textContent="Fără conexiune? Încearcă din nou sau scrie-ne la contact@supraveghere24h.ro."})}
})})();</script>
'''
i = src.index('  <section class="s24-base s24-pol">'); j = src.index('</section>', i) + len('</section>\n')
page = src[:i] + FORM + src[j:]
page = page.replace('<title>Livrare, retur și garanție – SUPRAVEGHERE24h</title>', '<title>Retragere din contract – SUPRAVEGHERE24h</title>')
page = page.replace('https://supraveghere24h.ro/livrare-si-retur"', 'https://supraveghere24h.ro/retragere"')
page = page.replace('content="Livrare, retur și garanție – SUPRAVEGHERE24h"', 'content="Retragere din contract – SUPRAVEGHERE24h"')
page = re.sub(r'(<meta name="description" content=")[^"]*', r'\1Retrage-te online din contractul de cumpărare sau anulează o comandă din magazinul SUPRAVEGHERE24h. Confirmarea vine imediat pe e-mail.', page)
page = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\1Retragere din contract sau anularea comenzii, online.', page)
if '<meta name="robots"' not in page: page = page.replace('<head>', '<head>\n  <meta name="robots" content="noindex, follow">', 1)
open('retragere.html', 'w', encoding='utf-8').write(page)

LINK = '<a href="retragere.html" class="s24-flink">Retragere din contract</a><span class="s24-fsep">·</span>'
n = 0
for f in glob.glob('*.html'):
    s = open(f, encoding='utf-8').read()
    if 'class="s24-flink">Retragere din contract</a>' in s: continue
    m = re.search(r'(<a href="livrare-si-retur\.html"[^>]*class="s24-flink[^"]*"[^>]*>Livrare și retur</a><span class="s24-fsep">·</span>)', s) or \
        re.search(r'(<a href="termeni-si-conditii\.html"[^>]*>Termeni și condiții</a><span class="s24-fsep">·</span>)', s)
    if not m: continue
    s = s[:m.end()] + '\n          ' + LINK + s[m.end():]
    open(f, 'w', encoding='utf-8').write(s); n += 1
print('subsol:', n)

t = open('termeni-si-conditii.html', encoding='utf-8').read()
if 's24-rol' not in t:
    a = '<strong>Prețurile</strong> sunt afișate în lei'
    i = t.index(a); i = t.rfind('<p class="s24-pol-t">', 0, i)
    add = ('<p class="s24-pol-t" id="s24-rol"><strong>Cine vinde.</strong> Vânzătorul produselor din magazinul online și emitentul facturii este <strong>Yca Solutions SRL</strong>, CUI 45211628, Nr. Reg. Com. J2021019754409, cu sediul în Str. Aviator Mircea Petre nr. 10, Camera 1, Sector 1, București, telefon 0763 354 355, e-mail contact@supraveghere24h.ro. '
           'Acționăm ca <strong>comerciant (vânzător direct)</strong>: vindem în nume propriu produsele pe care le cumpărăm de la producători și distribuitori autorizați. Nu suntem o platformă de tip marketplace și nu intermediem vânzări între alți comercianți și clienți.</p>\n      ')
    t = t[:i] + add + t[i:]
if 's24-anul' not in t:
    a = 'Livrarea, dreptul de retragere în 14 zile'
    i = t.index(a); i = t.rfind('<p class="s24-pol-t">', 0, i)
    add = ('<p class="s24-pol-t" id="s24-anul"><strong>Anularea comenzii.</strong> Poți anula gratuit o comandă care nu a fost încă expediată: online, din pagina <a href="retragere.html">Retragere din contract / anularea comenzii</a>, telefonic la 0763 354 355 sau pe e-mail la contact@supraveghere24h.ro. Dacă ai plătit deja, îți returnăm întreaga sumă în cel mult 14 zile, prin aceeași metodă de plată. '
           'După expediere, anularea se face prin exercitarea dreptului de retragere. Putem anula și noi comanda în situațiile de mai sus (produs indisponibil, date incomplete, preț evident greșit), cu informarea ta și returnarea integrală a sumelor plătite.</p>\n      '
           '<p class="s24-pol-t"><strong>Retragerea online.</strong> Pe pagina <a href="retragere.html">Retragere din contract</a>, accesibilă din subsolul fiecărei pagini, îți poți exercita online dreptul de retragere (art. 11<sup>1</sup> din OUG nr. 34/2014); confirmarea primirii îți vine imediat pe e-mail, cu data și ora.</p>\n      ')
    t = t[:i] + add + t[i:]
open('termeni-si-conditii.html', 'w', encoding='utf-8').write(t)

l = open('livrare-si-retur.html', encoding='utf-8').read()
old = 'Pentru a te retrage, trimite-ne o declarație clară înainte de expirarea termenului: un e-mail la'
if 'retragere.html' not in l:
    l = l.replace(old, 'Pentru a te retrage, cel mai simplu este <strong><a href="retragere.html">formularul online de retragere</a></strong>: îți trimitem imediat pe e-mail confirmarea, cu data și ora. Poți trimite și o altă declarație clară înainte de expirarea termenului: un e-mail la', 1)
    i = l.index('<h2 class="s24-pol-s">2. Livrarea</h2>')
    l = l[:i] + ('<h2 class="s24-pol-s">Anularea comenzii</h2>\n      <p class="s24-pol-t">O comandă care nu a fost încă expediată o poți anula gratuit, oricând: <a href="retragere.html">online</a>, telefonic la 0763 354 355 sau pe e-mail. Dacă ai plătit deja, îți returnăm întreaga sumă în cel mult 14 zile, prin aceeași metodă de plată. După expediere se aplică dreptul de retragere de mai jos.</p>\n      ') + l[i:]
open('livrare-si-retur.html', 'w', encoding='utf-8').write(l)
print('ok')
