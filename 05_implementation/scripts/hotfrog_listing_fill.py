ensure_real_tab()
res = js("""
(function(){
  return new Promise(function(resolve){
    var tries=0;
    var iv=setInterval(function(){
      tries++;
      var ins=Array.from(document.querySelectorAll('input')).filter(function(i){return i.type==='text'||i.type==='';});
      if(ins.length>=8 || tries>20){
        clearInterval(iv);
        function set(el,val){if(!el)return;el.focus();el.value=val;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));}
        // Reihenfolge: 0 Firmenname,1 Gebaeude,2 Adresse,3 Str2,4 Str3,5 District,6 Ort,7 Land,8 PLZ
        set(ins[0],'Johnson Services');
        set(ins[2],'George-Washington-Straße 219');
        set(ins[6],'Mannheim');
        set(ins[7],'Deutschland');
        set(ins[8],'68309');
        resolve(JSON.stringify({count:ins.length, vals:ins.map(function(e){return e.value;})}));
      }
    },300);
  });
})()
""")
print("RESULT:", res)
print("SHOT:", capture_screenshot())