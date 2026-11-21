# „Monitor live” de pe prima pagină cu filmări reale (Pexels, licență liberă pentru uz comercial, fără atribuire obligatorie;
# prelucrate: tăiate, 480×300, 15 cadre/s, culori atenuate, zgomot de cameră). Înlocuiește desenele SVG din animatii.py.
# Re-rulabil: python3 scripts/monitor_video.py (animatii.py folosește și el MONITOR de aici).
# Surse: pexels.com/video/7702046 (scară), 9100884 (parcare subterană), 34779661 (lift), 40163470 (stradă noaptea).
import os
CAMS = [('CAM 1 · SCARĂ', 'cam1-scara'), ('CAM 2 · PARCARE', 'cam2-parcare'), ('CAM 3 · LIFT', 'cam3-lift'), ('CAM 4 · EXTERIOR', 'cam4-exterior')]
def tile(label, f):
    return (f'<div class="s24m-t"><video class="s24m-v" src="images/cctv/{f}.mp4" poster="images/cctv/{f}.jpg" muted loop playsinline autoplay preload="metadata" '
            f'disablepictureinpicture tabindex="-1"></video><span class="s24m-l">{label}</span><span class="s24m-r"><i></i>REC</span><span class="s24m-ts"></span></div>')
MONITOR = ('<!-- s24-mon --><div class="s24m" aria-hidden="true"><div class="s24m-top"><span class="s24m-live"><i></i>LIVE</span><span>Monitorizare bloc · 4 camere</span><span class="s24m-clock"></span></div>'
           '<div class="s24m-grid">' + ''.join(tile(l, f) for l, f in CAMS) + '</div>'
           '<div class="s24m-bot"><span><b>●</b> Toate camerele online</span><span>Înregistrare 24/7 · 21 de zile</span></div></div><!-- /s24-mon -->')
BLOCK = ('<!-- s24-monv --><style>.s24m-v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;pointer-events:none;background:#0F2236}'
         '.s24m-t::before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.35))}'
         '.s24m-t::after{z-index:1}.s24m-l,.s24m-r,.s24m-ts{z-index:2}</style>'
         '<script>(function(){var V=[].slice.call(document.querySelectorAll(".s24m-v"));if(!V.length)return;'
         'var rm=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;'
         'V.forEach(function(v,i){var off=function(){try{v.currentTime=(i*1.7)%Math.max(1,v.duration||8)}catch(e){}};if(v.readyState>0)off();else v.addEventListener("loadedmetadata",off,{once:true});if(rm){v.removeAttribute("autoplay");v.pause();}});'
         'if(rm||!("IntersectionObserver" in window))return;'
         'var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){});}else v.pause();});},{threshold:.1});'
         'V.forEach(function(v){io.observe(v);});'
         '})();</script><!-- /s24-monv -->\n')
if __name__ == '__main__':
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(ROOT, 'index.html'); s = open(p).read()
    i = s.find('<!-- s24-mon -->'); j = s.find('<!-- /s24-mon -->', i); assert i >= 0 and j > i
    s = s[:i] + MONITOR + s[j + len('<!-- /s24-mon -->'):]
    while '<!-- s24-monv -->' in s:
        a = s.find('<!-- s24-monv -->'); b = s.find('<!-- /s24-monv -->\n', a); s = s[:a] + s[b + len('<!-- /s24-monv -->\n'):]
    s = s.replace('</body>', BLOCK + '</body>', 1)
    open(p, 'w').write(s); print('monitor video pus pe index.html')
