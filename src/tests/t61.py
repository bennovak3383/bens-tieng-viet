# 61–64: story reader (tap a word), sound boards (touch / one by one / test), scenes (explore / check / sentences), sentence builder, recording part "ab"
import json, urllib.request
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':390,'height':844})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(400); print('tiles with "Soon":',pg.locator('.z59t em').count())
    # stories
    pg.locator('.z59-sto').click(); pg.wait_for_timeout(300); print('stories:',pg.locator('.z61s').count(),'| locked:',pg.locator('.z61s.lock').count())
    pg.locator('.z61ch button').first.click(); pg.wait_for_timeout(300); print('reader:',pg.locator('#sheet-body h1').inner_text(),'| paragraphs:',pg.locator('.z61p').count(),'| words to tap:',pg.locator('.z61story .zw').count(),'| text visible:',pg.locator('.z61p').first.is_visible())
    w=pg.locator('.z61story .zw',has_text='sống').first; w.click(); pg.wait_for_timeout(200); print('tap a word →',pg.locator('.z61pw').inner_text().replace('\n',' | '),'| its sentence:',pg.locator('.z61ps').inner_text().replace('\n',' | '))
    pg.locator('.z61sv').click(); print('saved to cards:',T("!!S.w['sống']"))
    pg.locator('.z61bar .chip:text-is("English")').click(); print('English shown:',pg.locator('.z61en').first.inner_text()[:50])
    pg.locator('.z61play').click(); pg.wait_for_timeout(300); print('playing → button says:',pg.locator('.z61play').inner_text(),'| a sentence is lit:',pg.locator('.z61sent.on').count()); pg.locator('.z61play').click()
    print('questions:',pg.locator('.z61q').count()); pg.locator('.z61q .chip').first.click(); print('answer shown:',pg.locator('.z61a').first.inner_text())
    pg.locator('#sheet-body .btn.primary').last.click(); pg.wait_for_timeout(300); print('marked read:',pg.locator('.z61ch button.done').count()); T("closeSheet()")
    # sounds
    pg.locator('.z59-snd').click(); pg.wait_for_timeout(500); print('boards:',[x.locator('b').inner_text() for x in pg.locator('.z62m').all()])
    pg.locator('.z62m').first.click(); pg.wait_for_timeout(200); print('alphabet tiles:',pg.locator('.z62t').count()); pg.locator('.z62t').nth(3).click(); pg.wait_for_timeout(200); print('touch B →',pg.locator('.z62card').inner_text().replace('\n',' | '),'| heard:',T("Object.keys(S.set.s62.abc.seen)"))
    pg.locator('.z62tabs button').nth(1).click(); pg.wait_for_timeout(200); pg.locator('.z62nav button').last.click(); pg.wait_for_timeout(150); print('one by one:',pg.locator('.z62cnt').inner_text(),pg.locator('.z62card').inner_text().replace('\n',' | '))
    pg.locator('.z62tabs button').nth(2).click(); pg.wait_for_timeout(300)
    for i in range(10):
        a=pg.locator('.z60stage').get_attribute('data-a')
        if pg.locator('.z60end').count(): break
        if i==0: pg.locator('.z62t:not([data-k="%s"])'%a).first.click()
        pg.locator('.z62t[data-k="%s"]'%a).click(); pg.wait_for_timeout(1800)      # v70: the answer card stays up a moment before the next question
    pg.wait_for_selector('.z60end',timeout=6000)
    print('test result:',pg.locator('.z60big').inner_text(),'| best:',T("S.set.s62.abc.best")); T("closeSheet()")
    pg.locator('.z59-snd').click(); pg.wait_for_timeout(300)
    for i in range(1,7): 
        pg.locator('.z62m').nth(i).click(); pg.wait_for_timeout(150); n=pg.locator('.z62t').count(); pg.locator('.z62t').first.click(); print('  board',i,pg.locator('#sheet-body .lbl').first.inner_text(),'tiles',n,'→',pg.locator('.z62card').inner_text().replace('\n',' | ')[:60]); pg.locator('.sess-top .x').first.click(); pg.wait_for_timeout(150)
    T("closeSheet()")
    # scenes
    pg.locator('.z59-scn').click(); pg.wait_for_timeout(500); print('scenes:',[x.locator('b').inner_text() for x in pg.locator('.z63m').all()])
    pg.locator('.z63m').first.click(); pg.wait_for_timeout(200); print('people in the picture:',pg.locator('.z63p').count())
    pg.locator('.z63p[data-i="3"]').click(force=True); pg.wait_for_timeout(200); print('tap a person →',pg.locator('.z63who').inner_text().replace('\n',' | '),'||',[x.inner_text().replace('\n',' | ') for x in pg.locator('.z63ln').all()],'| name tag:',pg.locator('.z63tag:not([hidden])').inner_text())
    print('actions:',[x.locator('b').inner_text() for x in pg.locator('.z63a').all()])
    pg.locator('.z62tabs button').nth(1).click(); pg.wait_for_timeout(300); k=0
    while pg.locator('.z60end').count()==0 and k<40:
        st=pg.locator('.z60stage'); t=st.get_attribute('data-t'); a=st.get_attribute('data-a'); k+=1
        if t=='tap':
            i=T("Z63.d.scenes[0].people.findIndex(p=>p.k==='%s')"%a)
            if k==1: pg.locator('.z63p[data-i="%d"]'%((i+1)%7)).click(force=True); pg.wait_for_timeout(200)
            pg.locator('.z63p[data-i="%d"]'%i).click(force=True)
        else: pg.locator('.z63o[data-k="%s"]'%a).click()
        pg.wait_for_timeout(900)
    print('check result:',pg.locator('.z60big').inner_text(),'| best:',T("S.set.s63.fam.best"),'| rounds:',k)
    pg.locator('button:has-text("the sentences")').click(); pg.wait_for_timeout(200); print('dialogue lines:',pg.locator('.z63d').count(),'| sentences:',pg.locator('.z60stage .z63ln').count())
    pg.locator('button:has-text("games with these words")').click(); pg.wait_for_timeout(300); print('games set chosen:',pg.locator('.z60set[aria-pressed="true"]').inner_text().replace('\n',' | ')); T("closeSheet()")
    # builder
    pg.locator('.z59-bld').click(); pg.wait_for_timeout(500); rd=lambda: pg.locator('.z64s').inner_text().replace('\n','')+' = '+pg.locator('.z64en').inner_text()
    print('builder:',rd()); pg.locator('.z64o',has_text='bác sĩ').click(); print(' pick a person:',rd()); pg.locator('.z64forms button').nth(2).click(); print(' right?:',rd()); pg.locator('.z64forms button').nth(1).click(); print(' question:',rd())
    pg.locator('.z64st button').nth(1).click(); pg.wait_for_timeout(200); pg.locator('.z64o',has_text='sân bay').click(); print(' place:',rd())
    pg.locator('.z64st button').nth(2).click(); pg.wait_for_timeout(200); pg.locator('.z64o',has_text='Giáo viên').click(); print(' person fills the action:',rd()); pg.locator('.z64slot').nth(1).click(); pg.locator('.z64o',has_text='đọc sách').click(); print(' swap the action:',rd()); pg.locator('.z64forms button').nth(1).click(); print(' question:',rd())
    print(' sentences made:',T("S.set.b64.n"),'| stage 2 locked:',pg.locator('.z64stages button').nth(1).get_attribute('class'))
    pg.locator('.z64forms button').nth(0).click()
    for w in ['Bác sĩ','Đầu bếp','Tài xế','Lễ tân']: pg.locator('.z64slot').first.click(); pg.locator('.z64o',has_text=w).first.click()
    print(' after 10 in stage 1 → stage 2:',pg.locator('.z64stages button').nth(1).inner_text().replace('\n',' '),'| made:',T("S.set.b64.st[1]"))
    pg.locator('.z64stages button').nth(1).click(); pg.wait_for_timeout(300); pg.locator('.z64o',has_text='cuốn sách').click(); print(' stage 2 thing:',rd()); pg.locator('.z64st button').nth(1).click(); pg.wait_for_timeout(200); pg.locator('.z64o',has_text='con mèo').click(); pg.locator('.z64forms button').nth(2).click(); print(' animal, right?:',rd()); pg.locator('.z64st button').nth(2).click(); pg.wait_for_timeout(200); pg.locator('.z64o',has_text='xe buýt').click(); print(' transport:',rd())
    T("S.set.b64.open=3; save()"); T("z64Build(0,3)"); pg.wait_for_timeout(400); pg.locator('.z64o',has_text='Cô ấy').click(); pg.locator('.z64slot').nth(1).click(); pg.locator('.z64o',has_text='giáo viên').click(); print(' stage 3 job:',rd()); pg.locator('.z64forms button').nth(2).click(); print('  no:',rd()); pg.locator('.z64forms button').nth(1).click(); print('  right?:',rd())
    pg.locator('.z64st button').nth(1).click(); pg.wait_for_timeout(200); pg.locator('.z64o',has_text='Nhật Bản').click(); print(' country:',rd(),'| flag drawn:',pg.locator('.z64pic.fl svg').count()); pg.locator('.z64forms button').nth(1).click(); print('  question:',rd())
    pg.locator('.z64st button').nth(2).click(); pg.wait_for_timeout(200); pg.locator('.z64o',has_text='nhà thuốc').click(); print(' why you go:',rd()); pg.locator('.z64slot').nth(1).click(); pg.locator('.z64o',has_text='gặp bạn').click(); print('  swap the reason:',rd()); pg.locator('.z64forms button').nth(1).click(); print('  question:',rd())
    T("closeSheet()")
    pg.locator('.z59-scn').click(); pg.wait_for_timeout(400)
    for i in range(pg.locator('.z63m:not(.z73m)').count()):      # v73: the animals tile is not a people scene
        pg.locator('.z63m:not(.z73m)').nth(i).click(); pg.wait_for_timeout(200); n=pg.locator('.z63p').count(); pg.locator('.z63p').first.click(force=True); pg.wait_for_timeout(120); print('  scene',pg.locator('#sheet-body .lbl').first.inner_text(),'| people',n,'|',pg.locator('.z63ln').last.inner_text().replace('\n',' = ')); pg.locator('.sess-top .x').first.click(); pg.wait_for_timeout(200)
    T("closeSheet()")
    T("accPush&&0"); pg.reload(); pg.wait_for_timeout(1500); print('after reload: scores kept:',T("JSON.stringify([S.set.s62.abc.best,S.set.s63.fam.best,S.set.b64.n])"))
    print('teacher waves:',pg.locator('.z59tam animateTransform').count(),'| blinking eyes in a scene thumbnail:',T("z63Svg(Z63.d.scenes[0],true).split('z63eye').length-1"))
    # recording list
    vl=json.load(open('data/voice-lines.json'))['parts']; print('recording list: first parts',[(x['id'],len(x['lines'])) for x in vl[:12]],'| total',sum(len(x['lines']) for x in vl))
    br.close()
print('ERR',errs or 'none')
