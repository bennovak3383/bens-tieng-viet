import sys, json, time
from playwright.sync_api import sync_playwright
B='http://localhost:8890'
errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
    ctx=br.new_context(viewport={'width':390,'height':844},permissions=['microphone'])
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('PAGE '+str(e)))
    pg.on('console',lambda m: errs.append('CONSOLE '+m.text) if m.type=='error' and 'mp3' not in m.text and '404' not in m.text else None)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    pg.evaluate("__T(\"try{ localStorage.setItem('x','1') }catch(e){}\")")
    # close welcome if present
    pg.evaluate("__T(\"S.set.ob7=1; S.me.name=S.me.name||'Ben'; save(); try{ closeSheet() }catch(e){}\")"); pg.reload(); pg.wait_for_timeout(1500); pg.evaluate("__T(\"try{ closeSheet() }catch(e){}\")")
    home=pg.inner_text('#z-home'); print('HOME has Sharp ears:', 'Sharp ears' in home, '| listen card:', 'listen more' in home.lower())
    pg.evaluate("__T(\"location.hash='prac'\")"); pg.wait_for_timeout(400)
    pr=pg.inner_text('#z-prac'); print('PRACTICE tiles:', [w for w in ['Viết · Write','Trò chơi · Games','Nghe kỹ · Sharp ears','listen more'] if w.lower() in pr.lower()])
    # games tile goes to library
    pg.click("text=Trò chơi · Games"); pg.wait_for_timeout(500); print('GAMES ->', pg.evaluate("__T(\"location.hash\")"), '| match up on page:', 'Match up' in pg.inner_text('#v-today') or 'Match' in pg.inner_text('#v-today'))
    # sharp ears: 2 rounds
    pg.evaluate("__T(\"zEar10()\")"); pg.wait_for_timeout(600)
    print('EAR label:', pg.inner_text('#sheet-body .lbl >> nth=1') if pg.locator('#sheet-body .lbl').count()>1 else pg.inner_text('#sheet-body')[:80])
    opts=pg.locator('.z10opt'); print('EAR options:', opts.count())
    opts.nth(0).click(); pg.wait_for_timeout(9000)
    print('EAR after pick:', pg.inner_text('#sheet-body .z7status')[:90])
    print('EAR saved misses:', pg.evaluate("__T(\"JSON.stringify(S.set.ear)\")"))
    pg.evaluate("__T(\"closeSheet()\")")
    # sign in
    pg.evaluate("""__T(`fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Ben'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); window.__code=j.code })`)"""); pg.wait_for_timeout(800)
    code=pg.evaluate("__T(\"window.__code\")"); print('CODE', code)
    # fake mic + hear
    pg.evaluate("""__T(`SPEECH.on=true; zMic=function(){return true}; zHear=function(ms,cb){ return new Promise(function(r){ setTimeout(function(){ if(cb) cb('tôi tên là Ben'); r({alts:['tôi tên là ben'],blob:new Blob([new Uint8Array(3000)],{type:'audio/webm'}),first:700,total:1500}) },300) }) }`)""")
    # writing typed
    pg.evaluate("__T(\"S.set.wmode='type'; z10Write()\")"); pg.wait_for_timeout(400)
    print('WRITE pick list:', pg.locator('.z10q').count())
    pg.locator('.z10q').first.click(); pg.wait_for_timeout(300)
    vals=['Bạn tên là gì?','Tôi tên là Ben.','Hôm nay tôi tên là Ben.','Hôm nay ở nhà tôi tên là Ben.']
    for i,v in enumerate(vals):
        pg.fill('.z10ta',v); pg.click('#rf-next'); pg.wait_for_timeout(200)
    # finish early button is on step >=3; now at step 4 -> click finish
    pg.click("text=That is enough · finish"); pg.wait_for_timeout(300)
    print('PHOTO step:', 'photo' in pg.inner_text('#sheet-body').lower())
    # attach a photo
    import base64,os
    png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==')
    open('/tmp/p.png','wb').write(png)
    pg.set_input_files('#sheet-body input[type=file]','/tmp/p.png'); pg.wait_for_timeout(800)
    print('PHOTO preview:', pg.locator('.z10photo img').count())
    pg.click('#rf-next'); pg.wait_for_timeout(5000)
    print('SEND:', pg.inner_text('#sheet-body .z7status')[:120])
    w=pg.evaluate("__T(\"fetch('/api/w',{headers:{'X-Code':window.__code}}).then(r=>r.json())\")"); print('SERVER items:', len(w['items']), w['items'][0]['lines'], w['items'][0]['photo'], w['items'][0]['recs'])
    # hand mode no typing
    pg.evaluate("__T(\"S.set.wmode='hand'; z10Write()\")"); pg.wait_for_timeout(300); pg.locator('.z10q').nth(1).click(); pg.wait_for_timeout(200)
    for i in range(6): pg.click('#rf-next'); pg.wait_for_timeout(150)
    print('HAND reaches photo:', 'photo of your page' in pg.inner_text('#sheet-body').lower())
    pg.evaluate("__T(\"closeSheet()\")")
    # speak now both ways
    pg.evaluate("__T(\"z7Speak(4)\")"); pg.wait_for_timeout(800); l1=pg.inner_text('#sheet-body .lbl >> nth=1')
    pg.wait_for_timeout(4000); l2=pg.inner_text('#sheet-body')
    print('SPEAK first label:', l1); print('SPEAK reversed seen:', 'ask the question' in l2.lower())
    pg.evaluate("__T(\"closeSheet()\")")
    # teacher
    tp=ctx.new_page(); tp.on('pageerror',lambda e: errs.append('TEACHER '+str(e)))
    tp.goto(B+'/teacher.html'); tp.wait_for_timeout(500); tp.click("text=Create the teacher key"); tp.wait_for_timeout(500); tp.click("text=Open the teacher view"); tp.wait_for_timeout(600)
    tp.click('.stu'); tp.wait_for_timeout(800)
    t=tp.inner_text('#writing'); print('TEACHER writing panel:', t[:160].replace('\n',' | '))
    tp.click("text=🖼 Show the photo"); tp.wait_for_timeout(500); print('TEACHER photo shown:', tp.locator('#writing img').count())
    tp.fill('#writing textarea','Rất tốt! Thêm "vào buổi sáng" nha.'); tp.click("#writing >> text=Send reply"); tp.wait_for_timeout(500)
    tp.click("text=🎤 Record a voice reply"); tp.wait_for_timeout(1500); tp.click("text=⏹ Stop and save"); tp.wait_for_timeout(1200)
    print('TEACHER voice btn:', tp.locator("text=▶ My voice reply").count())
    tp.click("text=Writing >> nth=-1") if tp.locator('.filters >> text=Writing').count() else None
    tp.locator('.filters >> text=Writing').click(); tp.wait_for_timeout(200); print('TEACHER write recordings:', tp.locator('.rec .tag:text("write")').count())
    # student progress
    pg.evaluate("__T(\"location.hash='prog'\")"); pg.wait_for_timeout(1500)
    pt=pg.inner_text('#z10wr'); print('PROGRESS:', pt[:260].replace('\n',' | '))
    pg.click("text=▶ Play the teacher’s voice reply"); pg.wait_for_timeout(800); print('PROGRESS voice audio el:', pg.locator('#z10wr audio').count())
    # done day screen
    pg.evaluate("__T(\"zDoneDay()\")"); pg.wait_for_timeout(300); print('DONE has more+listen:', 'Want more?' in pg.inner_text('#sheet-body'), 'listen more' in pg.inner_text('#sheet-body').lower())
    # laptop width check
    pg.set_viewport_size({'width':1280,'height':800}); pg.evaluate("__T(\"closeSheet(); location.hash='prac'\")"); pg.wait_for_timeout(300); pg.screenshot(path='/home/claude/tests/prac_laptop.png')
    pg.set_viewport_size({'width':390,'height':844}); pg.evaluate("__T(\"location.hash='home'\")"); pg.wait_for_timeout(300); pg.screenshot(path='/home/claude/tests/home_phone.png',full_page=True)
    br.close()
print('ERRORS:', errs[:10])
