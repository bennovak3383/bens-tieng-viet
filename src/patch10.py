# Version 10 build: take the live 9.2 index.html, swap in the new v7 layer files, and move the embedded
# clips (script tag audio6) out into audio/e6a.b64 + audio/e6b.b64 (base64 text) (split at a clip boundary).
# Usage: python3 patch10.py OLD_SRC_DIR NEW_SRC_DIR LIVE_INDEX OUT_DIR
import sys,json,base64,os
old,new,live,out=sys.argv[1:5]
s=open(live,encoding='utf-8').read()
for f in ['v7/v7.js','v7/v7.css','v7/sections.html']:
    a=open(old+'/'+f,encoding='utf-8').read(); b=open(new+'/'+f,encoding='utf-8').read()
    assert s.count(a)==1, f; s=s.replace(a,b)
a=s.find('<script type="text/plain" id="audio6">')
if a>=0:
    a2=s.find('>',a)+1; b=s.find('</script>',a2); raw=base64.b64decode(s[a2:b].strip())
    ia=s.find('<script type="application/json" id="audio6idx">'); ia2=s.find('>',ia)+1; ib=s.find('</script>',ia2); idx=json.loads(s[ia2:ib])
    assert all(raw[o]==0xff and (raw[o+1]&0xe0)==0xe0 for o,l in idx.values())
    cut=min(o for o,l in idx.values() if o>=len(raw)//2)
    new_idx={k:([0,o,l] if o<cut else [1,o-cut,l]) for k,(o,l) in idx.items()}
    os.makedirs(out+'/audio',exist_ok=True)
    open(out+'/audio/e6a.b64','w').write(base64.b64encode(raw[:cut]).decode()); open(out+'/audio/e6b.b64','w').write(base64.b64encode(raw[cut:]).decode())
    s=s[:ia2]+json.dumps(new_idx,ensure_ascii=False)+s[ib:]
    a=s.find('<script type="text/plain" id="audio6">'); b=s.find('</script>',a)+9
    if s[b:b+1]=='\n': b+=1
    s=s[:a]+s[b:]
# base fixes (idempotent)
s=s.replace("r.lang='vi-VN'; r.interimResults","r.lang=SPEECH.lang||'vi-VN'; r.interimResults")  # 11: lets the chat listen in English once
open(out+'/index.html','w',encoding='utf-8').write(s); print('ok',len(s.encode()))
