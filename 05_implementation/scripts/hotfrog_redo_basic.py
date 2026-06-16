ensure_real_tab()
res = js("""
(function(){
  return new Promise(function(resolve){
    var tries=0;
    var iv=setInterval(function(){
      tries++;
      var ins=Array.from(document.querySelectorAll('input')).filter(function(i){return i.type==='text'||i.type==='';});
      if(ins.length>=8 || tries>25){
        clearInterval(iv);
        function set(el,val){if(!el)return;el.focus();el.value=val;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}
        set(ins[0],'Johnson Services');
        set(ins[2],'George-Washington-Straße 219');
        set(ins[6],'Mannheim');
        set(ins[7],'Deutschland');
        set(ins[8],'68309');
        resolve(JSON.stringify({count:ins.length, fn:ins[0].value, adr:ins[2].value, ort:ins[6].value, plz:ins[8].value}));
      }
    },300);
  });
})()
""")
print("FILL:", res)
# Finde die Adresse klicken
loc = js("(function(){var b=Array.from(document.querySelectorAll('button,input[type=submit],a')).find(function(x){return /Finde die Adresse/i.test((x.innerText||x.value||''));});if(!b)return JSON.stringify({f:false});var r=b.getBoundingClientRect();return JSON.stringify({f:true,x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)});})()")
print("FINDBTN:", loc)
import json
d=json.loads(loc)
if d.get("f"):
    click_at_xy(d["x"], d["y"])
    js("new Promise(function(r){setTimeout(r,3500);})")
    print("NACH:", js("document.body.innerText.indexOf('erfolgreich zugeordnet')>-1 ? 'ADRESSE OK' : 'pruefen'"))
    print("SHOT:", capture_screenshot())