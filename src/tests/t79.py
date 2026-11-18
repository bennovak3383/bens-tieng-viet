# 79: one recording for the same words (capitals / punctuation do not count), and the recording page puts words first, lets the speaker pick anything, and drops finished parts to the bottom.
import json, re, unicodedata, collections
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
D=json.load(open('data/voice-lines.json'))['parts']; LINES=[l for p in D for l in p['lines']]
K=lambda s: re.sub(r'\s+',' ',re.sub(r'[-–—]',' ',re.sub(r'[.,!?…;:"“”()]','',unicodedata.normalize('NFC',s).lower()))).strip()
g=collections.defaultdict(list)
for l in LINES: g[K(l['vi'])].append(l)
twins=[v for v in g.values() if len(v)>1]; A,Bn=twins[0][0],twins[0][1]
print('lines',len(LINES),'| groups that differ only by capitals or punctuation:',len(twins),'| example:',repr(A['vi']),'/',repr(Bn['vi']))
def page(ctx,all_,url='/record.html?v=test&who=kim'):
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('REC '+str(e)))
    pg.route('**/api/voice/mine*',lambda r: r.fulfill(json={'done':{},'all':all_,'claims':{},'fixes':{},'lineFix':{},'g':{},'me':{}}))
    pg.route('**/api/voice/claim*',lambda r: r.fulfill(json={'ok':True}))
    # the page's code is closed off, so the test adds one line that lets it look inside (the real file is not changed)
    html=open('record.html',encoding='utf8').read(); cut=html.rindex('})();'); pg.route('**/record.html*',lambda r: r.fulfill(body=html[:cut]+'window.__R=function(c){ return eval(c) };\n'+html[cut:],content_type='text/html; charset=utf-8'))
    pg.add_init_script("navigator.mediaDevices=navigator.mediaDevices||{}; navigator.mediaDevices.getUserMedia=navigator.mediaDevices.getUserMedia||function(){ return Promise.reject(new Error('no mic in the lab')) }; window.MediaRecorder=window.MediaRecorder||function(){}")
    pg.goto(B+url); pg.wait_for_timeout(1800); return pg
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block')
    # --- the recording page, nothing recorded yet
    pg=page(ctx,{})
    print('RECORDING PAGE (nothing recorded)')
    print(' parts to do:',pg.locator('button.part:not(.done)').count(),'| groups shown:',[t[:44] for t in pg.locator('h3.grp').all_inner_texts()])
    info=pg.evaluate("(c)=>__R(c)","(function(){ var w=CH.filter(function(c){ return c.kind==='w' }), s=CH.filter(function(c){ return c.kind==='s' }), n=function(a){ return a.reduce(function(x,c){ return x+c.lines.length },0) }; return {w:w.length,s:s.length,wl:n(w),sl:n(s),firstS:CH.findIndex(function(c){ return c.kind==='s' }),allWordsFirst:CH.slice(0,w.length).every(function(c){ return c.kind==='w' }),maxW:Math.max.apply(null,w.map(function(c){ return Math.max.apply(null,c.lines.map(syl)) })),minS:Math.min.apply(null,s.map(function(c){ return Math.min.apply(null,c.lines.map(syl)) })),big:Math.max.apply(null,CH.map(function(c){ return c.lines.length })),ids:CH.every(function(c){ return /^[a-z0-9_]{1,40}$/.test(c.id) }),uniq:new Set(CH.map(function(c){ return c.id })).size===CH.length} })()")
    print(' word parts',info['w'],'with',info['wl'],'lines | sentence parts',info['s'],'with',info['sl'],'lines | no line lost:',info['wl']+info['sl']==len(LINES))
    print(' every word part is above every sentence part:',info['allWordsFirst'],'| longest "word" line',info['maxW'],'syllables | shortest sentence',info['minS'],'| biggest part',info['big'],'lines | part names fit the server and are unique:',info['ids'],info['uniq'])
    print(' the big button starts with:',pg.locator('button.btn.primary').first.inner_text()[:70])
    print(' same words, different punctuation → counted as one:',pg.evaluate("(c)=>__R(c)","K(%s)===K(%s)"%(json.dumps(A['vi']),json.dumps(Bn['vi']))),'| capitals:',pg.evaluate("(c)=>__R(c)","K('Cà Phê')===K('cà phê')"),'| different tones stay different:',pg.evaluate("(c)=>__R(c)","K('ma')!==K('má')"))
    # pick something else: a sentence part far down the list
    pg.locator('button.part:not(.done)').nth(info['firstS']+5).click(); pg.wait_for_timeout(500)
    t=pg.locator('.line').inner_text(); print(' picking a sentence part further down opens it:',len(K(t).split(' '))>3,'|',t[:50]); pg.close()
    # --- someone recorded: one twin, the whole first word part, and half of the second
    first=None
    pg=page(ctx,{}); ch=pg.evaluate("(c)=>__R(c)","CH.slice(0,3).map(function(c){ return {id:c.id,vi:c.vi,lines:c.lines.map(function(l){ return [l.id,l.vi] })} })"); pg.close()
    done={l[0]:[1,l[1]] for l in ch[0]['lines']}; done.update({l[0]:[1,l[1]] for l in ch[1]['lines'][:len(ch[1]['lines'])//2]}); done[A['id']]=[1,A['vi']]
    pg=page(ctx,{'an':done})
    print('RECORDING PAGE (someone else recorded part 1, half of part 2, and %r)'%A['vi'])
    print(' the twin %r now counts as recorded:'%Bn['vi'],pg.evaluate("(c)=>__R(c)","(function(){ var l=null; CH.forEach(function(c){ c.lines.forEach(function(x){ if(x.id===%s) l=x }) }); return covered(l)&&!need(l) })()"%json.dumps(Bn['id'])))
    names=pg.locator('button.part:not(.done) b').all_inner_texts()
    print(' finished part 1 is gone from the list:',ch[0]['vi'] not in names,'| the list now starts with part 2:',names[0]==ch[1]['vi'],'| it shows only what is left:',pg.locator('button.part:not(.done) .n').first.inner_text())
    fb=pg.locator('button.x',has_text='đã xong'); print(' finished parts sit at the bottom behind:',fb.inner_text()[:40],'| it is the last thing on the page:',pg.evaluate("(c)=>__R(c)","(function(){ var b=[].filter.call(document.querySelectorAll('button.x'),function(x){ return /đã xong/.test(x.textContent) })[0], ps=document.querySelectorAll('button.part'); return b.getBoundingClientRect().top>ps[ps.length-1].getBoundingClientRect().top })()"))
    fb.click(); pg.wait_for_timeout(300); print(' opened: finished parts',pg.locator('button.part.done').count(),'| first is part 1:',pg.locator('button.part.done b').first.inner_text()==ch[0]['vi'])
    pg.locator('button.part:not(.done)').first.click(); pg.wait_for_timeout(500); print(' opening part 2 starts on its first unrecorded line:',pg.locator('.line').inner_text()==ch[1]['lines'][len(ch[1]['lines'])//2][1])
    pg.locator('button.x').first.click(); pg.wait_for_timeout(1500); pg.locator('button.szc').nth(1).click(); pg.wait_for_timeout(300); print(' "short" filter still works:',pg.locator('button.part:not(.done)').count()>0,'| groups still labelled:',pg.locator('h3.grp').count()); pg.close()
    pg=page(ctx,{'an':done},'/record.html?v=test&who=kim&part=ab'); print(' a link with &part=ab opens the alphabet part:',pg.locator('.line').count()==1 and pg.evaluate("(c)=>__R(c)","document.body.textContent.indexOf('Alphabet')>=0||document.body.textContent.indexOf('chữ')>=0")); pg.close()
    # --- the app: playback
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2200); T("S.set.ob7=1; S.set.vx='r'; S.set.src='auto'; save()")
    print('THE APP (a real recording exists only for %r)'%A['vi'])
    T("Z17.map={}; Z17.map[%s]=['v:/api/voice/clip?w=an&i=x&t=1']"%json.dumps(A['vi']))
    f=lambda s: T("(function(){ var c=clipFor(%s); return !!(c&&String(c[0]).indexOf('w=an')>0) })()"%json.dumps(s))
    print(' plays for the exact text:',f(A['vi']),'| for its twin:',f(Bn['vi']),'| in capitals:',f(A['vi'].upper()),'| with extra spaces and "!":',f('  '+A['vi'].replace(' ','  ')+' !'),'| not for other words:',not f('xin chào'))
    print(' a line with no real recording still gets its old clip:',T("(function(){ var k=Object.keys(AUD.idx.clips)[5]; var c=clipFor(k); return !!c&&String(c[0]).indexOf('w=an')<0 })()"),'| phone-voice setting still returns none:',T("(function(){ var o=S.set.src; S.set.src='phone'; var c=clipFor(%s); S.set.src=o; return c===null })()"%json.dumps(A['vi'])))
    br.close()
print('ERR',errs or 'none')
