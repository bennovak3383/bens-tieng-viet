import json, urllib.request
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
def call(path,method='GET',body=None):
    r=urllib.request.Request(B+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(r) as f: return json.loads(f.read())
key=call('/api/setup','POST',{}).get('key')
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':390,'height':800},device_scale_factor=1)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    bad=[]; pg.on('response',lambda r: bad.append(r.url) if r.status>=400 and 'guide' in r.url else None)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Ben'; S.set.k27={snd:1,d:{}}; save(); try{closeSheet()}catch(e){}; zRenderHome()"); pg.wait_for_timeout(400)
    print('home button:',pg.locator('#z-home .z57h').count()); T("location.hash='more'"); pg.wait_for_timeout(500); print('more tile:',pg.locator('#z-more .z57t').inner_text().replace('\n',' | '))
    pg.click('#z-more .z57t'); pg.wait_for_timeout(1500)
    print('sections:',pg.locator('#sheet-body .z57s').count(),'| toc chips:',pg.locator('#sheet-body .z57toc .chip').count(),'| images:',pg.locator('#sheet-body .z57f img').count())
    pg.locator('#sheet-body .z57toc .chip').nth(4).click(); pg.wait_for_timeout(900); pg.screenshot(path='/tmp/g1.png')
    n=pg.evaluate("Promise.all([].map.call(document.querySelectorAll('#sheet-body .z57f img'),function(i){ i.loading='eager'; return i.decode().then(function(){ return i.naturalWidth>0 },function(){ return false }) }))"); print('images loaded:',n)
    T("closeSheet()"); pg.goto(B+'/#guide'); pg.wait_for_timeout(3200); print('#guide opens sheet:',pg.locator('#sheet-body .z57s').count()>0,'| hash now:',pg.evaluate("location.hash"))
    tc=br.new_context(viewport={'width':1000,'height':900}); tp=tc.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1300)
    tp.click('button:has-text("Hướng dẫn · guide")'); tp.wait_for_timeout(1200); print('teacher guide panels:',tp.locator('#app .panel').count(),'| images:',tp.locator('#app figure img').count(),'| h1:',tp.locator('#app h1').inner_text())
    tp.screenshot(path='/tmp/g2.png'); tp.click('button:has-text("For students")'); tp.wait_for_timeout(900); print('student tab panels:',tp.locator('#app .panel').count(),'| h1:',tp.locator('#app h1').inner_text())
    tp.click('button:has-text("All students")'); tp.wait_for_timeout(600); print('back to list ok:',tp.locator('h1').inner_text()[:22])
    print('bad requests:',bad)
    br.close()
print('ERR',errs or 'none')
