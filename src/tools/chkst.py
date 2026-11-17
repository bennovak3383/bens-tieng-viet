import sys,re,json,unicodedata
sys.path.insert(0,'/home/claude/bens-tieng-viet/src/core')
N=lambda s: unicodedata.normalize('NFC',s.strip())
def syl(s): return [x for x in re.sub(r'[“”"…·,.!?;:()/–—-]',' ',N(s).lower()).split() if x]
repo='/home/claude/bens-tieng-viet'
c=json.load(open(repo+'/data/core.json',encoding='utf8'))
base=set('ben lan nam mai tâm việt mỹ anh sài gòn huế hà nội một hai ba bốn năm sáu bảy tám chín mười mike úc'.split())
B=json.load(open(repo+'/data/beginner.json',encoding='utf8'))
for st in B['steps']:
    for sp in st['stops']:
        for it in sp.get('items',[]): base.update(syl(it[0]))
known_at=[]; k=set(base)
for u in c['units']:
    for w in u['w']: k.update(syl(w[0]))
    known_at.append(set(k))
cur=None; bad=0
for ln,raw in enumerate(open(repo+'/src/core/stories.txt',encoding='utf8'),1):
    l=N(raw)
    if not l or (l.startswith('#') and not l.startswith('##')): continue
    if l.startswith('## '): p=l[3:].split('|'); cur=int(p[1]); kn=known_at[cur-1]; continue
    t=l[0]; p=[x.strip() for x in l[1:].split('|')]
    if t=='+': kn=kn|set(syl(p[0])); continue
    for vi in ([p[0]] if t=='=' else [p[0],p[1]]):
        m=[x for x in syl(vi) if x not in kn]
        if m: bad+=1; print('LINE',ln,vi,'->',sorted(set(m)))
print('bad',bad)
