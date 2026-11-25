# Builds data/sent.json: the English of every Vietnamese sentence and phrase in the app, for "Cả câu · whole sentence"
# in the tap-a-word card. Run after any content change:  python3 src/sent/make_sent.py .   (add --gaps to list lines with no English)
# Sources: the three content blocks in index.html, every data/*.json file, art/cards.json, then src/sent/extra.tsv
# (hand-written English for lines the content has none for, and corrections, which win over the content).
import re,json,sys,glob,unicodedata,collections
repo=sys.argv[1]; s=open(repo+'/index.html',encoding='utf-8').read()
VN=re.compile('[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]',re.I)
EN=set("the a an is are am was were be to of in on at and or but it its this that these those what where who why how when which i you he she we they my your his her our their me him us them do does did not no yes with for from by as have has had can will would should please here there i'm you're don't it's one two three very so too just say said like want go going come get eat drink live near up out down little big good called every morning than then more all some any about into over only also still".split())
SYL=set()   # every syllable used in a 'vi' field: lets "anh", "ba", "con" count as Vietnamese without marks
def lang(x):
    if not isinstance(x,str): return None
    t=re.findall(r"[^\W\d_]+(?:'[a-z]+)?",x.lower())
    if not t: return None
    vn=sum(1 for w in t if VN.search(w) or (w in SYL and w not in EN)); en=len(t)-vn
    if SYL:
        if vn>=len(t)*0.6 and VN.search(x) or vn==len(t): return 'vn'
        return 'en' if en else 'vn'
    e2=sum(1 for w in t if w in EN)
    if e2>=max(1,len(t)*0.25) and e2>=vn*0.5: return 'en'
    return 'vn' if VN.search(x) else 'en'
def isvn(x): return lang(x)=='vn'
def allvn(x):   # every word looks Vietnamese ("y tá"), so it is not an English gloss
    t=re.findall(r"[^\W\d_]+",x.lower())
    return bool(t) and all(VN.search(w) or w in SYL or (len(w)<=2 and w not in EN) for w in t)
def isen(x): return lang(x)=='en'
def K(t):   # same as z79K in v7.js
    t=unicodedata.normalize('NFC',str(t)).lower()
    t=re.sub(r'[.,!?…;:"“”()]','',t); t=re.sub(r'[-–—]',' ',t); return re.sub(r'\s+',' ',t).strip()
NOTE=re.compile(r'^(swap|answer|southern|north|hanoi|south\b|change|reply|use |say |tip|or:|note|casual|polite|formal)',re.I)
pairs={}; seen=collections.OrderedDict()
def sents(t): return [x.strip() for x in re.findall(r'[^.!?…]+[.!?…]*[”"’)]?',t.replace(' / ','. ')) if x.strip(' “”"')]
def unq(t):   # a sentence cut out of a quote keeps only balanced quote marks
    for o,c in (('“','”'),('"','"')):
        if o!=c and t.count(c)>t.count(o): t=t.rstrip(c+' ')
        if o!=c and t.count(o)>t.count(c): t=t.lstrip(o+' ')
    return t.strip()
def add(vi,en,strong=False):
    if not isinstance(vi,str) or not isinstance(en,str) or '{' in vi or '___' in vi: return
    vi=vi.strip(); en=en.strip()
    if not vi or not en or not isvn(vi) or NOTE.match(en) or VN.search(en) and not isen(en) or en.startswith('<'): return
    ew=en.split()
    if not strong and len(ew)>12 and len(ew)>4*len(vi.split()): return   # a page blurb is not a translation
    k=K(vi)
    if not k: return
    if strong or k not in pairs: pairs[k]=en
    a,b=sents(vi),sents(en)            # "Chào chị. Tôi khỏe." → each sentence on its own too, when both sides split the same way
    if len(a)>1 and len(a)==len(b):
        for x,y in zip(a,b):
            if K(x) not in pairs: pairs[K(x)]=unq(y)
def see(v,where):
    if isinstance(v,str) and isvn(v) and '{' not in v:
        for line in v.split('\n'):
            m=re.match(r'^(?:[^:|#]{1,20}:\s*)?#?\s*(.+?)\s*\|\s*(.+)$',line.strip())
            if m: add(m.group(1),m.group(2)); line=m.group(1)
            m=re.match(r'^(.+?)\s+·\s+(.+)$',line.strip())
            if m and isvn(m.group(1)) and isen(m.group(2)): add(m.group(1),m.group(2)); line=m.group(1)
            for x in [line]+sents(line):
                k=K(x)
                if k and len(k.split())>=2 and isvn(x) and k not in seen: seen[k]=(x.strip(),where,K(line))
P={'vi':['en'],'xv':['xe'],'ex':['exen','xe'],'q':['qEn','en'],'a':['aEn'],'t':['en'],'text':['en'],'subj':['ens'],'line':['en'],'s':['en']}
def walk(o,w):
    if isinstance(o,dict):
        for k,v in o.items():
            if isinstance(v,str):
                see(v,w+'.'+k)
                if isvn(k) and isen(v) and not isen(k): add(k,v)      # glossaries: {"cà phê sữa đá": "iced milk coffee"}
                for p in P.get(k,[])+[k+'En',k+'en',k+'_en']:
                    if isinstance(o.get(p),str) and isen(o[p]): add(v,o[p]); break
            else: walk(v,w+'.'+k)
        if isinstance(o.get('alt'),list) and isinstance(o.get('qEn'),str):        # other ways to ask the same question
            for a in o['alt']:
                if isinstance(a,str): add(a,o['qEn'])
                elif isinstance(a,list) and a and isinstance(a[0],str): add(a[0],a[1] if len(a)>1 and isen(a[1]) else o['qEn'])
    elif isinstance(o,list):
        if len(o)>=3 and all(isinstance(x,str) for x in o[:3]) and isvn(o[0]) and isvn(o[1]) and isen(o[2]):   # street lines: casual, standard, English, note
            add(o[0],o[2]); add(o[1],o[2])
        for i,v in enumerate(o):
            if isinstance(v,str):
                see(v,w)
                if i+1<len(o) and isinstance(o[i+1],str) and isen(o[i+1]) and not allvn(o[i+1]): add(v,o[i+1])   # [vi, en] pairs; a list of words ("biên giới", "y tá") is not
            else: walk(v,w+'[]')
src=[]
for i in ['content','content6','content7']:
    src.append((i,json.loads(re.search(r'<script[^>]*id="%s"[^>]*>(.*?)</script>'%i,s,re.S).group(1))))
for f in sorted(glob.glob(repo+'/data/*.json'))+[repo+'/art/cards.json']:
    if f.endswith(('voice-lines.json','sent.json','ver.json')): continue
    try: src.append((f.split('/')[-1],json.load(open(f,encoding='utf-8'))))
    except Exception as e: print('skip',f,e)
def syl(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ('vi','xv','q','a') and isinstance(v,str) and VN.search(v): SYL.update(w for w in re.findall(r"[^\W\d_]+",v.lower()) if len(w)>1)
            else: syl(v)
    elif isinstance(o,list):
        for v in o: syl(v)
for n,o in src: syl(o)
SYL-=EN
for n,o in src: walk(o,n)
xn=0
for line in open(repo+'/src/sent/extra.tsv',encoding='utf-8'):
    if line.startswith('#') or '\t' not in line: continue
    vi,en=line.rstrip('\n').split('\t')[:2]
    if vi.strip() and en.strip(): pairs[K(vi)]=en.strip(); xn+=1
out={'v':1,'n':len(pairs),'s':dict(sorted(pairs.items()))}
open(repo+'/data/sent.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,separators=(',',':')))
gaps=[(k,v) for k,v in seen.items() if k not in pairs and v[2] not in pairs and K(re.sub(r'^[^:“"]{1,24}:\s+','',v[0])) not in pairs]
print('sentences with English: %d (hand-written: %d) · lines still without: %d'%(len(pairs),xn,len(gaps)))
if '--gaps' in sys.argv:
    for k,(x,w,_) in gaps: print(x+'\t'+w)
