import secrets, string, json, time

ROOT = "/Users/clarence/Desktop/AUTOMATED ADS/Agentic Johnson Services/05_implementation/scripts"
pw = "JsMa9" + "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

def sel(name):
    return "document.querySelector(" + json.dumps("[name='" + name + "']") + ")"

def setval(name, val):
    js("var e=" + sel(name) + "; if(e){e.value=" + json.dumps(val)
       + "; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true}));}")

new_tab("https://www.golocal.de/registrierung/")
wait_for_load()

setval("newUser.email", "info@johnson-services.de")
setval("newUser.loginname", "JohnsonServicesMannheim")
setval("newUser.password", pw)
setval("newUser.confirmPassword", pw)
setval("newUser.locality", "Mannheim")
js("var r=" + sel("newUser.salutationcode") + "; if(r){r.checked=true; r.dispatchEvent(new Event('change',{bubbles:true}));}")
# Pflicht-Checkboxen (z.B. AGB) ankreuzen, Newsletter NICHT
js("Array.from(document.querySelectorAll('input[type=checkbox]')).forEach(function(c){ if(c.required && c.name!=='subscribeNewsletter'){ c.checked=true; c.dispatchEvent(new Event('change',{bubbles:true})); } });")

print("email:", js("(" + sel("newUser.email") + "||{}).value"))
print("locality:", js("(" + sel("newUser.locality") + "||{}).value"))
print("pw_len:", js("((" + sel("newUser.password") + "||{}).value||'').length"))
print("checkboxes:", js("JSON.stringify(Array.from(document.querySelectorAll('input[type=checkbox]')).map(function(c){return {name:c.name,checked:c.checked,req:c.required};}))"))

with open(ROOT + "/platform_accounts.txt", "a") as f:
    f.write("GoLocal | https://www.golocal.de | login: info@johnson-services.de / JohnsonServicesMannheim | pw: " + pw + "\n")

# Absenden: Button mit 'registrier' im Text finden
js("var bs=Array.from(document.querySelectorAll('button, input[type=submit], a')); var b=bs.find(function(x){return /registrier/i.test((x.innerText||x.value||''));}); if(b){b.click();}")
wait_for_load()
print("URL_NACH_SUBMIT:", page_info().get("url"))
print("SEITENTEXT:", js("document.body.innerText.replace(/\\s+/g,' ').slice(0,500)"))
