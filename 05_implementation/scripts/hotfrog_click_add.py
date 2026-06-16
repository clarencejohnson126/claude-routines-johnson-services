new_tab("https://www.hotfrog.de/")
wait_for_load()
loc = js(
  "(function(){var els=Array.from(document.querySelectorAll('a,button,span,div,li'));"
  "var t=els.find(function(e){return /F.gen Sie Ihr Unternehmen/i.test((e.innerText||'').trim()) && (e.innerText||'').length<40;});"
  "if(!t) return JSON.stringify({found:false});"
  "var r=t.getBoundingClientRect();"
  "return JSON.stringify({found:true, x:Math.round(r.left+r.width/2), y:Math.round(r.top+r.height/2), tag:t.tagName, txt:t.innerText.trim(), href:t.href||t.closest('a')?(t.closest('a')||{}).href:''});})()"
)
print("LOC:", loc)
import json
d = json.loads(loc)
if d.get("found"):
    click_at_xy(d["x"], d["y"])
    wait_for_load()
    print("NACH KLICK URL:", page_info().get("url"))
    print("SHOT:", capture_screenshot())