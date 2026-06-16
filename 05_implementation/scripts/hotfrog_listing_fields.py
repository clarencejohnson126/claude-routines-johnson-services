ensure_real_tab()
print("URL:", page_info().get("url"))
print("INPUTS:", js(
  "JSON.stringify(Array.from(document.querySelectorAll('input,select,textarea')).map(function(e,i){"
  "var lab='';"
  "var pl=e.previousElementSibling; "
  "var p=e.closest('div'); if(p){var l=p.querySelector('label,span,strong'); if(l) lab=(l.innerText||'').trim();}"
  "return {i:i,name:e.name||e.id,type:e.type||e.tagName,lab:lab.slice(0,30)};})"
  ".filter(function(e){return e.type!=='hidden';}))"
))