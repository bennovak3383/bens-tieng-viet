# 58: "open everything" for one student, set on the teacher page
import json, urllib.request
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
def call(path,method='GET',body=None):
    r=urllib.request.Request(B+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(r) as f: return json.loads(f.read())
key=call('/api/setup','POST',{}).get('key')
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':390,'height':844})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Ben'; var d={}; Z27.units.slice(0,2).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; zRenderHome()")
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Ben'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(1500)
    def state(tag):
        T("location.hash='prac'"); pg.wait_for_timeout(400); tile=pg.locator('#z-prac .settile:has-text("Truyện")'); vis=tile.count() and tile.first.is_visible()
        T("location.hash='home'"); pg.wait_for_timeout(400)
        print(tag,'| units open:',T("z27N()"),'of',T("Z27.units.length"),'| lessons open:',T("z53Ls().filter(z53Open).length"),'| stories open:',T("Z27.st.filter(z38Open).length"),'| Stories tile shown:',bool(vis),'| voice note:',T("z50VnOn()"),'| units done:',T("Object.keys(z27St().d).length"))
    state('BEFORE')
    tp=ctx.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1300); tp.locator('.stu').first.click(); tp.wait_for_timeout(1500)
    sp=tp.locator('.panel:has(h2:has-text("Lộ trình"))'); sp.locator('label:has-text("Open everything") input').check(); sp.locator('button:has-text("Save for this student")').click(); tp.wait_for_timeout(1000); print('teacher msg:',sp.locator('p.small').first.inner_text())
    T("accPull(false)"); pg.wait_for_timeout(2500); state('AFTER ')
    print('home note:',pg.locator('#z53 .z58n').count(),'| story card:',pg.locator('.z49c').count())
    pg.click('#z53 button:has-text("Lộ trình")'); pg.wait_for_timeout(300); print('locked lessons on map:',pg.locator('#sheet-body .z53l.lock').count()); pg.locator('#sheet-body .z53l').nth(7).click(); pg.wait_for_timeout(300)
    print('E2 lesson parts:',[x.inner_text().split('\n')[0]+' ['+'|'.join(b.inner_text() for b in x.locator('button').all())+']' for x in pg.locator('#sheet-body .z53p').all()][:4])
    pg.click('#sheet-body .z53p:has-text("Mẫu câu") button.btn'); pg.wait_for_timeout(500); print('opens a later structure:',pg.inner_text('#sheet-body')[:160].replace('\n',' | ')); T("closeSheet()")
    T("location.hash='story'"); pg.wait_for_timeout(600); print('stories page lists:',' | '.join(x for x in pg.inner_text('body').split('\n') if 'Mike' in x or 'course' in x.lower())[:260].replace('\n',' | '))
    tp.reload(); tp.wait_for_timeout(1300); tp.locator('.stu').first.click(); tp.wait_for_timeout(1500); sp=tp.locator('.panel:has(h2:has-text("Lộ trình"))'); print('box still ticked after reload:',sp.locator('label:has-text("Open everything") input').is_checked())
    sp.locator('button:has-text("Follow the class again")').click(); tp.wait_for_timeout(1500); T("accPull(false)"); pg.wait_for_timeout(2500); state('OFF   ')
    br.close()
print('ERR',errs or 'none')
