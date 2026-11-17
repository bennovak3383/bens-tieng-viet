# Screenshots for the user guide (img/guide). Run after build.sh (fresh server).
import json, urllib.request, struct, math, urllib.parse, sys
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; OUT='/home/claude/bens-tieng-viet/img/guide/'; R='/home/claude/bens-tieng-viet/'
def call(path,method='GET',body=None,headers=None,raw=None):
    h={'Content-Type':'application/json'}; h.update(headers or {})
    r=urllib.request.Request(B+path,method=method,data=raw if raw is not None else (json.dumps(body).encode() if body is not None else None),headers=h)
    with urllib.request.urlopen(r) as f: return json.loads(f.read())
def wav(sec=0.6,sr=16000):
    n=int(sec*sr); d=b''.join(struct.pack('<h',int(8000*math.sin(i*0.07))) for i in range(n))
    return b'RIFF'+struct.pack('<I',36+len(d))+b'WAVEfmt '+struct.pack('<IHHIIHH',16,1,1,sr,sr*2,2,16)+b'data'+struct.pack('<I',len(d))+d
key=call('/api/setup','POST',{})['key']; TH={'X-Teacher':key}
plan=json.load(open(R+'data/plan.json')); plan['rel']={'open':2,'next':'','hw':'Read dialogue 2 out loud twice before Thursday’s class.','hp':[]}
call('/api/t/plan','POST',plan,TH)
vk=call('/api/t/voice-key','POST',{},TH)['key']
for l in json.load(open(R+'data/voice-lines.json'))['parts'][0]['lines'][:5]: call('/api/voice/rec?v=%s&who=voice3&id=%s&part=x'%(vk,l['id']),'POST',headers={'Content-Type':'audio/wav','X-Text':urllib.parse.quote(l['vi'])},raw=wav())
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
    ctx=br.new_context(viewport={'width':390,'height':800},device_scale_factor=2); pg=ctx.new_page(); pg.on('pageerror',lambda e: print('APPERR',e)); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    def shot(name,sel=None,h=None):
        o=dict(path=OUT+name,type='jpeg',quality=74)
        if sel:
            bb=pg.locator(sel).first.bounding_box(); o['clip']={'x':bb['x'],'y':max(0,bb['y']),'width':bb['width'],'height':min(bb['height'],h or bb['height'])}
        pg.screenshot(**o); print('shot',name)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1800)
    T("S.set.ob7=1; S.set.lvl0='some'; S.set.g42='f'; S.me.name='Anna'; S.set.k27={snd:1,d:{}}; save(); try{closeSheet()}catch(e){}; zRenderHome()")
    T("fetch('/api/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Anna'})}).then(r=>r.json()).then(j=>{ accSet({code:j.code,id:j.id,name:j.name}); accPush(true) })"); pg.wait_for_timeout(1500)
    pg.click('#z48 button:has-text("Set up my plan")'); pg.wait_for_timeout(300)
    sb=lambda t: pg.locator('#sheet-body button:has-text("%s")'%t).first.click()
    nxt=lambda: pg.locator('#sheet-body button.primary').last.click()
    sb('I live or work in Vietnam'); nxt(); sb('A little'); nxt(); sb('Small talk with locals'); nxt()
    pg.locator('#sheet-body .z48rate').nth(0).locator('button').nth(1).click(); pg.locator('#sheet-body .z48rate').nth(1).locator('button').nth(0).click(); nxt()
    sb('Yes, every day'); nxt(); sb('Café, restaurant'); sb('Grab, taxi'); nxt(); sb('Tones'); sb('Nervous to speak'); nxt(); sb('Evening'); nxt()
    sb('30 min'); sb('6 days'); nxt(); pg.locator('#sheet-body .z48chip:text-is("2")').click(); nxt(); sb('Friends'); nxt(); sb('Apps (Duolingo, etc.)'); nxt(); nxt()
    pg.fill('#sheet-body textarea','I want to chat with my neighbours without switching to English.'); nxt(); pg.wait_for_timeout(400)
    T("document.querySelector('#sheet').scrollTop=0; document.querySelector('#sheet-body').scrollTop=0"); pg.wait_for_timeout(200); shot('s-plan.jpg')
    pg.click('#sheet-body button:has-text("Start my plan")'); pg.wait_for_timeout(700)
    T("var d=z27St().d; Z27.units.slice(0,6).forEach(function(u,i){ d[u.id]={t:Date.now()-(6-i)*DAY,o:4,on:4,g:4,gn:5,s:3,sn:4} }); FC.slice(0,30).forEach(function(c,i){ S.fc[c.id+'|l']={ivl:i%4?3:0,ease:2.3,reps:2,lapses:i%7===0?2:0,due:Date.now()+(i%5?9e7:-1e5),first:Date.now()-3*DAY} }); for(var i=0;i<6;i++){ S.days[dayKey(new Date(Date.now()-i*DAY))]=25; S.d6[dayKey(new Date(Date.now()-i*DAY))]={fc:1,ku:1,sp:1} } S.set.sl49={}; S.set.life51={t:1}; save()")
    T("z53St('e1l1').sounds=dayKey(new Date(Date.now()-3*DAY)); z53St('e1l1').soundsn=2; z53St('e1l1').dialogn=3; z53St('e1l1').vocabn=4; z53St('e1l1').oraln=2; z53St('e1l1').life=dayKey(); z53St('e1l2').dialog=dayKey(); z53St('e1l2').vocab=dayKey(); z53St('e1l2').vocabn=2; save()")
    T("S.set.ask50=[{t:Date.now()-3600000,s:'Đây là bạn tôi.',q:'Why this word order? Why is it “bạn tôi” and not “tôi bạn”?',w:'unit 6'}]; save(); accPush(true)"); pg.wait_for_timeout(1500)
    for m in [("{kind:'unit',ref:'u06',prompt:'Unit 6 · say it: This is my friend.',target:'Đây là bạn tôi.',ok:true,score:0,heard:'',ms:0}"),("{kind:'unit',ref:'u05',prompt:'Unit 5 · say it: The café is over there.',target:'Quán cà phê ở kia.',ok:true,score:0,heard:'',ms:0}"),("{kind:'q',ref:'q1',lv:1,prompt:'Chị tên gì?',target:'Tôi tên là Anna.',heard:'tôi tên là anna',score:1,ok:true,ms:1800}"),("{kind:'card',ref:'c1',target:'cà phê',heard:'cà phe',score:0.5,ok:false}"),("{kind:'retell',ref:'g1',prompt:'Retell: Mike ở Sài Gòn',target:'tên, ở, bạn'}")]:
        T("navigator.mediaDevices.getUserMedia({audio:true}).then(function(st){ var ch=[], mr=new MediaRecorder(st); mr.ondataavailable=function(e){ if(e.data.size) ch.push(e.data) }; mr.onstop=function(){ zRecSave(%s,new Blob(ch,{type:mr.mimeType})) }; mr.start(); setTimeout(function(){ mr.stop() },500) })"%m); pg.wait_for_timeout(1300)
    pg.reload(); pg.wait_for_timeout(2200); T("try{closeSheet()}catch(e){}; zRenderHome()"); pg.wait_for_timeout(600)
    T("document.querySelector('#z53').scrollIntoView({block:'start'}); window.scrollBy(0,-8)"); pg.wait_for_timeout(300); shot('s-home.jpg')
    T("document.querySelector('.z49c').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300); shot('s-story.jpg','.z49c')
    T("z53Dlg(z53Ls()[0],function(){ closeSheet() })"); pg.wait_for_timeout(400); pg.click('#sheet-body button:has-text("Be Anna")'); pg.wait_for_timeout(3500); T("document.querySelector('#sheet-body .z53dl').scrollIntoView({block:'start'}); document.querySelector('#sheet').scrollBy(0,-90)"); pg.wait_for_timeout(300); shot('s-dialog.jpg'); T("closeSheet()")
    T("window.SpeechRecognition=window.webkitSpeechRecognition=undefined; SPEECH.on=true; z12Recall(null,3)"); pg.wait_for_timeout(700); pg.locator('#sheet-body .z55rec').click(); pg.wait_for_timeout(900); pg.screenshot(path=OUT+'s-record.jpg',type='jpeg',quality=74,clip={'x':0,'y':0,'width':390,'height':640}); print('shot s-record.jpg'); pg.locator('#sheet-body .z55rec').click(); pg.wait_for_timeout(900); T("closeSheet(); SPEECH.on=false")
    T("S.set.fcdir='l'; fcSession(null,5)"); pg.wait_for_timeout(900); pg.click('#sheet-body #rf-next'); pg.wait_for_timeout(600); T("document.querySelector('#sheet-body .fcback').scrollIntoView({block:'start'}); document.querySelector('#sheet').scrollBy(0,-14)"); pg.wait_for_timeout(300); pg.screenshot(path=OUT+'s-cards.jpg',type='jpeg',quality=74,clip={'x':0,'y':0,'width':390,'height':620}); print('shot s-cards.jpg'); T("closeSheet()")
    T("z50Ask('Đây là bạn tôi.','unit 6')"); pg.wait_for_timeout(500); pg.click('#sheet-body .z48chip:has-text("Why this word order?")'); pg.wait_for_timeout(200); shot('s-ask.jpg'); T("closeSheet()")
    T("z52Reps(null,3)"); pg.wait_for_timeout(1500); pg.screenshot(path=OUT+'s-reps.jpg',type='jpeg',quality=74,clip={'x':0,'y':0,'width':390,'height':510}); print('shot s-reps.jpg'); T("closeSheet()")
    # teacher
    tc=br.new_context(viewport={'width':1000,'height':900},device_scale_factor=1.5); tp=tc.new_page(); tp.on('pageerror',lambda e: print('TERR',e))
    def tshot(name,sel=None,h=None,full=False):
        o=dict(path=OUT+name,type='jpeg',quality=74)
        if sel:
            tp.locator(sel).first.scroll_into_view_if_needed(); tp.wait_for_timeout(200); bb=tp.locator(sel).first.bounding_box(); o['clip']={'x':max(0,bb['x']-8),'y':max(0,bb['y']-8),'width':bb['width']+16,'height':min(bb['height']+16,h or 1e9)}
        tp.screenshot(**o); print('shot',name)
    tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1500); tp.set_viewport_size({'width':1000,'height':300}); tp.wait_for_timeout(200); tshot('t-students.jpg'); tp.set_viewport_size({'width':1000,'height':900})
    tp.click('button:has-text("Khóa học · course plan")'); tp.wait_for_timeout(1200); tp.evaluate("window.scrollTo(0,0)"); tp.set_viewport_size({'width':1000,'height':1250}); tp.wait_for_timeout(200); tshot('t-plan.jpg'); tp.set_viewport_size({'width':1000,'height':900})
    tp.click('button:has-text("All students")'); tp.wait_for_timeout(900); tp.locator('.stu').first.click(); tp.wait_for_timeout(1600)
    tshot('t-lessons.jpg','.panel:has(h2:has-text("Lộ trình"))')
    a=tp.locator('.panel:has(h2:has-text("Kế hoạch"))').first; b=tp.locator('.panel:has(h2:has-text("Câu hỏi"))').first; a.scroll_into_view_if_needed(); tp.wait_for_timeout(200)
    tp.set_viewport_size({'width':1000,'height':1400}); a.scroll_into_view_if_needed(); tp.wait_for_timeout(300); ba=a.bounding_box(); bb=b.bounding_box()
    tp.screenshot(path=OUT+'t-week.jpg',type='jpeg',quality=74,clip={'x':ba['x']-8,'y':ba['y']-8,'width':ba['width']+16,'height':(bb['y']+bb['height'])-ba['y']+16}); print('shot t-week.jpg')
    tshot('t-recs.jpg','.panel:has(h2:has-text("Recordings"))',h=760)
    tp.set_viewport_size({'width':1000,'height':900}); tp.click('button:has-text("All students")'); tp.wait_for_timeout(900); tp.click('button:has-text("Thu âm · recording links")'); tp.wait_for_timeout(1500)
    tp.locator('button:has-text("listen to their recordings")').first.click(); tp.wait_for_timeout(600); tp.locator('button:text-is("Good")').first.click(); tp.wait_for_timeout(200)
    hd=tp.locator('.panel:has(button:has-text("listen to their recordings"))').first; hd.scroll_into_view_if_needed(); tp.wait_for_timeout(300); bb=hd.bounding_box()
    tp.screenshot(path=OUT+'t-voices.jpg',type='jpeg',quality=74,clip={'x':bb['x']-8,'y':max(0,bb['y']-8),'width':bb['width']+16,'height':min(bb['height']+16,560)}); print('shot t-voices.jpg')
    br.close()
