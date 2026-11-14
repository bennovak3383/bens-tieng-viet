from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); pg=br.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8890/#home'); pg.wait_for_timeout(2500)
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    r=T("""(function(){ var j=JSON.parse(document.getElementById('audio6idx').textContent), ks=Object.keys(j).filter(function(k){ return AUD.idx.clips[k][0][0]>=AUD.idx.bundles.length-2 }); var out=[]; return Promise.all(ks.filter(function(k,i){ return i%50===0 }).map(function(k){ var c=AUD.idx.clips[k][0]; return loadBundle(c[0]).then(function(ab){ var u=new Uint8Array(ab.slice(c[1],c[1]+2)); return [k,AUD.idx.bundles[c[0]],u[0].toString(16)+u[1].toString(16),c[2]] }) })).then(function(a){ return {n:ks.length,bundles:AUD.idx.bundles.slice(-3),samples:a} }) })()""")
    print(json.dumps(r,ensure_ascii=False)[:900]); print('ERR',errs)
    br.close()
