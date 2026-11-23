# Meniul „Categorii” din magazin (grupe + subcategorii pe coloane), stil la finalul css/...webflow.css (marcaj s24-mega). Re-rulabil.
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CSS = '''/* s24-mega */
.s24x-tools{position:relative}
.s24x-r1{display:flex;align-items:center;gap:10px;min-width:0;flex:1 1 auto}.s24x-r1 .s24x-chips{min-width:0}
.s24x-catbtn[aria-expanded="true"]{background:#F5A100;color:#0D1F33}.s24x-catbtn svg{color:#F5A100}.s24x-catbtn[aria-expanded="true"] svg{color:#0D1F33}
.s24x-catbtn{display:inline-flex;align-items:center;gap:10px;flex-shrink:0;border:0;border-radius:999px;background:#0D1F33;color:#fff;font:700 14px/1 Manrope,Segoe UI,Arial,sans-serif;padding:11px 18px 11px 16px;cursor:pointer;min-height:44px}
.s24x-mega{display:grid;grid-template-columns:270px 1fr;background:#fff;border:1px solid #E1E6EC;border-radius:16px;box-shadow:0 30px 60px -28px rgba(13,31,51,.35);margin:10px 0 16px;overflow:hidden;min-height:300px}
.s24x-mega[hidden]{display:none}
.s24x-mg-l{background:#F7F9FC;border-right:1px solid #EEF1F5;padding:8px 0}
.s24x-mg-g{display:flex;align-items:center;gap:10px;width:100%;border:0;background:none;text-align:left;padding:12px 18px;font:600 14.5px/1.2 Manrope,Segoe UI,Arial,sans-serif;color:#14202E;cursor:pointer}
.s24x-mg-g span{width:22px;text-align:center;font-size:15px}.s24x-mg-g em{margin-left:auto;font-style:normal;font-size:12px;color:#8A96A8;font-weight:700}.s24x-mg-g b{color:#9AA6B4;font-size:18px;font-weight:400}
.s24x-mg-g:hover,.s24x-mg-g.on{background:#fff;color:#0B5FB0}.s24x-mg-g.on{box-shadow:inset 3px 0 0 #F5A100}
.s24x-mg-g.red,.s24x-mg-g.red:hover{color:#D92D20}
.s24x-mg-r{padding:20px 26px}.s24x-mg-h{font:800 18px/1.2 Manrope,Segoe UI,Arial,sans-serif;color:#0D1F33;margin:0 0 14px}
.s24x-mg-cols{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:18px 26px}
.s24x-mg-c{display:flex;flex-direction:column;gap:2px}
.s24x-mg-c a{color:#3C4A59;text-decoration:none;font-size:14.5px;padding:6px 0;line-height:1.3}.s24x-mg-c a:hover{color:#0B5FB0;text-decoration:underline}
.s24x-mg-c a small{color:#9AA6B4;font-size:12px;font-weight:600}
.s24x-mg-c a.s24x-mg-t{font-weight:800;color:#0D1F33;text-decoration:underline;text-underline-offset:3px;margin-bottom:4px}
@media (max-width:767px){
  .s24x-r1{flex-direction:column;align-items:stretch;width:100%}
  .s24x-catbtn{width:100%;justify-content:center}
  .s24x-mega{grid-template-columns:1fr;min-height:0}
  .s24x-mg-l{display:flex;overflow-x:auto;padding:6px;gap:4px;border-right:0;border-bottom:1px solid #EEF1F5;scrollbar-width:none}
  .s24x-mg-g{flex-shrink:0;width:auto;padding:10px 12px;border-radius:999px;white-space:nowrap}.s24x-mg-g em,.s24x-mg-g b{display:none}.s24x-mg-g.on{box-shadow:none;background:#0D1F33;color:#fff}
  .s24x-mg-r{padding:14px 16px}.s24x-mg-cols{grid-template-columns:1fr 1fr;gap:14px}
}
/* /s24-mega */
'''
p = 'css/supraveghere24h-ro.webflow.css'; s = open(p).read()
s = re.sub(r'/\* s24-mega \*/.*?/\* /s24-mega \*/\n?', '', s, flags=re.S)
open(p, 'w').write(s.rstrip('\n') + '\n' + CSS)
n = 0
for f in glob.glob('*.html'):
    h = open(f).read(); o = h
    h = re.sub(r'js/s24catalog\.js\?v=\d+', 'js/s24catalog.js?v=7', h)
    h = re.sub(r'(css/supraveghere24h-ro\.webflow\.css)(\?v=[\w.-]+)?"', r'\1?v=mega1"', h)
    if h != o: open(f, 'w').write(h); n += 1
print('meniu categorii; pagini actualizate:', n)
