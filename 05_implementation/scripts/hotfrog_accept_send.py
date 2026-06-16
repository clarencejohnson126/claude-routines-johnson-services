ensure_real_tab()
# 1) AGB-Checkbox (unchecked) anhaken
cb = js("""(function(){
  var boxes=Array.from(document.querySelectorAll('input[type=checkbox]'));
  var info=boxes.map(function(b){var p=b.closest('div')||b.parentElement;var t=p?(p.innerText||'').trim():'';return {checked:b.checked,txt:t.slice(0,40)};});
  var terms=boxes.find(function(b){var p=b.closest('div')||b.parentElement;var t=p?(p.innerText||''):'';return /Nutzungsbedingungen gelesen|akzeptiert|beiden Parteien/i.test(t);});
  if(terms && !terms.checked){terms.click();}
  return JSON.stringify({boxes:info, termsToggled: !!terms, termsChecked: terms?terms.checked:null});
})()""")
print("CHECKBOX:", cb)
# 2) Senden-Element per Text finden (beliebiges Tag)
loc = js("""(function(){
  var all=Array.from(document.querySelectorAll('button,input[type=submit],a,div,span'));
  var b=all.find(function(x){var t=(x.innerText||x.value||'').trim();return t==='Senden'||/^Senden$/i.test(t);});
  if(!b) return JSON.stringify({f:false});
  var r=b.getBoundingClientRect();
  return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),tag:b.tagName});
})()""")
print("SENDEN:", loc)
print("SHOT-VOR:", capture_screenshot())