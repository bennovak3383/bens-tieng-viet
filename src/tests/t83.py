# 83: Home order back (rooms, then the lesson), games show English instead of a symbol picture, the welcome picture has the new cartoons
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]; out='/home/claude/work/shots/'
SETUP="S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; save(); try{closeSheet()}catch(e){}; renderAll()"
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block',device_scale_factor=2)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2400); T(SETUP); pg.wait_for_timeout(500); T("location.hash='hub'"); pg.wait_for_timeout(1300)
    print('HOME order:',T("[].map.call(document.getElementById('z-hub').children,function(c){ return c.className.split(' ')[0]||c.tagName }).join(' > ')"),'| rooms in',T("getComputedStyle(document.querySelector('#z-hub .z59grid')).gridTemplateColumns.split(' ').length"),'columns | path still in the lesson card:',pg.locator('.z59day .z80d').count(),'dots | handbook still in tools:',pg.locator('.z74-book').count()); pg.screenshot(path=out+'g-home.png',full_page=True)
    print('PICTURES: symbol/face/hand pictures listed',T("Z70.vague.length"),'|',T("['đói','ổn','không phải','hả','hiểu','muốn'].map(function(w){ return w+':'+z83Vague(w) }).join(' ')"),'| things keep pictures:',T("['cà phê','con chó','bàn','đen','mẹ','xe máy'].map(function(w){ return w+':'+!z83Vague(w) }).join(' ')"))
    T("S.set.help74='pic'; save(); z60Menu()"); pg.wait_for_timeout(700); pg.locator('.z60g').first.click(); pg.wait_for_timeout(1300)
    left=pg.locator('.z60cols .z60tile:not(.r)'); print('Match up, words:',[left.nth(i).inner_text().strip() for i in range(left.count())])
    r=pg.locator('.z60cols .z60tile.r'); txt=[(r.nth(i).inner_text().strip() or '[picture]') for i in range(r.count())]; print('Match up, answers:',txt,'| pictures',pg.locator('.z60cols .z60tile.r .z60pf').count(),'| words',sum(1 for x in txt if x!='[picture]')); pg.screenshot(path=out+'g-match.png'); T("closeSheet()")
    print('outside a game the card picture is unchanged:',T("z70Has('hiểu')&&z60Has('hiểu')"))
    print('WELCOME picture: new Thầy Tâm',T("Z21AL.indexOf('#0B0B10')>0"),'| new Ben',T("Z21AL.indexOf('#3F6FA8')>0"),'| old Ben hair colour gone:',T("Z21AL.indexOf('#C98A3F')<0"))
    T("(function(){ var b=zOpen(); b.appendChild(h('div',{class:'z13wel z21wel',html:Z21AL})) })()"); pg.wait_for_timeout(500); pg.locator('.z21wel').screenshot(path=out+'g-welcome.png'); br.close()
print('ERR',errs or 'none')
