# v97: painted pictures move gently; other pictures do not get the new motion; reduced-motion users get none
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome')
    for rm in ('no-preference','reduce'):
        ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block',reduced_motion=rm); pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
        pg.goto(B+'/'); pg.wait_for_timeout(2400); T("S.set.ob7=1;save()")
        T("document.body.insertAdjacentHTML('beforeend','<div id=tt style=\"position:fixed;inset:0;background:#fff;z-index:99999\"></div>'); ['ăn','nước'].forEach(function(w){ document.getElementById('tt').appendChild(z60Pic(w)) })"); pg.wait_for_timeout(900)
        a=T("[].map.call(document.querySelectorAll('#tt img'),function(i){ return (i.getAttribute('src').indexOf('x-c-')>0?'painted':'other')+':'+getComputedStyle(i).animationName }).join(' | ')")
        m1=T("getComputedStyle(document.querySelector('#tt img')).transform"); pg.wait_for_timeout(1500); m2=T("getComputedStyle(document.querySelector('#tt img')).transform")
        print(rm,'->',a,'| painted picture is moving:',m1!=m2)
        ctx.close()
    print('ERR',errs or 'none')
