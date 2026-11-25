# v103: tap a word, the card also shows the whole sentence with its English. Word part unchanged.
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
    ok = r and r['word'].lower().startswith('bớt') and r['sent'] == 'Bớt chút được không cô?' and r['en'] == 'Can you take a little off?' and not errs
    print('errors', errs); print('PASS' if ok else 'FAIL'); b.close()
