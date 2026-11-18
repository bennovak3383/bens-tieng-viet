# v94: cut a 3x3 picture sheet (made in ChatGPT) into 9 word pictures.
# python3 src/art/sheet_add.py sheet.png "key=word;word" x9 (reading order). Use "-" to skip a square.
# Keeps the painted background, rounds the corners, saves the original square to src/art/canva/ and a 256 px copy to src/art/custom/c-<key>.png.
import sys
from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGB'); W,H=im.size; g=im.convert('L')
def bands(n,get):
    # runs of non-white lines = the squares
    on=[get(i) for i in range(n)]; out=[]; s=None
    for i,v in enumerate(on+[False]):
        if v and s is None: s=i
        if not v and s is not None:
            if i-s>n*0.2: out.append((s,i))
            s=None
    return out
px=g.load()
cols=bands(W,lambda x: sum(1 for y in range(0,H,7) if px[x,y]<244)>H/7*0.25)
rows=bands(H,lambda y: sum(1 for x in range(0,W,7) if px[x,y]<244)>W/7*0.25)
assert len(cols)==3 and len(rows)==3,(cols,rows)
L=['','# --- pictures cut from a ChatGPT sheet by sheet_add.py']; n=0
for i,a in enumerate(sys.argv[2:11]):
    if a=='-': continue
    k,ws=a.split('='); (x0,x1),(y0,y1)=cols[i%3],rows[i//3]; c=im.crop((x0+2,y0+2,x1-2,y1-2)); c.save('src/art/canva/%s.png'%k)
    c=c.resize((256,256),Image.LANCZOS).convert('RGBA'); m=Image.new('L',(1024,1024),0); ImageDraw.Draw(m).rounded_rectangle((0,0,1023,1023),radius=150,fill=255); c.putalpha(m.resize((256,256),Image.LANCZOS)); c.save('src/art/custom/c-%s.png'%k)
    for w in ws.split(';'): L.append('%s | custom:c-%s'%(w.strip(),k))
    n+=1
open('src/art/pics_map.txt','a',encoding='utf8').write('\n'.join(L)+'\n'); print(n,'pictures cut',cols,rows)
