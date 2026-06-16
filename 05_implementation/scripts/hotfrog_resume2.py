new_tab("https://admin.hotfrog.de/add/index-card/basic")
wait_for_load()
js("new Promise(function(r){setTimeout(r,2500);})")
print("URL:", page_info().get("url"))
print("TEXT:", js("document.body.innerText.replace(/\\n+/g,' | ').slice(0,400)"))
# Sind Felder vorbefüllt (Session erhalten)?
print("VALS:", js("JSON.stringify(Array.from(document.querySelectorAll('input')).filter(function(i){return i.type==='text';}).map(function(e){return e.value;}).filter(Boolean).slice(0,12))"))
print("SHOT:", capture_screenshot())