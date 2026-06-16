ensure_real_tab()
import json
# XHR/fetch-Logger injizieren
js("""(function(){
  if(window.__hooked) return;
  window.__hooked=true; window.__log=[];
  var oO=XMLHttpRequest.prototype.open, oS=XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.open=function(m,u){this.__u=u;return oO.apply(this,arguments);};
  XMLHttpRequest.prototype.send=function(){var x=this;x.addEventListener('loadend',function(){window.__log.push({u:(x.__u||'')+'',status:x.status,resp:(x.responseText||'').slice(0,250)});});return oS.apply(this,arguments);};
})()""")
# reCAPTCHA frisch
loc=js("""(function(){var f=Array.from(document.querySelectorAll('iframe')).find(function(x){return /recaptcha.*anchor/i.test(x.src||'');});if(!f)return JSON.stringify({f:false});f.scrollIntoView({block:'center'});var r=f.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left)+30,y:Math.round(r.top+r.height/2)});})()""")
d=json.loads(loc)
if d.get("f"): click_at_xy(d["x"],d["y"])
js("new Promise(function(r){setTimeout(r,2500);})")
tok=js("(function(){var t=document.querySelector('textarea[name=g-recaptcha-response]');return t&&t.value?t.value.length:0;})()")
print("TOKEN:",tok)
# Button
bloc=js("""(function(){var b=Array.from(document.querySelectorAll('button')).find(function(x){return (x.innerText||'').trim()==='Senden';});if(!b)return JSON.stringify({f:false});b.scrollIntoView({block:'center'});var r=b.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)});})()""")
b=json.loads(bloc)
if b.get("f"): click_at_xy(b["x"],b["y"])
js("new Promise(function(r){setTimeout(r,2500);})")
print("LOG:", js("JSON.stringify((window.__log||[]).slice(-6))"))