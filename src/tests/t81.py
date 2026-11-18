# 81: the lesson quiz. Its questions come only from that lesson (the teacher's course); the review quiz is unchanged.
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
SETUP="S.set.ob7=1; S.set.lvl0='some'; S.me.name='Anna'; var d={}; Z27.units.slice(0,12).forEach(u=>d[u.id]={t:1}); S.set.k27={snd:1,d:d}; S.set.in48={t:Date.now(),goal:'chat',mins:60,days:6,r:[{t:Date.now()}],sit:[],hard:[],tried:[]}; save(); try{closeSheet()}catch(e){}; renderAll()"
import json
def answer(pg,T,right=True):
    st=pg.locator('.z60stage'); kind=st.get_attribute('data-t'); a=st.get_attribute('data-a')
    if kind=='order':
        for i in range(pg.locator('.z74w').count()): pg.locator('.z74w[data-i="%d"]'%i).click()
    else:
        pg.locator('.z74o[data-k=%s]'%json.dumps(a,ensure_ascii=False)).click()
    pg.wait_for_timeout(2100)
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'); ctx=br.new_context(viewport={'width':393,'height':800},service_workers='block')
    pg=ctx.new_page(); pg.on('pageerror',lambda e: errs.append('APP '+str(e))); T=lambda c: pg.evaluate('(c)=>__T(c)',c)
    pg.goto(B+'/'); pg.wait_for_timeout(2200); T(SETUP); pg.wait_for_timeout(500)
    info=T("(function(){ var ls=z53Ls(), L=ls[0], P=z81Pool(L), own={}; for(var i=L.from;i<=L.to;i++){ var u=Z27.units[i]; (u.w||[]).forEach(function(w){ own[String(w[0]).toLowerCase()]=1 }); (u.ex||[]).forEach(function(e){ own[String(e[0]).toLowerCase()]=1 }) } z53Dlgs(L).forEach(function(d){ d.lines.forEach(function(l){ own[String(l.vi||l[1]).toLowerCase()]=1 }) }); var k={}; P.forEach(function(x){ k[x.src]=(k[x.src]||0)+1 }); return {n:P.length,kinds:k,onlyOwn:P.every(function(x){ return own[x.vi.toLowerCase()] }),other:z81Pool(ls[1]).some(function(x){ return P.some(function(y){ return y.vi===x.vi }) }),locked:z81Pool(ls[ls.length-1]).length} })()")
    print('lesson 1 quiz set:',info['n'],'items',info['kinds'],'| every item is from lesson 1:',info['onlyOwn'],'| shares items with lesson 2:',info['other'],'| a lesson with nothing finished has',info['locked'],'items')
    T("z53Lesson(z53Ls()[0])"); pg.wait_for_timeout(600); row=pg.locator('#sheet-body .z53p',has_text='Lesson quiz'); print('lesson page: quiz row',row.count(),'|',row.locator('.small').inner_text()[:80],'| button:',row.locator('button').inner_text())
    row.locator('button').click(); pg.wait_for_timeout(900); print('quiz opens:',pg.locator('.sess-top .lbl').inner_text(),'|',pg.locator('.z62q small').inner_text())
    seen=[]
    for i in range(10):
        if pg.locator('.z60end').count(): break
        seen.append(pg.locator('.z60stage').get_attribute('data-t')); answer(pg,T)
    pg.wait_for_timeout(600); print('question kinds met:',sorted(set(seen)),'| end screen:',pg.locator('.z60big').inner_text() if pg.locator('.z60big').count() else 'NOT REACHED','| back button:',pg.locator('.z81back').count())
    print('score kept on the lesson:',T("JSON.stringify((function(){ var q=z53St(z53Ls()[0].l.id).qz; return {n:q.n,last:q.last,best:q.best} })())"),'| the review quiz record was not touched:',T("!S.set.rv74||!S.set.rv74.t"))
    pg.locator('.z81back').click(); pg.wait_for_timeout(600); row=pg.locator('#sheet-body .z53p',has_text='Lesson quiz'); print('back on the lesson page the row shows:',row.locator('b').first.inner_text()[:60],'| button:',row.locator('button').inner_text())
    T("z53Lesson(z53Ls()[z53Ls().length-1])"); pg.wait_for_timeout(500); row=pg.locator('#sheet-body .z53p',has_text='Lesson quiz'); print('a lesson not started: quiz row',row.count(),'| button shown:',row.locator('button').count(),'|',row.locator('.small').inner_text()[:60]); T("closeSheet()")
    T("z74Review()"); pg.wait_for_timeout(900); print('review quiz still opens as itself:',pg.locator('.sess-top .lbl').inner_text(),'|',pg.locator('.z62q small').inner_text()); br.close()
print('ERR',errs or 'none')
