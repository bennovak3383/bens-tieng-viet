from playwright.sync_api import sync_playwright
import json,urllib.request
B='http://localhost:8890'; errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--use-fake-ui-for-media-stream'])
    pg=br.new_context(viewport={'width':390,'height':844}).new_page(); pg.on('pageerror',lambda e: errs.append(str(e)))
    T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/#home'); pg.wait_for_timeout(1500)
    T("S.set.ob7=1; S.set.lvl0='more'; S.me.name='Ben'; S.set.k27={snd:1,d:{}}; save()"); pg.reload(); pg.wait_for_timeout(2200); T("try{closeSheet()}catch(e){}")
    print('units',T("Z27.units.length"),'| levels',T("Z27.units.map(function(u){return u.lv[0]+u.lv[1]}).join('')"))
    print('open at start:',T("z27N()"))
    T("Z27.units.forEach(function(u){ if(u.lv==='A1') z27St().d[u.id]={t:1} }); save()"); print('after A1 done:',T("z27N()"),'next unit:',T("Z27.units[z27Idx()].id+' '+Z27.units[z27Idx()].vi"))
    T("z27List()"); pg.wait_for_timeout(300); txt=pg.inner_text('#sheet-body'); i=txt.find('B1 preview'); print('list B1 line:',txt[i:i+120].replace('\n',' ')); T("closeSheet()")
    T("Z27.units.forEach(function(u){ if(u.lv==='A2') z27St().d[u.id]={t:1} }); save()"); print('after A2 done:',T("z27N()"),'next:',T("Z27.units[z27Idx()].id"))
    T("z27St().d={}; z27St().t='B1'; save()"); print('teacher B1:',T("z27N()")); T("z27St().t='A2'; save()"); print('teacher A2:',T("z27N()")); T("z27St().t='A1'; save()"); print('teacher A1:',T("z27N()"))
    # A2 done card text
    T("z27St().t=''; Z27.units.forEach(function(u){ if(u.lv!=='B1') z27St().d[u.id]={t:1} }); z27St().t='A2'; save()")
    T("z27St().t='A2'; Z27.units.forEach(function(u){ if(u.lv==='B1') delete z27St().d[u.id] });")
    # open each new unit and walk to the words step
    for uid in ['u46','u48','u47','u49','u50']:
        ui=T("Z27.units.findIndex(function(u){return u.id==='%s'})"%uid)
        T("z27Unit(%d)"%ui); pg.wait_for_timeout(300); h=pg.inner_text('#sheet-body')[:140].replace('\n',' / ')
        T("z26Learn&&0"); print(uid,'opens at',ui+1,':',h[:120]); T("closeSheet()")
    print('gaps per new unit:',[T("z27Gaps(Z27.units.find(function(u){return u.id==='%s'})).length"%u) for u in ['u46','u48','u47','u49','u50']])
    print('cards made for new units:',T("FC.filter(function(c){return /^k4[6-9]_|^k50_/.test(c.id)}).length"))
    br.close()
# server accepts B1 (no teacher key locally: just check code path by grepping)
print('ERR',errs or 'none')
