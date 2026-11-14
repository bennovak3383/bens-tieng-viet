from playwright.sync_api import sync_playwright
B='http://localhost:8890'
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    pg=br.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto(B+'/#home'); pg.wait_for_timeout(1200)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    T("S.set.ob7=1; save(); closeSheet()")
    T("z10Games()"); pg.wait_for_timeout(900); print('GAMES in view:', pg.evaluate("document.getElementById('games-panel').getBoundingClientRect().top"))
    print('LIBRARY text:', pg.inner_text('#v-today')[:600].replace('\n',' | '))
    T("SPEECH.on=true; zMic=function(){return true}; zHear=function(ms,cb){ return new Promise(function(r){ setTimeout(function(){ r({alts:['xyz'],blob:null,first:500,total:900}) },200) }) }")
    T("z7Speak(4)"); pg.wait_for_timeout(1200); pg.click("text=Skip (S)")
    for k in range(12):
        pg.wait_for_timeout(1500); t=pg.inner_text('#sheet-body')
        if 'ask the question' in t.lower(): print('REVERSED round seen at', k, '|', [l for l in t.split('\n') if 'ASK' in l.upper()][:2]); break
    else: print('no reverse; last:', t[:200])
    br.close(); print('ERR',errs)
