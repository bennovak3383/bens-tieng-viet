# 78: people redrawn in one style. Every person comes from the new z63Person; Thầy Tâm and Ben have their own looks; Ben stands on the end-of-round screen.
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block')
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000); T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; save(); try{closeSheet()}catch(e){}; renderAll(); location.hash='hub'"); pg.wait_for_timeout(1200)
    NEW="M-20 -38 Q-20 -58 0 -58"   # the jaw-shaped face only the new drawing has
    print('new face in use:',T("z63Person({},false).indexOf('%s')>=0"%NEW),'| no gradients or ids inside a person:',T("!/id=|url\\(/.test(z63Person({hair:'long',glasses:1},true))"))
    print('Home: people on the tiles',T("document.querySelectorAll('.z59t .z63eye').length"),'| all new:',T("[].every.call(document.querySelectorAll('.z59t svg'),function(s){ return s.innerHTML.indexOf('z63eye')<0||s.innerHTML.indexOf('%s')>=0 })"%NEW),'| Thầy Tâm on the welcome card: new face',T("document.querySelector('.z59tam').innerHTML.indexOf('%s')>=0"%NEW),'| his black fade hair:',T("document.querySelector('.z59tam').innerHTML.indexOf('#0B0B10')>=0"),'| still waves:',T("document.querySelector('.z59tam animateTransform')!=null"))
    print('teacher badge (built when the app starts) uses the new face:',T("Z21TA.indexOf('%s')>=0"%NEW))
    looks=T("(function(){ var n=0,bad=0; Z63.d?0:0; return 0 })()")
    T("z63Load(function(){})"); pg.wait_for_timeout(900)
    print('every scene look draws:',T("(function(){ var n=0,bad=[]; Z63.d.scenes.forEach(function(s){ s.people.forEach(function(p){ n++; var x=z63Person(p.look,true); if(x.indexOf('undefined')>=0||x.indexOf('NaN')>=0||x.indexOf('%s')<0) bad.push(p.k) }) }); return n+' people, problems: '+(bad.join(',')||'none') })()"%NEW))
    print('family pictures on cards:',T("['ba','mẹ','ông','bà','anh','chị','em'].map(function(k){ return k+':'+(z70Img(k).indexOf('%s')>=0) }).join(' ')"%NEW))
    print('Ben: blue eyes',T("z78Ben(false).indexOf('#3F6FA8')>=0"),'| beard',T("z78Ben(false).indexOf('#8A6A3F')>=0"),'| black shirt',T("z78Ben(false).indexOf('#1F1F24')>=0"))
    T("z60Menu()"); pg.wait_for_timeout(600); pg.locator('.z60g').first.click(); pg.wait_for_timeout(900)
    T("(function(){ var b=document.getElementById('sheet-body'); b.appendChild(z60Mascot('Giỏi lắm!')) })()"); pg.wait_for_timeout(300)
    print('end-of-round mascots: Ben',pg.locator('.z60mas .z78ben').count(),'| Thầy Tâm',pg.locator('.z60mas .z59tam:not(.z78ben)').count(),'| Ben is taller:',T("document.querySelector('.z60mas .z78ben').getBoundingClientRect().height>document.querySelector('.z60mas .z59tam:not(.z78ben)').getBoundingClientRect().height")); T("closeSheet()")
    T("z63Load(function(){ z63Scene('caf') })"); pg.wait_for_timeout(1200); print('café scene: people',pg.locator('.z63p').count(),'| eyes that blink',pg.locator('.z63p .z63eye').count()); pg.locator('.z63p').first.click(); pg.wait_for_timeout(500); print('  tapping a person still works:',pg.locator('.z63who').count()>=1); br.close()
print('ERR',errs or 'none')
