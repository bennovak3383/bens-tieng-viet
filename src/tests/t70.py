# 70: new picture set everywhere, every sound word has a picture, the sound test has one right answer, teacher page shows practice
import json, urllib.request
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
def call(path,method='GET',body=None):
    r=urllib.request.Request(B+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(r) as f: return json.loads(f.read())
key=call('/api/setup','POST',{}).get('key')
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); bad=[]; pg.on('response',lambda r: bad.append(r.url) if '/img/p/' in r.url and r.status!=200 else None)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(400)
    print('picture list loaded:',T("Object.keys(Z70.map).length"),'words | people drawn as cartoons:',T("Object.keys(Z70L).length"))
    print('a thing:',T("z12Pic('nhà','xs').innerHTML.slice(0,60)"),'| a person:',T("z12Pic('ông','xs').querySelector('svg')?'cartoon':'none'"),'| unknown word falls back:',T("z12Pic('rằng','xs').className"))
    cov=T("(function(){ var a=0,b=0,o=0; Z27.units.forEach(function(u){ u.w.forEach(function(w){ a++; if(z70Has(w[0])) b++; else if(Z12.art[w[0]]) o++ }) }); return [a,b,o] })()"); print('core course words:',cov[0],'| new picture:',cov[1],'| old drawing only:',cov[2],'| none:',cov[0]-cov[1]-cov[2])
    print('flashcard decks:',T("(function(){ var a=0,b=0,o=0; C7.cards.forEach(function(c){ a++; if(z70Has(c.vi)) b++; else if(Z12.art[c.vi]) o++ }); return a+' cards | new '+b+' | old drawing '+o+' | none '+(a-b-o) })()"))
    # every sound board: every tile shows a picture
    T("z62Menu()"); pg.wait_for_timeout(500); nb=pg.locator('.z62m').count(); miss=[]
    for i in range(nb):
        pg.locator('.z62m').nth(i).click(); pg.wait_for_timeout(150); n=pg.locator('.z62t').count()
        for k in range(n):
            pg.locator('.z62t').nth(k).click()
            if pg.locator('.z62card .z12pic img, .z62card .z12pic svg').count()==0: miss.append(pg.locator('.z62card').inner_text().replace('\n',' '))
        print('  board',pg.locator('#sheet-body .lbl').first.inner_text(),'| tiles',n); pg.locator('.sess-top .x').first.click(); pg.wait_for_timeout(150)
    print('sound tiles without a picture:',miss or 'none')
    # the test: wrong choices are never inside the word; play it through on three boards
    bare="function(t){ return String(t).normalize('NFD').replace(/[\\u0300\\u0301\\u0303\\u0309\\u0323]/g,'').normalize('NFC').toLowerCase() }"
    for bid in ['abc','cc','v0']:
        T("z62Board('%s','test')"%bid); pg.wait_for_timeout(300); amb=0; qs=[]
        for q in range(10):
            if pg.locator('.z60end').count(): break
            a=pg.locator('.z60stage').get_attribute('data-a'); w=T("z62Boards().filter(b=>b.id==='%s')[0].items.filter(x=>x.k===%s)[0].w"%(bid,json.dumps(a,ensure_ascii=False)))
            opts=[x.get_attribute('data-k') for x in pg.locator('.z62t').all()]
            for o in opts:
                if o!=a:
                    inside=T("(function(){ var bare=%s; var w=bare(%s), o=bare(%s); return %s })()"%(bare,json.dumps(w,ensure_ascii=False),json.dumps(o,ensure_ascii=False),"w.indexOf(o)===0" if bid=='cc' else "w.indexOf(o)>=0"))
                    if inside: amb+=1
            if q==0: qs.append(pg.locator('.z62q').inner_text().replace('\n',' | ')); pg.locator('.z62t:not([data-k=%s])'%json.dumps(a,ensure_ascii=False)).first.click(); pg.wait_for_timeout(200)
            pg.locator('.z62t[data-k=%s]'%json.dumps(a,ensure_ascii=False)).click(); pg.wait_for_timeout(300)
            if q==0: qs.append('after the right answer: '+pg.locator('.z62rev').inner_text().replace('\n',' = '))
            pg.wait_for_timeout(1400)
        pg.wait_for_selector('.z60end',timeout=5000); print('test',bid,'|',qs,'| choices that could also be right:',amb,'| result',pg.locator('.z60big').inner_text())
    T("closeSheet()")
    T("z63Load(function(){ z63Scene('res') })"); pg.wait_for_timeout(600); print('scene action cards with pictures:',pg.locator('.z63a .ic img').count(),'of',pg.locator('.z63a').count())
    T("S.set.b64={n:0,seen:{},open:3}; z64Build(1,1)"); pg.wait_for_timeout(500); print('builder places with pictures:',pg.locator('.z64o .ic img').count(),'of',pg.locator('.z64o').count())
    T("z64Build(0,2)"); pg.wait_for_timeout(400); print('builder things with pictures:',pg.locator('.z64o .ic img').count(),'of',pg.locator('.z64o').count()); T("closeSheet()")
    # every menu box on the older pages carries a picture too
    for v in ['prac','fc','quest','van','more']:
        T("location.hash='%s'"%v); pg.wait_for_timeout(700)
        r=T("(function(){ var a=[].filter.call(document.querySelectorAll('.settile'),function(e){ return e.offsetParent }), no=a.filter(function(e){ return !e.querySelector('img,svg') }).map(function(e){ var b=e.querySelector('b'); return b?b.textContent:'?' }); return a.length+' boxes, without a picture: '+(no.join(' / ')||'none') })()")
        print('menu',v,'|',r)
    print('cards with a picture:',T("(function(){ var n=0; C7.cards.forEach(function(c){ if(z70Has(c.vi)||(typeof Z12!=='undefined'&&Z12.art&&Z12.art[c.vi])) n++ }); return n+' of '+C7.cards.length })()"))
    T("location.hash='home'"); pg.wait_for_timeout(300)
    pg.wait_for_timeout(600); print('picture files that failed to load:',bad or 'none')
    # teacher page follows the student
    T("S.set.g60={'Le1l1:match':{n:3,best:94,t:Date.now()},'Le1l1:unj':{n:1,best:50,t:Date.now()-3600000},'Sfam:find':{n:2,best:75,t:Date.now()-86400000}}; save()")
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Anna'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(2500)
    tp=ctx.new_page(); tp.set_viewport_size({'width':900,'height':900}); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e))); tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1300)
    print('teacher page look:',tp.evaluate("getComputedStyle(document.body).backgroundColor"),'| header:',tp.locator('.t70').inner_text().replace('\n',' | ')); tp.screenshot(path='/home/claude/scratch/t_list.png')
    tp.locator('.stu').first.click(); tp.wait_for_timeout(1500); pn=tp.locator('.panel:has(h2:has-text("Luyện tập"))')
    print('practice panel:',[x.inner_text().replace('\n',' ') for x in pn.locator('.stat').all()]); print('  rows:',[x.inner_text().replace('\n',' | ') for x in pn.locator('.x70c').all()][:7])
    pn.scroll_into_view_if_needed(); tp.screenshot(path='/home/claude/scratch/t_stu.png')
    br.close()
print('ERR',errs or 'none')
