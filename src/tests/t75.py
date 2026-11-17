# 75: real photos on the Saigon places board: credit, link, and the fallback when a photo cannot load (the lab has no route to Wikimedia)
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2000)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; save(); try{closeSheet()}catch(e){}; renderAll()"); pg.wait_for_timeout(300)
    print('items with a real photo:',T("JSON.stringify(Z74.sg.boards.map(function(b){ return [b.id,b.items.filter(function(it){ return it[6]&&it[6].f }).map(function(it){ return it[0]+' ← '+it[6].by+', '+it[6].lic })] }).filter(function(x){ return x[1].length }))"))
    print('photo address:',T("z75Url('Ben Thanh Market (36350099003).jpg',960)")); print('credit link:',T("z75Page('Ben Thanh Market (36350099003).jpg')"))
    print('photo block as built:',T("(function(){ var f=z75Photo(Z74.sg.boards[2].items[0][6]); return f.querySelector('img').getAttribute('src').slice(0,60)+'… | '+f.querySelector('figcaption').textContent+' | opens in a new tab: '+(f.querySelector('a').target==='_blank') })()"))
    T("z74Saigon('place')"); pg.wait_for_timeout(900); print('rows marked with a camera:',pg.locator('.z74sgi.hasph .z75cam').count(),'| credits fold:',pg.locator('summary:has-text("photo credits")').inner_text())
    pg.locator('.z74sgh').first.click(); pg.wait_for_timeout(2500)
    print('in the lab the photo cannot load, so the block removes itself:',pg.locator('.z74sgx:not([hidden]) .z75fig').count()==0,'| the rest of the item is still there:',pg.locator('.z74sgx:not([hidden])').inner_text().replace('\n',' | ')[:120])
    br.close()
print('ERR',errs or 'none')
