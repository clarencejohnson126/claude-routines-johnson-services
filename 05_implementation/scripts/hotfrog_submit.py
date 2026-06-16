loc = js(
  "(function(){var b=Array.from(document.querySelectorAll('button,input[type=submit],a')).find(function(x){return /Erste Schritte|weiter|absenden|submit/i.test((x.innerText||x.value||'').trim());});"
  "if(!b) return JSON.stringify({found:false});var r=b.getBoundingClientRect();"
  "return JSON.stringify({found:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),txt:(b.innerText||b.value||'').trim()});})()"
)
print("BTN:", loc)
import json
d=json.loads(loc)
if d.get("found"):
    click_at_xy(d["x"], d["y"])
    js("new Promise(function(r){setTimeout(r,2500);})")
    print("URL:", page_info().get("url"))
    print("TEXT:", js("document.body.innerText.replace(/\\n+/g,' | ').slice(0,500)"))
    print("FIELDS-NEU:", js("JSON.stringify(Array.from(document.querySelectorAll('input,select,textarea')).map(function(e){return {name:e.name||e.id,type:e.type,ph:e.placeholder};}).filter(function(e){return e.type!=='hidden';}).slice(0,20))"))
    print("SHOT:", capture_screenshot())