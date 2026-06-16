ensure_real_tab()
import json
# 1) reCAPTCHA frisch
loc = js("""(function(){var f=Array.from(document.querySelectorAll('iframe')).find(function(x){return /recaptcha.*anchor/i.test(x.src||'');});if(!f)return JSON.stringify({f:false});var r=f.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left)+30,y:Math.round(r.top+r.height/2)});})()""")
d=json.loads(loc); print("RECAP:", loc)
if d.get("f"): click_at_xy(d["x"], d["y"])
js("new Promise(function(r){setTimeout(r,2500);})")
tok = js("(function(){var t=document.querySelector('textarea[name=g-recaptcha-response]');return t&&t.value?t.value.length:0;})()")
print("TOKEN:", tok)
# 2) echten <button> mittig per Koordinate (trusted)
if tok and int(tok)>0:
    bloc = js("""(function(){var b=Array.from(document.querySelectorAll('button')).find(function(x){return (x.innerText||'').trim()==='Senden';});if(!b)return JSON.stringify({f:false});b.scrollIntoView({block:'center'});var r=b.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),w:Math.round(r.width),h:Math.round(r.height)});})()""")
    print("BTN:", bloc)
    b=json.loads(bloc)
    if b.get("f"):
        click_at_xy(b["x"], b["y"])
        print("TRUSTED-KLICK auf Button")