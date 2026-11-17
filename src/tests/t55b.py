# 55: cards — "say it" side: tap to record, tap to stop, record again; nothing starts by itself; last try is saved on grading
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']); pg=br.new_page(viewport={'width':390,'height':844}); pg.on('pageerror',lambda e: errs.append(str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Ben'; var d={}; Z27.units.slice(0,2).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.fcdir='p'; save(); try{closeSheet()}catch(e){}")
    T("SPEECH.on=true; window._saved=[]; var zr=zRecSave; zRecSave=function(m,b){ window._saved.push([m.kind,m.target,b?b.size:0]); return Promise.resolve() }")
    T("fcSession(null,3)"); pg.wait_for_timeout(1200)
    rb=pg.locator('#sheet-body .z55rec')
    print('button:',rb.inner_text(),'| listening by itself?',T("!!SPEECH.cur"),'| heard text:',repr(pg.locator('#sheet-body .fcard p.heard').first.inner_text()))
    rb.click(); pg.wait_for_timeout(1500); print('recording:',rb.inner_text(),'| class on:','on' in rb.get_attribute('class'),'| cur:',T("!!SPEECH.cur"),'|',pg.locator('#sheet-body .fcard p.heard').first.inner_text())
    pg.wait_for_timeout(4000); print('still recording after 5.5s (no auto stop):',rb.inner_text())
    rb.click(); pg.wait_for_timeout(1200); print('after stop:',rb.inner_text(),'| heard panel:',pg.locator('#sheet-body .zheard').count(),'| cur:',T("!!SPEECH.cur"))
    rb.click(); pg.wait_for_timeout(1000); rb.click(); pg.wait_for_timeout(1200); print('redo done:',rb.inner_text(),'| panels:',pg.locator('#sheet-body .zheard').count(),'| saved so far:',T("window._saved.length"))
    pg.click('#sheet-body #rf-next'); pg.wait_for_timeout(400); print('after reveal, redo still there:',rb.inner_text())
    rb.click(); pg.wait_for_timeout(800); pg.locator('#sheet-body .fcgrade button').nth(2).click(); pg.wait_for_timeout(700)
    print('graded while recording -> saved:',T("JSON.stringify(window._saved)"),'| fast reset:',T("SPEECH.fast"),'| cur:',T("!!SPEECH.cur"))
    print('next card button:',pg.locator('#sheet-body .z55rec').inner_text(),'| listening by itself?',T("!!SPEECH.cur"))
    pg.click('#sheet-body #rf-next'); pg.wait_for_timeout(300); pg.locator('#sheet-body .fcgrade button').nth(2).click(); pg.wait_for_timeout(500); print('no recording -> saved count still:',T("window._saved.length"))
    pg.screenshot(path='/tmp/t55.png')
    br.close()
print('ERR',errs or 'none')
