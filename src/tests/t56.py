# 56: tap to record / tap to stop / try again in every section; gate for the auto-listening screens at the slow stage
import sys
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]; NOREC='norec' in sys.argv
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']); pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: errs.append(str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Ben'; var d={}; Z27.units.slice(0,7).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; FC.slice(0,12).forEach(c=>{ S.fc[c.id+'|l']={ivl:1,ease:2.5,reps:1,lapses:0,due:Date.now()+9e7} }); save(); try{closeSheet()}catch(e){}")
    T(("window.SpeechRecognition=window.webkitSpeechRecognition=undefined; " if NOREC else "")+"SPEECH.on=true; window._sv=[]; zRecSave=function(m,b){ window._sv.push(m.kind); return Promise.resolve() }")
    def cycle(name, sel='#sheet-body .z55rec', n=0, hold=900):
        b=pg.locator(sel).nth(n); a=b.inner_text(); auto=T("!!SPEECH.cur")
        b.click(); pg.wait_for_timeout(hold); mid=b.inner_text(); b.click(); pg.wait_for_timeout(1300)
        end=b.inner_text() if b.count() and b.is_visible() else '(gone)'
        print('%-22s start=%-28s auto-listening=%s | recording=%-14s | after=%s | fast=%s'%(name,a,auto,mid,end,T("SPEECH.fast")))
        return b
    print('stage',T("z52Stage()"))
    T("z12Recall(null,3)"); pg.wait_for_timeout(500); b=cycle('recall'); print('   revealed:',pg.locator('#sheet-body .rf-reveal').count(),'· redo:'); cycle('recall redo'); T("closeSheet()")
    T("z13First()"); pg.wait_for_timeout(500); cycle('first 3 minutes'); print('   heard:',pg.locator('#sheet-body p.heard').first.inner_text()); T("closeSheet()")
    T("z13Shadow(function(){},1,z13Items([['cảm ơn','thank you']]))"); pg.wait_for_timeout(1500); cycle('shadowing'); pg.wait_for_timeout(800); print('   graph/out:',pg.locator('#sheet-body svg').count(),'| status:',pg.locator('#sheet-body .z7status').first.inner_text()); T("closeSheet()")
    T("z29Speak(function(){},0,2)"); pg.wait_for_timeout(700); cycle('speaking topic',hold=1500); print('   msg:',('Recorded.' in pg.inner_text('#sheet-body')),'| saved yet:',T("_sv.length")); cycle('speaking redo')
    pg.click('#sheet-body button:has-text("show an example")'); pg.wait_for_timeout(400); print('   after example: saved kinds',T("_sv.join(',')")); T("closeSheet()")
    T("z27Say([['Tôi tên là Ben.','My name is Ben.']],function(){},{s:0,sn:0})"); pg.wait_for_timeout(500); cycle('unit say-it'); print('   revealed:',pg.locator('#sheet-body .rf-reveal').count()); T("closeSheet()")
    T("vanTwist()"); pg.wait_for_timeout(500); cycle('tongue twister'); T("closeSheet()")
    T("zOpenStory(z38Story(Z27.st[0]),0)"); pg.wait_for_timeout(700); cycle('story read aloud','#sheet-body .chip.z55rec'); print('   heard view:',pg.locator('#sheet-body .zheard').count())
    pg.click('#sheet-body button:has-text("I read it")'); pg.wait_for_timeout(2500); cycle('story question','#sheet-body .btn.z55rec'); print('   answer shown:',pg.locator('#sheet-body .rf-reveal').count(),'next btn:',pg.locator('#sheet-body #rf-next').count()); cycle('story q redo','#sheet-body .btn.z55rec'); print('   views:',pg.locator('#sheet-body .zheard').count(),'answers:',pg.locator('#sheet-body .rf-reveal').count()); T("closeSheet()")
    T("vanOpen(C7.van[0],function(){})"); pg.wait_for_timeout(500)
    for k in range(40):
        if pg.locator('#sheet-body .z55rec').count(): break
        if not T("(function(){ var b=document.querySelector('#sheet-body #rf-next'); if(b){ b.click(); return true } return false })()"): break
        pg.wait_for_timeout(300)
    if pg.locator('#sheet-body .z55rec').count():
        pg.wait_for_timeout(3500); cycle('sound lesson sentence'); print('   status:',pg.locator('#sheet-body .z7status').first.inner_text())
    else: print('sound lesson sentence: could not reach the step (', pg.inner_text('#sheet-body')[:120].replace('\n',' | '),')')
    T("closeSheet()")
    print('--- screens that used to listen by themselves, at the slow stage (gate) ---')
    T("z7Speak(3)")
    for k in range(6):
        pg.wait_for_timeout(1500)
        if pg.locator('#sheet-body .z56gate').count(): break
    print('speak now: gate btn',pg.locator('#sheet-body .z56gate').count(),'| status:',pg.locator('#sheet-body .z7status').first.inner_text(),'| listening by itself:',T("!!SPEECH.cur"))
    if pg.locator('#sheet-body .z56gate').count(): cycle('speak now','#sheet-body .z56gate'); print('   status after:',pg.locator('#sheet-body .z7status').first.inner_text())
    T("closeSheet()")
    # scenes and the everyday question cards: see t56b.py
    T("S.set.pace52='push'; z7Speak(3)"); pg.wait_for_timeout(6000); print('speak now at pace push: gate btn',pg.locator('#sheet-body .z56gate').count(),'| listening by itself:',T("!!SPEECH.cur")); T("closeSheet(); S.set.pace52='auto'")
    print('fast at end:',T("SPEECH.fast"),'| cur:',T("!!Z56.cur"))
    br.close()
print('ERR',errs or 'none')
