/* s24formresult: afișează mesajul de succes/eroare după ce serverul redirecționează înapoi (?trimis=1 / ?eroare=...) */
(function(){
  var CSS = '.w-form-done,.w-form-fail{background:transparent!important;padding:0!important;text-align:center}'
    + '.w-form.s24-sent{display:flex;flex-direction:column;justify-content:center;min-height:100%}'
    + '.s24-done{display:flex;flex-direction:column;align-items:center;gap:12px;padding:36px 20px;text-align:center}'
    + '.s24-done-ic{width:72px;height:72px;border-radius:50%;background:#E8F6EC;display:flex;align-items:center;justify-content:center;animation:s24pop .45s cubic-bezier(.2,1.4,.4,1) both}'
    + '.s24-done-ic svg{width:38px;height:38px;stroke:#16803C;stroke-width:3;fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:30;stroke-dashoffset:30;animation:s24draw .5s .25s ease forwards}'
    + '.s24-done h3{margin:6px 0 0;font-size:26px;line-height:1.2;color:#0D1F33;font-weight:800}'
    + '.s24-done p{margin:0;max-width:420px;color:#52606F;font-size:16px;line-height:1.55;font-weight:500}'
    + '.s24-done .s24-done-ph{margin-top:6px;font-size:15px;color:#52606F}.s24-done .s24-done-ph a{color:#0D1F33;font-weight:800;text-decoration:none}'
    + '.s24-done button{margin-top:10px;background:none;border:1.5px solid #0D1F33;color:#0D1F33;border-radius:10px;padding:11px 20px;font:700 14px/1 inherit;font-family:inherit;cursor:pointer}'
    + '.s24-done button:hover{background:#0D1F33;color:#fff}'
    + '@keyframes s24pop{from{transform:scale(.4);opacity:0}to{transform:scale(1);opacity:1}}@keyframes s24draw{to{stroke-dashoffset:0}}'
    + '@media(prefers-reduced-motion:reduce){.s24-done-ic,.s24-done-ic svg{animation:none;stroke-dashoffset:0}}';
  function run(){
    var q=new URLSearchParams(location.search), ok=q.get('trimis'), err=q.get('eroare');
    if(!ok && !err) return;
    var box=document.querySelector('.w-form'); if(!box) return;
    var st=document.createElement('style'); st.textContent=CSS; document.head.appendChild(st);
    var form=box.querySelector('form'), done=box.querySelector('.w-form-done'), fail=box.querySelector('.w-form-fail');
    if(ok){
      if(form) form.style.display='none';
      if(done){
        var orig=(done.textContent||'').replace(/\s+/g,' ').trim()||'Mulțumim! Am primit cererea ta și te contactăm în cel mai scurt timp, în zilele lucrătoare.';
        var esc=function(x){return x.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};
        var ttl=/e-?mail/i.test(orig)&&/ofert/i.test(orig)?'Oferta a fost trimisă!':'Mesaj trimis!';
        done.innerHTML='<div class="s24-done" role="status"><div class="s24-done-ic"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>'
          + '<h3>'+ttl+'</h3><p>'+esc(orig)+'</p>'
          + '<div class="s24-done-ph">Grabă? Sună-ne la <a href="tel:+40763354355">0763 354 355</a></div>'
          + '<button type="button">'+(ttl==='Mesaj trimis!'?'Trimite alt mesaj':'Calculează din nou')+'</button></div>';
        done.style.display='block'; box.classList.add('s24-sent');
        done.querySelector('button').addEventListener('click',function(){ done.style.display='none'; box.classList.remove('s24-sent'); if(form){ form.reset(); form.style.display=''; } });
      }
    }
    else if(fail){ var t=fail.querySelector('div')||fail; if(err && err!=='1') t.textContent=err; fail.style.display='block'; }
    try{ (done&&ok?done:fail||box).scrollIntoView({block:'center'}); }catch(e){}
    try{ history.replaceState(null,'',location.pathname+location.hash); }catch(e){}
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
})();
