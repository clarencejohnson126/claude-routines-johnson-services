ensure_real_tab()
# Senden-Element finden + in den Viewport scrollen
loc = js("""(function(){
  var all=Array.from(document.querySelectorAll('button,input[type=submit],a,div,span'));
  var b=all.find(function(x){var t=(x.innerText||x.value||'').trim();return t==='Senden';});
  if(!b) return JSON.stringify({f:false});
  b.scrollIntoView({block:'center'});
  var r=b.getBoundingClientRect();
  return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2),tag:b.tagName});
})()""")
print("SENDEN-INVIEW:", loc)
import json
d=json.loads(loc)
if d.get("f"):
    click_at_xy(d["x"], d["y"])
print("geklickt @ in-view")