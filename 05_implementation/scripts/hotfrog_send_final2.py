ensure_real_tab()
import json
# 1) reCAPTCHA in den Viewport scrollen, dann frische Koordinaten holen + klicken
loc = js("""(function(){
  var f=Array.from(document.querySelectorAll('iframe')).find(function(x){return /recaptcha.*anchor/i.test(x.src||'');});
  if(!f)return JSON.stringify({f:false});
  f.scrollIntoView({block:'center'});
  var r=f.getBoundingClientRect();
  return JSON.stringify({f:true,x:Math.round(r.left)+30,y:Math.round(r.top+r.height/2)});
})()""")
print("RECAP:", loc)
d=json.loads(loc)
if d.get("f"): click_at_xy(d["x"], d["y"])
js("new Promise(function(r){setTimeout(r,2500);})")
tok = js("(function(){var t=document.querySelector('textarea[name=g-recaptcha-response]');return t&&t.value?t.value.length:0;})()")
print("TOKEN:", tok)
if tok and int(tok)>0:
    # 2) Button in Viewport scrollen, frische Koordinaten, trusted Klick
    bloc = js("""(function(){
      var b=Array.from(document.querySelectorAll('button')).find(function(x){return (x.innerText||'').trim()==='Senden';});
      if(!b)return JSON.stringify({f:false});
      b.scrollIntoView({block:'center'});
      var r=b.getBoundingClientRect();
      return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)});
    })()""")
    print("BTN:", bloc)
    b=json.loads(bloc)
    if b.get("f"):
        click_at_xy(b["x"], b["y"])
        print("KLICK gesetzt")