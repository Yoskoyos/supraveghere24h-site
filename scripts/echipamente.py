# Echipamentele folosite (din facturile furnizorului) → blocul de produse de pe paginile de echipamente. Idempotent.
# Ilustrațiile din images/ sunt desene simple; se pot înlocui cu poze reale păstrând numele fișierelor.
import os, re, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BULLET = dict(img='images/cam-hilook-bullet.svg', alt='Cameră IP bullet HiLook IPC-B140HA-LUC',
  h='Cameră IP exterior HiLook IPC-B140HA-LUC — 4 MP (2560 × 1440), Smart Hybrid Light, microfon',
  lead='Camera de bază pentru exteriorul blocului: parcare, intrări, loc de joacă, căi de acces.',
  li=['Rezoluție 4 MP (2560 × 1440)', 'Lentilă 2,8 mm, unghi larg de aproximativ 103°', 'Iluminare duală Smart Hybrid Light: infraroșu sau lumină albă, până la 20 m',
      'Imagine color noaptea când se aprinde lumina albă', 'Microfon încorporat', 'Detecție de mișcare 2.0, cu filtrare oameni', 'Compresie H.265+ (ocupă puțin pe hard disk)',
      'Protecție IP67 la apă și praf', 'Alimentare prin cablul de rețea (PoE)'],
  meta=[('Cod produs', 'IPC-B140HA-LUC'), ('Marcă', 'HiLook by Hikvision'), ('Tip', 'Bullet, exterior'), ('Garanție', 'Inclusă pe toată durata abonamentului')])
TURRET = dict(img='images/cam-hilook-turret.svg', alt='Cameră IP turret HiLook IPC-T240HA-LUC',
  h='Cameră IP turret HiLook IPC-T240HA-LUC — 4 MP (2560 × 1440), Smart Hybrid Light, microfon',
  lead='Camera compactă pentru interior: scări, holuri, lift, intrări. Rezistă și afară, sub streașină.',
  li=['Rezoluție 4 MP (2560 × 1440)', 'Lentilă 2,8 mm, unghi larg de aproximativ 104°', 'Iluminare duală Smart Hybrid Light: infraroșu sau lumină albă, până la 20 m',
      'Microfon încorporat', 'Detecție de mișcare 2.0, cu filtrare oameni', 'Compresie H.265+', 'Protecție IP67', 'Alimentare prin cablul de rețea (PoE)', 'Carcasă discretă, greu de rotit sau de acoperit'],
  meta=[('Cod produs', 'IPC-T240HA-LUC'), ('Marcă', 'HiLook by Hikvision'), ('Tip', 'Turret, interior / exterior'), ('Garanție', 'Inclusă pe toată durata abonamentului')])
KIT = dict(img='images/kit-hilook-8.svg', alt='Kit supraveghere 8 camere HiLook cu NVR',
  h='Sistem complet pentru bloc — 8 camere HiLook, NVR și rack',
  lead='Configurația tipică pe care o montăm la un bloc: 4 camere afară, 4 camere înăuntru, înregistrare locală, totul închis în rack.',
  li=['4 × cameră exterior HiLook IPC-B140HA-LUC (4 MP, 2560 × 1440, Smart Hybrid Light, microfon)', '4 × cameră interior HiLook IPC-T240HA-LUC (4 MP, 2560 × 1440, Smart Hybrid Light, microfon)',
      'Recorder NVR HiLook NVR-108MH-C(E), 8 canale, înregistrare 4K, H.265+, Motion Detection 2.0', 'Hard disk pentru înregistrare continuă (până la 8 TB)',
      'Rack metalic Safer SAF-WMA-6604, 4U, ușă din sticlă securizată, cu yală', 'Cablu, doze, pat de cablu, switch PoE și manoperă incluse'],
  meta=[('Camere', '8 (4 exterior + 4 interior)'), ('Recorder', 'HiLook NVR-108MH-C(E)'), ('Rack', 'Safer SAF-WMA-6604'), ('Garanție', 'Inclusă pe toată durata abonamentului')])

def card(p):
    lis = ''.join(f'\n                <li>{H.escape(x)}</li>' for x in p['li'])
    rows = ''.join(f'''
                  <tr>
                    <td class="s24-pd-k s24-pd-k">{H.escape(k)}</td>
                    <td class="s24-pd-v s24-pd-v">{H.escape(v)}</td>
                  </tr>''' for k, v in p['meta'])
    return f'''          <div class="s24-pd"><img src="{p['img']}" loading="lazy" alt="{H.escape(p['alt'])}" class="s24-pd-img" width="400" height="300">
            <div class="s24-pd-info">
              <h3 class="s24-pd-h">{H.escape(p['h'])}</h3>
              <p class="s24-pd-lead">{H.escape(p['lead'])}</p>
              <ul role="list" class="s24-pd-list">{lis}
              </ul>
              <table class="s24-pd-meta s24-pd-meta">
                <tbody>{rows}
                </tbody>
              </table>
              <a href="calculator-pret.html" class="s24-pd-cta">Calculează prețul</a>
              <p class="s24-pd-note">Echipamentele sunt incluse în abonamentul lunar, fără investiție inițială.</p>
            </div>
          </div>
'''
def block(h, p, items):
    return f'''<div id="camere-ip" class="s24-block">
          <h2 class="s24-block-h">{h}</h2>
          <p class="s24-block-p">{p}</p>
{''.join(card(x) for x in items)}        </div>'''

PAGES = {
  'echipamente.html': ('Ce montăm la blocuri', 'Folosim camere IP HiLook, Hikvision și Dahua. Acestea sunt modelele pe care le montăm cel mai des.', [BULLET, TURRET, KIT]),
  'camere-ip.html': ('Camere IP', 'Camerele pe care le montăm cel mai des, pentru exterior și interior.', [BULLET, TURRET]),
  'camere-ip-exterior.html': ('Camere IP exterior', 'Pentru parcare, intrări, loc de joacă și căi de acces.', [BULLET, TURRET]),
  'camere-ip-interior.html': ('Camere IP interior', 'Pentru scări, holuri, lift și intrări.', [TURRET]),
  'kit-uri-camere.html': ('Sistem complet pentru bloc', 'Tot ce intră într-un sistem montat de noi: camere, recorder, rack și instalare.', [KIT]),
}
INTRO = 'Camerele IP pe care le montăm: HiLook, Hikvision și Dahua, cu iluminare duală și microfon. Echipamentele sunt incluse în abonament, fără investiție inițială.'

def end_of_div(s, i):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group() == '<div' else -1
        if d == 0: return i + m.end()
    raise ValueError('div neînchis')

for f, (h, p, items) in PAGES.items():
    path = os.path.join(ROOT, f); s = open(path).read()
    i = s.index('<div id="camere-ip" class="s24-block">'); j = end_of_div(s, i)
    s = s[:i] + block(h, p, items) + s[j:]
    s = re.sub(r'<p class="s24-shop-p">[^<]*</p>', f'<p class="s24-shop-p">{INTRO}</p>', s, count=1)
    open(path, 'w').write(s)
print('echipamente actualizate pe', len(PAGES), 'pagini')
