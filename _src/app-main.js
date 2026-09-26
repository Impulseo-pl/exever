(function(){
  /* menu na telefonie */
  var btn=document.querySelector('.menu-btn'),menu=document.getElementById('menu');
  if(btn&&menu){
    btn.addEventListener('click',function(){var o=menu.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');btn.textContent=o?'Zamknij':'Menu';});
    menu.addEventListener('click',function(e){if(e.target.tagName==='A'){menu.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.textContent='Menu';}});
  }

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
