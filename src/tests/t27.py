# Version 27 test: the core course. Run against src/site8/devserver.mjs with a TEST copy of index.html that has the __T hook.
import sys, json
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
    ctx=br.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page()
    pg.on('pageerror',lambda e: errs.append('PAGE '+str(e)))
    pg.on('console',lambda m: errs.append('CONSOLE '+m.text) if m.type=='error' and 'mp3' not in m.text and '404' not in m.text and 'Failed to load' not in m.text else None)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; save(); try{ closeSheet() }catch(e){}"); pg.reload(); pg.wait_for_timeout(1800); T("try{ closeSheet() }catch(e){}")
    print('1 core data loaded:', T("!!(Z27&&Z27.on)"), '| units', T("Z27.units.length"), '| core cards', T("FC.filter(function(c){return c.k27!=null}).length"))
    print('1 home card:', pg.locator('#z27').count(), '|', pg.inner_text('#z27')[:70].replace('\n',' / '))
    print('1 cards for "và":', T("FC.filter(function(c){return c.vi==='và'}).map(function(c){return c.id}).join(',')"), '| "nếu":', T("FC.filter(function(c){return c.vi==='nếu'}).map(function(c){return c.id}).join(',')"))
    print('1 core cards closed before the unit is done:', T("FC.filter(function(c){return c.k27!=null&&fcOn(c)}).length"))
    pg.click("text=I already know the tones"); pg.wait_for_timeout(300)
    print('2 after sounds gate:', pg.inner_text('#z27')[:90].replace('\n',' / '))
    pg.click('#z27-start'); pg.wait_for_timeout(400)
    print('2 grammar page:', pg.inner_text('#sheet-body')[:160].replace('\n',' / '), '| examples', pg.locator('.z27ex').count())
    pg.click('#z27-go'); pg.wait_for_timeout(400)
    n=T("Z27.units[0].w.length")
    for i in range(n): pg.click("text=I said it · next"); pg.wait_for_timeout(120)
    pg.wait_for_timeout(500); q=0
    while pg.locator('.z13opt').count() and q<12:
        pg.locator('.z13opt').first.click(); pg.wait_for_timeout(150); pg.get_by_role("button",name="Next",exact=True).click(); pg.wait_for_timeout(250); q+=1
    print('2 word quiz questions:', q); pg.wait_for_timeout(300); print('   after quiz:', pg.inner_text('#sheet-body')[-120:].replace('\n',' / '))
    if pg.get_by_role("button",name="Next",exact=True).count(): pg.get_by_role("button",name="Next",exact=True).click(); pg.wait_for_timeout(400)
    o=0
    while pg.locator('.z27tray').count() and o<8:
        while pg.locator('.z27tray .z27tile').count(): pg.locator('.z27tray .z27tile').first.click(); pg.wait_for_timeout(60)
        pg.wait_for_timeout(200); pg.get_by_role("button",name="Next",exact=True).click(); pg.wait_for_timeout(250); o+=1
    print('2 order drill sentences:', o)
    g=0; txt=''
    while pg.locator('.z27gap').count() and g<8:
        txt=pg.inner_text('.z27gap'); pg.locator('.z25opt').first.click(); pg.wait_for_timeout(150); pg.get_by_role("button",name="Next",exact=True).click(); pg.wait_for_timeout(250); g+=1
    print('2 gap drill sentences:', g, '| sample:', txt)
    s=0
    while pg.locator("text=I said it · show me").count() and s<8:
        pg.click("text=I said it · show me"); pg.wait_for_timeout(120); pg.click("text=I had it"); pg.wait_for_timeout(250); s+=1
    print('2 say drill sentences:', s)
    print('2 done screen:', pg.inner_text('#sheet-body')[:200].replace('\n',' / '))
    print('2 saved:', T("JSON.stringify(S.set.k27.d.u01)"))
    print('2 unit 1 cards now open:', T("FC.filter(function(c){return c.k27===0&&fcOn(c)}).length"), '| first new cards:', T("fcFresh().slice(0,4).join(' ')"))
    pg.click("text=That is enough for today"); pg.wait_for_timeout(400)
    pg.reload(); pg.wait_for_timeout(1800); T("try{ closeSheet() }catch(e){}")
    print('3 after reload:', pg.inner_text('#z27')[:80].replace('\n',' / '), '| done kept:', T("!!S.set.k27.d.u01"))
    # every unit: grammar page opens, drills can be built
    bad=[]
    for i in range(T("Z27.units.length")):
        r=json.loads(T("(function(){ var u=Z27.units[%d]; z27Gram(u,%d,function(){}); var all=u.ex.concat(u.w.map(function(w){return [w[2],w[3]]})); return JSON.stringify({g:z27Gaps(u).length,o:all.filter(function(s){var n=s[0].split(/\\s+/).length;return n>=3&&n<=7}).length,ex:document.querySelectorAll('.z27ex').length}) })()" % (i,i)))
        if r['g']<3 or r['o']<4 or r['ex']<4: bad.append((i+1,r))
    T("closeSheet()"); print('4 units with too few drill sentences:', bad or 'none')
    # sentence rotation after several units are done
    T("Z27.units.slice(0,12).forEach(function(u){ S.set.k27.d[u.id]={t:1} }); save(); Z27.rd=''; z27Rot()")
    print('5 "tôi" card sentence today:', T("FCBY.k01_1.xv"), '| original:', T("FCBY.k01_1.xv0"), '| an old card (phở):', T("(function(){var c=FC.filter(function(c){return c.vi==='phở'})[0]; return c?c.xv+' <- '+c.xv0:'none'})()"))
    T("location.hash='prac'"); pg.wait_for_timeout(400); print('6 practice tile:', 'Core course' in pg.inner_text('#z-prac'))
    T("z27List()"); pg.wait_for_timeout(300); print('6 unit list rows:', pg.locator('.z27row').count(), '| done rows:', pg.locator('.z27row.done').count()); T("closeSheet()")
    T("location.hash='fc'"); pg.wait_for_timeout(400); print('6 cards page opens:', len(pg.inner_text('#v-fc'))>50 if pg.locator('#v-fc').count() else 'no #v-fc')
    # a brand-new beginner does not see the core card
    T("S.set.lvl0='zero'; S.set.z0={s:0,d:{}}; save(); location.hash='home'; zRenderHome()"); pg.wait_for_timeout(300); print('7 beginner sees core card:', pg.locator('#z27').count(), '| beginner card:', pg.locator('#z26').count())
    T("S.set.lvl0='more'; save(); zRenderHome()")
    # laptop width
    pg.set_viewport_size({'width':1280,'height':800}); pg.wait_for_timeout(300); print('8 laptop width card visible:', pg.locator('#z27').is_visible())
    pg.screenshot(path='/home/claude/out/t27-home.png'); 
    pg.set_viewport_size({'width':390,'height':844}); T("z27Unit(1)"); pg.wait_for_timeout(500); pg.screenshot(path='/home/claude/out/t27-gram.png')
    br.close()
print('ERRORS:', errs or 'none')
