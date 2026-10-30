/* s24formresult: afișează mesajul de succes/eroare după ce serverul redirecționează înapoi (?trimis=1 / ?eroare=...) */
(function(){
  function run(){
    var q=new URLSearchParams(location.search), ok=q.get('trimis'), err=q.get('eroare');
    if(!ok && !err) return;
    var box=document.querySelector('.w-form'); if(!box) return;
    var form=box.querySelector('form'), done=box.querySelector('.w-form-done'), fail=box.querySelector('.w-form-fail');
    if(ok){ if(form) form.style.display='none'; if(done) done.style.display='block'; }
    else if(fail){ var t=fail.querySelector('div')||fail; if(err && err!=='1') t.textContent=err; fail.style.display='block'; }
    try{ (done&&ok?done:fail||box).scrollIntoView({block:'center'}); }catch(e){}
    try{ history.replaceState(null,'',location.pathname+location.hash); }catch(e){}
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
})();
