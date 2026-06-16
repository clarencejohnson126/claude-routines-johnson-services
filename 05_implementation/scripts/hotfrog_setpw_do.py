import sys, secrets, string, datetime
SCRIPTS = "/Users/clarence/Desktop/AUTOMATED ADS/Agentic Johnson Services/05_implementation/scripts"
sys.path.insert(0, SCRIPTS)

# starkes Passwort generieren
alpha = string.ascii_letters + string.digits
pw = "Js" + "".join(secrets.choice(alpha) for _ in range(14)) + "!9"

# Felder per Placeholder befüllen (mit Retry für SPA-Render)
ok = js("""
(function(pw){
  var ins = Array.from(document.querySelectorAll('input')).filter(function(i){return i.type!=='hidden';});
  if(ins.length < 2) return JSON.stringify({ready:false, count:ins.length});
  function set(el,val){el.focus();el.value=val;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}
  set(ins[0], pw); set(ins[1], pw);
  return JSON.stringify({ready:true, v0:ins[0].value.length, v1:ins[1].value.length});
})(%r)
""" % pw)
print("FILL:", ok)

import json
d = json.loads(ok)
if d.get("ready"):
    # platform_accounts.txt aktualisieren (gitignored)
    line = "\n[Hotfrog.de / Central Index] %s\n  URL: https://admin.hotfrog.de/login\n  E-Mail: info@johnson-services.de\n  Passwort: %s\n" % (
        datetime.date(2026,6,15).isoformat(), pw)
    with open(SCRIPTS + "/platform_accounts.txt", "a") as f:
        f.write(line)
    # absenden
    loc = js("(function(){var b=Array.from(document.querySelectorAll('button,input[type=submit]')).find(function(x){return /festlegen|set password|submit|speich/i.test((x.innerText||x.value||''));});if(!b)return JSON.stringify({f:false});var r=b.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)});})()")
    print("BTN:", loc)
    b = json.loads(loc)
    if b.get("f"):
        click_at_xy(b["x"], b["y"])
        js("new Promise(function(r){setTimeout(r,3000);})")
        print("URL:", page_info().get("url"))
        print("TEXT:", js("document.body.innerText.replace(/\\n+/g,' | ').slice(0,400)"))
        print("SHOT:", capture_screenshot())
else:
    print("Felder nicht bereit, count:", d.get("count"))