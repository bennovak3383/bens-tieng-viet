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
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.k27={snd:1,d:{u01:{t:1,o:4,on:4,g:5,gn:5,s:4,sn:4},u02:{t:1,o:1,on:4,g:1,gn:5,s:1,sn:4},u03:{t:1}}}; S.fc['k02_3|l']={due:Date.now(),ivl:0,lapses:4}; S.fc['k01_5|p']={due:Date.now(),ivl:0,lapses:2}; save(); try{closeSheet()}catch(e){}")
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Ben'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(2000)
    T("Z39.last=Z27.units[0]; z27Say(Z27.units[0].ex.slice(0,1),function(){},{s:0,sn:0})"); pg.wait_for_timeout(300); pg.click('text=I said it · show me'); pg.wait_for_timeout(200)
    b=pg.locator('#sheet-body .z36rec button').first; b.click(); pg.wait_for_timeout(1000); b.click(); pg.wait_for_timeout(1500)
    tp=ctx.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.set_viewport_size({'width':1000,'height':900}); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1200)
    tp.locator('.stu').first.click(); tp.wait_for_timeout(1500)
    tp.locator('button:has-text("hỏi/ngã")').first.click(); tp.wait_for_timeout(800)
    tp.click('text=Refresh'); tp.wait_for_timeout(1500)
    t=tp.inner_text('#app'); i=t.find('Tuần này'); print(t[i:i+1500])
    tp.screenshot(path='/tmp/t45.png')
    br.close()
print('ERR',errs or 'none')
