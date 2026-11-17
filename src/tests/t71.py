# 71: Thầy Tâm in the shaded style, the bright Today header, lifted scene rooms, a picture for every word and card, the guide's new Home section
import json
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); bad=[]; pg.on('response',lambda r: bad.append(r.url) if ('/img/' in r.url and r.status>=400) else None)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(500)
    # Thầy Tâm
    T("location.hash='hub'"); pg.wait_for_timeout(600)
    print('Home welcome: new Thầy Tâm:',pg.locator('#z-hub .z71tam svg').count(),'| waves:',pg.locator('#z-hub .z71tam animateTransform').count(),'| old outlined drawing left:',T("document.querySelector('#z-hub .z59tam').innerHTML.indexOf('#1B1230')>=0"))
    print('round avatar is the same person:',T("Z21TA.indexOf('z71c')>0 && z21Av().querySelector('svg')!=null"))
    print('game mascot uses the same drawing:',T("z60Mascot('Tốt lắm!').querySelector('.z71tam svg')!=null"))
    # Today header
    T("location.hash='home'"); pg.wait_for_timeout(900)
    print('Today header:',pg.locator('#v-home .zhero .z12scene').get_attribute('data-k'),'| scooter picture:',pg.locator('#v-home .z12scene image').count(),'| height',T("Math.round(document.querySelector('#v-home .z12scene').getBoundingClientRect().height)"))
    T("S.set.look59='old'; S.set.skin='night'; save(); z19Apply()"); pg.wait_for_timeout(400); print('old look keeps its own header:',pg.locator('#v-home .zhero .z12scene').get_attribute('data-k'))
    T("S.set.look59='bright'; save(); z19Apply()"); pg.wait_for_timeout(400); print('back to bright:',pg.locator('#v-home .zhero .z12scene').get_attribute('data-k'))
    # scenes: every room draws, with its extra layers, and still opens and plays
    r=T("new Promise(function(ok){ z63Load(function(){ ok(JSON.stringify(Z63.d.scenes.map(function(sc){ var a=z63Bg71(sc.bg).length, b=z63Bg(sc.bg).length, s=z63Svg(sc); var d=document.createElement('div'); d.innerHTML=s; return [sc.id, b-a, d.querySelectorAll('.z63p').length, d.querySelector('parsererror')?'BROKEN':'ok'] }))) }) })")
    print('scene rooms (id, added drawing, people, state):',json.loads(r))
    for sid in ['fam','res','tax']:
        T("z63Scene('%s')"%sid); pg.wait_for_timeout(600); pg.locator('.z63p').first.click(); pg.wait_for_timeout(300)
        print('  scene',sid,'| tap a person →',pg.locator('.z63card, .z63say, .z63who').first.inner_text().replace('\n',' | ')[:70] if pg.locator('.z63card, .z63say, .z63who').count() else 'opened'); T("closeSheet()"); pg.wait_for_timeout(200)
    # pictures: every core word and every card
    print('core words without a picture:',T("(function(){ var n=0,s={}; Z27.units.forEach(function(u){ (u.w||[]).forEach(function(w){ if(!s[w[0]]){ s[w[0]]=1; if(!z70Has(w[0])) n++ } }) }); return n+' of '+Object.keys(s).length })()"))
    print('cards without a picture:',T("(function(){ var n=0; C7.cards.forEach(function(c){ if(!z70Has(c.vi)) n++ }); return n+' of '+C7.cards.length })()"))
    T("location.hash='fc'"); pg.wait_for_timeout(500)
    # guide
    T("z57Guide()"); pg.wait_for_timeout(1500)
    print('guide: Home section:',pg.locator('#sheet-body h2:has-text("six big boxes")').count(),'| Today section:',pg.locator('#sheet-body h2:has-text("Today: your lesson")').count(),'| pictures:',pg.locator('#sheet-body img').count(),'| files found:',T("Promise.all([].map.call(document.querySelectorAll('#sheet-body img'),function(i){ return fetch(i.src).then(function(r){ return r.ok?1:0 }) })).then(function(a){ return a.reduce(function(x,y){ return x+y },0) })"))
    T("closeSheet()"); pg.wait_for_timeout(500)
    print('image files that failed to load:',bad or 'none')
    br.close()
print('ERR',errs or 'none')
