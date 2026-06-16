new_tab("https://www.hotfrog.de/")
wait_for_load()
# Alle Links/Buttons mit "Unternehmen" oder "Fügen"
print("MATCH:", js(
  "JSON.stringify(Array.from(document.querySelectorAll('a,button')).map(function(a){"
  "return {t:(a.innerText||'').trim().slice(0,40), href:(a.href||''), tag:a.tagName};})"
  ".filter(function(x){return /unternehmen|f.gen|hinzu|eintrag/i.test(x.t);}).slice(0,12))"
))
print("SHOT:", capture_screenshot())