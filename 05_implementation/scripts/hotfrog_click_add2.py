new_tab("https://www.hotfrog.de/")
wait_for_load()
info = js(
  "(function(){var as=Array.from(document.querySelectorAll('a'));"
  "var hits=as.map(function(a){var r=a.getBoundingClientRect();return {txt:(a.innerText||'').trim().slice(0,30),href:a.href,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),w:Math.round(r.width)};})"
  ".filter(function(o){return o.w>0 && o.y<120 && o.y>0;});"
  "return JSON.stringify(hits.slice(0,15));})()"
)
print("TOP-LINKS:", info)