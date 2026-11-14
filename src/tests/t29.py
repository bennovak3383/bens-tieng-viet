# Version 29 test: the at-my-level day plan and test practice.
import json
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
    pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: errs.append('PAGE '+str(e)))
    T=lambda c: pg.evaluate('(c)=>__T(c)',c); NX=lambda: pg.get_by_role("button",name="Next",exact=True)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.mins=60; S.set.k27={snd:1,d:{u01:{t:1},u02:{t:1},u03:{t:1},u04:{t:1},u05:{t:1}}}; save(); try{closeSheet()}catch(e){}"); pg.reload(); pg.wait_for_timeout(2000); T("try{closeSheet()}catch(e){}")
    print('1 plan at my level (60 min):', T("z12Stops().map(function(x){return x.k}).join(',')"), '| 10:', T("S.set.mins=10, z12Stops().map(function(x){return x.k}).join(',')"), '| 30:', T("S.set.mins=30, z12Stops().map(function(x){return x.k}).join(',')"), '| 90:', T("S.set.mins=90, z12Stops().map(function(x){return x.k}).join(',')"))
    T("S.set.mins=60; save(); zRenderHome()"); pg.wait_for_timeout(300); print('1 note on Today:', pg.inner_text('.z29lv')[:60].replace('\n',' / '))
    print('1 full plan when switched:', T("S.set.k27.full=1, z12Stops().map(function(x){return x.k}).join(',')")); T("S.set.k27.full=0; save()")
    print('1 sounds not done -> sound lesson first:', T("(function(){ var k=S.set.k27, o=k.snd; k.snd=0; var r=z12Stops().map(function(x){return x.k}).join(','); k.snd=o; return r })()"))
    print('1 known sentences:', T("z27Known().length"), '| practice pool only known:', T("(function(){ var P=z12Pool(); return P.seen.length+' seen, '+P.rest.length+' rest' })()"))
    # listening at my level
    T("z27Hear(function(){ window.__h=1 },4)"); pg.wait_for_timeout(600)
    for i in range(4): pg.locator('.z13opt').first.click(); pg.wait_for_timeout(120); NX().click(); pg.wait_for_timeout(250)
    print('2 listen:', pg.inner_text('#sheet-body')[-90:].replace('\n',' / '), '| marked done today:', T("!!zTodayDone().kl")); NX().click(); pg.wait_for_timeout(200); print('2 carried on:', T("window.__h"))
    # marks
    T("z29Write(function(){ window.__w=1 },5)"); pg.wait_for_timeout(500); smp=pg.inner_text('.z27gap')+' -> '+' | '.join(pg.locator('.z25opt').all_inner_texts())
    n=0
    while pg.locator('.z25opt').count() and n<8: pg.locator('.z25opt').first.click(); pg.wait_for_timeout(120); NX().click(); pg.wait_for_timeout(250); n+=1
    print('3 marks items:', n, '| sample:', smp, '| saved:', T("JSON.stringify(S.set.k27.ex.w1)")); NX().click()
    # hear the question
    T("z29Hear1(function(){ window.__q=1 })"); pg.wait_for_timeout(600); opts=pg.locator('.z13opt').all_inner_texts(); n=0
    while pg.locator('.z13opt').count() and n<10: pg.locator('.z13opt').first.click(); pg.wait_for_timeout(120); NX().click(); pg.wait_for_timeout(250); n+=1
    print('4 hear-the-question items:', n, '| options sample:', opts, '| saved:', T("JSON.stringify(S.set.k27.ex.h1)")); NX().click()
    # reading
    T("z29Read(function(){ window.__r=1 })"); pg.wait_for_timeout(500); print('5 reading text:', pg.inner_text('.z29txt')[:80].replace('\n',' / ')); n=0
    while pg.locator('.z13opt').count() and n<6: pg.locator('.z13opt').nth(0).click(); pg.wait_for_timeout(120); NX().click(); pg.wait_for_timeout(250); n+=1
    print('5 reading questions:', n, '| saved:', T("JSON.stringify(S.set.k27.ex.r1)")); NX().click()
    # speaking without the mic
    T("SPEECH.on=false; z29Speak(function(){ window.__s=1 })"); pg.wait_for_timeout(500); print('6 speaking topic:', pg.inner_text('#sheet-body .sess-top')[:70].replace('\n',' / ') if pg.locator('#sheet-body .sess-top').count() else pg.inner_text('#sheet-body')[:90].replace('\n',' / '))
    pg.click('text=Show the question'); n=0
    while pg.locator('text=I answered out loud').count() and n<8: pg.click('text=I answered out loud'); pg.wait_for_timeout(120); pg.click('text=I could answer'); pg.wait_for_timeout(250); n+=1
    print('6 speaking questions:', n, '| saved:', T("JSON.stringify(S.set.k27.ex.s1)"), '| done today:', T("!!zTodayDone().kq")); NX().click()
    # speaking with a pretend mic
    T("SPEECH.on=true; zHear=function(ms,cb){ return new Promise(function(r){ setTimeout(function(){ if(cb) cb('tôi tên là Ben'); r({alts:['tôi tên là ben'],blob:new Blob([new Uint8Array(3000)],{type:'audio/webm'}),first:700,total:1500}) },300) }) }; z29Speak(null,0)"); pg.wait_for_timeout(500)
    print('6 record button with mic on:', pg.locator('text=Record my answer for my teacher').count()); pg.click('text=Record my answer for my teacher'); pg.wait_for_timeout(900); print('6 after recording, example shown:', pg.locator('text=One way to answer').count()); T("closeSheet()")
    # menu, practice tile, the whole day runs
    T("z29Exam()"); pg.wait_for_timeout(300); print('7 test practice rows:', pg.locator('.z27row').count(), '|', pg.inner_text('#sheet-body')[-70:].replace('\n',' / ')); T("closeSheet(); location.hash='prac'"); pg.wait_for_timeout(300); print('7 practice tile:', 'Test practice' in pg.inner_text('#z-prac'))
    T("location.hash='home'; S.d6={}; save(); zToday()"); pg.wait_for_timeout(700); print('8 Start my day opens:', pg.inner_text('#sheet-body')[:60].replace('\n',' / ')); T("closeSheet()")
    T("z27Unit(5,function(){ window.__u=1 })"); pg.wait_for_timeout(300); print('8 unit opened from the plan:', pg.locator('.z27ex').count()>0)
    # all speaking topics and texts open without errors at the top level
    T("closeSheet(); Z27.units.forEach(function(u){ S.set.k27.d[u.id]={t:1} }); save()"); print('9 topics at the end:', T("z29Topics().length"), '| texts:', T("z29Texts().length"))
    for i in range(T("z29Topics().length")): T("z29Speak(null,%d)"%i); pg.wait_for_timeout(120)
    for i in range(6): T("S.set.k27.exr=%d; z29Read()"%i); pg.wait_for_timeout(120)
    T("z29Write(null,10)"); pg.wait_for_timeout(200); T("closeSheet()")
    pg.screenshot(path='/home/claude/out/t29.png'); br.close()
print('ERRORS:', errs or 'none')
