# 80: simpler Home (today first, numbered path, smaller rooms), tap any word anywhere, the handbook
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
SETUP="S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()"
def tapword(pg,loc,fx=.5,fy=.5):
    bb=loc.bounding_box(); pg.mouse.click(bb['x']+bb['width']*fx,bb['y']+bb['height']*fy); pg.wait_for_timeout(350)
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block')
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2200); T(SETUP); pg.wait_for_timeout(500); T("location.hash='hub'"); pg.wait_for_timeout(1300)
    print('HOME order:',T("[].map.call(document.getElementById('z-hub').children,function(c){ return c.className.split(' ')[0]||c.tagName }).join(' > ')"))
    print(' today card is above the rooms:',T("document.querySelector('#z-hub .z59day').getBoundingClientRect().top<document.querySelector('#z-hub .z59grid').getBoundingClientRect().top"),'| rooms',pg.locator('#z-hub .z59t').count(),'in',T("getComputedStyle(document.querySelector('#z-hub .z59grid')).gridTemplateColumns.split(' ').length"),'columns | tools',pg.locator('.z74strip .z74b').count(),'| nothing removed (old five still there):',T("['rev','sg','fc','add','all'].every(function(k){ return !!document.querySelector('.z74-'+k) })"))
    print(' path:',pg.locator('.z80ph b').inner_text(),'| dots',pg.locator('.z80d').count(),'| done',pg.locator('.z80d.done').count(),'| now',pg.locator('.z80d.now').inner_text(),'| start button still there:',pg.locator('.z59day .btn.primary').count()==1)
    pg.locator('.z80d.done').first.click(); pg.wait_for_timeout(600); print(' tapping lesson 1 opens it:',pg.locator('#sheet-body h1').inner_text()[:40]); T("closeSheet()"); pg.wait_for_timeout(300)
    pg.locator('.z80map').click(); pg.wait_for_timeout(500); print(' course map link opens the map:','course map' in pg.locator('#sheet-body').inner_text().lower()[:200]); T("closeSheet()"); pg.wait_for_timeout(300)
    print('TAP ANY WORD: words known',T("Object.keys(z80Dict()).length"))
    tapword(pg,pg.locator('.z59dt h2'),.55,.3); print(' lesson title:',pg.locator('.z80pop .z61pw b').all_inner_texts(),pg.locator('.z80pop .z61pw span').all_inner_texts(),'| buttons:',pg.locator('.z80pop .z61sv').all_inner_texts(),'| tip went away:',pg.locator('.z80tip').count()==0)
    tapword(pg,pg.locator('.z59dt p.muted')); print(' English line under it → no popup:',pg.locator('.z80pop').count()==0)
    tapword(pg,pg.locator('.z59hero .z59bub')); print(' "Welcome to your lesson." → no popup:',pg.locator('.z80pop').count()==0)
    tapword(pg,pg.locator('.z59dt h2'),.55,.3); pg.locator('.z59t').first.click(); pg.wait_for_timeout(600); print(' a button still does its own job and closes the popup: sheet open',T("!document.getElementById('sheet').hidden"),'| popup',pg.locator('.z80pop').count()); T("closeSheet()"); pg.wait_for_timeout(300)
    print(' phrase beats single word:',T("(function(){ var d=document.createElement('p'); d.id='t80'; d.style.cssText='position:fixed;left:20px;top:300px;z-index:999;background:#fff;font-size:22px;padding:6px'; d.textContent='Tôi muốn uống cà phê sữa đá.'; document.body.appendChild(d); return true })()"),end=' ')
    tapword(pg,pg.locator('#t80'),.62,.5); print(pg.locator('.z80pop .z61pw b').all_inner_texts(),pg.locator('.z80pop .z61pw span').all_inner_texts(),'| sentence button:',pg.locator('.z80pop .z61sv').first.inner_text()[:34])
    T("document.getElementById('t80').textContent='Please sign in to continue.'"); tapword(pg,pg.locator('#t80'),.3,.5); print(' English sentence with "to", "in" → no popup:',pg.locator('.z80pop').count()==0); T("document.getElementById('t80').remove()")
    T("(function(){ var a=z61All(); z61Read(a[0],0) })()"); pg.wait_for_timeout(900)
    if pg.locator('.z61story .zw').count():
        pg.locator('.z61story .zw').first.click(); pg.wait_for_timeout(400); print(' stories keep their own popup: story popup',pg.locator('.z61pop:not(.z80pop):not([hidden])').count(),'| new popup',pg.locator('.z80pop').count())
    else: print(' (no story opened in this run)')
    T("closeSheet()"); pg.wait_for_timeout(300)
    pg.locator('.z74-book').click(); pg.wait_for_timeout(700); print('HANDBOOK: links',pg.locator('.z80bi').count(),'| word rows',pg.locator('.z80w').count(),'|',pg.locator('#sheet-body p.small.muted').first.inner_text())
    pg.locator('#sheet-body .z74q').fill('coffee'); pg.wait_for_timeout(300); print(' search "coffee":',pg.locator('.z80w b').all_inner_texts()[:4]); pg.locator('.z80w').first.click(); pg.wait_for_timeout(400); print(' tapping a row shows the word card:',pg.locator('.z80pop .z61pw b').all_inner_texts())
    pg.locator('.z80pop .x').click(); pg.wait_for_timeout(200); pg.locator('#sheet-body .z74q').fill(''); pg.locator('.z80bi').first.click(); pg.wait_for_timeout(700); print(' first link goes to the tones room:',T("location.hash"))
    T("location.hash='hub'"); pg.wait_for_timeout(600); T("z74Find()"); pg.wait_for_timeout(500); pg.locator('#sheet-body .z74q').fill('handbook'); pg.wait_for_timeout(300); print(' "find anything" knows the handbook:',pg.locator('.z74res button').count()>=1)
    br.close()
print('ERR',errs or 'none')
