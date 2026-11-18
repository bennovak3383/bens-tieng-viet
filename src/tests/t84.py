# v84: our own drawings show in games; checked pictures stay; grammar words show English
import sys; sys.path.insert(0,'src/tests')
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; out='/home/claude/work/shots/'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block',device_scale_factor=2)
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    bad=[]; pg.on('response',lambda r: bad.append(r.url) if r.status>=400 else None)
    pg.goto(B+'/'); pg.wait_for_timeout(2400); T("S.set.ob7=1;save()"); pg.wait_for_timeout(300)
    print('own drawings:',T("['ăn','muốn','hiểu','giúp','trên','gia đình','họp'].map(function(w){ return w+':'+Z70.map[z70Key(w)]+':'+!z83Vague(w) }).join(' ')"))
    print('checked pictures kept:',T("['nước','màn hình','du lịch','sợ','cấm'].map(function(w){ return w+':'+!z83Vague(w) }).join(' ')"),'| grammar words show English:',T("['bị','vì vậy','vẫn','hả','đã'].map(function(w){ return w+':'+z83Vague(w) }).join(' ')"))
    T("S.set.help74='pic'; save(); z60Menu()"); pg.wait_for_timeout(700); pg.locator('.z60g').first.click(); pg.wait_for_timeout(1500)
    print('game picture tiles:',pg.locator('.z60cols .z60tile.r .z60pf').count()); pg.screenshot(path=out+'h-match.png'); T("closeSheet()")
    T("document.body.insertAdjacentHTML('beforeend','<div id=tt style=\"position:fixed;inset:0;background:#fff;z-index:99999;display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:10px\"></div>'); ['ăn','uống','đi','muốn','thích','hiểu','nói','hỏi','nghe','chờ','đưa','kéo'].forEach(function(w){ var d=document.createElement('div'); d.appendChild(z60Pic(w)); d.appendChild(document.createTextNode(w)); document.getElementById('tt').appendChild(d) })"); pg.wait_for_timeout(1200)
    print('drawings loaded:',T("[].filter.call(document.querySelectorAll('#tt img'),function(i){ return i.naturalWidth>0 }).length"),'of',T("document.querySelectorAll('#tt img').length")); pg.screenshot(path=out+'h-tiles.png')
    print('failed loads:',[u for u in bad if 'img/p' in u][:5]); print('ERR',errs or 'none')
