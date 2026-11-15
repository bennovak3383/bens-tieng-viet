from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-ui-for-media-stream'])
    pg=br.new_context(viewport={'width':390,'height':844}).new_page(); pg.on('pageerror',lambda e: errs.append(str(e)))
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='more'; S.set.k27={snd:1,d:{}}; save()"); pg.reload(); pg.wait_for_timeout(2500); T("try{closeSheet()}catch(e){}")
    T("Z27.units.forEach(function(u){ if(u.lv==='A1') z27St().d[u.id]={t:1} }); save(); zRenderHome()"); pg.wait_for_timeout(300)
    print('core card:',pg.inner_text('#z27')[:220].replace('\n',' / '))
    ui=T("Z27.units.findIndex(function(u){return u.id==='u22'})")
    T("z27Unit(%d)"%ui); pg.wait_for_timeout(300); pg.get_by_role('button').filter(has_text='Next').first.click(); pg.wait_for_timeout(500)
    print('learn screen:',pg.inner_text('#sheet-body')[:300].replace('\n',' / ')); pg.screenshot(path='/tmp/l39.png')
    n=0
    while pg.locator('text=I said it · next').count() and n<30: pg.click('text=I said it · next'); pg.wait_for_timeout(120); n+=1
    print('must-know screens:',n)
    # quiz
    for i in range(20):
        t=pg.inner_text('#sheet-body')
        if 'optional' in t.lower(): break
        b=[x for x in pg.locator('#sheet-body .z13opt:visible').all()]
        if b: b[0].click(); pg.wait_for_timeout(250)
        nx=pg.get_by_role('button',name='Next',exact=True)
        if nx.count(): nx.first.click(); pg.wait_for_timeout(250)
    print('optional screen:',pg.inner_text('#sheet-body')[:260].replace('\n',' / ')); pg.screenshot(path='/tmp/o39.png')
    uid='u22'
    T("z27St().d['u22']={t:1}; save()")
    print('cards on for u22: must',T("FC.filter(function(c){return c.c==='k22'&&fcOn(c)&&!z39IsOpt(c)}).length"),'| optional on',T("FC.filter(function(c){return c.c==='k22'&&fcOn(c)&&z39IsOpt(c)}).length"))
    pg.get_by_text('Add these to my cards').click(); pg.wait_for_timeout(200)
    print('after add: optional on',T("FC.filter(function(c){return c.c==='k22'&&fcOn(c)&&z39IsOpt(c)}).length"))
    pg.get_by_role('button',name='Next',exact=True).click(); pg.wait_for_timeout(400)
    print('next step:',pg.inner_text('#sheet-body')[:80].replace('\n',' / '))
    # A1 unit: all must
    print('A1 u01 must',T("z39Must(Z27.units[0]).length"),'of',T("Z27.units[0].w.length"))
    br.close()
print('ERR',errs or 'none')
