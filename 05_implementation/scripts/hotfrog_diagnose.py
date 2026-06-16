ensure_real_tab()
js("window.scrollTo(0,0);")
# Sichtbare Validierungs-/Fehlermeldungen (auch rote Texte)
print("VALIDIERUNG:", js("""JSON.stringify(Array.from(document.querySelectorAll('*')).filter(function(e){
  var c=getComputedStyle(e); var t=(e.childElementCount===0?(e.innerText||''):'').trim();
  return t && t.length<80 && (c.color.indexOf('255, 0, 0')>-1 || c.color.indexOf('220, 53, 69')>-1 || /erforderlich|required|pflicht|bitte|ungültig|invalid|fehl/i.test(t));
}).map(function(e){return (e.innerText||'').trim().slice(0,60);}).filter(Boolean).slice(0,12))"""))
# Leere Pflichtfelder (mit *)
print("PFLICHTFELDER:", js("""JSON.stringify(Array.from(document.querySelectorAll('input,select,textarea')).filter(function(e){return e.required && !e.value && e.type!=='hidden';}).map(function(e){return (e.name||e.id||e.placeholder||'?');}).slice(0,15))"""))
# Alle sichtbaren Selects (Kategorie?)
print("SELECTS:", js("""JSON.stringify(Array.from(document.querySelectorAll('select')).map(function(s){return {name:s.name||s.id, val:s.value, opts:s.options.length};}).slice(0,8))"""))
print("SHOT:", capture_screenshot())