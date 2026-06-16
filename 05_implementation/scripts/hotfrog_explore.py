new_tab("https://www.hotfrog.de/")
wait_for_load()
print("URL:", page_info().get("url"))
print("TITLE:", js("document.title"))
# Suche nach "Firma eintragen / hinzufügen / kostenlos"
print("ADD-LINKS:", js(
  "JSON.stringify(Array.from(document.querySelectorAll('a')).map(function(a){"
  "return (a.innerText||'').trim()+' || '+a.href;})"
  ".filter(function(x){return /eintrag|hinzu|firma|unternehmen|kostenlos|anmeld|registr|add|company|werben/i.test(x);}).slice(0,20))"
))
print("TEXT:", js("document.body.innerText.replace(/\\n+/g,' | ').slice(0,400)"))