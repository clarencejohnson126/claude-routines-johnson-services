ensure_real_tab()
res = js("""
(function(){
  function labelOf(el){
    var p=el.closest('div'); var best='';
    if(p){var l=p.querySelector('label'); if(l) best=(l.innerText||'').trim();
          if(!best){var prev=p.previousElementSibling; if(prev) best=(prev.innerText||'').trim();}}
    var prev=el.previousElementSibling; if(!best && prev) best=(prev.innerText||'').trim();
    return best;
  }
  function set(el,val){if(!el)return false;el.focus();el.value=val;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return true;}
  var ins=Array.from(document.querySelectorAll('input')).filter(function(i){return i.type==='text'||i.type==='tel'||i.type==='email'||i.type==='url'||i.type==='';});
  var phone=null,mail=null,web=null;
  ins.forEach(function(i){var L=labelOf(i).toLowerCase(); var ph=(i.placeholder||'').toLowerCase();
    if(!phone && /telefonnummer\*|^telefonnummer|^telefon/.test(L)) phone=i;
    if(!mail && (/e-mail|email/.test(L))) mail=i;
    if(!web && (/webadresse|website/.test(L) || /mysite/.test(ph))) web=i;
  });
  var r={};
  r.phone=set(phone,'+49 151 57731682');
  r.mail=set(mail,'info@johnson-services.de');
  r.web=set(web,'https://johnson-services.de');
  r.vals={phone:phone&&phone.value, mail:mail&&mail.value, web:web&&web.value};
  return JSON.stringify(r);
})()
""")
print("RESULT:", res)
print("SHOT:", capture_screenshot())