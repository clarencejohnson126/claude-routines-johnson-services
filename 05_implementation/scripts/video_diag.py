new_tab("https://johnson-services.de/")
wait_for_load()
info = js("""
(function(){
  var v=document.querySelector('video');
  if(!v) return JSON.stringify({video:false, note:'kein video-Tag auf der Seite'});
  function box(el){ if(!el) return null; var r=el.getBoundingClientRect(); var cs=getComputedStyle(el);
    return {tag:el.tagName, cls:(el.className||'').toString().slice(0,45), w:Math.round(r.width), h:Math.round(r.height),
            cssWidth:cs.width, maxWidth:cs.maxWidth, display:cs.display, ml:cs.marginLeft, mr:cs.marginRight, ta:cs.textAlign}; }
  var chain=[]; var el=v; for(var i=0;i<6 && el;i++){ chain.push(box(el)); el=el.parentElement; }
  return JSON.stringify({video:true, src:(v.currentSrc||v.src), readyState:v.readyState, networkState:v.networkState,
                         videoW:v.videoWidth, videoH:v.videoHeight, inIframe:(window.top!==window.self), chain:chain}, null, 1);
})()
""")
print(info)
