# 82: cards. One Speed button, two answer buttons (four still available), new cards follow the lesson.
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
SETUP="S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; save(); try{closeSheet()}catch(e){}; renderAll()"
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block',device_scale_factor=2)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2200); T(SETUP); pg.wait_for_timeout(500)
    cur=T("JSON.stringify({from:z53Cur().from,to:z53Cur().to})"); f=T("fcFresh().map(function(k){ var c=FCBY[k.split('|')[0]]; return c.c==='dq'?'dq':(c.k27!=null?'k'+c.k27:'topic') })")
    first=[x for x in f if x!='dq' and x!='topic'][:1]; i_dq=f.index('dq') if 'dq' in f else -1; print('lesson now covers structures',cur,'| first new cards:',f[:6],'| everyday questions start at place',i_dq+1,'| same cards as before, only the order changed:',T("(function(){ var a=fcFresh82().slice().sort(), b=fcFresh().slice().sort(); return a.length===b.length&&a.every(function(x,i){ return x===b[i] }) })()"))
    T("location.hash='fc'"); pg.wait_for_timeout(900); print('cards page note:',pg.locator('.z82note').inner_text())
    T("fcSession(null,6)"); pg.wait_for_timeout(900)
    print('session: speed buttons visible at the start:',pg.locator('.z7speed .speed').is_visible(),'| one button:',pg.locator('.z82sp').inner_text()); pg.screenshot(path='/home/claude/work/shots/f-card.png')
    pg.locator('.z82sp').click(); pg.wait_for_timeout(200); n=pg.locator('.z7speed .speed button').count(); print(' tap it → choices shown:',n); pg.locator('.z7speed .speed button').nth(3).click(); pg.wait_for_timeout(400); print(' pick one → folds again:',not pg.locator('.z7speed .speed').is_visible(),'|',pg.locator('.z82sp').inner_text(),'| speed saved:',T("S.set.speed"))
    pg.keyboard.press('Space'); pg.wait_for_timeout(500); print('answer buttons:',pg.locator('.fcgrade button b').all_inner_texts(),'|',pg.locator('.z82more').inner_text()); pg.screenshot(path='/home/claude/work/shots/f-grade.png')
    k=T("Object.keys(S.fc).length"); pg.locator('.fcgrade .fcg2').click(); pg.wait_for_timeout(500); print(' "Got it" files the card as Good:',T("(function(){ var ks=Object.keys(S.fc), s=S.fc[ks[ks.length-1]]; return ks.length===%d+1&&s.ivl>=1 })()"%k))
    pg.keyboard.press('Space'); pg.wait_for_timeout(400); pg.locator('.z82more').click(); pg.wait_for_timeout(200); print(' more choices:',pg.locator('.fcgrade button b').all_inner_texts(),'| remembered:',T("S.set.fcg4"),'|',pg.locator('.z82more').inner_text())
    pg.locator('.fcgrade .fcg0').click(); pg.wait_for_timeout(400); pg.keyboard.press('Space'); pg.wait_for_timeout(400); print(' next card keeps four:',pg.locator('.fcgrade button').count()); pg.locator('.z82more').click(); pg.wait_for_timeout(200); print(' back to two:',pg.locator('.fcgrade button').count()); br.close()
print('ERR',errs or 'none')
