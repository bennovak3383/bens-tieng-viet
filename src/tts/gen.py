import json,os,sys,re
from vieneu import Vieneu
from time import time
items=json.load(open('texts.json'))
tts=Vieneu(); V=['Đức Trí','Kim Thanh']
t0=time()
for i,it in enumerate(items):
    out=f'wav/{i:04d}.wav'
    if os.path.exists(out): continue
    txt=re.sub(r'[,\s]+$','',it['s']) 
    if not re.search(r'[.?!]$',txt): txt+='.'
    try:
        au=tts.infer(txt,voice=V[i%2]); tts.save(au,out+'.tmp.wav'); os.rename(out+'.tmp.wav',out)
    except Exception as e:
        print('ERR',i,it['k'],e,flush=True)
    if i%25==0: print(i,round(time()-t0),flush=True)
print('DONE',flush=True)
