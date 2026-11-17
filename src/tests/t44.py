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
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500); T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.k27={snd:1,d:{}}; save(); try{closeSheet()}catch(e){}")
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Ben'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(2000)
    print('due before:',T("z44Due()"))
    T("Z27.units.forEach(function(u){ if(u.lv==='A1') z27St().d[u.id]={t:1} }); save(); zRenderHome()"); pg.wait_for_timeout(400)
    print('due after A1:',T("z44Due()"),'| card:',pg.locator('#z27 .z44c').count()); pg.screenshot(path='/tmp/c44.png')
    pg.get_by_role('button',name='Take the E1 check').click(); pg.wait_for_timeout(400); pg.click('text=Start part 1'); pg.wait_for_timeout(300)
    for i in range(20):
        pg.locator('#sheet-body .z13opt').first.click(); pg.wait_for_timeout(80); pg.get_by_role('button',name='Next',exact=True).click(); pg.wait_for_timeout(80)
    print('after part 1:',pg.inner_text('#sheet-body')[:120].replace('\n',' / '))
    pg.click('text=Start part 2'); pg.wait_for_timeout(300)
    for i in range(8):
        b=pg.locator('#sheet-body .z36rec button').first; b.click(); pg.wait_for_timeout(1000); b.click(); pg.wait_for_timeout(700)
        if i==0: print('q1:',pg.inner_text('#sheet-body')[:160].replace('\n',' / '))
        pg.click('text=Next question'); pg.wait_for_timeout(200)
    print('end:',pg.inner_text('#sheet-body')[:250].replace('\n',' / '))
    print('saved:',T("JSON.stringify(z27St().lc44)"))
    pg.locator('#sheet-body button:has-text("Done")').click(); pg.wait_for_timeout(1500); T("accPush(true)"); pg.wait_for_timeout(1500)
    tp=ctx.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.set_viewport_size({'width':1000,'height':900}); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1200)
    tp.locator('.stu').first.click(); tp.wait_for_timeout(1500)
    t=tp.inner_text('#app'); i=t.find('Kiểm tra E1'); print('teacher panel:',t[i:i+260].replace('\n',' / '))
    tp.locator('button:has-text("Level checks")').click(); tp.wait_for_timeout(300); print('check recordings shown:',tp.locator('.rec').count())
    tp.locator('label:has-text("Introduce yourself") input').check(); tp.locator('label:has-text("Order food") input').check()
    tp.locator('button:has-text("Passed · open E2")').click(); tp.wait_for_timeout(1200)
    t=tp.inner_text('#app'); i=t.find('Marked'); print('teacher after:',t[i:i+80])
    pg.reload(); pg.wait_for_timeout(2500); T("accPull()"); pg.wait_for_timeout(1500); print('student level now:',T("z27St().t"),'| note:',T("(ACCN[0]||{}).text"))
    br.close()
print('ERR',errs or 'none')
