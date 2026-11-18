# v98: Home tiles show painted art that changes; opening scene shows once per app open and goes away
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; out='/home/claude/work/shots/'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':852},service_workers='block',device_scale_factor=2)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c); bad=[]; pg.on('response',lambda r: bad.append(r.url) if r.status>=400 else None)
    pg.goto(B+'/'); pg.wait_for_timeout(2200); print('first ever open (not set up yet) has no opening scene:',pg.locator('#z98sp').count()==0)
    T("S.set.ob7=1;S.me=S.me||{};S.me.name='Ben';save()"); pg.reload(); pg.wait_for_timeout(1500)
    print('opening scene shows:',pg.locator('#z98sp').count()==1,'| cards:',pg.locator('#z98sp .cd').count()); pg.screenshot(path=out+'i-open.png')
    pg.wait_for_timeout(2300); print('gone after about 3 s:',pg.locator('#z98sp').count()==0)
    print('tiles with art:',pg.locator('.z59t.z98t').count(),'| pictures loaded:',T("[].filter.call(document.querySelectorAll('.z98ph img'),function(i){return i.naturalWidth>0}).length"),'of',pg.locator('.z98ph img').count())
    a=T("[].map.call(document.querySelectorAll('.z98ph'),function(p){ return [].findIndex.call(p.children,function(i){return i.classList.contains('on')}) }).join('')"); pg.screenshot(path=out+'i-home.png'); pg.wait_for_timeout(9500)
    b=T("[].map.call(document.querySelectorAll('.z98ph'),function(p){ return [].findIndex.call(p.children,function(i){return i.classList.contains('on')}) }).join('')"); print('art changes over time:',a,'->',b,a!=b)
    pg.locator('.z59-gam').click(); pg.wait_for_timeout(900); print('Games tile still opens games:',pg.locator('#sheet:not([hidden])').count()==1); T("closeSheet()")
    pg.reload(); pg.wait_for_timeout(1200); print('no second opening scene in the same visit:',pg.locator('#z98sp').count()==0)
    print('failed loads:',[u for u in bad if 'home' in u][:3]); print('ERR',errs or 'none')
