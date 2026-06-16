ensure_real_tab()
# reCAPTCHA-Anchor-iframe finden
loc = js("""(function(){
  var f=Array.from(document.querySelectorAll('iframe')).find(function(x){return /recaptcha\\/api2\\/anchor|recaptcha.*anchor/i.test(x.src||'');});
  if(!f) return JSON.stringify({f:false});
  var r=f.getBoundingClientRect();
  return JSON.stringify({f:true, left:Math.round(r.left), top:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)});
})()""")
print("RECAPTCHA-IFRAME:", loc)
import json
d=json.loads(loc)
if d.get("f"):
    # Checkbox sitzt links (~30px rein), vertikal mittig
    cx = d["left"] + 30
    cy = d["top"] + d["h"]//2
    print("Klicke Checkbox @", cx, cy)
    click_at_xy(cx, cy)
    js("new Promise(function(r){setTimeout(r,3000);})")
    print("SHOT:", capture_screenshot())
    # Submit-Button suchen
    print("BTNS:", js("JSON.stringify(Array.from(document.querySelectorAll('button,input[type=submit],a')).map(function(b){return (b.innerText||b.value||'').trim();}).filter(function(t){return t && /speich|absend|submit|weiter|next|fertig|erstell|hinzu|continue|save/i.test(t);}).slice(0,10))"))