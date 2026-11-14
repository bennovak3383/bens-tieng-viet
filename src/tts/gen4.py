import json,os,re
from vieneu import Vieneu
items=json.load(open('texts4.json'))
tts=Vieneu(); V=['Đức Trí','Kim Thanh']
for i,t in enumerate(items):
    o=f'wav4/{i:04d}.wav'
    if os.path.exists(o): continue
    s=t if re.search(r'[.?!]$',t) else t+'.'
    au=tts.infer(s,voice=V[i%2]); tts.save(au,o+'.tmp.wav'); os.rename(o+'.tmp.wav',o)
print('DONE',len(items),flush=True)
