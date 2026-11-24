# v101: Today has the painted strip (pictures load), today's route with Start comes first, laptop puts the lesson on the right,
# the older duplicate "How this app works" button is hidden, Start still opens the first step
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    for w,hgt in [(1440,900),(390,844)]:
        ctx=br.new_context(viewport={'width':w,'height':hgt},service_workers='block'); pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
        pg.goto(B+'/'); pg.wait_for_timeout(1200); T("S.set.ob7=1;S.me=S.me||{};S.me.name='Ben';save();sessionStorage.setItem('z98','1')"); pg.reload(); pg.wait_for_timeout(2000)
        pg.locator('nav button',has_text='Today').first.click(); pg.wait_for_timeout(1200)
        loaded=T("[].filter.call(document.querySelectorAll('.z101strip img'),function(i){return i.naturalWidth>0&&i.offsetParent}).length")
        old=T("(function(){var s=document.querySelector('#v-home .zhero .z12scene');return s?s.offsetHeight:0})()")
        route=pg.locator('#z-plan').bounding_box(); lesson=pg.locator('#z53').bounding_box(); start=pg.locator('#z-plan .btn.primary').first.bounding_box()
        dup=T("[].filter.call(document.querySelectorAll('#z-home>button'),function(b){return b.offsetParent&&/how this app works/i.test(b.textContent)}).length")
        print(w,'| painted pictures showing:',loaded,'| old drawing hidden:',old==0,'| route above or beside lesson:',route['y']<lesson['y'] or route['x']<lesson['x'],
              '| lesson on the right:',lesson['x']>route['x']+route['width']-1,'| Start visible:',start['y']+start['height']<=hgt,'| how-it-works buttons:',dup)
        if w==1440:
            pg.locator('#z-plan .btn.primary').first.click(); pg.wait_for_timeout(1200); print('Start opens a step:',T("!document.getElementById('sheet').hidden"))
        ctx.close()
    print('ERR',errs or 'none')
