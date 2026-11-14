# Version 27 test, teacher side: review and edit a core unit, the app picks it up, the student panel shows core progress, recording page lists the core lines.
import json, urllib.request
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
def call(path,method='GET',body=None,headers=None):
    r=urllib.request.Request(B+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers=dict({'Content-Type':'application/json'},**(headers or {})))
    try:
        with urllib.request.urlopen(r) as f: return f.status,json.loads(f.read())
    except urllib.error.HTTPError as e: return e.code,json.loads(e.read())
print('1 save without the teacher key:', call('/api/t/core','POST',{'u':{'u01':{'note':'x'}}}))
st,j=call('/api/setup','POST',{}); key=j.get('key'); print('1 teacher key made:', bool(key))
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']); ctx=br.new_context(viewport={'width':1100,'height':900})
    # a student who has done two units and signed in
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500); T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.k27={snd:1,d:{u01:{t:1,o:4,on:4,g:5,gn:5,s:4,sn:4},u02:{t:2,o:1,on:4,g:1,gn:5,s:1,sn:4}}}; save(); try{closeSheet()}catch(e){}")
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Ben'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(2500)
    # teacher
    tp=ctx.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1200)
    print('2 teacher buttons:', [b for b in ['Nền tảng · core course','Từ vựng · word list','Thu âm · recording links'] if tp.locator('text='+b).count()])
    tp.click('text=Nền tảng · core course'); tp.wait_for_timeout(900)
    print('2 units listed:', tp.locator('details').count(), '|', tp.inner_text('#app')[:120].replace('\n',' / '))
    tp.locator('details').nth(0).locator('summary').click(); tp.wait_for_timeout(300)
    d=tp.locator('details').nth(0); print('2 unit 1 fields: textareas', d.locator('textarea').count(), '| inputs', d.locator('input[type=text]').count())
    d.locator('textarea').nth(0).fill('EDITED BY TEACHER: là joins two things.'); d.locator('input[type=text]').nth(0).fill('Tôi là Ben nè.'); d.locator('textarea').nth(3).fill('Sentence 3 sounds stiff.'); d.locator('input[type=checkbox]').check()
    d.locator('text=Save this unit').click(); tp.wait_for_timeout(700)
    print('2 after save:', tp.locator('details').nth(0).locator('summary').inner_text(), '|', call('/api/core')[1]['u']['u01'].keys())
    # the app picks it up
    pg.reload(); pg.wait_for_timeout(2200); T("try{closeSheet()}catch(e){}")
    print('3 app shows the edit:', T("Z27.units[0].how[0]"), '|', T("Z27.units[0].ex[0][0]"), '| words untouched:', T("FCBY.k01_1.vi"))
    # teacher edits a word
    d.locator('input[type=text]').nth(12).fill('tui'); d.locator('text=Save this unit').click(); tp.wait_for_timeout(700)
    pg.reload(); pg.wait_for_timeout(2200); print('3 word edit reaches the card:', T("FCBY.k01_1.vi"), T("FCBY.k01_1.en"))
    d.locator('text=Back to the original').click(); tp.wait_for_timeout(700); print('3 back to original:', call('/api/core')[1])
    # student panel
    tp.click('text=‹ All students'); tp.wait_for_timeout(700); tp.locator('.stu').first.click(); tp.wait_for_timeout(900)
    txt=tp.inner_text('#app'); i=txt.find('Core course'); print('4 student panel:', txt[i:i+260].replace('\n',' / ') if i>=0 else 'NOT SHOWN')
    # recording page lists the core parts
    tp.click('text=‹ All students'); tp.wait_for_timeout(500); tp.click('text=Thu âm · recording links'); tp.wait_for_timeout(700); link=tp.locator('input[readonly]').first.input_value()
    rp=ctx.new_page(); rp.on('pageerror',lambda e: errs.append('REC '+str(e))); rp.goto(link); rp.wait_for_timeout(1500); t=rp.inner_text('body'); print('5 recording page has core parts:', 'Nền tảng 1' in t, '| total shown text has', t.count('Nền tảng'), 'core part names')
    br.close()
print('ERRORS:', errs or 'none')
