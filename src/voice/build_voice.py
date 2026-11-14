# Cut a real speaker's recordings at the pauses and load them into the app as voice 2 ("real voice").
# usage: python3 build_voice.py REPO part1.m4a part2.m4a part3.m4a
import subprocess,numpy as np,sys,json,re,os,tempfile
SR=16000; OSR=44100
repo=sys.argv[1]; files=sys.argv[2:5]
def load(f,sr): return np.frombuffer(subprocess.run(['ffmpeg','-v','quiet','-i',f,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout,dtype=np.int16).astype(np.float32)/32768
def segs(x,gap=0.5,minlen=0.15):
    hop=int(SR*0.01); n=len(x)//hop; e=np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()) for i in range(n)]); db=20*np.log10(e+1e-7)
    floor=np.percentile(db,10); top=np.percentile(db,95); thr=floor+(top-floor)*0.35; on=db>thr; out=[]; i=0
    while i<n:
        if on[i]:
            j=i; last=i
            while j<n and (on[j] or (j-last)*0.01<gap):
                if on[j]: last=j
                j+=1
            if (last-i)*0.01>=minlen: out.append((i*0.01,(last+1)*0.01))
            i=j
        else: i+=1
    return out
s=open(repo+'/index.html').read()
C=json.loads(re.search(r'<script[^>]*id="content7"[^>]*>(.*?)</script>',s,re.S).group(1))
texts=[[c['vi'] for c in C['cards'] if c['c']=='p75'],[c['vi'] for c in C['cards'] if c['c']=='say'],['ma','má','mà','mả','mã','mạ','ba','bá','bà','bả','bã','bạ']]
idx=json.load(open(repo+'/audio/index.json'))
# remove an earlier build of this voice
old=[i for i,b in enumerate(idx['bundles']) if b.startswith('r')]
for k in list(idx['clips']): idx['clips'][k]=[c for c in idx['clips'][k] if not (len(c)>3 and c[3]==2)]
idx['bundles']=[b for b in idx['bundles'] if not b.startswith('r')]
bi=len(idx['bundles']); blob=b''; n=0; report=[]
tmp=tempfile.mkdtemp()
for f,tx in zip(files,texts):
    sg=segs(load(f,SR)); hi=load(f,OSR)
    if len(sg)>len(tx): sg=sg[:len(tx)]            # trailing noise after the last line
    assert len(sg)==len(tx),(f,len(sg),len(tx))
    for (a,b),t in zip(sg,tx):
        x=hi[max(0,int((a-0.10)*OSR)):int((b+0.16)*OSR)].copy()
        rms=np.sqrt((x*x).mean()); g=min(0.11/max(rms,1e-5),8.0); x=np.tanh(x*g*1.15)/1.15   # even loudness, soft limit
        k=int(0.02*OSR); x[:k]*=np.linspace(0,1,k); x[-k:]*=np.linspace(1,0,k)
        raw=(np.clip(x,-1,1)*32767).astype(np.int16).tobytes(); out=tmp+'/c.mp3'
        subprocess.run(['ffmpeg','-v','quiet','-y','-f','s16le','-ar',str(OSR),'-ac','1','-i','-','-codec:a','libmp3lame','-b:a','96k','-write_xing','0','-id3v2_version','0','-write_id3v1','0',out],input=raw,check=True)
        d=open(out,'rb').read(); idx['clips'].setdefault(t,[]).append([bi,len(blob),len(d),2]); blob+=d; n+=1; report.append((t,round(b-a,2)))
open(repo+'/audio/r00.mp3','wb').write(blob); idx['bundles'].append('r00.mp3')
if 'Real voice' not in idx['voices']: idx['voices'].append('Real voice')
json.dump(idx,open(repo+'/audio/index.json','w'),ensure_ascii=False,separators=(',',':'))
print('clips',n,'bundle bytes',len(blob)); json.dump(report,open(tmp+'/report.json','w'),ensure_ascii=False); print(report[:6],report[70:78],report[-12:])
