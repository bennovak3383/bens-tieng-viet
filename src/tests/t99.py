# v99: the app notices a newer version and reloads once; the version line shows on Home
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':852},service_workers='block')
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    loads=[]; pg.on('framenavigated',lambda f: loads.append(1))
    pg.goto(B+'/'); pg.wait_for_timeout(2500); n0=len(loads); print('same version: no reload:',n0==1,'| version line:',pg.locator('.z99v').inner_text())
    pg.route('**/data/ver.json*',lambda r: r.fulfill(status=200,content_type='application/json',body='{"v":999}'))
    pg.reload(); pg.wait_for_timeout(3500); print('newer version on the server: page loads',len(loads)-n0,'times (1 reload + 1 self-reload = 2):',len(loads)-n0==2)
    pg.wait_for_timeout(2500); print('and it does not loop:',len(loads)-n0==2); print('ERR',errs or 'none')
