# 59–60: the Home hub (tiles, today's lesson, time picker) and the five games, each played to the end
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':390,'height':844})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,5).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(400)
    print('lands on hub:',pg.locator('#v-hub').is_visible(),'| look:',T("document.documentElement.getAttribute('data-look')"),'| tiles:',pg.locator('.z59t').count(),'| greeting:',pg.locator('.z59hero h1').inner_text())
    print('today card:',pg.locator('.z59day h2').inner_text(),'| ring:',pg.locator('.z59ring b').inner_text(),'| bars:',[x.inner_text().replace('\n',' ') for x in pg.locator('.z59bar .t').all()])
    pg.locator('.z59mins button').nth(1).click(); pg.wait_for_timeout(200); print('minutes saved:',T("S.set.mins"),'| button:',pg.locator('.z59day .btn.primary').inner_text())
    pg.locator('.z59day .btn.primary').click(); pg.wait_for_timeout(900); print('start → view:',T("location.hash"),'| sheet open:',not pg.locator('#sheet').is_hidden()); T("closeSheet()"); T("location.hash='hub'"); pg.wait_for_timeout(400)
    print('Today page folded:',pg.locator('#z-home.z59less').count()==1)
    # games
    pg.locator('.z59-gam').click(); pg.wait_for_timeout(400); print('sets:',[x.inner_text().split('\n')[0] for x in pg.locator('.z60set').all()],'| games:',[x.inner_text().split('\n')[0] for x in pg.locator('.z60g').all()])
    SET="z60Sets().filter(s=>s.id===Z60.sel)[0]"
    def end(tag):
        pg.wait_for_selector('.z60end',timeout=8000); print(tag,'→',pg.locator('.z60big').inner_text(),'| stars on:',pg.locator('.z60stars svg.on').count(),'| best saved:',T("JSON.stringify(S.set.g60)")[:120]); pg.locator('button:has-text("All games")').click(); pg.wait_for_timeout(300)
    # match up (one wrong try first)
    pg.locator('.z60g').nth(0).click(); pg.wait_for_timeout(300)
    mp=dict(T(SET+".words.map(w=>[w.vi,z60En(w.en)])"))
    l0=pg.locator('.z60tile.l').nth(0); wrong=[r for r in pg.locator('.z60tile.r').all() if r.inner_text().strip()!=mp[l0.inner_text().strip()]][0]; l0.click(); wrong.click(); pg.wait_for_timeout(500)
    while pg.locator('.z60end').count()==0:
        ls=[x for x in pg.locator('.z60tile.l:not(.ok)').all()]
        if not ls: pg.wait_for_timeout(400); continue
        vi=ls[0].inner_text().strip(); ls[0].click()
        [r for r in pg.locator('.z60tile.r:not(.ok)').all() if r.inner_text().strip()==mp[vi]][0].click(); pg.wait_for_timeout(120)
    end('match up (1 miss)')
    # flash cards
    pg.locator('.z60g').nth(1).click(); pg.wait_for_timeout(300); n=0
    while pg.locator('.z60end').count()==0 and n<40:
        pg.locator('.z60card').click(); pg.locator('.z60y' if n%4 else '.z60n').click(); n+=1; pg.wait_for_timeout(60)
    end('flash cards')
    # unjumble
    pg.locator('.z60g').nth(2).click(); pg.wait_for_timeout(300); sm=dict(T(SET+".sents.map(s=>[s.en,s.vi])")); k=0
    while pg.locator('.z60end').count()==0:
        en=pg.locator('.z60clue b').inner_text().strip(); words=sm[en].rstrip('.?!…').split()
        if k==0: words=list(reversed(words))
        for w in words: pg.locator('.z60tray .z60w',has_text=w).filter(has_text=w).first.click() if False else [x for x in pg.locator('.z60tray .z60w').all() if x.inner_text()==w][0].click()
        pg.locator('.z60stage .btn.primary').click(); pg.wait_for_timeout(150)
        if k==0:
            print('wrong order message:',pg.locator('.z60msg').inner_text()); 
            for x in pg.locator('.z60line .z60w').all()[::-1]: x.click()
            k=1; continue
        pg.locator('.z60stage .btn.primary').click(); pg.wait_for_timeout(120)
    end('unjumble (1 miss)')
    # find the match
    pg.locator('.z60g').nth(3).click(); pg.wait_for_timeout(300); inv={v:k for k,v in mp.items()}
    while pg.locator('.z60end').count()==0:
        en=pg.locator('.z60find b').inner_text().strip(); c=[x for x in pg.locator('.z60tile.f:not(.gone):not(.ok)').all() if mp.get(x.inner_text().strip())==en]
        if c: c[0].click()
        pg.wait_for_timeout(750)
    end('find the match')
    # listen and choose
    pg.locator('.z60g').nth(4).click(); pg.wait_for_timeout(400)
    while pg.locator('.z60end').count()==0:
        a=pg.locator('.z60stage').get_attribute('data-a'); [x for x in pg.locator('.z60opt').all() if x.inner_text().strip()==a][0].click(); pg.wait_for_timeout(100); pg.locator('.z60stage .btn.primary').click(); pg.wait_for_timeout(350)
    end('listen and choose')
    T("closeSheet()"); pg.locator('.z59-lis').click(); pg.wait_for_timeout(300); print('listening corner:',[x.inner_text().split('\n')[0] for x in pg.locator('.z60g').all()])
    for i in range(2,6):
        pg.locator('.z60g').nth(i).click(); pg.wait_for_timeout(500); print('  opens:',pg.locator('#sheet-body .lbl').first.inner_text()); T("closeSheet()"); pg.locator('.z59-lis').click(); pg.wait_for_timeout(250)
    T("closeSheet()")
    # old look still there
    T("S.set.look59='old'; S.set.skin='night'; save(); z19Apply()"); print('old look:',T("document.documentElement.getAttribute('data-skin')+' '+document.documentElement.getAttribute('data-look')"))
    br.close()
print('ERR',errs or 'none')
