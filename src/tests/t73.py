# 73: sentence builder stages 4 and 5 (six new patterns), and the animals board (tap every animal, play the check through)
import json
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); bad=[]; pg.on('response',lambda r: bad.append(r.url) if ('/img/' in r.url and r.status>=400) else None)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(500)
    # builder: locked until earned, then every new pattern in its three forms
    T("S.set.b64={n:0,seen:{}}; save(); z64Build(0,1)"); pg.wait_for_timeout(900)
    print('stage buttons:',[x.inner_text().replace('\n',' ') for x in pg.locator('.z64stages button').all()])
    pg.locator('.z64stages button').nth(3).click(); pg.wait_for_timeout(300); print('tap stage 4 while locked →',pg.locator('.z64note').inner_text().replace('\n',' | '))
    T("S.set.b64={n:0,seen:{},open:5}; save()"); n=0
    for stg in (4,5):
        for si in range(3):
            T("z64Build(%d,%d)"%(si,stg)); pg.wait_for_timeout(600); out=[]
            sent=lambda: pg.locator('.z64s').inner_text().replace('\n','')+' = '+pg.locator('.z64en').inner_text()
            out.append(sent()); pg.locator('.z64o').nth(2).click(); pg.wait_for_timeout(250); out.append(sent())
            slots=pg.locator('.z64slot').count()
            if slots>1: pg.locator('.z64slot').nth(1).click(); pg.wait_for_timeout(200); pg.locator('.z64o').nth(3).click(); pg.wait_for_timeout(250); out.append(sent())
            for fi in (1,2): pg.locator('.z64forms button').nth(fi).click(); pg.wait_for_timeout(250); out.append(sent())
            pics=pg.locator('.z64pic img, .z64pic svg').count(); n+=1
            print('stage',stg,'|',pg.locator('.z64st button[aria-pressed="true"] b').inner_text(),'| picture:',pics,'| options with a picture:',pg.locator('.z64o .ic img, .z64o .ic svg').count(),'of',pg.locator('.z64o').count()); [print('     ',o) for o in out]
    print('patterns in all:',T("z64Structs(z64Data()).length"),'| sentences counted:',T("S.set.b64.n"),'| by stage:',T("JSON.stringify(S.set.b64.st)")); T("closeSheet()")
    # animals
    T("location.hash='hub'"); pg.wait_for_timeout(400); pg.locator('.z59-scn').click(); pg.wait_for_timeout(800)
    print('animals tile in the scenes menu:',pg.locator('.z73m b').inner_text(),'|',pg.locator('.z73m span').inner_text(),'| menu tiles:',pg.locator('.z63m').count())
    pg.locator('.z73m').click(); pg.wait_for_timeout(700); na=pg.locator('.z73a').count(); seen=[]
    for i in range(na):
        pg.locator('.z73a[data-i="%d"] image'%i).click(force=True); pg.wait_for_timeout(120); seen.append(pg.locator('.z73who b').inner_text()+'='+pg.locator('.z73who div span').inner_text())
    print('animals in the picture:',na,'| each answers a tap:',len(set(seen)),'|',', '.join(seen)); print('  lines:',[x.inner_text().replace('\n',' = ') for x in pg.locator('.z73ln').all()],'|',pg.locator('.z60tip').last.inner_text())
    pg.locator('.z62tabs button').nth(1).click(); pg.wait_for_timeout(400); k=0; kinds=set()
    while pg.locator('.z60end').count()==0 and k<14:
        st=pg.locator('.z60stage'); a=st.get_attribute('data-a'); kinds.add(st.get_attribute('data-t')); k+=1
        if k==1: pg.locator('.z73o:not([data-k=%s])'%json.dumps(a,ensure_ascii=False)).first.click(); pg.wait_for_timeout(200)
        pg.locator('.z73o[data-k=%s]'%json.dumps(a,ensure_ascii=False)).click(); pg.wait_for_timeout(2100)
    print('check:',pg.locator('.z60big').inner_text(),'| kinds of question:',sorted(kinds),'| saved best:',T("S.set.s63.ani.best"),'| heard:',T("Object.keys(S.set.s63.ani.seen).length")); T("closeSheet()")
    print('animals word set in Games:',T("Z60.extra.reduce(function(a,f){ return a.concat(f()) },[]).filter(function(s){ return s.id==='Sani' }).map(function(s){ return s.t+' '+s.words.length+' words' }).join('')"))
    pg.wait_for_timeout(400); print('image files that failed to load:',bad or 'none')
    br.close()
print('ERR',errs or 'none')
