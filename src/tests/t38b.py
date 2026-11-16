from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-ui-for-media-stream'])
    pg=br.new_context(viewport={'width':390,'height':844}).new_page(); pg.on('pageerror',lambda e: errs.append(str(e)))
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.k27={snd:1,d:{}}; save()"); pg.reload(); pg.wait_for_timeout(2500); T("try{closeSheet()}catch(e){}")
    print('stories in data:',T("Z27.st.length"),'| sentences pool:',T("Z27.sent.length"))
    print('unread at 0 units:',T("!!z38Unread()"),'| graded in zStories:',T("zStories().filter(function(s){return s.core}).length"))
    T("Z27.units.slice(0,6).forEach(function(u){ z27St().d[u.id]={t:1} }); save(); zRenderHome()"); pg.wait_for_timeout(300)
    print('after 6 units, unread:',T("z38Unread().id"),'| button on home:',pg.locator('#z27 .z49c').count(),'| in story list:',T("zStories().filter(function(s){return s.core}).map(function(s){return s.id}).join(',')"))
    pg.screenshot(path='/tmp/s38-home.png')
    pg.locator('#z27 .z49c button.primary').click(); pg.wait_for_timeout(800)
    print('story opens:',pg.inner_text('#sheet-body')[:300].replace('\n',' / '))
    pg.screenshot(path='/tmp/s38-story.png')
    # tap through reader
    for i in range(30):
        b=pg.locator('#sheet-body button:visible'); labs=[x.inner_text().strip() for x in b.all()]
        c=[x for x,l in zip(b.all(),labs) if l.startswith(('Next','Done','Finish','Check','I read','Questions','Start','Carry'))]
        if not c: break
        c[0].click(); pg.wait_for_timeout(300)
    print('end of reader:',pg.inner_text('#sheet-body')[:200].replace('\n',' / ') if pg.locator('#sheet-body').count() else '', '| buttons', labs[:10])
    print('read flag:',T("zRead('g1:0')"))
    # rotation includes extra sentences: check a word with an extra sentence
    T("Z27.units.forEach(function(u,i){ if(i<30) z27St().d[u.id]={t:1} }); Z27.rd=''; z27Rot()")
    print('a u21 card rotates among:',T("(function(){var c=FC.filter(function(c){return c.id==='k21_1'})[0]; return c?c.vi+' | '+c.xv:''})()"))
    print('unread now:',T("z38Unread()&&z38Unread().id"))
    br.close()
print('ERR',errs or 'none')
