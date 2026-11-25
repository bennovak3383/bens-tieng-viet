# v103: tap a word, and v104: highlight words, the card also shows the whole sentence with its English. Word part unchanged.
# Usage: python3 src/tests/t103.py [URL]   (test site from src/tools/build.sh, with window.__T)
from playwright.sync_api import sync_playwright
import sys
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8890/'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); pg = b.new_page(viewport={'width':420,'height':860}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_function("window.__T&&__T('typeof z103Find')==='function'", timeout=20000)
    pg.wait_for_function("__T('z103Load().then(function(){return 1})')&&__T('!!Z103.s')", timeout=20000)
    pg.evaluate('''c=>window.__T(c)''', '''(function(){ zSay=function(){}; var d=document.createElement('p'); d.id='t103'; d.style.cssText='position:fixed;top:120px;left:10px;z-index:99;background:#fff;font-size:22px';
      d.innerHTML='Lan: Mắc quá cô ơi. <b>Bớt</b> chút được không cô?'; document.body.appendChild(d) })()''')
    box = pg.locator('#t103 b').bounding_box(); pg.mouse.click(box['x']+box['width']/2, box['y']+box['height']/2); pg.wait_for_timeout(400)
    r = pg.evaluate('''c=>window.__T(c)''', '''(function(){ var p=document.querySelector('.z80pop'); if(!p) return null; var s=p.querySelector('.z103s');
      return {word:p.querySelector('.z61pw b').textContent, sent:s&&s.querySelector('b').textContent, en:s&&s.querySelector('.z103e').textContent, save:!!p.querySelector('.z80row')} })()''')
    print(r)
    ok = r and r['word'].lower().startswith('bớt') and r['sent'] == 'Bớt chút được không cô?' and r['en'] == 'Can you take a little off?'
    # v104: drag across the words to highlight them: the card shows what they mean together, and no word card opens on mouse-up
    t = pg.locator('#t103'); bb = t.bounding_box(); y = bb['y']+bb['height']/2
    x0 = pg.evaluate('''c=>window.__T(c)''', '''(function(){ var n=document.getElementById('t103').lastChild, r=document.createRange(); r.setStart(n,1); r.setEnd(n,2); return r.getBoundingClientRect().left-8 })()''')
    pg.mouse.click(5, 5); pg.mouse.move(x0, y); pg.mouse.down(); pg.mouse.move(bb['x']+bb['width']-2, y, steps=8); pg.mouse.up(); pg.wait_for_timeout(700)
    r2 = pg.evaluate('''c=>window.__T(c)''', '''(function(){ var p=document.querySelector('.z80pop.z103sel'); return p?{vi:p.querySelector('.z103v').textContent,en:p.querySelector('.z103e').textContent}:null })()''')
    print(r2)
    ok = ok and r2 and 'chút được không cô' in r2['vi'] and r2['en'] in ('Can you take a little off?', 'Part of the sentence below') and not errs
    print('errors', errs); print('PASS' if ok else 'FAIL'); b.close()
