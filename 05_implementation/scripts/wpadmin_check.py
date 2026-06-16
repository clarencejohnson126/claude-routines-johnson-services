new_tab("https://johnson-services.de/wp-admin/")
wait_for_load()
js("new Promise(function(r){setTimeout(r,2000);})")
print("URL:", page_info().get("url"))
print("TITLE:", js("document.title"))
# Login-Form sichtbar?
print("LOGIN-FORM:", js("!!document.querySelector('#loginform, #user_login')"))
print("DASHBOARD:", js("!!document.querySelector('#wpadminbar, #adminmenu')"))
print("SHOT:", capture_screenshot())