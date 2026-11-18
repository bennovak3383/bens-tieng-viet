# v89: add Canva AI pictures to the app.  python3 src/art/canva_add.py <folder with downloaded png> "key=fileid=word; word" ...
# Saves the original to src/art/canva/<key>.png, a 256 px see-through copy to src/art/custom/c-<key>.png, and adds the lines to pics_map.txt.
import sys,glob,os
from PIL import Image, ImageDraw
R=sys.argv[1]; L=['','# --- Canva AI pictures added by canva_add.py']
for a in sys.argv[2:]:
    k,t,ws=a.split('='); f=glob.glob(os.path.join(R,'*'+t+'*.png'))[0]; im=Image.open(f).convert('RGBA'); im.save('src/art/canva/%s.png'%k)
    m=im.convert('RGB')
    for xy in ((0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)):
        if min(m.getpixel(xy))>236: ImageDraw.floodfill(m,xy,(255,0,255),thresh=22)
    px=m.load(); al=im.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x,y]==(255,0,255): al[x,y]=(255,255,255,0)
    im.resize((256,256),Image.LANCZOS).save('src/art/custom/c-%s.png'%k)
    for w in ws.split(';'): L.append('%s | custom:c-%s'%(w.strip(),k))
open('src/art/pics_map.txt','a',encoding='utf8').write('\n'.join(L)+'\n'); print(len(sys.argv)-2,'added')
