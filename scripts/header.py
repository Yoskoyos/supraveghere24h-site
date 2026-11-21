# Antet nou pe toate paginile: bara de sus cu încredere (monitorizare non-stop · IGPR · nota Google), meniul cu „Servicii” ▾ și „Ghiduri”,
# telefonul lângă „Cere ofertă”, antet care rămâne sus la derulare. CSS la finalul css/...webflow.css (marcaj s24-hdr2), JS în js/s24navfx.js.
# Re-rulabil: python3 scripts/header.py
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PHONE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
SHIELD = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>'
CHEV = '<svg class="s24-chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

TOP = ('<div class="s24-wrap s24-top-in"><span class="s24-tbar">'
       '<span class="s24-ti"><i class="s24-live" aria-hidden="true"></i>Monitorizare non-stop</span>'
       f'<span class="s24-ti">{SHIELD}Acreditați IGPR</span>'
       '<a class="s24-ti s24-grate" id="s24-grate" href="https://g.page/r/CQV6InDh9bMwEBM/review" target="_blank" rel="noopener" hidden></a>'
       '</span><span class="s24-tr">Luni–Vineri 9:00–18:00 · '
       '<a href="tel:+40763354355" class="s24-toplink">0763 354 355</a><span class="s24-tmail"> · <a href="mailto:contact@supraveghere24h.ro" class="s24-toplink">contact@supraveghere24h.ro</a></span>'
       '</span></div>')

SERV = {'oferta-asociatii.html', 'supraveghere-video-firme.html', 'echipamente.html', 'camere-ip.html', 'camere-ip-exterior.html',
        'camere-ip-interior.html', 'kit-uri-camere.html', 'nvr-uri.html', 'stocare.html', 'accesorii.html', 'sistem-vechi.html'}
def nav(f):
    cur = lambda c: ' aria-current="page" class="s24-link w--current"' if c else ' class="s24-link"'
    isS = f in SERV or f.startswith('supraveghere-video-bloc-')
    it = lambda href, b, sub, on: f'<a href="{href}" class="s24-dd-i{" on" if on else ""}" role="menuitem"><b>{b}</b><span>{sub}</span></a>'
    return ('<nav class="s24-links">\n'
            f'          <div class="s24-dd"><a href="oferta-asociatii.html"{cur(isS).replace("s24-link", "s24-link s24-dd-t")} aria-haspopup="true" aria-expanded="false">Servicii{CHEV}</a>\n'
            '            <div class="s24-dd-m" role="menu">\n'
            f'              {it("oferta-asociatii.html", "Pentru asociații de proprietari", "Abonament fix, de la 189 lei/lună pe bloc", f == "oferta-asociatii.html")}\n'
            f'              {it("supraveghere-video-firme.html", "Pentru firme și case", "Sistem gândit pentru locația ta", f == "supraveghere-video-firme.html")}\n'
            f'              {it("echipamente.html", "Echipamente", "Camere, NVR-uri, stocare, accesorii", f in SERV and f not in ("oferta-asociatii.html", "supraveghere-video-firme.html"))}\n'
            '            </div></div>\n'
            f'          <a href="/#pasi" class="s24-link">Cum funcționează</a>\n'
            f'          <a href="calculator-pret.html"{cur(f == "calculator-pret.html")}>Calculator preț</a>\n'
            f'          <a href="despre-noi.html"{cur(f == "despre-noi.html")}>Despre noi</a>\n'
            f'          <a href="contact.html"{cur(f == "contact.html")}>Contact</a>\n'
            '        </nav>')

TEL = f'<a href="tel:+40763354355" class="s24-navtel" aria-label="Sună la 0763 354 355">{PHONE_SVG}<span><small>Sună acum</small><b>0763 354 355</b></span></a>\n        '

n = 0
for f in sorted(glob.glob('*.html')):
    s = open(f).read(); o = s
    if '<nav class="s24-links">' not in s: continue
    s = re.sub(r'<nav class="s24-links">.*?</nav>', lambda m: nav(f), s, count=1, flags=re.S)
    s = re.sub(r'<div class="s24-wrap s24-top-in">.*?</div>', TOP, s, count=1, flags=re.S)
    if 'class="s24-navtel"' not in s:
        s = re.sub(r'(</nav>\s*)(<a href="[^"]*" class="s24-btn s24-btn-a">Cere ofertă</a>)', lambda m: m.group(1) + TEL + m.group(2), s, count=1)
    assert 's24-navtel' in s and 's24-dd-m' in s and 's24-live' in s, f
    if s != o: open(f, 'w').write(s); n += 1

CSS = '''
/* s24-hdr2: antet — bara de încredere, meniu „Servicii”, telefon, antet lipit sus la derulare */
html { scroll-padding-top: 96px; }
.s24-header { position: sticky; top: 0; z-index: 900; }
.s24-header .s24-nav { transition: box-shadow .25s ease, background-color .25s ease; }
.s24-header.s24-scrolled .s24-nav { box-shadow: 0 8px 26px rgba(13,31,51,.10); background-color: rgba(255,255,255,.96); backdrop-filter: saturate(1.4) blur(8px); -webkit-backdrop-filter: saturate(1.4) blur(8px); }
.s24-nav-in { transition: padding .25s ease; }
.s24-header.s24-scrolled .s24-nav-in { padding-top: 12px; padding-bottom: 12px; }
.s24-top-in { align-items: center; gap: 16px; font-size: 13.5px; }
.s24-tbar { display: inline-flex; align-items: center; gap: 22px; flex-wrap: wrap; }
.s24-ti { display: inline-flex; align-items: center; gap: 7px; color: #DCE5EF; font-weight: 600; text-decoration: none; white-space: nowrap; }
.s24-ti svg { width: 15px; height: 15px; fill: none; stroke: #F5A100; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
a.s24-ti:hover { color: #fff; }
.s24-ti .s24-stars { color: #F5A100; letter-spacing: 1px; }
.s24-live { position: relative; width: 8px; height: 8px; border-radius: 50%; background: #22C55E; display: inline-block; }
.s24-live::after { content: ""; position: absolute; inset: -4px; border-radius: 50%; border: 2px solid #22C55E; opacity: 0; animation: s24Pulse 2s ease-out infinite; }
@keyframes s24Pulse { 0% { transform: scale(.5); opacity: .9; } 100% { transform: scale(1.6); opacity: 0; } }
.s24-tr { color: #B9C6D6; white-space: nowrap; }
.s24-tr a { color: #fff; text-decoration: none; }
@media screen and (max-width: 1100px) { .s24-tmail { display: none; } .s24-tr { font-size: 13px; } }
@media screen and (max-width: 991px) { .s24-tr { display: none; } .s24-top-in { justify-content: center; } }
/* Servicii ▾ */
.s24-dd { position: relative; display: inline-flex; }
.s24-chev { width: 15px; height: 15px; margin-left: 4px; vertical-align: -2px; fill: none; stroke: currentColor; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; transition: transform .25s ease; }
.s24-dd-m { position: absolute; top: calc(100% + 10px); left: 50%; min-width: 320px; background: #fff; border: 1px solid #E1E6EC; border-radius: 16px; padding: 8px; box-shadow: 0 22px 48px rgba(13,31,51,.16);
  opacity: 0; visibility: hidden; transform: translate(-50%, 8px); transition: opacity .2s ease, transform .2s ease, visibility .2s; z-index: 50; }
.s24-dd-m::before { content: ""; position: absolute; top: -12px; left: 0; right: 0; height: 12px; }
.s24-dd:hover .s24-dd-m, .s24-dd:focus-within .s24-dd-m, .s24-dd.s24-dd-open .s24-dd-m { opacity: 1; visibility: visible; transform: translate(-50%, 0); }
.s24-dd:hover .s24-chev, .s24-dd.s24-dd-open .s24-chev { transform: rotate(180deg); }
.s24-dd-i { display: block; padding: 12px 14px; border-radius: 12px; text-decoration: none; transition: background-color .15s ease; }
.s24-dd-i b { display: block; color: #0D1F33; font-family: Manrope, Segoe UI, Arial, sans-serif; font-size: 15px; font-weight: 700; }
.s24-dd-i span { display: block; color: #6B7785; font-size: 13.5px; margin-top: 2px; }
.s24-dd-i:hover, .s24-dd-i:focus-visible, .s24-dd-i.on { background: #FFF6E0; }
/* telefonul de lângă „Cere ofertă” */
.s24-navtel { display: inline-flex; align-items: center; gap: 10px; color: #0D1F33; text-decoration: none; flex-shrink: 0; }
.s24-navtel svg { width: 20px; height: 20px; padding: 10px; box-sizing: content-box; border-radius: 50%; background: #EAF4FB; fill: none; stroke: #1B7AB3; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; transition: transform .2s ease, background-color .2s ease; }
.s24-navtel:hover svg { transform: rotate(-12deg) scale(1.06); background: #D9ECF8; }
.s24-navtel span { display: flex; flex-direction: column; line-height: 1.15; }
.s24-navtel small { color: #6B7785; font-size: 12px; font-weight: 600; }
.s24-navtel b { font-family: Manrope, Segoe UI, Arial, sans-serif; font-size: 16px; font-weight: 800; white-space: nowrap; }
@media screen and (min-width: 992px) and (max-width: 1279px) { .s24-navtel span { display: none; } }
@media screen and (max-width: 991px) { .s24-navtel { display: none; } }
/* telefon (meniul cu 3 liniuțe): Servicii devine listă simplă */
@media screen and (max-width: 767px) {
  .s24-nav-in > .s24-links.s24-open .s24-dd { display: contents; }
  .s24-nav-in > .s24-links.s24-open .s24-dd-t { display: none !important; }
  .s24-nav-in > .s24-links.s24-open .s24-dd-m { display: contents; visibility: visible; opacity: 1; transform: none; }
  .s24-nav-in > .s24-links.s24-open .s24-dd-i { padding: 12px 4px; border-radius: 0; border-bottom: 1px solid #F0F3F6; }
  .s24-nav-in > .s24-links.s24-open .s24-dd-i span { display: none; }
  .s24-nav-in > .s24-links.s24-open .s24-dd-i b { font-size: 17px; font-weight: 600; }
  .s24-nav-in > .s24-links.s24-open .s24-dd-i.on { background: none; }
  .s24-header.s24-scrolled .s24-nav-in { padding-top: 10px; padding-bottom: 10px; }
}
@media (prefers-reduced-motion: reduce) { .s24-live::after { animation: none; } .s24-dd-m, .s24-chev, .s24-nav-in, .s24-navtel svg { transition: none !important; } }
'''
p = 'css/supraveghere24h-ro.webflow.css'; css = open(p).read()
if 's24-hdr2' not in css: open(p, 'a').write(CSS)
print('antet nou pe', n, 'pagini')
