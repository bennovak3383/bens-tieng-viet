# 72: five more scenes (café, apartment, post office, hair salon, market): each opens, every person answers, the check plays through
import json
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); bad=[]; pg.on('response',lambda r: bad.append(r.url) if ('/img/' in r.url and r.status>=400) else None)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(500); T("location.hash='hub'"); pg.wait_for_timeout(500)
    pg.locator('.z59-scn').click(); pg.wait_for_timeout(700); names=[x.locator('b').inner_text() for x in pg.locator('.z63m').all()]; print('scenes in the menu:',len(names),names[9:])
    T("closeSheet()")
    for sid in ['caf','apt','pos','sal','mkt']:
        T("z63Scene('%s')"%sid); pg.wait_for_timeout(700); n=pg.locator('.z63p').count(); who=[]
        for i in range(n):
            pg.locator('.z63p[data-i="%d"]'%i).click(force=True); pg.wait_for_timeout(250); who.append(pg.locator('.z63who').inner_text().replace('\n',' = ')+' → '+' / '.join(x.inner_text().split('\n')[0] for x in pg.locator('.z63ln').all()))
        acts=pg.locator('.z63a').count(); pics=pg.locator('.z63a .ic img').count(); props=pg.locator('.z63svg image').count()
        print(sid,'| people',n,'| actions',acts,'with a picture',pics,'| things drawn from the picture set',props); [print('   ',w) for w in who]
        pg.locator('.z62tabs button').nth(1).click(); pg.wait_for_timeout(300); k=0
        while pg.locator('.z60end').count()==0 and k<40:
            st=pg.locator('.z60stage'); t=st.get_attribute('data-t'); a=st.get_attribute('data-a'); k+=1
            if t=='tap':
                i=T("Z63.d.scenes.filter(s=>s.id==='%s')[0].people.findIndex(p=>p.k===%s)"%(sid,json.dumps(a,ensure_ascii=False)))
                if k==1: pg.locator('.z63p[data-i="%d"]'%((i+1)%n)).click(force=True); pg.wait_for_timeout(200)
                pg.locator('.z63p[data-i="%d"]'%i).click(force=True)
            else: pg.locator('.z63o[data-k=%s]'%json.dumps(a,ensure_ascii=False)).click()
            pg.wait_for_timeout(900)
        print('    check:',pg.locator('.z60big').inner_text(),'| saved best:',T("S.set.s63.%s.best"%sid),'| questions:',k)
        pg.locator('.z62tabs button').nth(2).click() if pg.locator('.z62tabs button').count()>2 else None; pg.wait_for_timeout(300)
        T("closeSheet()"); pg.wait_for_timeout(200)
    T("z60Menu()"); pg.wait_for_timeout(600); print('scene word sets offered in Games:',T("Z60.extra.reduce(function(a,f){ return a.concat(f()) },[]).filter(function(s){ return /^S(caf|apt|pos|sal|mkt)$/.test(s.id) }).map(function(s){ return s.t+' '+s.words.length }).join(', ')")); T("closeSheet()")
    pg.wait_for_timeout(400); print('image files that failed to load:',bad or 'none')
    br.close()
print('ERR',errs or 'none')
