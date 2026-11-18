# 76: offline. Open once online, let it save itself, cut the internet, reload: the app opens, games / writing / review / scenes work,
# pictures and sounds come from the saved copy, and nothing throws. Then the internet comes back.
import json, time
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    print('this browser can save the app:',T("z76Can()"),'| list:',T("fetch('data/offline.json').then(r=>r.json()).then(j=>j.files.length+' files '+j.mb+' MB + '+j.audio.length+' sound files '+j.audio_mb+' MB')"))
    t0=time.time()
    while time.time()-t0<150 and not T("!!(S.set.off76&&S.set.off76.t)"): pg.wait_for_timeout(1000)
    print('saved itself after %ds:'%(time.time()-t0),T("JSON.stringify(S.set.off76)"),'| files kept:',T("caches.open('btv-1').then(c=>c.keys()).then(k=>k.length)"))
    T("location.hash='hub'"); pg.wait_for_timeout(500); print('Home chip:',pg.locator('.z76chip').inner_text())
    # cut the internet and open the app again
    ctx.set_offline(True); pg.reload(); pg.wait_for_timeout(2500)
    print('OFFLINE · app opens:',pg.locator('#z-hub .z59t').count(),'Home boxes | bar:',pg.locator('.z76bar').inner_text()[:44],'| chip:',pg.locator('.z76chip').inner_text())
    print('  lesson data from the saved copy:',T("Z27.units.length+' units, '+C7.cards.length+' cards, '+Object.keys(Z70.map).length+' picture words, '+(Z63.d?Z63.d.scenes.length:0)+' scenes'"))
    T("z60Menu()"); pg.wait_for_timeout(600); pg.locator('.z60g').first.click(); pg.wait_for_timeout(900)
    pg.wait_for_function("[].every.call(document.querySelectorAll('.z60tile .z70i'),i=>i.complete)",timeout=8000)
    print('  game: tiles',pg.locator('.z60tile').count(),'| pictures showing:',T("[].filter.call(document.querySelectorAll('.z60tile .z70i'),i=>i.naturalWidth>0).length+' of '+document.querySelectorAll('.z60tile .z70i').length"))
    w=pg.locator('.z60tile.l').first.inner_text(); pg.locator('.z60tile.l').first.click()
    en=T("(function(){ var s=z60Sets().filter(function(s){ return s.id===Z60.sel })[0]; var x=s.words.filter(function(w){ return w.vi===%s })[0]; return z60En(x.en) })()"%json.dumps(w,ensure_ascii=False))
    pg.locator('.z60tile.r',has_text=en).first.click(); pg.wait_for_timeout(500); print('  game: matched a pair offline:',pg.locator('.z60tile.ok').count()==2); T("closeSheet()")
    T("z10Write()"); pg.wait_for_timeout(700); print('  writing drill opens:',pg.locator('#sheet-body h1').first.inner_text(),'| choices:',pg.locator('#sheet-body button').count()); T("closeSheet()")
    T("z74Review()"); pg.wait_for_timeout(1200); print('  review opens:',pg.locator('.z62q').inner_text().replace('\n',' | ')); T("closeSheet()")
    T("z63Load(function(){ z63Scene('caf') })"); pg.wait_for_timeout(1200); print('  scene opens: people',pg.locator('.z63p').count(),'| things drawn from saved pictures:',T("[].filter.call(document.querySelectorAll('.z63svg image'),function(i){ return i.getBBox().width>0 }).length")); T("closeSheet()")
    print('  recorded voices from the saved copy:',T("fetch('audio/'+AUD.idx.bundles[0]).then(r=>r.ok+' '+r.status).catch(e=>'failed')"),'| recorded clips known:',T("Object.keys(AUD.idx.clips).length"))
    print('  sync call fails quietly (no crash):',T("fetch('/api/state').then(r=>'answered '+r.status).catch(e=>'no internet, as expected')"))
    T("z76Sheet()"); pg.wait_for_timeout(500); print('  offline sheet:',pg.locator('.z76msg').inner_text()); T("closeSheet()")
    T("S.set.own74=S.set.own74||[]; z74Save('máy bay cất cánh','the plane takes off','',''); save()"); print('  a word added offline is kept on the device:',T("S.set.myc13[S.set.myc13.length-1].vi"))
    ctx.set_offline(False); pg.wait_for_timeout(1200); print('ONLINE again · bar gone:',pg.locator('.z76bar').count()==0,'| chip:',pg.locator('.z76chip').inner_text() if pg.locator('.z76chip').count() else '(open Home)')
    pg.goto(B+'/?nosw=1'); pg.wait_for_timeout(5500); print('switch-off address clears it: workers',pg.evaluate("navigator.serviceWorker.getRegistrations().then(r=>r.length)"),'| saved copies',pg.evaluate("caches.keys().then(k=>k.length)"))
    br.close()
print('ERR',errs or 'none')
