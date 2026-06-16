ensure_real_tab()
res = js("""(function(){
  var btn=Array.from(document.querySelectorAll('button')).find(function(b){return (b.innerText||'').trim()==='Senden';});
  if(!btn) return JSON.stringify({f:false});
  btn.scrollIntoView({block:'center'});
  btn.click();
  return JSON.stringify({f:true, cls:(btn.className||'').slice(0,60), type:btn.type});
})()""")
print("CLICK:", res)