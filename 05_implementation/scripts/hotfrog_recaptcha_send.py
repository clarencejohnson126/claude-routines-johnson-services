ensure_real_tab()
import json
# 1) reCAPTCHA-Checkbox frisch klicken
loc = js("""(function(){
  var f=Array.from(document.querySelectorAll('iframe')).find(function(x){return /recaptcha.*anchor/i.test(x.src||'');});
  if(!f) return JSON.stringify({f:false});
  var r=f.getBoundingClientRect();
  return JSON.stringify({f:true, x:Math.round(r.left)+30, y:Math.round(r.top+r.height/2)});
})()""")
print("RECAP:", loc)
d=json.loads(loc)
if d.get("f"):
    click_at_xy(d["x"], d["y"])
# 2) kurz warten (unter Socket-Timeout)
js("new Promise(function(r){setTimeout(r,2500);})")
# 3) Token prüfen
tok = js("(function(){var t=document.querySelector('textarea[name=g-recaptcha-response]');return t&&t.value?t.value.length:0;})()")
print("TOKEN-LEN:", tok)
# 4) wenn Token da: Senden klicken
if tok and int(tok) > 0:
    sloc = js("""(function(){var b=Array.from(document.querySelectorAll('div,span,button,input')).find(function(x){return (x.innerText||x.value||'').trim()==='Senden';});if(!b)return JSON.stringify({f:false});b.scrollIntoView({block:'center'});var r=b.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)});})()""")
    print("SENDEN:", sloc)
    s=json.loads(sloc)
    if s.get("f"):
        click_at_xy(s["x"], s["y"])
        print("SENDEN GEKLICKT")
else:
    print("Kein Token — reCAPTCHA evtl. Challenge")
print("SHOT:", capture_screenshot())