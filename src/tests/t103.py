# v103: tap any Vietnamese (not a button) -> card with the whole sentence, its English, and tappable words with meanings.
# Also an audit: on each main screen, how many Vietnamese lines are tappable and how many have a saved English.
from playwright.sync_api import sync_playwright
import sys, json
B = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8890/'
CHROME = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'
AUDIT = r'''(function(){ var VN=Z103VN, out={blocks:0,tap:0,inBtn:0,en:0,miss:[]}, seen={};
  var els=[].slice.call(document.querySelectorAll($('#sheet').hidden?'#app *:not(script):not(style)':'#sheet-body *:not(script):not(style)')).filter(function(el){
    if(!el.offsetParent&&getComputedStyle(el).position!=='fixed') return false;
    var own=[].some.call(el.childNodes,function(n){ return n.nodeType===3&&VN.test(n.textContent) }); return own });
  els.forEach(function(el){ var b=el.closest('button,a,[role="button"],label,summary')?null:z103Block(el); var tx=(b||el).textContent.replace(/\s+/g,' ').trim(); if(seen[tx]) return; seen[tx]=1; out.blocks++;
    if(!b){ out.inBtn++; return } if(el.closest('.z60stage')&&!el.closest('.z60rev')) return; out.tap++;
    var rs=z103Resolve(b,tx,-1,''), ok=!!(rs&&rs.en);
    if(ok) out.en++; else if(out.miss.length<6) out.miss.push(tx.slice(0,70)) });
  return out })()'''
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME); errs = []
    for W, H in ((1366, 860), (390, 844)):
        pg = br.new_page(viewport={'width': W, 'height': H}); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(B); pg.wait_for_function("window.__T&&__T('typeof z103Load')==='function'", timeout=20000)
        pg.evaluate("c=>window.__T(c)", "z103Load().then(function(d){ try{ closeSheet() }catch(e){} return Object.keys(d).length })"); pg.wait_for_timeout(600); pg.evaluate("c=>window.__T(c)", "z27Unit(0)"); pg.wait_for_timeout(1200)
        n = pg.evaluate("c=>window.__T(c)", "Object.keys(Z103.d||{}).length")
        # find a plain (non-button) Vietnamese line on Home or in a lesson and tap a word in it
        res = pg.evaluate("c=>window.__T(c)", r'''(function(){ var c=[].slice.call(document.querySelectorAll('#sheet-body p, #sheet-body b, #sheet-body span, #sheet-body h1, #sheet-body h2, #sheet-body div')).filter(function(el){ var q=el.getBoundingClientRect(); return el.offsetParent&&q.top>0&&q.bottom<innerHeight&&document.elementFromPoint(q.left+3,q.top+q.height/2)&&el.contains(document.elementFromPoint(q.left+3,q.top+q.height/2))&&!el.closest(Z103SKIP)&&[].some.call(el.childNodes,function(n){ return n.nodeType===3&&Z103VN.test(n.textContent)&&n.textContent.trim().split(/\s+/).length>=2 }) })[0];
          if(!c) return null; var tn=[].filter.call(c.childNodes,function(n){ return n.nodeType===3&&Z103VN.test(n.textContent) })[0], r=document.createRange(), i=tn.textContent.search(/\S/); r.setStart(tn,i); r.setEnd(tn,i+1); var bx=r.getBoundingClientRect(); return {x:bx.left+bx.width/2,y:bx.top+bx.height/2,t:c.textContent.trim().slice(0,60)} })()''')
        print(W, 'pairs', n, 'tap target', res and res['t'])
        if res:
            pg.wait_for_timeout(800); pg.mouse.click(res['x'], res['y']); pg.wait_for_selector('#z103', timeout=4000)
            card = pg.evaluate("c=>window.__T(c)", "(function(){ var c=document.getElementById('z103'); return {words:c.querySelectorAll('.zw').length, en:c.querySelector('.z103en').textContent, word:(c.querySelector('.z103w:not([hidden])')||{}).textContent||'', inview: c.getBoundingClientRect().bottom<=innerHeight&&c.getBoundingClientRect().left>=0 } })()")
            print(W, 'card', card)
            pg.click('#z103 .zw >> nth=-1'); w2 = pg.evaluate("c=>window.__T(c)", "document.querySelector('#z103 .z103w').textContent")
            print(W, 'tap last word ->', w2)
            pg.keyboard.press('Escape'); print(W, 'closed', pg.evaluate("c=>window.__T(c)", "!document.getElementById('z103')"))
        # a button with Vietnamese must keep its own job (no card)
        btn = pg.evaluate("c=>window.__T(c)", "(function(){ var b=[].filter.call(document.querySelectorAll('#sheet-body button'),function(b){ return b.offsetParent&&Z103VN.test(b.textContent) })[0]; if(!b) return 'none'; var e=new MouseEvent('click',{bubbles:true}); Object.defineProperty(e,'target',{value:b}); z103Click(e); return !document.getElementById('z103') })()")
        print(W, 'button left alone', btn)
        if W == 1366:
            for name, js in (('home', "location.hash='home'"), ('lesson', "z27Unit(0)"), ('words', "location.hash='cards'"), ('story', "z61Read(z61All()[0],0)"), ('scenes', "Z59.act.scn()"), ('saigon', "z74Saigon()")):
                try:
                    pg.evaluate("c=>window.__T(c)", js); pg.wait_for_timeout(1500)
                    print('AUDIT', name, json.dumps(pg.evaluate("c=>window.__T(c)", AUDIT), ensure_ascii=False))
                except Exception as e:
                    print('AUDIT', name, 'could not open:', str(e)[:80])
                try: pg.evaluate("c=>window.__T(c)", "closeSheet()")
                except Exception: pass
        pg.close()
    print('errors', errs[:5]); br.close()
