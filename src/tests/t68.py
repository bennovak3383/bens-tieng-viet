# 68: hide text in stories; scene action bubbles + spotlight; word-only answers; scene pictures in games; hub tile drawings
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':390,'height':844})
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()")
    pg.wait_for_timeout(400)
    print('hub tiles:',pg.locator('.z59t').count(),'| with a cartoon drawing:',pg.locator('.z59t .ic.art svg').count(),'| tiles still open their page:',end=' ')
    pg.locator('.z59-gam').click(); pg.wait_for_timeout(300); print(pg.locator('#sheet-body').inner_text()[:30].replace('\n',' | ')); T("closeSheet()")
    # story: hide text
    pg.locator('.z59-sto').click(); pg.wait_for_timeout(300); pg.locator('.z61ch button').first.click(); pg.wait_for_timeout(300)
    blur=lambda: pg.evaluate("getComputedStyle(document.querySelector('.z61sent')).filter")
    print('story text before:',blur()); pg.locator('.z68hide').click(); pg.wait_for_timeout(350)
    print('after "hide text":',blur(),'| button now says:',pg.locator('.z68hide').inner_text(),'| note shown:',pg.locator('.z68hn').is_visible(),'| English button off:',pg.locator('.z61bar .chip:text-is("English")').is_disabled())
    pg.locator('.z61story .zw').first.click(force=True); pg.wait_for_timeout(200); print('word tap while hidden opens popup:',pg.locator('.z61pop').is_visible())
    pg.locator('.z61play').click(); pg.wait_for_timeout(300); print('play still works while hidden → button:',pg.locator('.z61play').inner_text(),'| sentence lit:',pg.locator('.z61sent.on').count()); pg.locator('.z61play').click()
    T("closeSheet()"); pg.locator('.z59-sto').click(); pg.wait_for_timeout(300); pg.locator('.z61ch button').nth(1).click(); pg.wait_for_timeout(300); print('next chapter stays hidden:',blur())
    pg.locator('.z68hide').click(); pg.wait_for_timeout(350); print('after "show text":',blur(),'| English button on again:',pg.locator('.z61bar .chip:text-is("English")').is_enabled())
    pg.locator('.z61story .zw').first.click(); pg.wait_for_timeout(200); print('word tap works again:',pg.locator('.z61pop').is_visible()); T("closeSheet()")
    # scenes
    T("z63Load(function(){})"); pg.wait_for_timeout(600); ids=T("Z63.d.scenes.map(s=>s.id)"); print('scenes:',ids)
    for sid in ids:
        T("closeSheet(); z63Scene('%s','see')"%sid); pg.wait_for_timeout(400)
        print(' ',sid,'people:',pg.locator('.z63pic .z63p').count(),'| action bubbles:',pg.locator('.z63pic .z63b').count(),'| people with an action in the data:',T("Z63.d.scenes.filter(s=>s.id==='%s')[0].people.filter(p=>p.act).length"%sid))
    T("closeSheet(); z63Scene('fam','quiz')"); pg.wait_for_timeout(500); seen={}; k=0
    while pg.locator('.z60end').count()==0 and k<40:
        k+=1; t=pg.locator('.z60stage').get_attribute('data-t'); a=pg.locator('.z60stage').get_attribute('data-a')
        if t not in seen:
            seen[t]=1
            if t=='tap': print('  tap question: nobody dimmed:',pg.locator('.z63pic.asking').count()==0)
            else: print(' ',t,'question → one person in the light:',pg.locator('.z63p.ask').count(),'| others dimmed:',pg.locator('.z63pic.asking').count()==1,'| their bubble lit:',pg.locator('.z63b.ask').count(),'| faces in the answer buttons:',pg.locator('.z63o .z63av').count(),'| icons in the answer buttons:',pg.locator('.z63o .ic').count(),'| buttons:',[x.inner_text() for x in pg.locator('.z63o').all()])
        if t=='tap':
            i=T("Z63.d.scenes.filter(s=>s.id==='fam')[0].people.findIndex(p=>p.k==='%s')"%a); pg.locator('.z63p[data-i="%d"]'%i).dispatch_event('click')
        else: pg.locator('.z63o[data-k="%s"]'%a).click()
        pg.wait_for_timeout(1150)
    print('check finished:',pg.locator('.z60end').count()==1,'| question types seen:',sorted(seen)); T("closeSheet()")
    # games with a scene's words use the scene's pictures; lesson sets keep theirs
    for g in ['match','find','flash','listen']:
        T("closeSheet(); var s=z60Sets().filter(x=>x.id==='Sfam')[0]; z60Play('%s',s)"%g); pg.wait_for_timeout(500); print(' ',g,'scene pictures:',pg.locator('#sheet-body .z68px').count(),'| old drawings:',pg.locator('#sheet-body .z60pf:not(.z68px)').count())
    T("closeSheet(); var s=z60Sets().filter(x=>x.id.charAt(0)!=='S')[0]; z60Play('match',s)"); pg.wait_for_timeout(500); print('  lesson set match: scene pictures:',pg.locator('#sheet-body .z68px').count(),'| its own drawings:',pg.locator('#sheet-body .z60pf').count())
    # play one full Match up round with the scene set
    T("closeSheet(); var s=z60Sets().filter(x=>x.id==='Sfam')[0]; z60Play('match',s)"); pg.wait_for_timeout(500)
    print('errors:',errs or 'none'); br.close()
