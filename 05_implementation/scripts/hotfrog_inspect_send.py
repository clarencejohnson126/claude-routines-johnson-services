ensure_real_tab()
info = js("""(function(){
  var b=Array.from(document.querySelectorAll('div,span,button,input,a')).find(function(x){return (x.innerText||x.value||'').trim()==='Senden';});
  if(!b) return JSON.stringify({f:false});
  var chain=[]; var el=b; for(var i=0;i<4 && el;i++){chain.push(el.tagName+'.'+(el.className||'').toString().slice(0,30)+(el.onclick?'[onclick]':'')); el=el.parentElement;}
  var form=b.closest('form');
  return JSON.stringify({
    f:true, tag:b.tagName, cls:(b.className||'').toString().slice(0,60),
    onclick: !!b.onclick, html:b.outerHTML.slice(0,160),
    chain:chain, hasForm: !!form, formAction: form?form.action:null
  });
})()""")
print("INSPECT:", info)
tok = js("(function(){var t=document.querySelector('textarea[name=g-recaptcha-response]');return t&&t.value?t.value.length:0;})()")
print("TOKEN-LEN:", tok)