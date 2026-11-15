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
        add('k'+u['id'][1:],'Nền tảng %d: %s'%(i+1,u['vi']),'Core %d: %s'%(i+1,u['en']),rows)
    for g in json.load(open(repo+'/data/core.json')).get('st',[]):   # 38: graded stories, one after every few units
        add(g['id'],'Truyện ngắn: '+g['t'],'Short story: '+g['en'],[(l['vi'],l['en']) for l in g['lines']]+[r for q in g['qs'] for r in ((q['q'],q['en']),(q['a'],''))])
except FileNotFoundError: pass
try:
    X=json.load(open(repo+'/data/exam.json'))   # 29: test practice (questions with example answers, then the reading texts)
    add('x0','Câu hỏi hằng ngày','What people ask you every day',[r for q in X['daily']['q'] for r in ((q[0],q[1]),(q[2],q[3]))])
    rows=[]
    for t in X['speak']:
        for q in t['q']: rows.append((q[0],q[1])); rows.append((q[2],q[3]))
    add('x1','Thi thử: hỏi và trả lời','Test practice: questions and answers',rows)
    add('x2','Thi thử: bài đọc','Test practice: reading texts',[(x,'') for t in X['read'] for x in t['text']])
except FileNotFoundError: pass
ks=[p for p in parts if p['id'][0]=='k' and p['id'][1:].isdigit()]; gs={p['id']:p for p in parts if p['id'][0]=='g' and p['id'][1:].isdigit()}
try: GAT=[(g['id'],g['at']) for g in json.load(open(repo+'/data/core.json')).get('st',[])]
except FileNotFoundError: GAT=[]
core=[p for p in parts if p['id']=='x0']
for n,kp in enumerate(ks):
    core.append(kp); core+=[gs[g] for g,at in GAT if at==n+1 and g in gs]
rest=[p for p in parts if p not in core]; at=next((n+1 for n,p in enumerate(rest) if p['id']=='z0'),0); parts=rest[:at]+core+rest[at:]
NOTES={'Anh nói với cô bán hàng: “Chào chị. Tôi muốn mưa một cái áo.”':'Câu này cố ý sai: trong truyện, Jake nói nhầm “mua” thành “mưa” nên cô bán hàng mới cười. Bạn cứ đọc đúng như chữ, có chữ “mưa”. · This mistake is on purpose: it is the joke of the story. Read it exactly as written.'}
for p in parts:
    for l in p['lines']:
        if l['vi'] in NOTES: l['note']=NOTES[l['vi']]
json.dump({'parts':parts},open(repo+'/data/voice-lines.json','w'),ensure_ascii=False,separators=(',',':'))
print([(p['id'],len(p['lines'])) for p in parts],'total',sum(len(p['lines']) for p in parts))
