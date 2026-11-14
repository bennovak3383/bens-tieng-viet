import json,os,subprocess,numpy as np,sys
from scipy.io import wavfile
idx=json.load(open('/home/claude/repo_audio_orig_index.json'))   # original: c00-c13 only
assert len(idx['bundles'])==14
asr=json.load(open('asr.json')); bad=set(int(k) for k,v in asr.items() if 'r' in v and v['r']<0.5)
src=[]  # (key, wavpath)
for i,it in enumerate(json.load(open('texts.json'))):
    if i not in bad: src.append((it['k'],f'wav/{i:04d}.wav'))
for i,it in enumerate(json.load(open('texts2.json'))): src.append((it['k'],f'wav2/{i:04d}.wav'))
for i,(t,v) in enumerate(json.load(open('jobs3.json'))): src.append((t,f'wav3/{i:04d}.wav'))
for i,t in enumerate(json.load(open('texts4.json'))): src.append((t,f'wav4/{i:04d}.wav'))
os.makedirs('mp3r',exist_ok=True); os.makedirs('out2',exist_ok=True)
def proc(path,out):
    sr,x=wavfile.read(path); x=x.astype(np.float32)/32768.0
    if x.ndim>1: x=x.mean(1)
    w=int(sr*0.01); n=len(x)//w; env=np.sqrt((x[:n*w].reshape(n,w)**2).mean(1)); pk=env.max()
    act=np.where(env>max(0.004,pk*0.03))[0]
    a=max(0,act[0]*w-int(0.04*sr)); b=min(len(x),(act[-1]+1)*w+int(0.09*sr)); y=x[a:b].copy()
    fi=int(0.008*sr); fo=int(0.05*sr); y[:fi]*=np.linspace(0,1,fi); y[-fo:]*=np.linspace(1,0,fo)
    rms=np.sqrt((y[np.abs(y)>0.01]**2).mean()) if (np.abs(y)>0.01).any() else 1e-3
    g=min(0.89/np.abs(y).max(),0.16/rms); y=np.clip(y*g,-1,1)
    wavfile.write('/tmp/p.wav',sr,(y*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/p.wav','-ar','32000','-ac','1','-b:a','64k','-write_xing','0','-id3v2_version','0',out],check=True)
cur=bytearray(); bi=0; nb=14; n=0
def flush():
    global cur,bi
    if not cur: return
    name='m%02d.mp3'%bi; open('out2/'+name,'wb').write(cur); idx['bundles'].append(name); bi+=1; cur=bytearray()
for j,(k,p) in enumerate(src):
    o=f'mp3r/{j:04d}.mp3'
    if not os.path.exists(o): proc(p,o)
    d=open(o,'rb').read()
    if len(cur)+len(d)>1_400_000: flush()
    idx['clips'].setdefault(k,[]) 
    if j==[jj for jj,(kk,pp) in enumerate(src) if kk==k][0]: idx['clips'][k]=[]   # first time we see this key: replace any older entry
    idx['clips'][k].append([nb+bi,len(cur),len(d)]); cur+=d; n+=1
flush()
json.dump(idx,open('out2/index.json','w'),ensure_ascii=False,separators=(',',':'))
print('clips',n,'bundles',bi,'bytes',sum(os.path.getsize('out2/'+f) for f in os.listdir('out2')),'keys',len(idx['clips']),flush=True)
