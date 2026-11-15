from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-ui-for-media-stream'])
    pg=br.new_context(viewport={'width':390,'height':844}).new_page(); pg.on('pageerror',lambda e: errs.append(str(e)))
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    def setup(done):
        d=','.join('u%02d:{t:1}'%i for i in range(1,done+1))
        T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.mins=60; S.set.k27={snd:1,d:{%s}}; save(); try{closeSheet()}catch(e){}"%d); pg.reload(); pg.wait_for_timeout(2200); T("try{closeSheet()}catch(e){}"); T("zRenderHome()"); pg.wait_for_timeout(300)
    def vis(q): return pg.evaluate("(q)=>{const e=document.querySelector(q); return !!(e&&e.offsetParent)}",q)
    for done in (0,6,12):
        setup(done)
        print(f'--- {done} units done | height',pg.evaluate("document.body.scrollHeight"))
        print(' first panel after code is core card:', pg.evaluate("(()=>{const el=document.querySelector('#z-home'); const k=[...el.children].filter(x=>x.offsetParent); return k.slice(0,3).map(x=>x.id||x.className).join(' | ')})()"))
        print(' scenes',vis('#z18-sit'),'mission',vis('#z13-ms'),'speak btn',pg.evaluate("[...document.querySelectorAll('#z-home button')].some(b=>/hands-free/.test(b.textContent)&&b.offsetParent)"), 'more-situations', pg.locator('#z-home details.z37more').count(), 'hint', pg.locator('#z37next').count())
        pg.screenshot(path=f'/tmp/h37-{done}.png',full_page=True)
    T("location.hash='prac'"); pg.wait_for_timeout(700)
    print('prac tiles visible:', pg.evaluate("[...document.querySelectorAll('#z-prac .settile')].filter(t=>t.offsetParent).map(t=>t.querySelector('b').textContent).join(' / ')"), '| more folded:', pg.locator('#z-prac details.z37more').count())
    setup(2); T("location.hash='prac'"); pg.wait_for_timeout(700)
    print('prac tiles at 2 units:', pg.evaluate("[...document.querySelectorAll('#z-prac .settile')].filter(t=>t.offsetParent).map(t=>t.querySelector('b').textContent).join(' / ')"), '| more folded:', pg.locator('#z-prac details.z37more').count())
    pg.screenshot(path='/tmp/p37.png',full_page=True)
    T("location.hash='more'"); pg.wait_for_timeout(600); print('more:', pg.evaluate("[...document.querySelectorAll('#z-more .settile b')].map(b=>b.textContent).join(' / ')"))
    # full plan restores everything
    T("z27St().full=1; save(); location.hash='home'"); pg.wait_for_timeout(500); T("zRenderHome()"); print('full plan scenes visible:', vis('#z18-sit'))
    print('core text:', pg.inner_text('#z27')[:300].replace('\n',' / ') if pg.locator('#z27').count() else '')
    br.close()
print('ERR',errs or 'none')
