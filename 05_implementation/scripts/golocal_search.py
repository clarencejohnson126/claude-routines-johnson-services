new_tab("https://www.golocal.de/unternehmen/")
wait_for_load()
js("var ins=Array.from(document.querySelectorAll('input')); "
   "var n=ins.find(function(i){return /name|kategorie|branche/i.test(i.placeholder||'');}); "
   "var o=ins.find(function(i){return /plz|ort|adresse/i.test(i.placeholder||'');}); "
   "if(n){n.value='Johnson Services'; n.dispatchEvent(new Event('input',{bubbles:true}));} "
   "if(o){o.value='Mannheim'; o.dispatchEvent(new Event('input',{bubbles:true}));}")
js("var b=Array.from(document.querySelectorAll('button, input[type=submit]')).find(function(x){return /suchen/i.test((x.innerText||x.value||''));}); if(b){b.click();}")
wait_for_load()
print("URL:", page_info().get("url"))
print("TEXT:", js("document.body.innerText.replace(/\\n+/g,' | ').slice(0,700)"))
print("SHOT:", capture_screenshot())
