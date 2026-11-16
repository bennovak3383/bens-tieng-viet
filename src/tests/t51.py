# 51: lifelines drill, soft clock on say-it, start-talking bar via zHear, Home tidy, time-to-start on the week panel
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']); pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: errs.append(str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.pace52='push'; S.set.ob7=1; S.set.lvl0='some'; S.me.name='Ben'; var d={}; Z27.units.slice(0,3).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),path:'here',goal:'chat',mins:60,days:6,r:[{t:Date.now(),ear:2,spk:2}],sit:['grab'],hard:['shy'],tried:[],mine:'x'}; save(); try{closeSheet()}catch(e){}; zRenderHome()")
    pg.wait_for_timeout(500)
    order=[ (e.get_attribute('id') or e.get_attribute('class') or '')[:14] for e in pg.locator('#z-home > *').all() if e.is_visible()]; print('home order:',order)
    print('plan card:',pg.locator('#z48').inner_text().replace('\n',' | ')[:300])
    print('week panel:',pg.locator('.z12wk .z51lat').inner_text())
    print('lifeline slip:',pg.locator('.z51c').count())
    pg.click('.z51c button'); pg.wait_for_timeout(400)
    print('soft clock on say-it:',pg.locator('#sheet-body .z51bar').count(), pg.locator('#sheet-body .z51bar').inner_text())
    pg.wait_for_timeout(5600); print('after 5s:',pg.locator('#sheet-body .z51bar').get_attribute('class'), pg.locator('#sheet-body .z51bar').inner_text())
    for k in range(10):
        pg.click('#sheet-body button:has-text("I said it")'); pg.wait_for_timeout(200)
        rb=pg.locator('#sheet-body .z36rec button')
        pg.click('#sheet-body button:has-text("I had it")'); pg.wait_for_timeout(200)
    print('drill end:',pg.inner_text('#sheet-body')[-300:].replace('\n',' | '))
    pg.click('#sheet-body button:has-text("Done")'); pg.wait_for_timeout(300); print('slip gone:',pg.locator('.z51c').count()==0)
    # zHear bar: fake a listen inside a sheet with a status line
    T("var b=zOpen(); b.appendChild(zTop('Nói ngay · speak now',0,null)); b.appendChild(h('p',{class:'z7status on',text:'🎤 Your turn'})); window._r=null; zHear(1500,function(){}).then(r=>{ window._r=r })"); pg.wait_for_timeout(300)
    print('hear bar shown:',pg.locator('#sheet-body .z51bar').count(),' lifelines on speak screen:',pg.locator('#sheet-body .z51life').count())
    pg.wait_for_timeout(2000)
    T("z51Log(2400); z51Log(1800); S.set.lat51[dayKey(new Date(Date.now()-8*DAY))]=[8000,2]; closeSheet(); zRenderHome()"); pg.wait_for_timeout(300)
    print('week panel now:',pg.locator('.z12wk .z51lat').inner_text())
    T("location.hash='prac'"); pg.wait_for_timeout(500); print('practice tile:',pg.locator('.z51pt').count())
    T("var g=Z27.st[0]; zOpenStory(z38Story(g),0); "); pg.wait_for_timeout(300)
    T("z49Retell(z38Story(Z27.st[0]),0,function(){})"); pg.wait_for_timeout(400); print('lifelines on retell:',pg.locator('#sheet-body .z51life').count())
    pg.screenshot(path='/tmp/t51.png')
    br.close()
print('ERR',errs or 'none')
