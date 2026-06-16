new_tab("https://admin.hotfrog.de/add/index-card")
wait_for_load()
# iframes?
print("IFRAMES:", js("Array.from(document.querySelectorAll('iframe')).map(function(f){return f.src;}).join(' || ') || 'keine'"))
# Registrier-Button/Link
loc = js(
  "(function(){var els=Array.from(document.querySelectorAll('a,button,div,span'));"
  "var t=els.find(function(e){var x=(e.innerText||'').trim();return /kein Konto|Hier anmelden|registr/i.test(x) && x.length<60;});"
  "if(!t) return JSON.stringify({found:false});"
  "var r=t.getBoundingClientRect();"
  "return JSON.stringify({found:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),txt:t.innerText.trim(),href:t.href||''});})()"
)
print("REG:", loc)
import json
d=json.loads(loc)
if d.get("found"):
    if d.get("href"):
        new_tab(d["href"]); wait_for_load()
    else:
        click_at_xy(d["x"], d["y"]); wait_for_load()
    print("URL:", page_info().get("url"))
    print("FIELDS:", js(
      "JSON.stringify(Array.from(document.querySelectorAll('input,select,textarea')).map(function(e){"
      "return {name:e.name||e.id, type:e.type||e.tagName, ph:e.placeholder||''};})"
      ".filter(function(e){return e.type!=='hidden';}).slice(0,30))"
    ))
    print("SHOT:", capture_screenshot())