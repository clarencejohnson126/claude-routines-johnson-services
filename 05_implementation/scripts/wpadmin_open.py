import json
ensure_real_tab()
ok=False
for attempt in range(3):
    try:
        new_tab("https://johnson-services.de/wp-login.php")
        wait_for_load()
        js("new Promise(function(r){setTimeout(r,1800);})")
        url=page_info().get("url","")
        if "chrome-error" not in url:
            ok=True; break
    except Exception as e:
        print("retry", attempt, str(e)[:60])
print("URL:", page_info().get("url"))
print("TITLE:", js("document.title"))
print("LOGIN-FORM:", js("!!document.querySelector('#loginform, #user_login, input[name=log]')"))
print("DASHBOARD:", js("!!document.querySelector('#wpadminbar, #adminmenu')"))
print("SHOT:", capture_screenshot())