new_tab("https://www.yalwa.de/")
wait_for_load()
js("new Promise(function(r){setTimeout(r,1500);})")
print("URL:", page_info().get("url"))
print("TITLE:", js("document.title"))
print("ADD-LINKS:", js(
  "JSON.stringify(Array.from(document.querySelectorAll('a')).map(function(a){return (a.innerText||'').trim()+' || '+a.href;})"
  ".filter(function(x){return /eintrag|hinzu|kostenlos|firma|unternehmen|inseri|anzeige|gewerbe/i.test(x);}).slice(0,15))"
))
print("SHOT:", capture_screenshot())