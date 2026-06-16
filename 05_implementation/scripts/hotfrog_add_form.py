new_tab("https://www.hotfrog.de/add")
wait_for_load()
print("URL:", page_info().get("url"))
print("TITLE:", js("document.title"))
print("FIELDS:", js(
  "JSON.stringify(Array.from(document.querySelectorAll('input,select,textarea')).map(function(e){"
  "return {name:e.name||e.id, type:e.type||e.tagName, ph:e.placeholder||'', req:e.required};})"
  ".filter(function(e){return e.type!=='hidden';}).slice(0,30))"
))
print("BUTTONS:", js(
  "JSON.stringify(Array.from(document.querySelectorAll('button,input[type=submit]')).map(function(b){return (b.innerText||b.value||'').trim();}).filter(function(t){return t;}).slice(0,10))"
))
print("SHOT:", capture_screenshot())