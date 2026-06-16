ensure_real_tab()
loc = js("(function(){var b=Array.from(document.querySelectorAll('button,input[type=submit],a')).find(function(x){return /Finde die Adresse|find address|weiter|next/i.test((x.innerText||x.value||''));});if(!b)return JSON.stringify({f:false});var r=b.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),txt:(b.innerText||b.value||'').trim()});})()")
print("BTN:", loc)
import json
d=json.loads(loc)
if d.get("f"):
    click_at_xy(d["x"], d["y"])
    js("new Promise(function(r){setTimeout(r,3500);})")
    print("URL:", page_info().get("url"))
    print("TEXT:", js("document.body.innerText.replace(/\\n+/g,' | ').slice(0,600)"))
    print("SHOT:", capture_screenshot())