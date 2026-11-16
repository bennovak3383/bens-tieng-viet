# 52: pace by stage, reps session, say-it mic button, brave ladder, settings
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']); pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: errs.append(str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    def units(n): T("var d={}; Z27.units.slice(0,%d).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; save(); try{closeSheet()}catch(e){}; zRenderHome()"%n); pg.wait_for_timeout(400)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Ben'; S.set.in48={t:Date.now(),path:'here',goal:'chat',around:'yes',mins:60,days:6,r:[{t:Date.now(),ear:2,spk:2}],sit:[],hard:['shy'],tried:[]}; save()")
    units(3)
    print('stage',T("z52Stage()"),'secs',T("[z52Sec('hear'),z52Sec('say')]"),'| week:',pg.locator('.z51lat').inner_text())
    print('route has reps:',T("z12Stops().map(x=>x.k).join(',')"))
    print('ladder:',pg.locator('#z48 .z52lad').inner_text().replace('\n',' | '))
    pg.click('#z48 .z52lad button'); pg.wait_for_timeout(300); print('ladder after:',pg.locator('#z48 .z52lad').inner_text().replace('\n',' | '))
    T("z27Say([['Tôi tên là Ben.','My name is Ben.']],function(){},{s:0,sn:0})"); pg.wait_for_timeout(400)
    print('stage1 say-it clock:',pg.locator('#sheet-body .z51bar').count(),' buttons:',[b.inner_text() for b in pg.locator('#sheet-body button.btn').all()])
    T("z52Reps(null,2)"); pg.wait_for_timeout(500); print('REPS:',pg.inner_text('#sheet-body')[-200:].replace('\n',' | '))
    pg.wait_for_timeout(9000); print('reps later:',pg.locator('#sheet-body .z52cue').inner_text() if pg.locator('#sheet-body .z52cue').count() else pg.inner_text('#sheet-body')[-150:].replace('\n',' | '))
    units(12); print('stage at 12 units',T("z52Stage()"),T("[z52Sec('hear'),z52Sec('say')]"),' route has reps:','rp' in T("z12Stops().map(x=>x.k).join(',')"))
    T("z27Say([['Tôi tên là Ben.','My name is Ben.']],function(){},{s:0,sn:0})"); pg.wait_for_timeout(400); print('stage2 clock:',pg.locator('#sheet-body .z51bar').inner_text())
    T("S.set.pace52='slow'"); print('slow override stage:',T("z52Stage()"))
    T("closeSheet(); openSettings()"); pg.wait_for_timeout(300); print('settings pace:',pg.locator('#sheet-body .z52set').inner_text()[:120].replace('\n',' | '))
    br.close()
print('ERR',errs or 'none')
