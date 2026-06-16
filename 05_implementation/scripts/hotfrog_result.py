print("URL:", page_info().get("url"))
print("TEXT:", js("document.body.innerText.replace(/\\n+/g,' | ').slice(0,600)"))
print("SHOT:", capture_screenshot())