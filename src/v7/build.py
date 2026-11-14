import json,re,sys
sys.path.insert(0,'/home/claude/v7')
SRC='/mnt/user-data/outputs/artifacts/4cb3761d-5b74-409b-b4e8-77075755f285/index.html'
s=open(SRC,encoding='utf-8').read()
# make idempotent: strip an earlier v7 build
if 'id="content7"' in s:
    a=s.find('<script type="application/json" id="content7">'); b=s.find('</script>\n',a)+10; s=s[:a]+s[b:]
    a=s.find('/* v7 */'); b=s.find('</style>',a); s=s[:a]+s[b:]
    a=s.find('<!-- CARDS (v7) -->'); b=s.find('\n</div>\n\n<div class="tabs">',a); s=s[:a].rstrip('\n')+s[b:]
    a=s.find('/* ===== Version 7'); b=s.find("\ngo(location.hash.slice(1)||'home');",a); s=s[:a].rstrip('\n')+s[b:]
    assert 'id="content7"' not in s and 'Version 7' not in s
exec(open('/home/claude/v7/vowels.py').read()); exec(open('/home/claude/v7/cards.py').read()); exec(open('/home/claude/v7/stories.py').read()); exec(open('/home/claude/v7/gloss.py').read()); exec(open('/home/claude/v7/fix_content.py').read())
# content fixes
a=s.find('id="content">')+len('id="content">'); b=s.find('</script>',a)
c=json.loads(s[a:b]); c2,n=fix(c,None); assert n==45
s=s[:a]+json.dumps(c2,ensure_ascii=False).replace('</','<\\/')+s[b:]
COUNTRIES=[("Mỹ","American","usa|us|america|united states"),("Úc","Australian","australia"),("Anh","British","uk|england|britain|united kingdom"),("Canada","Canadian",""),("Pháp","French","france"),("Đức","German","germany"),
("Hàn Quốc","Korean","korea|south korea"),("Trung Quốc","Chinese","china"),("Nhật","Japanese","japan"),("Đài Loan","Taiwanese","taiwan"),("Singapore","Singaporean",""),("Thái Lan","Thai","thailand"),("Philippines","Filipino","philippine"),("Ấn Độ","Indian","india"),
("Ý","Italian","italy"),("Tây Ban Nha","Spanish","spain"),("Hà Lan","Dutch","netherlands|holland"),("Thụy Điển","Swedish","sweden"),("Ireland","Irish",""),("New Zealand","New Zealander","nz|kiwi"),("Nga","Russian","russia"),("Nam Phi","South African","south africa"),("Brazil","Brazilian",""),("Mexico","Mexican","")]
a6=s.find('id="content6">')+len('id="content6">'); b6=s.find('</script>',a6); c6=json.loads(s[a6:b6])
for sl in c6['slots']:
    if sl['k']=='country': sl['o']=[[x[0],x[1]] for x in COUNTRIES]
s=s[:a6]+json.dumps(c6,ensure_ascii=False).replace('</','<\\/')+s[b6:]
# content7
cards=[]; cnt={}
for cat,e,vi,en,xv,xe in C:
    cnt[cat]=cnt.get(cat,0)+1; cards.append({"id":cat+str(cnt[cat]),"c":cat,"e":e,"vi":vi,"en":en,"xv":xv,"xe":xe})
cats={k:[vi,en,em] for k,vi,en,em in CATS}
stories=[]
for st in S:
    chs=[]
    for ch in st['ch']:
        lines=[]
        for p in ch['paras']:
            for i,(vi,en) in enumerate(p): lines.append({"vi":vi,"en":en,"p":1 if i==0 else 0})
        chs.append({"t":ch['t'],"en":ch['en'],"pic":ch['pic'],"new":ch['new'],"lines":lines,"qs":[{"q":q,"a":a2,"en":e2} for q,a2,e2 in ch['qs']]})
    stories.append({"id":st['id'],"t":st['t'],"en":st['en'],"pic":st['pic'],"lv":st['lv'],"ch":chs})
gl={}
for x in cards:
    k=x['vi'].lower().rstrip('?').strip()
    gl.setdefault(k,x['en'])
gl.update({k.lower():v for k,v in G.items()})
gl.update({"sách":"book","to":"big; heavy (rain)","ấy":"that; (cô ấy = she)","piano":"piano","mươi":"tens (ba mươi = thirty)","mực":"Mực (the dog's name; also 'squid' / 'ink')","hana":"Hana (a name)","jake":"Jake (a name)","thu":"Thu (a name)","hạnh":"Hạnh (a name)","minh":"Minh (a name)"})
c7={"van":VAN,"twist":TWIST,"rule":RULE,"chart":CHART,"countries":[list(x) for x in COUNTRIES],"cats":cats,"cards":cards,"stories":stories,"gloss":gl}
tag='<script type="application/json" id="content7">'+json.dumps(c7,ensure_ascii=False).replace('</','<\\/')+'</script>\n'
s=s.replace('<script type="application/json" id="content6">',tag+'<script type="application/json" id="content6">',1)
# tabs
old_nav=s[s.find('<nav id="tabs">'):s.find('</nav>')+6]
new_nav='''<nav id="tabs">
  <button class="tab" data-go="home"><b>Hôm nay</b>Today</button>
  <button class="tab" data-go="prac"><b>Luyện tập</b>Practice</button>
  <button class="tab" data-go="prog"><b>Tiến độ</b>Progress</button>
  <button class="tab" data-go="more"><b>Thêm</b>More</button>
</nav>'''
s=s.replace(old_nav,new_nav)
# sections
marker='\n</div>\n\n<div class="tabs">'
assert marker in s
s=s.replace(marker,'\n'+open('/home/claude/v7/sections.html').read()+marker,1)
# css
s=s.replace('</style></head>','</style></head>',1)
i=s.rfind('</style>',0,s.find('<div class="tabs">'))
s=s[:i]+open('/home/claude/v7/v7.css').read()+s[i:]
# merge keys
s=s.replace("'ms','d6','w'].forEach(function(k){ if(src[k]","'ms','d6','w','fc','fcn'].forEach(function(k){ if(src[k]",1)
assert "'fc','fcn'" in s
s=s.replace('quiet=setTimeout(finish,2600)','quiet=setTimeout(finish,SPEECH.fast||2600)')
assert 'SPEECH.fast||2600' in s
# js layer
end="\ngo(location.hash.slice(1)||'home');\nrenderAll();"
assert s.count(end)==1
s=s.replace(end,'\n'+open('/home/claude/v7/v7.js').read()+end)
# hero text + title
s=s.replace('<p class="small">Hear it, say it, read it. One session a day.</p>','<p class="small">One session a day: sounds, cards, speaking, a story, a scene.</p>')
s=s.replace('One session a day: cards, questions, a story, a scene.','One session a day: sounds, cards, speaking, a story, a scene.') # HERO8
open('/home/claude/v7/index.html','w',encoding='utf-8').write(s)
print(len(s), len(cards), len(stories))
