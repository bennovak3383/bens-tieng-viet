# 54: the teacher's exercise types, interactive: swap drill, build/transform, hear+reply, hear+tones, reading true/false, role-play from memory
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: errs.append(str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='zero'; S.me.name='New'; S.set.k27={snd:1,d:{}}; S.set.in48={t:Date.now(),goal:'chat',mins:30,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; zRenderHome()"); pg.wait_for_timeout(500)
    print('CARD:',pg.locator('#z53').inner_text().replace('\n',' | ')[:160])
    print('parts:',[x.inner_text().split('\n')[0]+' ['+('|'.join(b.inner_text() for b in x.locator('button').all()))+']' for x in pg.locator('#z53 .z53p').all()])
    part=lambda name: pg.locator('#z53 .z53p:has-text("%s") button.btn'%name).click()
    sb=lambda: pg.inner_text('#sheet-body').replace('\n',' | ')
    # dialogues
    part('Hội thoại'); pg.wait_for_timeout(300); pg.click('#sheet-body button:has-text("Be Anna")'); pg.wait_for_timeout(3000)
    print('ROLE: my line hidden:',pg.locator('#sheet-body .z53dl.me span[hidden]').count(),'| cue:',pg.locator('#sheet-body .z52cue').inner_text())
    pg.click('#sheet-body button:has-text("I said it · check")'); pg.wait_for_timeout(300); print(' after check:',pg.locator('#sheet-body .z53dl.me').first.inner_text().replace('\n',' / '))
    T("closeSheet(); zRenderHome()"); pg.wait_for_timeout(200)
    # oral: swap drills
    part('Thực hành nói'); pg.wait_for_timeout(300); print('SUB intro:',sb()[80:330])
    for d in range(4):
        pg.click('#sheet-body button:has-text("Now you say them")'); pg.wait_for_timeout(200)
        if d==0: print('SUB ask:',sb()[80:260])
        while pg.locator('#sheet-body button:has-text("I said it · show me")').count():
            pg.click('#sheet-body button:has-text("I said it · show me")'); pg.wait_for_timeout(120)
            if d==0 and pg.locator('#sheet-body .rf-reveal').count() and 'shown' not in dir(): shown=1; print('SUB reveal:',pg.locator('#sheet-body .rf-reveal').inner_text().replace('\n',' '))
            pg.click('#sheet-body #rf-next'); pg.wait_for_timeout(150)
        pg.wait_for_timeout(200)
    pg.wait_for_timeout(400); print('after oral, back home, oral ✓:', 'today' in pg.locator('#z53 .z53p:has-text("Thực hành nói")').inner_text())
    # written: fix
    part('Thực hành viết'); pg.wait_for_timeout(400); print('FIX:',sb()[80:330]); T("closeSheet(); zRenderHome()")
    # listening: reply + tone
    part('Thực hành nghe'); pg.wait_for_timeout(600); print('REPLY:',sb()[80:330])
    for k in range(5):
        pg.locator('#sheet-body .z13opt').first.click(); pg.wait_for_timeout(150)
        if k==0: print(' reveal:',pg.locator('#sheet-body .rf-reveal').inner_text().replace('\n',' / '))
        pg.click('#sheet-body #rf-next'); pg.wait_for_timeout(450)
    print(' score:',sb()[-40:]); pg.click('#sheet-body button:has-text("Next")'); pg.wait_for_timeout(600)
    print('TONE:',sb()[80:300])
    for k in range(6): pg.locator('#sheet-body .z13opt').first.click(); pg.wait_for_timeout(120); pg.click('#sheet-body #rf-next'); pg.wait_for_timeout(450)
    pg.click('#sheet-body button:has-text("Next")'); pg.wait_for_timeout(400)
    # reading
    part('Đọc hiểu'); pg.wait_for_timeout(300); pg.locator('#sheet-body .z54s').nth(3).click(); pg.wait_for_timeout(150)
    print('READ:',sb()[70:420])
    for i in range(4): pg.locator('#sheet-body .panel:has(.z13opt)').nth(i).locator('.z13opt').first.click(); pg.wait_for_timeout(100)
    print(' end:',pg.locator('#sheet-body button.primary').last.inner_text(),'| fb:',pg.locator('#sheet-body .panel:has(.z13opt)').nth(1).inner_text().replace('\n',' / ')[-60:])
    pg.screenshot(path='/tmp/t54.png'); pg.locator('#sheet-body button.primary').last.click(); pg.wait_for_timeout(400)
    print('HOME parts now:',[x.inner_text().split('\n')[0] for x in pg.locator('#z53 .z53p').all()])
    br.close()
print('ERR',errs or 'none')
