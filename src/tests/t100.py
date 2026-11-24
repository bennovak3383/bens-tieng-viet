# v100: laptop Home in two columns with Start visible, drawn shortcut icons, Sharp ears without picture hints, phone Home unchanged
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    for w,hgt in [(1440,900),(1280,800),(390,844)]:
        ctx=br.new_context(viewport={'width':w,'height':hgt},service_workers='block'); pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
        pg.goto(B+'/'); pg.wait_for_timeout(1200); T("S.set.ob7=1;S.me=S.me||{};S.me.name='Ben';save();sessionStorage.setItem('z98','1')"); pg.reload(); pg.wait_for_timeout(2500)
        st=pg.locator('#z-hub .z59day .btn.primary').first.bounding_box(); rooms=pg.locator('#z-hub .z59grid').bounding_box(); day=pg.locator('#z-hub .z59day').bounding_box()
        two=rooms['x']>day['x']+day['width']-1
        print(w,'| two columns:',two,'| Start visible without scrolling:',st['y']+st['height']<=hgt,'| drawn icons:',pg.locator('#z-hub .z100i svg').count(),'| emoji pictures left in strip:',pg.locator('#z-hub .z74strip .pi img').count())
        if w==1440:
            T("zEar10()"); pg.wait_for_timeout(900); print('Sharp ears picture hints shown:',T("[].filter.call(document.querySelectorAll('.z10opts .z10pic'),function(e){return e.offsetParent}).length"),'| choices:',pg.locator('.z10opt').count())
        ctx.close()
    print('ERR',errs or 'none')
