# Version 30 test: pictures on core cards, the everyday-questions deck and day stop, the "Can I do it?" page.
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
    pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: errs.append('PAGE '+str(e)))
    T=lambda c: pg.evaluate('(c)=>__T(c)',c); NX=lambda: pg.get_by_role("button",name="Next",exact=True)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.mins=60; S.set.k27={snd:1,d:{}}; save(); try{closeSheet()}catch(e){}"); pg.reload(); pg.wait_for_timeout(2200); T("try{closeSheet()}catch(e){}")
    print('1 drawings loaded:', T("Object.keys(Z12.art).length"), '| core cards with a picture:', T("FC.filter(function(c){ return c.k27!=null&&Z12.art[c.vi] }).length"), 'of', T("FC.filter(function(c){ return c.k27!=null }).length"))
    print('2 everyday deck:', T("FC.filter(function(c){ return c.c==='dq' }).length"), 'cards |', T("C7.cats.dq&&C7.cats.dq[1]"), '| first new cards:', T("fcFresh().slice(0,3).join(' ')"))
    for m in (10,30,60,90): print('3 plan', m, ':', T("S.set.mins=%d, z12Stops().map(function(x){return x.k}).join(',')"%m))
    T("S.set.mins=60; save(); zRenderHome()"); pg.wait_for_timeout(300); print('3 Today shows the stop:', 'What people ask you' in pg.inner_text('#z-home'))
    # run the everyday-questions stop from the plan
    T("var st=z12Stops().filter(function(x){return x.k==='kd'})[0]; st.run(function(){ window.__kd=1 })"); pg.wait_for_timeout(500)
    print('4 stop opens:', pg.inner_text('#sheet-body .sess-top')[:60].replace('\n',' / ') if pg.locator('#sheet-body .sess-top').count() else pg.inner_text('#sheet-body')[:80])
    n=0
    while pg.locator('text=I answered out loud').count() and n<12: pg.click('text=I answered out loud'); pg.wait_for_timeout(100); pg.get_by_role('button',name='I could answer',exact=True).click(); pg.wait_for_timeout(200); n+=1
    print('4 questions asked:', n, '| kd done:', T("!!zTodayDone().kd"), '| kq not ticked by it:', not T("!!zTodayDone().kq"), '| saved as:', T("JSON.stringify(S.set.k27.ex.dq)")); NX().click(); pg.wait_for_timeout(200); print('4 carried on:', T("window.__kd"))
    # answer-about-yourself stop skips the everyday topic
    T("S.set.k27.d.u01={t:1}; save(); z29Speak(null)"); pg.wait_for_timeout(300); print('5 kq topic:', pg.inner_text('#sheet-body .lbl')[:80]); T("closeSheet()")
    T("z29Exam()"); pg.wait_for_timeout(300); txt=pg.inner_text('#sheet-body'); print('6 check page:', txt[txt.find('Can I'):txt.find('Can I')+40].replace('\n',' '), '| everyday row:', 'What people ask you every day' in txt)
    pg.locator('.z27row', has_text='What people ask you every day').first.click(); pg.wait_for_timeout(400); n=0
    while pg.locator('text=I answered out loud').count() and n<14: pg.click('text=I answered out loud'); pg.wait_for_timeout(80); pg.get_by_role('button',name='Not yet',exact=True).click(); pg.wait_for_timeout(150); n+=1
    print('6 from the page: questions', n); T("closeSheet()")
    # a core unit shows pictures while learning words
    T("z27Unit(0)"); pg.wait_for_timeout(300); pg.click('#z27-go'); pg.wait_for_timeout(400); print('7 picture on the first word card:', pg.locator('.z12pic:not(.nopic) svg').count()>0); pg.screenshot(path='/home/claude/out/t30-word.png'); T("closeSheet()")
    T("location.hash='fc'"); pg.wait_for_timeout(500); T("fcSession(null,5)"); pg.wait_for_timeout(500); pg.screenshot(path='/home/claude/out/t30-card.png'); T("closeSheet()")
    br.close()
print('ERRORS:', errs or 'none')
