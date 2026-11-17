# 74: answer switch in games, save-to-my-cards everywhere, optional own sentence, review quiz, Saigon boards, find anything, teacher panel
import json, urllib.request
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
def call(path,method='GET',body=None):
    r=urllib.request.Request(B+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(r) as f: return json.loads(f.read())
key=call('/api/setup','POST',{}).get('key'); J=lambda x: json.dumps(x,ensure_ascii=False)
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); bad=[]; pg.on('response',lambda r: bad.append(r.url) if ('/img/' in r.url and r.status>=400) else None)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(500)
    # (1) the switch
    T("z60Menu()"); pg.wait_for_timeout(600); print('switch:',[x.inner_text().replace('\n',' / ') for x in pg.locator('.z74seg button').all()],'| on:',pg.locator('.z74seg button[aria-pressed="true"]').get_attribute('data-k'))
    res={}
    for k in ('both','en','pic'):
        T("z60Menu()"); pg.wait_for_timeout(400); pg.locator('.z74seg button[data-k="%s"]'%k).click(); pg.wait_for_timeout(150); pg.locator('.z60g').first.click(); pg.wait_for_timeout(700)
        res[k]=T("(function(){ var r=document.querySelectorAll('.z60tile.r'), pics=0, en=0; [].forEach.call(r,function(e){ if(e.querySelector('.z60pf')) pics++; var s=e.querySelector('span'); if(s&&getComputedStyle(s).display!=='none') en++ }); return r.length+' tiles: '+pics+' with a picture, '+en+' showing English' })()")
    print('match up answers |',res); T("S.set.help74='both'; save(); closeSheet()")
    # (2)+(3) save words and own sentence in a scene, the builder, animals
    n0=T("(S.set.myc13||[]).length"); T("z63Load(function(){ z63Scene('caf') })"); pg.wait_for_timeout(900)
    print('scene: words offered to save:',pg.locator('.z74list .z74row').count(),'| own-sentence box:',pg.locator('.z74own').count())
    pg.locator('.z74list summary').click(); pg.locator('.z74list .z74sv:not([disabled])').first.click(); pg.wait_for_timeout(200)
    pg.fill('.z74own textarea','Bạn tôi đang uống cà phê ở Quận 1.'); pg.locator('.z74own .btn.primary').click(); pg.wait_for_timeout(300)
    print('  after: my words',n0,'→',T("S.set.myc13.length"),'| new word is a card:',T("z74InFC(S.set.myc13[S.set.myc13.length-1].vi)"),'|',T("JSON.stringify(S.set.myc13[S.set.myc13.length-1]).slice(0,150)"),'| own sentences:',T("JSON.stringify(S.set.own74.map(function(o){ return [o.vi,o.from] }))"),'|',pg.locator('.z74own p').inner_text())
    pg.locator('.z62tabs button').nth(1).click(); pg.wait_for_timeout(400); print('  check tab stays clean (no own-sentence box):',pg.locator('.z74own').count()==0)
    T("S.set.b64={n:0,seen:{},open:5}; z64Build(0,4)"); pg.wait_for_timeout(700); pg.locator('.z64card .z74sv').click(); pg.wait_for_timeout(200); print('builder: saved sentence →',T("S.set.myc13[S.set.myc13.length-1].vi+' = '+S.set.myc13[S.set.myc13.length-1].en"),'| own-sentence box:',pg.locator('.z74own').count())
    T("z73Zoo()"); pg.wait_for_timeout(800); print('animals: words offered to save:',pg.locator('.z74list .z74row').count()); T("closeSheet()")
    # (4) review
    T("z74Review()"); pg.wait_for_timeout(1200); kinds={}; k=0
    while pg.locator('.z60end').count()==0 and k<16:
        st=pg.locator('.z60stage'); t=st.get_attribute('data-t'); a=st.get_attribute('data-a'); k+=1; kinds[t]=kinds.get(t,0)+1
        if t=='order':
            n=pg.locator('.z74w').count()
            if k==4:
                for i in reversed(range(n)): pg.locator('.z74w[data-i="%d"]'%i).click()
                pg.wait_for_timeout(1000)
            for i in range(n): pg.locator('.z74w[data-i="%d"]'%i).click()
        else:
            if k==1: pg.locator('.z74o:not([data-k=%s])'%J(a)).first.click(); pg.wait_for_timeout(200)
            pg.locator('.z74o[data-k=%s]'%J(a)).click()
        pg.wait_for_timeout(2100)
    print('review: questions',k,'| kinds',kinds,'| result',pg.locator('.z60big').inner_text(),'| saved',T("JSON.stringify({n:S.set.rv74.n,last:S.set.rv74.last,miss:S.set.rv74.miss})"),'| look-again list:',pg.locator('.z60stage .z73ln').count(),'| own sentence with skip:',pg.locator('.z74own button:has-text("skip")').count())
    pg.locator('.z74own button:has-text("skip")').click(); pg.wait_for_timeout(200); print('  skip removes it:',pg.locator('.z74own').count()==0); T("closeSheet()")
    # (5) Saigon
    T("z74Saigon()"); pg.wait_for_timeout(900); print('Saigon boards:',[x.inner_text().replace('\n',' | ') for x in pg.locator('.z74sgt').all()])
    for i in range(pg.locator('.z74sgt').count()):
        T("z74Saigon()"); pg.wait_for_timeout(300); pg.locator('.z74sgt').nth(i).click(); pg.wait_for_timeout(400); n=pg.locator('.z74sgi').count(); pg.locator('.z74sgh').nth(1).click(); pg.wait_for_timeout(250)
        print('  ',pg.locator('#sheet-body .lbl').first.inner_text(),'| items',n,'| open →',pg.locator('.z74sgx:not([hidden])').inner_text().replace('\n',' | ')[:150])
    print('  heard:',T("Object.keys(S.set.sg74.seen).length"),'| game sets:',T("Z60.extra.reduce(function(a,f){ return a.concat(f()) },[]).filter(function(s){ return /^G/.test(s.id) }).map(function(s){ return s.t+' '+s.words.length }).join(', ')")); T("closeSheet()")
    # (6) Home row, find anything, add my own word
    T("location.hash='hub'"); pg.wait_for_timeout(600); print('Home row:',[x.inner_text().replace('\n',' ') for x in pg.locator('.z74strip .z74b').all()])
    pg.locator('.z74-all').click(); pg.wait_for_timeout(500); print('find anything: groups',pg.locator('#sheet-body .z74grp').count(),'| entries',pg.locator('#sheet-body .z74it').count())
    for w in ('tones','tu cua toi','vocab','xyzzy'): pg.fill('#sheet-body .z74q',w); pg.wait_for_timeout(200); print('   search “%s” →'%w,[x.locator('b').inner_text() for x in pg.locator('#sheet-body .z74res .z74it').all()] or pg.locator('#sheet-body .z74res').inner_text())
    pg.fill('#sheet-body .z74q','add word'); pg.wait_for_timeout(200); pg.locator('#sheet-body .z74res .z74it').first.click(); pg.wait_for_timeout(600)
    ins=pg.locator('#sheet-body input[type="text"]'); ins.nth(0).fill('xe ba gác'); ins.nth(1).fill('three-wheeled cargo bike'); pg.locator('#sheet-body button:has-text("Add to my cards")').click(); pg.wait_for_timeout(300)
    print('add my own word:',T("S.set.myc13[S.set.myc13.length-1].vi+' = '+S.set.myc13[S.set.myc13.length-1].en"),'| my words now:',T("S.set.myc13.length")); T("closeSheet()")
    pg.locator('.z74-add').click(); pg.wait_for_timeout(500); print('“+ Từ” on Home opens:',pg.locator('#sheet-body h1').first.inner_text()); T("closeSheet()")
    T("location.hash='more'"); pg.wait_for_timeout(500); pg.fill('#z-more .z74q','sai gon'); pg.wait_for_timeout(200); print('More page search “sai gon” →',[x.locator('b').inner_text() for x in pg.locator('#z-more .z74res .z74it').all()],'| old tiles still there:',pg.locator('#z-more .settile').count())
    # teacher
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Anna'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(2500)
    tp=ctx.new_page(); tp.set_viewport_size({'width':900,'height':900}); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1300); tp.locator('.stu').first.click(); tp.wait_for_timeout(1500)
    pn=tp.locator('.panel:has(h2:has-text("Ôn tập"))'); print('teacher panel:',[x.inner_text().replace('\n',' ') for x in pn.locator('.stat').all()]); print('  ',[x.inner_text().replace('\n',' | ') for x in pn.locator('.x70c').all()][:6])
    print('image files that failed to load:',bad or 'none')
    br.close()
print('ERR',errs or 'none')
