ensure_real_tab()
new_tab("https://admin.hotfrog.de/login/register")
wait_for_load()
# kurze Wartezeit für SPA-Render
js("new Promise(function(r){setTimeout(r,1500);})")
n = js("document.querySelectorAll('input').length")
print("INPUT-COUNT:", n)
filled = js("""
(function(){
  function find(re){return Array.from(document.querySelectorAll('input')).find(function(i){return re.test((i.placeholder||'')+' '+(i.name||'')+' '+(i.id||''));});}
  var vor=find(/vorname|first/i), nach=find(/nachname|last/i), mail=find(/mail|email/i);
  function set(el,val){ if(!el) return false; el.focus(); el.value=val;
    el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true})); return true; }
  var r={vor:set(vor,'Clarence'), nach:set(nach,'Johnson'), mail:set(mail,'info@johnson-services.de')};
  r.values={vor:vor&&vor.value, nach:nach&&nach.value, mail:mail&&mail.value};
  return JSON.stringify(r);
})()
""")
print("FILLED:", filled)
print("SHOT:", capture_screenshot())