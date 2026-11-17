# Builds data/voice-lines.json: every line a real speaker can record, in priority order.
import re,json,sys
repo=sys.argv[1]; s=open(repo+'/index.html').read()
C7=json.loads(re.search(r'<script[^>]*id="content7"[^>]*>(.*?)</script>',s,re.S).group(1))
C6=json.loads(re.search(r'<script[^>]*id="content6"[^>]*>(.*?)</script>',s,re.S).group(1))
parts=[]; seen=set()
def add(pid,vi_title,en_title,rows):
    out=[]
    for vi,en in rows:
        k=vi.strip().lower()
        if not vi.strip() or k in seen or '{' in vi: continue
        seen.add(k); out.append({'id':'%s_%03d'%(pid,len(out)+1),'vi':vi.strip(),'en':en})
    if out: parts.append({'id':pid,'vi':vi_title,'en':en_title,'lines':out})
cards=C7['cards']; by=lambda c:[x for x in cards if x['c']==c]
add('a1','75 câu hằng ngày','75 everyday phrases',[(c['vi'],c['en']) for c in by('p75')])
add('a2','Câu nói ngắn','Short sayings',[(c['vi'],c['en']) for c in by('say')])
add('a3','Sáu thanh','The six tones',[(t,'') for t in ['ma','má','mà','mả','mã','mạ','ba','bá','bà','bả','bã','bạ']])
rows=[]   # 31: the sound lessons, so the word and its sentence are heard in the same real voice
for g in C7['van']:
    for st in g.get('sets',[]):
        for it in st: rows.append((it[0],it[1]))
    for st in g.get('sets',[]):
        for it in st:
            if len(it)>4 and it[3]: rows.append((it[3],it[4]))
add('v0','Vần: từ và câu','Sound lessons: words and sentences',rows)
B=json.load(open(repo+'/data/beginner.json')); rows=[]
for st in B['steps']:
    for sp in st['stops']:
        for it in sp.get('items',[]): rows.append((it[0],it[1]))
rows+=[(x[0],x[1]) for x in B['you']]
add('z0','Người mới bắt đầu','Beginner path',rows)
add('b1','12 mẫu câu','12 sentence patterns',[(c['xv'],c['xe']) for c in by('pat') if c.get('xv')])
for st in json.load(open(repo+'/data/situations.json'))['s']:
    add('t_'+st['id'][:6],'Tình huống: '+st['vi'],'Situation: '+st['en'],[(t[1],t[2]) for t in st['turns']])
L=[('c1','Ăn uống, nơi chốn, đi lại','Food, places, getting around',['food','place','move']),('c2','Động từ, tính từ','Doing and describing words',['verb','adj']),('c3','Nhà, đồ dùng, gia đình, thời gian','Home, things, family, time',['home','wear','ppl','time']),('c4','Tiền, cơ thể, nghề, màu, con vật','Money, body, jobs, colours, animals',['money','body','job','color','animal'])]
for pid,vt,et,cs in L:
    rows=[]
    for c in cs:
        for x in by(c):
            rows.append((x['vi'],x['en']))
            if x.get('xv'): rows.append((x['xv'],x['xe']))
    add(pid,vt,et,rows)
n=1
for st in C7['stories']+C6['stories']:
    rows=[(l['vi'],l.get('en','')) for ch in st['ch'] for l in ch['lines']]
    add('s%d'%n,'Truyện: '+st['t'],'Story: '+st.get('en',st['t']),rows); n+=1
for Lv in json.load(open(repo+'/data/words13.json'))['levels']:
    rows=[]
    for c in Lv['cards']: rows.append((c['vi'],c['en'])); rows.append((c['xv'],c['xe']))
    add('w%d'%Lv['n'],'Từ mới: '+Lv['t'].split(' · ')[0],'New words: '+Lv['t'].split(' · ')[-1],rows)
# 27: core course lines are added last so the ids of every older line stay the same (recordings are stored by id), then moved up so speakers meet them early
try:
    for i,u in enumerate(json.load(open(repo+'/data/core.json'))['units']):   # 27: the core course, unit by unit (examples, then each word and its sentence)
        rows=[(e[0],e[1]) for e in u['ex']]
        for w in u['w']: rows.append((w[0],w[1])); rows.append((w[2],w[3]))
        rows+= [(x[0],x[1]) for x in u.get('xs',[])]   # 38: extra review sentences
        rows+= [(x[0],x[2]+' (Saigon street talk: say it casually)') for x in u.get('street',[])]   # 41: on-the-street lines
        add('k'+u['id'][1:],'Nền tảng %d: %s'%(i+1,u['vi']),'Core %d: %s'%(i+1,u['en']),rows)
    for g in json.load(open(repo+'/data/core.json')).get('st',[]):   # 38: graded stories, one after every few units
        add(g['id'],'Truyện ngắn: '+g['t'],'Short story: '+g['en'],[(l['vi'],l['en']) for l in g['lines']]+[r for q in g['qs'] for r in ((q['q'],q['en']),(q['a'],''))])
except FileNotFoundError: pass
try:
    X=json.load(open(repo+'/data/exam.json'))   # 29: test practice (questions with example answers, then the reading texts)
    add('x0','Câu hỏi hằng ngày','What people ask you every day',[r for q in X['daily']['q'] for r in ((q[0],q[1]),(q[2],q[3]))])
    # 42: the same questions asked to a woman (anh -> chị, vợ -> chồng), so women learners hear a real voice too
    import re as _re
    def _f(t):
        w=_re.split(r'(\s+)',t)
        for i in range(0,len(w)):
            m=_re.match(r'^([“"(]*)(anh|Anh)([.,!?…”")]*)$',w[i])
            if not m: continue
            prev=(w[i-2] if i>=2 else '').lower(); nxt=(w[i+2] if i+2<len(w) else '')
            if prev in ('tiếng','người','nước') or _re.match(r'^(ấy|trai|ta)\b',nxt,_re.I) or (_re.match(r'^[A-ZĐ]',nxt) and nxt not in ('Có','Là')): continue
            w[i]=m.group(1)+('Chị' if m.group(2)=='Anh' else 'chị')+m.group(3)
        t=''.join(w); t=_re.sub(r'(^|[\s“"(])vợ(?=[\s.,!?…”")]|$)',r'\1chồng',t); return t.replace('bạn gái','bạn trai')
    fq=[(_f(q[0]),q[1]) for q in X['daily']['q'] if _f(q[0])!=q[0]]
    add('x0c','Câu hỏi hằng ngày (hỏi chị)','Everyday questions, asked to a woman',fq)
    rows=[]
    for t in X['speak']:
        for q in t['q']: rows.append((q[0],q[1])); rows.append((q[2],q[3]))
    add('x1','Thi thử: hỏi và trả lời','Test practice: questions and answers',rows)
    add('x2','Thi thử: bài đọc','Test practice: reading texts',[(x,'') for t in X['read'] for x in t['text']])
except FileNotFoundError: pass
# 62: letters (their sound names), letter pairs, and the vowel pairs on their own, so the sound boards play a real voice
try:
    SD=json.load(open(repo+'/data/sounds.json')); rows=[]
    for x in SD['letters']+SD['pairs']:
        rows.append((x['s'],'the sound of the letter "%s", as in "%s"'%(x['k'],x['w']))); rows.append((x['w'],x['en']))
    for g in C7['chart'][1:]:
        for q in g[1]: rows.append((q[0],'the vowel sound "%s" on its own, as in "%s"'%(q[0],q[1]))); rows.append((q[1],''))
    add('ab','Bảng chữ cái và vần','Alphabet, letter pairs and vowel pairs',rows)
except FileNotFoundError: pass
# 63: the tap-around scenes (people, actions, "Đây là …", "… đang …") and the places for "Đây là đâu?"
try:
    SC=json.load(open(repo+'/data/scenes.json')); lc=lambda t:t[0].lower()+t[1:]
    for sc in SC['scenes']:
        rows=[]
        for q in sc['people']:
            rows.append((q['k'],q['en'])); rows.append(('Đây là %s.'%lc(q['subj']),'This is %s.'%lc(q['ens'])))
            a=[a for a in sc['actions'] if a['k']==q['act']]
            if a: rows.append(('%s đang %s.'%(q['subj'],a[0]['k']),'%s is %s.'%(q['ens'],a[0]['ing']))); rows.append(('%s đang làm gì?'%q['subj'],'What is %s doing?'%lc(q['ens'])))
        rows+=[(a['k'],a['en']) for a in sc['actions']]+[(d[0],d[1]) for d in sc['dlg']]
        add('sc_'+sc['id'],'Cảnh: '+sc['vi'],'Scene: '+sc['en'],rows)
    BD=SC.get('build',{}); rows=[('Đó là cái gì?','What is that?'),('Kia là con gì?','What animal is that over there?'),('Đây là phương tiện gì?','What kind of transport is this?'),('Anh là người nước nào?','Which country are you from?')]
    rows+=[('%s %s'%(x[2],x[0]),x[1]) for x in BD.get('things',[])]+[('con %s'%x[0],x[1]) for x in BD.get('animals',[])]+[(x[0],x[1]) for x in BD.get('rides',[])]
    rows+=[r for x in BD.get('lands',[]) for r in ((x[0],'the country'),('Tôi là người %s.'%x[0],'I am %s.'%x[1]))]
    rows+=[r for x in BD.get('goes',[]) for r in (('Em đến %s để làm gì?'%x[0],'What do you go to %s for?'%x[1]),('Em đến %s để %s.'%(x[0],x[2]),'I go to %s to %s.'%(x[1],x[3])))]
    add('sc_zb','Mẫu câu: chặng 2 và 3','Sentence builder: stages 2 and 3',rows)
    add('sc_pl','Cảnh: nơi chốn','Scenes: places',[('Đây là đâu?','Where is this?')]+[r for q in SC['places'] for r in ((q[0],q[1]),('Đây là %s.'%q[0],'This is the %s.'%q[1]))])
except FileNotFoundError: pass
ks=[p for p in parts if p['id'][0]=='k' and p['id'][1:].isdigit()]; gs={p['id']:p for p in parts if p['id'][0]=='g' and p['id'][1:].isdigit()}
try: GAT=[(g['id'],g['at']) for g in json.load(open(repo+'/data/core.json')).get('st',[])]
except FileNotFoundError: GAT=[]
core=[p for p in parts if p['id'] in ('x0','x0c')]
for n,kp in enumerate(ks):
    core.append(kp); core+=[gs[g] for g,at in GAT if at==n+1 and g in gs]
rest=[p for p in parts if p not in core]; at=next((n+1 for n,p in enumerate(rest) if p['id']=='z0'),0); parts=rest[:at]+core+rest[at:]
first=[p for p in parts if p['id']=='ab']+[p for p in parts if p['id'].startswith('sc_')]; parts=first+[p for p in parts if p not in first]   # 62-63: the sound boards and scenes come first
NOTES={'Anh nói với cô bán hàng: “Chào chị. Tôi muốn mưa một cái áo.”':'Câu này cố ý sai: trong truyện, Jake nói nhầm “mua” thành “mưa” nên cô bán hàng mới cười. Bạn cứ đọc đúng như chữ, có chữ “mưa”. · This mistake is on purpose: it is the joke of the story. Read it exactly as written.'}
for p in parts:
    for l in p['lines']:
        if l['vi'] in NOTES: l['note']=NOTES[l['vi']]
json.dump({'parts':parts},open(repo+'/data/voice-lines.json','w'),ensure_ascii=False,separators=(',',':'))
print([(p['id'],len(p['lines'])) for p in parts],'total',sum(len(p['lines']) for p in parts))
