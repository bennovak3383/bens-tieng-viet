# v102: a phrase with no whole recording is said in one voice (or by the device voice), never mixed voices.
from playwright.sync_api import sync_playwright
import sys
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8890/'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); pg = b.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_function("window.__T&&__T('AUD.idx&&Object.keys(AUD.idx.clips).length>100')", timeout=20000); pg.wait_for_timeout(4000)
    r = pg.evaluate('c=>window.__T(c)', '''(function(){ var log=[], said=[];
      playClip=function(c,r,onend){ log.push(c[3]); setTimeout(function(){ onend&&onend() },5) };
      speakPhone=function(t,o){ said.push(t); o&&o.onend&&o.onend(); return true };
      var ws=Object.keys(AUD.idx.clips).filter(function(k){ var c=AUD.idx.clips[k]; return !/\\s/.test(k)&&c.some(function(x){return x[3]===0})&&c.some(function(x){return x[3]===1}) }).slice(0,6);
      var phrase=ws.join(' '), res={phrase:phrase, whole:!!z102List(phrase), runs:[]};
      return new Promise(function(done){ VOICES=[]; var k=0;
        (function go(){ if(k>=8){ VOICES=[{voiceURI:'x',lang:'vi-VN'}]; log.length=0; said.length=0; zSay(phrase);
            setTimeout(function(){ res.device={clips:log.length, said:said.length}; done(res) },300); return }
          log.length=0; zSay(phrase,{onend:function(){ res.runs.push(new Set(log).size+'/'+log.length); k++; go() }}) })() }) })()''')
    print(r)
    ok = (not r['whole']) and all(x.startswith('1/6') for x in r['runs']) and r['device'] == {'clips': 0, 'said': 1} and not errs
    print('errors', errs); print('PASS' if ok else 'FAIL'); b.close()
