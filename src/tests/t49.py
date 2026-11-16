# 49: story loop — listen, read, retell (recorded, sent to teacher), 4-word cap
import json, urllib.request
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
def call(path,method='GET',body=None):
    r=urllib.request.Request(B+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(r) as f: return json.loads(f.read())
key=call('/api/setup','POST',{}).get('key')
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']); ctx=br.new_context(viewport={'width':390,'height':844})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Ben'; var d={}; Z27.units.slice(0,7).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:1,goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; zRenderHome()")
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Ben'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(1500)
    print('CARD1:',pg.locator('.z49c').inner_text().replace('\n',' | '))
    pg.click('.z49c button.primary'); pg.wait_for_timeout(600)
    print('blind mode:',pg.locator('#sheet-body .z7story.zblind').count())
    # tap 5 words: 5th should be refused
    ws=pg.locator('#sheet-body .z7story .zw'); n=ws.count(); picked=0; i=0
    while picked<5 and i<n:
        k=ws.nth(i).get_attribute('data-k') ; ws.nth(i).click(); pg.wait_for_timeout(120); i+=1; picked=T("Object.keys(S.w).length") if picked<4 else picked+1
    print('focus words saved:',T("z49Focus(zChId(z38Story(Z27.st[0]),0)).length"),' cap msg:',pg.locator('#sheet-body .zgloss').inner_text()[-80:])
    pg.click('#sheet-body button:has-text("I read it")'); pg.wait_for_timeout(400)
    for _ in range(12):
        b=pg.locator('#sheet-body button:has-text("Show the answer"), #sheet-body #rf-next, #sheet-body button:has-text("Next question"), #sheet-body button:has-text("Finish the chapter")')
        if b.count()==0: break
        b.first.click(); pg.wait_for_timeout(250)
    pg.wait_for_timeout(500)
    print('CARD2:',pg.locator('.z49c').inner_text().replace('\n',' | '))
    pg.click('.z49c button:has-text("now anyway")'); pg.wait_for_timeout(600); print('day2 mode blind?',pg.locator('#sheet-body .z7story.zblind').count())
    pg.click('#sheet-body button:has-text("I read it")'); pg.wait_for_timeout(300)
    for _ in range(12):
        b=pg.locator('#sheet-body button:has-text("Show the answer"), #sheet-body #rf-next')
        if b.count()==0: break
        b.first.click(); pg.wait_for_timeout(250)
    pg.wait_for_timeout(500)
    print('CARD3:',pg.locator('.z49c').inner_text().replace('\n',' | '))
    pg.click('.z49c button:has-text("now anyway")'); pg.wait_for_timeout(500)
    print('RETELL:\n'+pg.inner_text('#sheet-body')[:900])
    pg.screenshot(path='/tmp/t49a.png')
    rb=pg.locator('#sheet-body .z36rec button'); rb.click(); pg.wait_for_timeout(2500); print('clock:',pg.locator('.z49clock').inner_text()); rb.click(); pg.wait_for_timeout(1500)
    pg.click('#sheet-body button:has-text("Send to Thầy")'); pg.wait_for_timeout(2500)
    print('AFTER SEND:',pg.inner_text('#sheet-body')[-400:].replace('\n',' | '))
    pg.click('#sheet-body button:has-text("Tell it again")'); pg.wait_for_timeout(400); print('round2 clock:',pg.locator('.z49clock').inner_text())
    rb=pg.locator('#sheet-body .z36rec button'); rb.click(); pg.wait_for_timeout(1500); rb.click(); pg.wait_for_timeout(1200); pg.click('#sheet-body button:has-text("Send to Thầy")'); pg.wait_for_timeout(2000)
    pg.click('#sheet-body button:has-text("Done")'); pg.wait_for_timeout(500)
    print('card after retell (next story or none):',pg.locator('.z49c').count(), pg.locator('.z49c').inner_text()[:80].replace('\n',' | ') if pg.locator('.z49c').count() else '')
    tp=ctx.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1200)
    tp.locator('.stu').first.click(); tp.wait_for_timeout(1500); tp.click('button:text-is("Retells")'); tp.wait_for_timeout(400)
    t=tp.inner_text('#app'); i=t.find('Retell:'); print('TEACHER:',t[i:i+200].replace('\n',' | '))
    br.close()
print('ERR',errs or 'none')
