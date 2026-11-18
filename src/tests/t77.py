# 77: movement (screens glide, parts arrive, sparkle on a right answer), sharper pictures, drawn Saigon places, and "reduce motion" switches it all off
import json
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
SETUP="S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()"
def solve(pg):
    tiles=pg.locator('.z60cols .z60tile'); n=tiles.count(); left=[i for i in range(n) if 'r' not in (tiles.nth(i).get_attribute('class') or '').split()]; right=[i for i in range(n) if i not in left]
    tiles.nth(left[0]).click()
    for j in right:
        tiles.nth(j).click(); pg.wait_for_timeout(60)
        if 'ok' in (tiles.nth(left[0]).get_attribute('class') or ''): return True
        pg.wait_for_timeout(500); tiles.nth(left[0]).click()
    return False
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    for mode in ('no-preference','reduce'):
        ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block',reduced_motion=mode); pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); bad=[]; pg.on('response',lambda r: bad.append(r.url) if r.status>=400 else None); out=[]; pg.on('request',lambda r: out.append(r.url) if 'wikimedia' in r.url else None)
        T=lambda c: pg.evaluate('(c)=>__T(c)',c)
        pg.goto(B+'/'); pg.wait_for_timeout(2000); T(SETUP); pg.wait_for_timeout(500); print('=== motion:',mode,'===')
        if mode=='no-preference':
            print('pictures: size of a word picture file:',T("new Promise(function(ok){ var i=new Image(); i.onload=function(){ ok(i.naturalWidth+'×'+i.naturalHeight) }; i.src='img/p/chair.webp' })"),'| bàn (table) uses:',T("Z70.map['bàn']"),'| its file loads:',T("new Promise(function(ok){ var i=new Image(); i.onload=function(){ ok(i.naturalWidth===256) }; i.onerror=function(){ ok(false) }; i.src='img/p/x-table.webp' })"))
            print('offline list has the drawings and the table:',T("fetch('data/offline.json').then(function(r){ return r.json() }).then(function(j){ return [j.files.indexOf('data/sgart.json')>=0, j.files.indexOf('img/p/x-table.webp')>=0, j.files.length] })"))
        T("location.hash='fc'"); pg.wait_for_timeout(60); print('screen change: animation on the new screen:',T("getComputedStyle(document.querySelector('.view:not([hidden])')).animationName")); T("location.hash='hub'"); pg.wait_for_timeout(500)
        T("z60Menu()"); pg.wait_for_timeout(80); print('sheet opens: animation:',T("getComputedStyle(document.getElementById('sheet-body')).animationName"),'| parts marked to arrive:',pg.locator('.z77dl,.z77in').count())
        pg.wait_for_timeout(1500); print('  1.5 s later the marks are gone:',pg.locator('.z77dl,.z77in').count()==0)
        pg.locator('.z60g').first.click(); pg.wait_for_timeout(1300); ok=solve(pg); print('match up: right pair found:',ok,'| sparkles:',pg.locator('.z77burst').count(),'| right-first-time counter:',T("document.querySelector('.z60sc.ok').textContent.trim()"))
        pg.wait_for_timeout(1200); print('  sparkles removed:',pg.locator('.z77burst').count()==0,'| tap makes the picture squish:',end=' ')
        t=pg.locator('.z60cols .z60tile.r:not(.ok)').first; t.dispatch_event('pointerdown'); print(T("!!document.querySelector('.z77tap')")); T("closeSheet()")
        T("z74Saigon('place')"); pg.wait_for_timeout(1200); print('Places board: rows',pg.locator('.z74sgi').count(),'| rows with a drawing:',pg.locator('.z74sgi.z77has .z77th svg').count())
        pg.locator('.z74sgh').first.click(); pg.wait_for_timeout(700)
        print('  open item: drawing',pg.locator('.z74sgx:not([hidden]) .z77fig svg').count(),'| photo block',pg.locator('.z74sgx:not([hidden]) .z75fig').count(),'| real-photo link kept:',pg.locator('.z74sgx:not([hidden]) .z77real a').get_attribute('href')[:60],'| links kept on the board:',pg.locator('.z77real a').count(),'| rider moves:',T("getComputedStyle(document.querySelector('.z74sgx:not([hidden]) .z77rd')).animationName"),'| requests to Wikimedia:',len(out))
        T("z74Saigon('place')"); pg.wait_for_timeout(600); print('  opening the board twice does not double the drawings:',pg.locator('.z77fig').count()==12)
        T("z74Saigon('sign')"); pg.wait_for_timeout(600); print('  other boards unchanged (no drawings):',pg.locator('.z77fig').count()==0,'| rows',pg.locator('.z74sgi').count()); T("closeSheet()")
        print('  missing files:',[b for b in bad if '/api/' not in b] or 'none'); ctx.close()
    br.close()
print('ERR',errs or 'none')
