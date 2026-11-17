from playwright.sync_api import sync_playwright
B='http://localhost:8890'
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']); pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: print('PAGEERR',e)); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; var d={}; Z27.units.slice(0,7).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; save(); try{closeSheet()}catch(e){}")
    T("window.SpeechRecognition=window.webkitSpeechRecognition=undefined; SPEECH.on=true; zRecSave=function(m,b){ return Promise.resolve() }")
    T("zOpenScene(zNextScene())"); pg.wait_for_timeout(700)
    print('SC all buttons:',[b.inner_text()[:30] for b in pg.locator('#sheet-body button:visible').all()])
    for c in pg.locator('#sheet-body .chip.phon').all():
        try: c.click(timeout=500)
        except Exception: pass
        pg.wait_for_timeout(120)
    pg.click('#sheet-body button:has-text("Start the scene")'); pg.wait_for_timeout(600)
    for k in range(12):
        print('SC',k,[b.inner_text()[:26] for b in pg.locator('#sheet-body button:visible').all()][-4:],'| gate',pg.locator('#sheet-body .z56gate').count(),'| heard:',[x.inner_text()[:50] for x in pg.locator('#sheet-body p.heard').all()])
        if pg.locator('#sheet-body .z56gate').count(): break
        pg.wait_for_timeout(2500)
    if pg.locator('#sheet-body .z56gate').count():
        g=pg.locator('#sheet-body .z56gate'); g.click(); pg.wait_for_timeout(900); print(' rec:',g.inner_text()); g.click(); pg.wait_for_timeout(1300)
        print(' after:',[b.inner_text()[:26] for b in pg.locator('#sheet-body button:visible').all()][-4:],'gate left',pg.locator('#sheet-body .z56gate').count(),'heardview',pg.locator('#sheet-body .zheard').count())
    T("closeSheet()")
    ids=T("Object.keys(S.q).slice(0,3).concat(C6.pairs.slice(0,3).map(p=>p.id)).slice(0,3)"); print('ids',ids)
    T("zRunQ(%s,'Hỏi – Đáp · questions',function(){})"%ids)
    for k in range(14):
        pg.wait_for_timeout(1500)
        if pg.locator('#sheet-body .z56gate').count(): break
        nb=pg.locator('#sheet-body #rf-next:visible')
        if nb.count(): nb.first.click()
    print('CARD gate',pg.locator('#sheet-body .z56gate').count(),'| btns:',[b.inner_text()[:26] for b in pg.locator('#sheet-body button:visible').all()][-6:],'| hint texts:',[x for x in pg.inner_text('#sheet-body').split('\n') if 'turn' in x or 'Listening' in x])
    if pg.locator('#sheet-body .z56gate').count():
        g=pg.locator('#sheet-body .z56gate'); g.click(); pg.wait_for_timeout(900); print(' rec:',g.inner_text()); g.click(); pg.wait_for_timeout(1300)
        print(' after:',[b.inner_text()[:26] for b in pg.locator('#sheet-body button:visible').all()][-4:],'gate left',pg.locator('#sheet-body .z56gate').count())
        pg.click('#sheet-body button:has-text("Missed it")'); pg.wait_for_timeout(400); pg.click('#sheet-body #rf-next')
        for k in range(8):
            pg.wait_for_timeout(1500)
            if pg.locator('#sheet-body .z56gate').count(): break
        print(' 2nd card gate',pg.locator('#sheet-body .z56gate').count()); pg.click("#sheet-body button:has-text(\"I don't know\")"); pg.wait_for_timeout(600); print(' after I dont know: gate left',pg.locator('#sheet-body .z56gate').count(),'next',pg.locator('#sheet-body #rf-next').count())
    pg.screenshot(path='/tmp/t56c.png')
    br.close()
