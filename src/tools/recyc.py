import json,re,collections,sys
c=json.load(open('/home/claude/bens-tieng-viet/data/core.json',encoding='utf8'))
def norm(s): return ' '+re.sub(r'[^\w\s]',' ',s.lower())+' '
S=[]
for u in c['units']:
    for e in u['ex']: S.append(norm(e[0]))
    for w in u['w']: S.append(norm(w[2]))
    for x in u.get('xs',[]): S.append(norm(x[0]))
for st in c.get('st',[]):
    for l in st['lines']: S.append(norm(l['vi']))
out={}
for lv in ['A1','A2','B1']:
    ws=[(u['id'],w[0]) for u in c['units'] if u['lv']==lv for w in u['w']]
    cnt=[(sum(1 for s in S if ' '+w.lower()+' ' in s),uid,w) for uid,w in ws]
    b=collections.Counter('1' if n<=1 else '2' if n==2 else '3+' for n,_,_ in cnt)
    print(lv,len(ws),dict(b))
    out[lv]=[(uid,w,n) for n,uid,w in cnt if n<=2]
if len(sys.argv)>1:
    for uid,w,n in out[sys.argv[1]]: print(uid,w,n,sep='|')
