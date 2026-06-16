ensure_real_tab()
# AGB-Checkbox anhaken
cb = js("""(function(){
  var boxes=Array.from(document.querySelectorAll('input[type=checkbox]'));
  var terms=boxes.find(function(b){var p=b.closest('div')||b.parentElement;var t=p?(p.innerText||''):'';return /Nutzungsbedingungen gelesen|akzeptiert|beiden Parteien/i.test(t);});
  if(terms && !terms.checked){terms.click();}
  return JSON.stringify({termsFound: !!terms, termsChecked: terms?terms.checked:null});
})()""")
print("AGB:", cb)
# Senden finden + klicken
loc = js("""(function(){
  var all=Array.from(document.querySelectorAll('button,input[type=submit],a,div,span'));
  var b=all.find(function(x){var t=(x.innerText||x.value||'').trim();return t==='Senden';});
  if(!b) return JSON.stringify({f:false});
  var r=b.getBoundingClientRect();
  return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)});
})()""")
print("SENDEN:", loc)
import json
d=json.loads(loc)
if d.get("f") and json.loads(cb).get("termsChecked"):
    click_at_xy(d["x"], d["y"])
print("geklickt (oder AGB fehlte)")