ensure_real_tab()
js("var b=Array.from(document.querySelectorAll('div,span')).find(function(x){return (x.innerText||'').trim()==='Senden';}); if(b) b.scrollIntoView({block:'center'});")
# Fehlermeldungen / Pflichtfeld-Hinweise sammeln
print("ERRORS:", js("JSON.stringify(Array.from(document.querySelectorAll('.error,.invalid,[class*=error],[class*=danger],.help-block,.text-danger')).map(function(e){return (e.innerText||'').trim();}).filter(Boolean).slice(0,10))"))
# reCAPTCHA noch grün? (response-token vorhanden?)
print("RECAPTCHA-TOKEN:", js("(function(){var t=document.querySelector('textarea[name=g-recaptcha-response]');return t? (t.value? 'TOKEN-DA('+t.value.length+')':'LEER'):'kein-feld';})()"))
print("SHOT:", capture_screenshot())