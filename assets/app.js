(function(){
  /* menu na telefonie */
  var btn=document.querySelector('.menu-btn'),menu=document.getElementById('menu');
  if(btn&&menu){
    btn.addEventListener('click',function(){var o=menu.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');btn.textContent=o?'Zamknij':'Menu';});
    menu.addEventListener('click',function(e){if(e.target.tagName==='A'){menu.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.textContent='Menu';}});
  }

  /* łagodne pojawianie się sekcji przy przewijaniu */
  var rv=document.querySelectorAll('[data-rv]');
  if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(el){io.observe(el);});
  }else{rv.forEach(function(el){el.classList.add('in');});}

  /* przekrój ściany: numer na rysunku <-> opis warstwy */
  var wall=document.querySelector('[data-wall]');
  if(wall){
    var pins=wall.querySelectorAll('.pin'),items=wall.querySelectorAll('.layers li');
    var mark=function(i){for(var k=0;k<items.length;k++){items[k].classList.toggle('on',k===i);if(pins[k])pins[k].classList.toggle('on',k===i);}};
    Array.prototype.forEach.call(items,function(li,i){li.addEventListener('mouseenter',function(){mark(i);});li.addEventListener('click',function(){mark(i);});});
    Array.prototype.forEach.call(pins,function(p,i){p.addEventListener('mouseenter',function(){mark(i);});p.addEventListener('click',function(){mark(i);});});
    wall.addEventListener('mouseleave',function(){mark(-1);});
  }

  /* filtr realizacji */
  var filters=document.querySelector('.filters');
  if(filters){
    filters.addEventListener('click',function(e){
      var b=e.target.closest('button');if(!b)return;
      var f=b.getAttribute('data-f');
      filters.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
      document.querySelectorAll('.gallery a').forEach(function(a){a.hidden=!(f==='all'||a.getAttribute('data-k')===f);});
    });
  }

  /* podgląd zdjęć */
  var links=document.querySelectorAll('.gallery a');
  if(links.length){
    var lb=document.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Podgląd zdjęcia');
    lb.innerHTML='<img alt=""><p></p><button class="x" type="button" aria-label="Zamknij">×</button><button class="prev" type="button" aria-label="Poprzednie">‹</button><button class="next" type="button" aria-label="Następne">›</button>';
    document.body.appendChild(lb);
    var img=lb.querySelector('img'),cap=lb.querySelector('p'),cur=0,last=null,vis=[];
    var show=function(i){cur=(i+vis.length)%vis.length;var a=vis[cur];img.src=a.getAttribute('href');img.alt=a.querySelector('img').alt;cap.textContent=a.getAttribute('data-cap')||'';};
    var close=function(){lb.classList.remove('open');document.body.style.overflow='';if(last)last.focus();};
    Array.prototype.forEach.call(links,function(a){a.addEventListener('click',function(e){e.preventDefault();last=a;vis=Array.prototype.filter.call(links,function(x){return !x.hidden;});show(vis.indexOf(a));lb.classList.add('open');document.body.style.overflow='hidden';lb.querySelector('.x').focus();});});
    lb.querySelector('.x').addEventListener('click',close);
    lb.querySelector('.prev').addEventListener('click',function(){show(cur-1);});
    lb.querySelector('.next').addEventListener('click',function(){show(cur+1);});
    lb.addEventListener('click',function(e){if(e.target===lb)close();});
    document.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1);});
  }

  /* formularz zapytania (demo – nic nie wysyła) */
  var q=document.getElementById('quote');
  if(q){
    var t=new URLSearchParams(location.search).get('temat');
    if(t){var r=q.querySelector('input[name=temat][value="'+t+'"]');if(r)r.checked=true;}
    q.addEventListener('submit',function(e){
      e.preventDefault();
      var msg=q.querySelector('.form-msg');msg.className='form-msg err';
      if(!q.imie.value.trim()){msg.textContent='Wpisz imię i nazwisko.';q.imie.focus();return;}
      if(q.tel.value.replace(/\D/g,'').length<9){msg.textContent='Sprawdź numer telefonu.';q.tel.focus();return;}
      if(!q.zgoda.checked){msg.textContent='Zaznacz zgodę na kontakt.';return;}
      msg.className='form-msg ok';msg.textContent='Dziękujemy. Oddzwonimy w godzinach pracy. (Wersja demonstracyjna – formularz nie wysyła jeszcze wiadomości).';
      q.reset();
    });
  }
})();

/* licznik otwarć dema – nie usuwać */
(function(){try{if(String(location.protocol).indexOf('http')!==0)return;try{if(/[?&#]team=1/.test(location.search+location.hash)){localStorage.setItem('nb_team','1');}}catch(e){}try{if(localStorage.getItem('nb_team')==='1')return;}catch(e){}if((document.referrer||'').indexOf('crm-newbeginning')>-1)return;try{if(navigator.webdriver)return;}catch(e){}try{if(/^https?:\/\/(kris20032|impulseo-pl)\.github\.io\/?$/i.test(document.referrer||''))return;}catch(e){}if(sessionStorage.getItem('_dv'))return;sessionStorage.setItem('_dv','1');var seg=(location.pathname.split('/').filter(Boolean)[0])||'';var base=location.origin+(seg?('/'+seg):'');var ua='';try{ua=(navigator.userAgent||'').slice(0,300);}catch(e){}var EP='https://zngfubfinbojfgaxdrbf.supabase.co/rest/v1/demo_views';var KEY='sb_publishable_MWwoyGlSCWnJ4awtOPF0ow_ZVS0Y8qK';function send(g){try{fetch(EP,{method:'POST',keepalive:true,headers:{'Content-Type':'application/json','apikey':KEY,'Authorization':'Bearer '+KEY,'Prefer':'return=minimal'},body:JSON.stringify({demo_url:base,page:location.pathname,referrer:(document.referrer||null),user_agent:(ua||null),ip:(g&&g.ip)||null,country:(g&&g.cc)||null,city:(g&&g.city)||null})}).catch(function(){});}catch(e){}}var done=false;function once(g){if(done)return;done=true;send(g);}try{var t=setTimeout(function(){once(null);},1500);fetch('https://ipwho.is/?fields=ip,success,country_code,city',{cache:'no-store'}).then(function(r){return r.json();}).then(function(d){clearTimeout(t);once(d&&d.success!==false?{ip:d.ip,cc:d.country_code,city:d.city}:null);}).catch(function(){clearTimeout(t);once(null);});}catch(e){once(null);}}catch(e){}})();
