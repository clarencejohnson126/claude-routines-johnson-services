new_tab("https://www.hotfrog.de/")
wait_for_load()
print("ALL-HREFS:", js(
  "JSON.stringify(Array.from(new Set(Array.from(document.querySelectorAll('a')).map(function(a){return a.href;})"
  ".filter(function(h){return /add|company|register|anmeld|eintrag|unternehmen|signup|join|claim|firm/i.test(h);}))).slice(0,25))"
))