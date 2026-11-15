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
    T("micOn&&micOn()"); pg.wait_for_timeout(500)
    # open unit 1 and jump to the Say step directly
    T("Z39.last=Z27.units[0]; window.__sc={s:0,sn:0}; z27Say(Z27.units[0].ex.slice(0,4),function(){ window.__said=1 },window.__sc)"); pg.wait_for_timeout(400)
    for i in range(4):
        pg.click('text=I said it · show me'); pg.wait_for_timeout(300)
        if pg.locator('#sheet-body .z36rec button').count():
            pg.locator('#sheet-body .z36rec button').first.click(); pg.wait_for_timeout(1500); pg.locator('#sheet-body .z36rec button').first.click(); pg.wait_for_timeout(1500)
            print(i,'graph drawn:',pg.locator('#sheet-body .z13graph').count(), '|', (pg.inner_text('#sheet-body .z13graph') if pg.locator('#sheet-body .z13graph').count() else pg.inner_text('#sheet-body')[-150:]).replace('\n',' ')[:140])
            if i==0: pg.screenshot(path='/tmp/say40.png')
        else: print(i,'no recorder (line 4 expected)')
        pg.click('text=I had it'); pg.wait_for_timeout(300)
    print('said done:',T("window.__said"),'score',T("JSON.stringify(window.__sc)"))
    pg.wait_for_timeout(1500)
    st=call('/api/state') if False else None
    # teacher
    tp=ctx.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.set_viewport_size({'width':1000,'height':900}); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1200)
    tp.locator('.stu').first.click(); tp.wait_for_timeout(1200)
    txt=tp.inner_text('#app'); i=txt.find('Recordings ('); print('teacher recordings:',txt[i:i+20])
    chips=tp.locator('button:has-text("hỏi/ngã")'); print('tone chips:',chips.count())
    if chips.count(): chips.first.click(); tp.wait_for_timeout(800); print('chip after click:',chips.first.inner_text())
    # student gets it back
    pg.reload(); pg.wait_for_timeout(2500); T("try{closeSheet()}catch(e){}"); T("accPull().then(function(){ zRenderHome() })"); pg.wait_for_timeout(1500)
    print('fix slip on home:',pg.locator('#z40fix').count(), '|', pg.inner_text('#z40fix')[:200].replace('\n',' / ') if pg.locator('#z40fix').count() else '')
    if pg.locator('#z40fix').count(): pg.screenshot(path='/tmp/fix40.png'); pg.click('text=Fix them now'); pg.wait_for_timeout(600); print('opens:',pg.inner_text('#sheet-body')[:120].replace('\n',' / '))
    br.close()
print('ERR',errs or 'none')
