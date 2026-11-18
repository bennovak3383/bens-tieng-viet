# v84-v87: our own drawings for words an emoji cannot show. 256x256, soft colours, same people look as the app.
import os,sys
SK='#F8D4B0'; SKD='#E4AC86'; HAIR='#2B2430'; INK='#2A2F45'
DEFS='''<defs>
<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FCE0C2"/><stop offset="1" stop-color="#F2C39A"/></linearGradient>
<linearGradient id="bl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5B8DEF"/><stop offset="1" stop-color="#2F6BE0"/></linearGradient>
<linearGradient id="gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4CC9A0"/><stop offset="1" stop-color="#1FA57C"/></linearGradient>
<linearGradient id="or" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB45C"/><stop offset="1" stop-color="#F58A1F"/></linearGradient>
<linearGradient id="pk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF8FA8"/><stop offset="1" stop-color="#EE5B7E"/></linearGradient>
<linearGradient id="ye" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE27A"/><stop offset="1" stop-color="#FFC531"/></linearGradient>
<linearGradient id="pu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A58BFF"/><stop offset="1" stop-color="#7B5CF0"/></linearGradient>
<linearGradient id="wh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E6ECF8"/></linearGradient>
<clipPath id="gnd"><rect x="0" y="0" width="256" height="233"/></clipPath>
</defs>'''
def shadow(cx=128,w=80,y=232): return '<ellipse cx="%g" cy="%g" rx="%g" ry="9" fill="#18203A" opacity=".13"/>'%(cx,y,w)
def stroke(d,col,w): return '<path d="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"/>'%(d,col,w)
def face(cx,cy,r,mood='smile',look=0,hair='short',hc=HAIR):
    s=r/30.0; o='<circle cx="%g" cy="%g" r="%g" fill="url(#sk)"/>'%(cx,cy,r)
    o+='<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="#F59A8B" opacity=".45"/><ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="#F59A8B" opacity=".45"/>'%(cx-17*s+look,cy+9*s,5*s,3.4*s,cx+17*s+look,cy+9*s,5*s,3.4*s)
    ex=cx+look
    if mood in('sleep','tired','joy'):
        k=-1 if mood=='joy' else 1
        for dx in(-10,10): o+=stroke('M%g %g q%g %g %g 0'%(ex+dx*s-4*s,cy,4*s,4*s*k,8*s),INK,2.6*s)
    else:
        for dx in(-10,10): o+='<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s"/>'%(ex+dx*s,cy,2.8*s,3.6*s,INK)
    if mood=='sad' or mood=='tired':
        o+=stroke('M%g %g q%g %g %g 0'%(ex-7*s,cy+16*s,7*s,-6*s,14*s),INK,2.6*s)
        for dx,k in((-10,-1),(10,1)): o+=stroke('M%g %g l%g %g'%(ex+dx*s-5*s,cy-10*s-2*k*s,10*s,4*k*s),INK,2.2*s)
    elif mood=='o': o+='<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="#7A2E3A"/>'%(ex,cy+15*s,4.5*s,5.5*s)
    elif mood=='open' or mood=='joy': o+='<path d="M%g %g q%g %g %g 0z" fill="#7A2E3A"/>'%(ex-9*s,cy+11*s,9*s,14*s,18*s)
    elif mood=='flat': o+=stroke('M%g %g h%g'%(ex-6*s,cy+15*s,12*s),INK,2.6*s)
    elif mood=='hmm':
        o+=stroke('M%g %g q%g %g %g %g'%(ex-6*s,cy+16*s,6*s,-3*s,12*s,1*s),INK,2.6*s); o+=stroke('M%g %g l%g %g'%(ex+5*s,cy-10*s,10*s,-3*s),INK,2.4*s)
    else: o+=stroke('M%g %g q%g %g %g 0'%(ex-8*s,cy+12*s,8*s,8*s,16*s),INK,2.8*s)
    if hair=='short': o+='<path d="M%g %g a%g %g 0 0 1 %g 0 q%g %g %g %g q%g %g %g %g z" fill="%s"/>'%(cx-r,cy-4*s,r,r,2*r,-4*s,-14*s,-22*s,-12*s,-20*s,6*s,-38*s,12*s,hc)
    elif hair=='long': o='<path d="M%g %g a%g %g 0 0 1 %g 0 v%g q%g %g %g 0z" fill="%s"/>'%(cx-r-3*s,cy,r+3*s,r+5*s,2*r+6*s,30*s,-(r+3*s),10*s,-(2*r+6*s),hc)+o+'<path d="M%g %g a%g %g 0 0 1 %g 0 q%g %g %g %g q%g %g %g %g z" fill="%s"/>'%(cx-r,cy-3*s,r,r,2*r,-8*s,-12*s,-30*s,-14*s,-14*s,4*s,-30*s,14*s,hc)
    return o
def arm(x1,y1,x2,y2,col,w=15,bend=0):
    mx=(x1+x2)/2+bend; my=(y1+y2)/2+abs(bend)*.4
    return stroke('M%g %g Q%g %g %g %g'%(x1,y1,mx,my,x2,y2),col,w)+'<circle cx="%g" cy="%g" r="%g" fill="url(#sk)"/>'%(x2,y2,w*.56)
def bust(cx=128,cy=96,r=34,shirt='bl',mood='smile',la=None,ra=None,hair='short',hc=HAIR,look=0,front='',w=1.0):
    # la / ra = hand positions (x,y,bend); body from neck down to the ground line
    by=cy+r-4; bw=46*w*r/34; o=''
    body='<path d="M%g %g q0 %g %g %g h%g q%g 0 %g %g V232 H%g z" fill="url(#%s)"/>'%(cx-bw,232,0,0,0,0,0,0,0,cx-bw,shirt)
    body='<path d="M%g 232 V%g q0 %g %g %g h%g q%g 0 %g %g V232z" fill="url(#%s)"/>'%(cx-bw,by+34,-26,26,-26,2*bw-52,26,26,26,shirt)
    col={'bl':'#2F6BE0','gr':'#1FA57C','or':'#F58A1F','pk':'#EE5B7E','pu':'#7B5CF0','ye':'#F5B81F','wh':'#D5DEEE'}[shirt]
    o+='<rect x="%g" y="%g" width="%g" height="%g" rx="6" fill="#F2C39A"/>'%(cx-9,by-8,18,22)+body
    o+=face(cx,cy,r,mood,look,hair,hc)+front
    for a,sx in((la,-1),(ra,1)):
        if a: o+=arm(cx+sx*(bw-9),by+22,a[0],a[1],col,15,a[2] if len(a)>2 else 0)
    return o
def bubble(x,y,w,h,inner,tail=(-1,1),think=False):
    o='<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="url(#wh)" stroke="#C9D4EA" stroke-width="2"/>'%(x,y,w,h,min(w,h)*.42)
    tx=x+ (w*.25 if tail[0]<0 else w*.75)
    if think: o+='<circle cx="%g" cy="%g" r="7" fill="#fff" stroke="#C9D4EA" stroke-width="2"/><circle cx="%g" cy="%g" r="4" fill="#fff" stroke="#C9D4EA" stroke-width="2"/>'%(tx+tail[0]*4,y+h+10,tx+tail[0]*14,y+h+24)
    else: o+='<path d="M%g %g l%g 18 l%g -19z" fill="#F1F5FC" stroke="#C9D4EA" stroke-width="2"/><rect x="%g" y="%g" width="34" height="5" fill="#EEF2FA"/>'%(tx-10,y+h-2,tail[0]*10,12-tail[0]*4,tx-13,y+h-5)
    return o+inner
def heart(cx,cy,s,fill='url(#pk)'): return '<path transform="translate(%g %g) scale(%g)" d="M0 10 C-22 -6 -12 -24 0 -12 C12 -24 22 -6 0 10z" fill="%s"/>'%(cx,cy,s,fill)
def bulb(cx,cy,s=1): return '<g transform="translate(%g %g) scale(%g)"><circle r="30" fill="#FFE27A" opacity=".35"/><path d="M-14 -4 a14 14 0 1 1 28 0 q0 8 -7 14 v6 h-14 v-6 q-7 -6 -7 -14z" fill="url(#ye)"/><rect x="-7" y="17" width="14" height="7" rx="3" fill="#8D95AD"/></g>'%(cx,cy,s)
def bowl(cx,cy,s=1,food=True): return '<g transform="translate(%g %g) scale(%g)">%s<path d="M-34 0 h68 q0 30 -34 30 q-34 0 -34 -30z" fill="url(#pk)"/><rect x="-36" y="-5" width="72" height="9" rx="4.5" fill="#FFB3C4"/></g>'%(cx,cy,s,'<path d="M-28 -3 q6 -14 14 -6 q6 -12 16 -4 q8 -10 16 0 q8 2 8 10z" fill="#FFF3D6"/><circle cx="-8" cy="-9" r="5" fill="#6CC36A"/><circle cx="12" cy="-10" r="5" fill="#E8674A"/>' if food else '')
def glass(cx,cy,s=1,fillp=.7,col='#7DC8F7'): 
    h=56; fh=h*fillp
    return '<g transform="translate(%g %g) scale(%g)"><path d="M-18 %g L-14 0 h28 L18 %g z" fill="%s"/><path d="M-20 -56 h40 l-5 58 q0 4 -4 4 h-22 q-4 0 -4 -4z" fill="#fff" opacity=".35" stroke="#B9C6E0" stroke-width="2.5"/></g>'%(cx,cy,s,-fh,-fh,col)
def clock(cx,cy,r,h=10,m=10):
    import math
    a=math.radians(h%12*30+m/2-90); b=math.radians(m*6-90)
    return '<circle cx="%g" cy="%g" r="%g" fill="url(#wh)" stroke="#5B6B8F" stroke-width="%g"/>'%(cx,cy,r,r*.13)+stroke('M%g %g L%g %g'%(cx,cy,cx+math.cos(a)*r*.48,cy+math.sin(a)*r*.48),INK,r*.11)+stroke('M%g %g L%g %g'%(cx,cy,cx+math.cos(b)*r*.72,cy+math.sin(b)*r*.72),'#EE5B7E',r*.08)
def house(cx,cy,s=1): return '<g transform="translate(%g %g) scale(%g)"><rect x="-30" y="-28" width="60" height="50" rx="4" fill="#FFE9C7"/><path d="M-40 -24 L0 -58 L40 -24z" fill="url(#or)"/><rect x="-9" y="-6" width="18" height="28" rx="3" fill="#8B5A34"/><rect x="12" y="-18" width="12" height="12" rx="2" fill="#9FD3F5"/></g>'%(cx,cy,s)
def spark(cx,cy,s=1,col='#FFC531'): return '<path transform="translate(%g %g) scale(%g)" d="M0 -12 Q2 -2 12 0 Q2 2 0 12 Q-2 2 -12 0 Q-2 -2 0 -12z" fill="%s"/>'%(cx,cy,s,col)
def mini(cx,by,s=1,shirt='bl',mood='smile',pose='stand',hair='short',hc=HAIR):
    # small whole person; by = ground line
    col={'bl':'#2F6BE0','gr':'#1FA57C','or':'#F58A1F','pk':'#EE5B7E','pu':'#7B5CF0','ye':'#F5B81F'}[shirt]; o='<g transform="translate(%g %g) scale(%g)">'%(cx,by,s)
    if pose=='run': o+=stroke('M-4 -46 L-22 -22 L-36 -26','#39456B',13)+stroke('M4 -46 L20 -26 L16 -2','#39456B',13)
    elif pose=='walk': o+=stroke('M-3 -46 L-14 -4','#39456B',13)+stroke('M3 -46 L16 -4','#39456B',13)
    elif pose=='sit': o+=stroke('M-4 -46 L22 -44 L24 -6','#39456B',13)
    else: o+=stroke('M-8 -46 V-4','#39456B',13)+stroke('M8 -46 V-4','#39456B',13)
    o+='<rect x="-19" y="-98" width="38" height="58" rx="15" fill="url(#%s)"/>'%shirt
    if pose=='run': o+=arm(-12,-88,-34,-66,col,11,-6)+arm(12,-88,36,-96,col,11,6)
    elif pose=='up': o+=arm(-14,-90,-34,-128,col,11)+arm(14,-90,34,-128,col,11)
    elif pose=='wave': o+=arm(-14,-88,-24,-58,col,11)+arm(14,-90,36,-124,col,11)
    elif pose=='sit': o+=arm(-10,-88,4,-58,col,11)
    else: o+=arm(-14,-88,-24,-56,col,11)+arm(14,-88,24,-56,col,11)
    return o+face(0,-118,24,mood,0,hair,hc)+'</g>'
# ---- v87: the people are now the same people as on the Home screen (exported from the app's z63Person into people.json).
import json as _json, re as _re
PPL=_json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'people.json')))
SKN='#F3CFA6'
WHO={('short','bl'):'man',('short','or'):'kid',('short','gr'):'man2',('short','pu'):'old',('short','ye'):'kid',('short','pk'):'man',('short','wh'):'man',
     ('long','bl'):'woman',('long','or'):'woman',('long','gr'):'pony',('long','pu'):'gran',('long','ye'):'woman',('long','pk'):'woman2',('long','wh'):'woman'}
SLEEVE={'man':'#F4F6FB','kid':'#F4F6FB','old':'#F4F6FB','gran':'#F4F6FB','woman':'#FFD23F','pony':'#FFD23F','man2':'#2F7BF6','woman2':'#F0527A'}
def person(k,mood='smile',tall=False):
    o=PPL[k][1 if tall else 0]
    if mood in('sad','tired','o','flat','hmm'):
        o=_re.sub(r'<path d="M-7\.300 -22\.100.*?#DB7474"/>','',o); o=_re.sub(r'<path d="M-6 -21\.600 Q0 -16\.600 6 -21\.600"[^>]*/>','',o)
        if mood=='o': o+='<ellipse cx="0" cy="-18.6" rx="3.2" ry="4" fill="#7A2B2B"/>'
        elif mood in('flat','hmm'): o+='<path d="M-5 -18.6 h10" fill="none" stroke="#3A2A2A" stroke-width="1.8" stroke-linecap="round"/>'
        else: o+='<path d="M-5.5 -17 Q0 -21.4 5.5 -17" fill="none" stroke="#3A2A2A" stroke-width="1.9" stroke-linecap="round"/><path d="M-13.5 -39 L-4 -42.6 M13.5 -39 L4 -42.6" fill="none" stroke="#17141C" stroke-width="1.5" stroke-linecap="round"/>'
    if mood in('sleep','tired'):
        o=_re.sub(r'<g class="z63eye".*?</g>','',o,flags=_re.S)+'<path d="M-12 -34 Q-8 -31 -4 -34 M12 -34 Q8 -31 4 -34" fill="none" stroke="#17141C" stroke-width="1.6" stroke-linecap="round"/>'
    return o
def harm(x1,y1,x2,y2,col,w=18,bend=0):
    mx=(x1+x2)/2+bend; my=(y1+y2)/2+abs(bend)*.4; d='M%g %g Q%g %g %g %g'%(x1,y1,mx,my,x2,y2)
    return stroke(d,'rgba(0,0,20,.14)',w+3)+stroke(d,col,w)+'<circle cx="%g" cy="%g" r="%g" fill="%s"/>'%(x2,y2,w*.58,SKN)
def bust(cx=128,cy=96,r=34,shirt='bl',mood='smile',la=None,ra=None,hair='short',hc=HAIR,look=0,front='',w=1.0):
    k=WHO.get((hair,shirt),'man'); sc=r/22.0; oy=cy+35*sc
    o='<g clip-path="url(#gnd)"><g transform="translate(%g %g) scale(%g)">%s</g></g>'%(cx,oy,sc,person(k,mood,True))+front
    for a,sx in((la,-1),(ra,1)):
        if a: o+=harm(cx+sx*27*sc,oy+10*sc,a[0],a[1],SLEEVE[k],13*sc,a[2] if len(a)>2 else 0)
    return o
def mini(cx,by,s=1,shirt='bl',mood='smile',pose='stand',hair='short',hc=HAIR):
    k=WHO.get((hair,shirt),'man'); col=SLEEVE[k]; o='<g transform="translate(%g %g) scale(%g)">'%(cx,by,s); P='#39456B'
    if pose=='run': o+=stroke('M-6 -42 L-22 -20 L-36 -24',P,14)+stroke('M6 -42 L20 -24 L16 -2',P,14)
    elif pose=='walk': o+=stroke('M-5 -42 L-15 -4',P,14)+stroke('M5 -42 L17 -4',P,14)
    elif pose=='sit': o+=stroke('M-4 -42 L24 -40 L26 -4',P,14)
    else: o+=stroke('M-10 -42 V-4',P,14)+stroke('M10 -42 V-4',P,14)
    A={'run':((-38,-58,-6),(40,-92,6)),'up':((-46,-136,0),(46,-136,0)),'wave':((-34,-48,0),(46,-126,0)),'sit':((6,-50,0),None),'flex':None}.get(pose,((-35,-48,0),(35,-48,0)))
    back=''; frontA=''
    if pose=='flex': back=stroke('M-26 -78 L-48 -84 L-46 -116','rgba(0,0,20,.14)',15)+stroke('M-26 -78 L-48 -84 L-46 -116',col,12)+stroke('M26 -78 L48 -84 L46 -116',col,12)+'<circle cx="-46" cy="-118" r="8" fill="%s"/><circle cx="46" cy="-118" r="8" fill="%s"/>'%(SKN,SKN)
    elif A:
        for a,sx in zip(A,(-1,1)):
            if a:
                g=harm(sx*26,-78,a[0],a[1],col,12,a[2])
                if pose=='up' or (pose=='wave' and sx>0): back+=g
                else: frontA+=g
    o+=back+'<g transform="translate(0 -84)">'+person(k,mood,False)+'</g>'+frontA
    return o+'</g>'

D={}
D['an']=('ăn','to eat', shadow()+bust(mood='open',la=(96,196,-8),ra=(160,150,10))+bowl(100,186,1.0)+stroke('M150 162 L176 118','#B98A5A',5)+stroke('M158 164 L186 124','#B98A5A',5)+stroke('M152 150 q10 -12 4 -22','#FFF3D6',5))
D['uong']=('uống','to drink', shadow()+bust(shirt='gr',mood='o',ra=(170,150,14),la=(88,214,-6))+glass(168,150,1.0,.6))
D['di']=('đi','to go', shadow(120,60)+'<path d="M20 232 Q130 200 250 214 V240 H20z" fill="#DCE6F7"/>'+mini(120,226,1.25,'or','smile','walk')+stroke('M28 150 h34','#B9C6E0',6)+stroke('M18 176 h44','#B9C6E0',6)+house(214,160,.7))
D['muon']=('muốn','to want', shadow()+bust(cx=106,mood='o',look=5,ra=(176,120,10),la=(156,150,30))+'<g transform="translate(206 92)"><circle r="40" fill="#FFE27A" opacity=".35"/><path d="M-14 6 L0 58 L14 6z" fill="#E9B36F"/><circle cy="-6" r="22" fill="url(#pk)"/><circle cx="-7" cy="-13" r="6" fill="#fff" opacity=".5"/></g>'+spark(170,52,1)+spark(238,44,.7))
D['thich']=('thích','to like', shadow()+bust(shirt='pu',mood='joy',la=(108,176,-14),ra=(148,176,14))+heart(128,180,2.3)+heart(62,60,1.0)+heart(200,48,.8))
D['hieu']=('hiểu','to understand', shadow()+bust(cy=128,mood='open',shirt='gr')+bulb(128,44,1.35)+spark(70,62,.8)+spark(190,70,.7))
D['khong-hieu']=('không hiểu','to not understand', shadow()+bust(cy=128,mood='hmm',shirt='or',ra=(166,160,22))+'<text x="52" y="78" font-family="Arial" font-weight="900" font-size="58" fill="#7B5CF0">?</text><text x="170" y="62" font-family="Arial" font-weight="900" font-size="44" fill="#A58BFF">?</text><text x="112" y="56" font-family="Arial" font-weight="900" font-size="34" fill="#C9BCFF">?</text>')
D['vui']=('vui','happy', shadow(128,60)+mini(128,228,1.45,'ye','joy','up')+spark(48,70,1.1)+spark(210,60,1.2)+spark(58,150,.7,'#FF8FA8')+spark(204,146,.8,'#5B8DEF'))
D['doi']=('đói','hungry', shadow()+bust(mood='sad',shirt='bl',la=(112,204,-10),ra=(144,204,10))+'<g transform="translate(206 70)"><ellipse rx="36" ry="30" fill="url(#wh)" stroke="#C9D4EA" stroke-width="2"/><circle cx="-22" cy="34" r="6" fill="#fff" stroke="#C9D4EA" stroke-width="2"/><g transform="scale(.55) translate(0 -2)"><path d="M-34 0 h68 q0 30 -34 30 q-34 0 -34 -30z" fill="url(#pk)"/><path d="M-28 -3 q6 -14 14 -6 q6 -12 16 -4 q8 -10 16 0 q8 2 8 10z" fill="#FFF3D6"/></g></g>'+stroke('M96 222 q8 -6 16 0 q8 6 16 0','#fff',3))
D['hon']=('hơn','more than', shadow(128,96)+glass(78,214,1.25,.3)+'<circle cx="180" cy="150" r="74" fill="#FFE27A" opacity=".4"/>'+glass(180,214,1.9,.85)+spark(232,62,1.1))
D['giup']=('giúp','to help', shadow(128,100)+mini(74,226,1.1,'bl','smile','stand')+mini(182,226,1.1,'pk','joy','stand','long')+'<rect x="92" y="118" width="72" height="56" rx="8" fill="#D9A066"/><rect x="92" y="118" width="72" height="14" rx="6" fill="#C48A50"/><rect x="122" y="118" width="12" height="56" fill="#F0C690"/>'+'<circle cx="96" cy="160" r="7" fill="url(#sk)"/><circle cx="160" cy="160" r="7" fill="url(#sk)"/>')
D['nho']=('nhớ','to remember, to miss', shadow()+bust(cx=96,cy=140,r=32,mood='smile',look=4,shirt='pu')+bubble(132,22,104,78,house(184,74,.72)+heart(214,40,.55),(-1,1),True))
D['tre']=('trễ','late', shadow(110,60)+mini(110,226,1.25,'or','o','run')+clock(204,70,38,9,12)+stroke('M22 120 h30','#B9C6E0',6)+stroke('M14 150 h40','#B9C6E0',6)+'<path d="M150 76 q6 10 0 16 q-6 -6 0 -16z" fill="#7DC8F7"/><path d="M164 96 q5 8 0 13 q-5 -5 0 -13z" fill="#7DC8F7"/>')
D['ban']=('bạn','friend', shadow(128,96)+mini(92,226,1.25,'bl','joy','stand')+mini(164,226,1.25,'gr','joy','stand','long')+stroke('M108 126 Q128 112 150 126','#F4F6FB',13)+heart(128,44,1.1))
D['gan']=('gần','near', shadow(128,100)+'<path d="M10 232 Q130 214 250 232 V244 H10z" fill="#CFEBD8"/>'+house(170,196,1.25)+mini(74,228,1.0,'bl','smile','wave'))
D['xa']=('xa','far', '<path d="M0 232 Q120 150 256 190 V256 H0z" fill="#CFEBD8"/><path d="M30 240 Q120 220 150 170 Q168 130 214 96" fill="none" stroke="#F3E3BF" stroke-width="16" stroke-linecap="round"/>'+house(222,84,.42)+mini(52,238,1.05,'bl','flat','stand'))
D['noi']=('nói','to speak', shadow()+bust(cx=96,cy=128,mood='open',shirt='gr',look=4)+bubble(138,30,100,64,stroke('M158 54 h60','#9AA8C7',6)+stroke('M158 72 h40','#9AA8C7',6)))
D['hoi']=('hỏi','to ask', shadow()+bust(cx=96,cy=128,mood='o',shirt='or',look=4,ra=(150,150,10))+bubble(138,26,96,72,'<text x="170" y="84" font-family="Arial" font-weight="900" font-size="60" fill="#2F6BE0">?</text>'))
D['nghe']=('nghe','to listen', shadow()+bust(cx=116,mood='smile',shirt='pu',ra=(170,100,26))+stroke('M196 78 q14 18 0 38','#5B8DEF',6)+stroke('M212 64 q26 32 0 66','#9DBBF7',6))
D['met']=('mệt','tired', shadow()+bust(cy=118,mood='tired',shirt='bl',la=(84,214,-8),ra=(172,214,8))+'<path d="M176 74 q8 13 0 20 q-8 -7 0 -20z" fill="#7DC8F7"/><path d="M76 86 q6 10 0 15 q-6 -5 0 -15z" fill="#7DC8F7"/>'+'<text x="182" y="56" font-family="Arial" font-weight="900" font-size="22" fill="#9AA8C7">z</text><text x="200" y="38" font-family="Arial" font-weight="900" font-size="30" fill="#B9C6E0">z</text>')
D['cho']=('chờ','to wait', shadow(128,96)+'<rect x="40" y="170" width="150" height="14" rx="6" fill="#C48A50"/><rect x="52" y="184" width="12" height="44" rx="4" fill="#A66E3A"/><rect x="166" y="184" width="12" height="44" rx="4" fill="#A66E3A"/>'+mini(104,222,1.2,'gr','flat','sit')+clock(206,66,36,3,30))
D['mua']=('mua','to buy', shadow(128,100)+mini(78,226,1.15,'bl','smile','stand')+'<rect x="150" y="150" width="90" height="78" rx="8" fill="#E9EEF8"/><rect x="142" y="138" width="106" height="20" rx="8" fill="url(#or)"/><path d="M142 110 h106 l-8 28 h-90z" fill="#FFD9A8"/>'+'<path d="M112 150 h30 v34 q0 6 -6 6 h-18 q-6 0 -6 -6z" fill="url(#pk)"/><path d="M118 150 q9 -18 18 0" fill="none" stroke="#C93E63" stroke-width="4"/>'+'<circle cx="196" cy="188" r="14" fill="url(#ye)"/>')

def box(x,y,w,h): return '<rect x="%g" y="%g" width="%g" height="%g" rx="7" fill="#D9A066"/><rect x="%g" y="%g" width="%g" height="%g" rx="5" fill="#C48A50"/><rect x="%g" y="%g" width="%g" height="%g" fill="#F0C690"/>'%(x,y,w,h,x,y,w,h*.24,x+w/2-5,y,10,h)
def ball(cx,cy,r=20): return '<circle cx="%g" cy="%g" r="%g" fill="url(#pk)"/><circle cx="%g" cy="%g" r="%g" fill="#fff" opacity=".45"/>'%(cx,cy,r,cx-r*.35,cy-r*.35,r*.3)
def table(y=150): return '<rect x="40" y="%g" width="176" height="16" rx="7" fill="#C48A50"/><rect x="56" y="%g" width="14" height="70" rx="5" fill="#A66E3A"/><rect x="186" y="%g" width="14" height="70" rx="5" fill="#A66E3A"/>'%(y,y+14,y+14)
def glow(cx,cy,r): return '<circle cx="%g" cy="%g" r="%g" fill="#FFE27A" opacity=".45"/>'%(cx,cy,r)
def apple(cx,cy,s=1): return '<g transform="translate(%g %g) scale(%g)"><path d="M0 -10 q4 -8 10 -8" stroke="#6B4A2A" stroke-width="3" fill="none"/><path d="M0 -8 C-22 -18 -24 18 -6 20 q6 2 6 0 q0 2 6 0 C24 18 22 -18 0 -8z" fill="#E8503F"/><ellipse cx="-8" cy="0" rx="4" ry="6" fill="#fff" opacity=".4"/></g>'%(cx,cy,s)
def stairs(up=True):
    o=''
    for i in range(4):
        x=40+i*46 if up else 40+(3-i)*46
        o+='<rect x="%g" y="%g" width="46" height="%g" fill="%s"/>'%(x,206-i*30,30+i*30,['#C9D4EA','#B9C6E0','#A9B8D8','#99AAD0'][i])
    return o
def X(k,vi,en,body): D[k]=(vi,en,body)
X('khong','không','no, not', shadow()+bust(mood='flat',shirt='or')+stroke('M96 214 L160 156','#F58A1F',16)+stroke('M160 214 L96 156','#F58A1F',16)+'<circle cx="160" cy="156" r="9" fill="url(#sk)"/><circle cx="96" cy="156" r="9" fill="url(#sk)"/>'+stroke('M40 70 q-8 10 0 20','#B9C6E0',5)+stroke('M216 70 q8 10 0 20','#B9C6E0',5))
X('nghi','nghĩ','to think', shadow()+bust(cx=100,cy=140,r=32,mood='hmm',shirt='bl',look=3,ra=(124,176,26))+bubble(134,24,100,70,'<circle cx="162" cy="60" r="7" fill="#9AA8C7"/><circle cx="184" cy="60" r="7" fill="#9AA8C7"/><circle cx="206" cy="60" r="7" fill="#9AA8C7"/>',(-1,1),True))
X('xem','xem','to look at, to watch', shadow(128,100)+bust(cx=78,cy=130,r=30,mood='smile',shirt='pu',look=6)+'<rect x="146" y="78" width="96" height="70" rx="8" fill="#39456B"/><rect x="153" y="85" width="82" height="56" rx="4" fill="#9FD3F5"/><path d="M153 141 l24 -26 l16 14 l14 -20 l28 32z" fill="#4CC9A0"/><circle cx="218" cy="98" r="7" fill="#FFC531"/><rect x="186" y="148" width="16" height="14" fill="#5B6B8F"/><rect x="166" y="160" width="56" height="8" rx="4" fill="#5B6B8F"/>'+stroke('M112 120 L140 112','#FFC531',4)+stroke('M112 132 L140 132','#FFC531',4))
X('den','đến','to arrive', shadow(128,100)+'<path d="M10 232 Q130 216 250 232 V244 H10z" fill="#CFEBD8"/>'+house(176,188,1.45)+'<rect x="163" y="180" width="26" height="40" rx="3" fill="#FFE9A8"/>'+mini(112,230,1.05,'or','joy','wave')+spark(60,90,1)+spark(226,70,.8))
X('len','lên','to go up', stairs(True)+mini(158,146,.82,'bl','smile','walk')+'<path d="M40 110 L74 76 M74 76 h-18 M74 76 v18" stroke="#1FA57C" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
X('xuong','xuống','to go down', stairs(False)+mini(104,146,.82,'or','smile','walk')+'<path d="M182 76 L216 110 M216 110 h-18 M216 110 v-18" stroke="#EE5B7E" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
X('tren','trên','on, above', shadow(128,96)+table()+glow(128,116,46)+ball(128,126,24))
X('duoi','dưới','under, below', shadow(128,96)+glow(128,206,42)+ball(128,208,22)+table(120))
X('trong','trong','in, inside', shadow(128,90)+glow(128,130,56)+ball(128,136,26)+'<path d="M56 140 h144 v70 q0 12 -12 12 h-120 q-12 0 -12 -12z" fill="#D9A066"/><rect x="48" y="130" width="160" height="18" rx="7" fill="#C48A50"/><path d="M48 132 l-18 -26 h30 l14 26z" fill="#E6B77E"/><path d="M208 132 l18 -26 h-30 l-14 26z" fill="#E6B77E"/>')
X('ngoai','ngoài','outside', shadow(120,100)+box(36,126,104,96)+glow(196,196,40)+ball(196,198,24))
X('nhieu','nhiều','a lot, many', shadow(128,104)+''.join(apple(x,y,1.05) for x,y in ((70,206),(108,206),(146,206),(184,206),(89,170),(127,170),(165,170),(108,134),(146,134),(127,98))))
X('it','ít','few, little', shadow(128,60)+'<ellipse cx="128" cy="206" rx="78" ry="16" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+apple(128,184,1.15))
X('ho','họ','they; people', shadow(128,106)+mini(66,226,1.0,'gr','smile','stand','long')+mini(190,226,1.0,'or','smile','stand')+mini(128,230,1.12,'bl','joy','stand'))
X('giadinh','gia đình','family', shadow(128,106)+mini(74,228,1.2,'bl','joy','stand')+mini(184,228,1.15,'pk','joy','stand','long')+mini(130,230,.72,'ye','joy','up')+heart(130,36,1.2))
X('toi','tôi','I, me', shadow()+bust(mood='smile',shirt='bl',ra=(132,186,-44))+glow(128,100,74).replace('.45','.22')+spark(46,60,1)+spark(212,70,.8))
X('motminh','một mình','alone', '<path d="M0 226 Q128 204 256 226 V256 H0z" fill="#DCE6F7"/>'+shadow(128,30,228)+mini(128,226,.8,'pu','flat','stand')+'<circle cx="206" cy="56" r="22" fill="#FFE9A8"/>')
X('dua','đưa','to hand over', shadow(128,106)+mini(64,226,1.15,'bl','smile','stand')+mini(196,226,1.15,'gr','joy','stand','long')+stroke('M84 132 L112 138','#F4F6FB',12)+stroke('M176 132 L150 140','#FFD23F',12)+box(108,112,46,40)+'<circle cx="112" cy="140" r="7" fill="url(#sk)"/><circle cx="150" cy="142" r="7" fill="url(#sk)"/>')
X('cam','cầm','to hold', shadow()+bust(mood='smile',shirt='gr')+box(92,150,72,60)+'<circle cx="92" cy="186" r="10" fill="url(#sk)"/><circle cx="164" cy="186" r="10" fill="url(#sk)"/>')
X('khoe','khỏe','healthy, strong', shadow(128,60)+mini(128,228,1.3,'gr','joy','flex')+spark(44,60,1.1)+spark(214,66,1))
X('te','té','to fall over', shadow(128,90)+'<g transform="rotate(62 128 190)">'+mini(128,214,1.2,'or','o','up')+'</g>'+spark(60,70,1.1,'#FF8FA8')+spark(96,44,.8)+stroke('M190 96 l14 -16','#B9C6E0',6)+stroke('M210 122 l20 -8','#B9C6E0',6))
X('gap','gặp','to meet', shadow(128,106)+mini(72,226,1.2,'bl','joy','wave')+'<g transform="translate(256 0) scale(-1 1)">'+mini(72,226,1.2,'pk','joy','wave','long')+'</g>')
X('oi','ơi','hey! (calling someone)', shadow()+bust(cx=104,mood='open',shirt='or',look=5,ra=(150,112,16))+stroke('M178 84 l26 -14','#F58A1F',7)+stroke('M184 108 h30','#F58A1F',7)+stroke('M178 132 l26 14','#F58A1F',7))
X('day','đẩy','to push', shadow(128,110)+'<g transform="rotate(14 80 226)">'+mini(80,226,1.15,'bl','flat','walk')+'</g>'+stroke('M100 138 L140 140','#F4F6FB',13)+'<circle cx="142" cy="140" r="8" fill="url(#sk)"/>'+box(146,112,92,112)+stroke('M20 150 h26','#B9C6E0',6)+stroke('M14 176 h32','#B9C6E0',6))
X('keo','kéo','to pull', shadow(128,110)+'<g transform="rotate(-16 70 226)">'+mini(70,226,1.15,'pu','flat','walk')+'</g>'+stroke('M92 146 L160 176','#8B5A34',5)+'<circle cx="94" cy="146" r="8" fill="url(#sk)"/>'+box(158,136,84,88))
X('nang','nâng','to lift', shadow(128,60)+box(84,16,88,50)+mini(128,228,1.0,'bl','smile','up'))
X('roi','rơi','to fall, to drop', shadow(128,70)+'<rect x="26" y="20" width="204" height="14" rx="7" fill="#8B5A34"/><ellipse cx="80" cy="30" rx="58" ry="26" fill="#4CC9A0"/><ellipse cx="180" cy="26" rx="62" ry="24" fill="#3DB58D"/>'+stroke('M128 58 v36','#B9C6E0',6)+stroke('M108 70 v24','#B9C6E0',5)+stroke('M148 70 v24','#B9C6E0',5)+apple(128,140,1.7))
X('xephang','xếp hàng','to queue', shadow(120,110)+mini(48,226,.95,'gr','flat','stand')+mini(104,226,.95,'or','smile','stand','long')+mini(160,226,.95,'bl','flat','stand')+'<rect x="204" y="150" width="44" height="76" rx="6" fill="#E9EEF8"/><rect x="198" y="140" width="56" height="16" rx="7" fill="url(#pu)"/>')
X('hop','họp','meeting', shadow(128,110)+mini(60,196,.85,'bl','smile','stand')+mini(128,190,.85,'pk','open','stand','long')+mini(196,196,.85,'gr','smile','stand')+'<path d="M28 176 h200 q10 0 10 10 v8 H18 v-8 q0 -10 10 -10z" fill="#C48A50"/><rect x="40" y="194" width="14" height="36" rx="5" fill="#A66E3A"/><rect x="202" y="194" width="14" height="36" rx="5" fill="#A66E3A"/><rect x="100" y="162" width="56" height="16" rx="3" fill="#fff" stroke="#C9D4EA" stroke-width="2"/>')

# ---- v85: fixes to three weak drawings, then batch 3
X('khong','không','no, not', shadow()+bust(mood='flat',shirt='or',la=(166,176,10),ra=(90,176,-10))+stroke('M40 70 q-8 10 0 20','#B9C6E0',5)+stroke('M216 70 q8 10 0 20','#B9C6E0',5)+stroke('M26 62 q-10 18 0 36','#D5DEEE',5)+stroke('M230 62 q10 18 0 36','#D5DEEE',5))
X('hon','hơn','more than', shadow(128,104)+'<ellipse cx="62" cy="212" rx="44" ry="10" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+apple(50,192,.9)+apple(76,192,.9)+glow(176,160,76)+'<ellipse cx="176" cy="212" rx="64" ry="12" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+''.join(apple(x,y,.95) for x,y in ((140,192),(176,192),(212,192),(158,160),(194,160),(176,128)))+spark(232,70,1.1))
X('toi','tôi','I, me', shadow()+glow(128,110,84).replace('.45','.3')+bust(mood='smile',shirt='bl',ra=(132,186,-44))+spark(40,60,1)+spark(218,70,.8))
def tick(cx,cy,on):
    return '<circle cx="%g" cy="%g" r="13" fill="%s"/>'%(cx,cy,'#1FA57C' if on else '#E6ECF8')+(stroke('M%g %g l5 5 l9 -10'%(cx-7,cy),'#fff',4) if on else '')
def week(n):
    o='<rect x="18" y="70" width="220" height="120" rx="18" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/><rect x="18" y="70" width="220" height="34" rx="16" fill="url(#bl)"/>'
    for i in range(7): o+='<circle cx="%g" cy="87" r="4" fill="#fff"/>'%(38+i*30)+tick(38+i*30,146,i in n)
    return shadow(128,100,216)+o
X('luon','luôn','always', week(range(7))); X('thuong','thường','usually, often', week((0,1,2,4,5))); X('doikhi','đôi khi','sometimes', week((1,5))); X('khongbaogio','không bao giờ','never', week(()))
X('dongy','đồng ý','to agree', shadow(128,106)+mini(74,226,1.2,'bl','joy','stand')+mini(182,226,1.2,'gr','joy','stand','long')+stroke('M96 134 L128 140','#F4F6FB',13)+stroke('M160 134 L128 140','#FFD23F',13)+'<circle cx="128" cy="140" r="11" fill="url(#sk)"/>'+'<circle cx="128" cy="52" r="24" fill="url(#gr)"/>'+stroke('M116 52 l9 9 l15 -18','#fff',6))
X('noichuyen','nói chuyện','to talk, to chat', shadow(128,106)+bust(cx=62,cy=150,r=26,mood='open',shirt='bl',look=4)+bust(cx=194,cy=150,r=26,mood='smile',shirt='pk',look=-4,hair='long')+bubble(24,26,92,54,stroke('M40 46 h58','#9AA8C7',5)+stroke('M40 62 h36','#9AA8C7',5),(-1,1))+bubble(140,58,92,48,stroke('M156 76 h58','#5B8DEF',5)+stroke('M156 90 h30','#5B8DEF',5),(1,1)))
X('quen','quên','to forget', shadow()+bust(cx=100,cy=140,r=32,mood='o',shirt='gr',ra=(132,104,30))+'<rect x="140" y="22" width="96" height="70" rx="28" fill="none" stroke="#C9D4EA" stroke-width="4" stroke-dasharray="8 8"/><circle cx="150" cy="104" r="6" fill="none" stroke="#C9D4EA" stroke-width="3"/><text x="172" y="76" font-family="Arial" font-weight="900" font-size="48" fill="#D5DEEE">?</text>')
X('sansang','sẵn sàng','ready', shadow(128,70)+'<rect x="160" y="60" width="74" height="168" rx="6" fill="#8B5A34"/><rect x="168" y="68" width="58" height="160" rx="4" fill="#B67B4A"/><circle cx="178" cy="150" r="5" fill="#FFC531"/>'+'<rect x="60" y="112" width="34" height="50" rx="12" fill="url(#or)"/>'+mini(100,228,1.25,'bl','joy','wave')+spark(40,60,1.1)+spark(132,44,.8))
X('sach','sạch','clean', shadow(128,90)+'<ellipse cx="128" cy="150" rx="88" ry="74" fill="url(#wh)" stroke="#C9D4EA" stroke-width="4"/><ellipse cx="128" cy="150" rx="56" ry="46" fill="#F6F9FF" stroke="#DCE6F7" stroke-width="3"/>'+spark(70,70,1.5)+spark(200,84,1.2)+spark(190,200,1.0,'#9FD3F5')+spark(128,150,1.3,'#9FD3F5'))
def tag(cx,cy,s=1): return '<g transform="translate(%g %g) scale(%g) rotate(-18)"><path d="M-46 -26 h66 l28 26 l-28 26 h-66 q-8 0 -8 -8 v-36 q0 -8 8 -8z" fill="url(#or)"/><circle cx="26" cy="0" r="7" fill="#fff"/><rect x="-40" y="-8" width="44" height="6" rx="3" fill="#fff" opacity=".8"/><rect x="-40" y="6" width="28" height="6" rx="3" fill="#fff" opacity=".8"/></g>'%(cx,cy,s)
def coin(cx,cy,r=18): return '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="#E0A21A"/><ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="url(#ye)"/>'%(cx,cy+5,r,r*.42,cx,cy,r,r*.42)
X('gia','giá','price', shadow(128,80)+tag(120,120,1.7)+coin(196,206)+coin(196,196))
X('re','rẻ','cheap', shadow(128,90)+tag(86,96,1.15)+coin(86,200,26)+bust(cx=186,cy=150,r=28,mood='joy',shirt='gr'))
X('mac','mắc','expensive', shadow(128,90)+tag(80,70,1.05)+''.join(coin(54,214-i*12,22) for i in range(6))+''.join(coin(104,214-i*12,22) for i in range(8))+bust(cx=194,cy=150,r=28,mood='o',shirt='or')+'<path d="M228 112 q7 11 0 17 q-7 -6 0 -17z" fill="#7DC8F7"/>')
X('ban2','bán','to sell', shadow(128,110)+'<path d="M26 70 h204 l-14 34 h-176z" fill="url(#pk)"/><path d="M26 70 h204 l-4 10 h-196z" fill="#fff" opacity=".35"/><rect x="38" y="104" width="10" height="70" fill="#8D95AD"/><rect x="208" y="104" width="10" height="70" fill="#8D95AD"/>'+mini(128,196,.95,'gr','joy','wave')+'<rect x="26" y="170" width="204" height="58" rx="8" fill="#E9EEF8"/><rect x="20" y="160" width="216" height="18" rx="8" fill="#C9D4EA"/>'+apple(60,150,.8)+apple(86,150,.8)+apple(190,150,.8))
X('chon','chọn','to choose', shadow(128,100)+bust(cx=128,cy=74,r=28,mood='hmm',shirt='pu',ra=(176,150,10))+glow(190,188,44)+'<rect x="34" y="158" width="68" height="62" rx="12" fill="url(#bl)"/><rect x="156" y="158" width="68" height="62" rx="12" fill="url(#pk)"/>')
X('batdau','bắt đầu','to begin, to start', shadow(110,70)+'<rect x="46" y="60" width="10" height="170" rx="4" fill="#5B6B8F"/><path d="M56 62 h64 l-14 18 l14 18 h-64z" fill="url(#gr)"/><rect x="20" y="226" width="216" height="8" rx="4" fill="#DCE6F7"/>'+mini(128,228,1.2,'or','smile','run')+stroke('M186 150 h36','#B9C6E0',6)+'<path d="M222 150 l-12 -8 v16z" fill="#B9C6E0"/>')
X('xong','xong','finished, done', shadow(128,80)+'<rect x="22" y="50" width="10" height="180" rx="4" fill="#5B6B8F"/><rect x="224" y="50" width="10" height="180" rx="4" fill="#5B6B8F"/>'+mini(128,228,1.3,'bl','joy','up')+stroke('M32 150 Q128 176 224 150','#EE5B7E',8)+spark(60,60,1.2)+spark(198,56,1.1)+spark(128,24,.9,'#FF8FA8'))
X('thap','thấp','short, low', shadow(128,104)+mini(80,228,1.45,'bl','smile','stand')+glow(184,170,62)+mini(184,228,.8,'or','smile','stand'))
X('yeu','yếu','weak', shadow(128,90)+mini(92,228,1.2,'pu','tired','stand')+'<rect x="150" y="196" width="14" height="30" rx="5" fill="#39456B"/><rect x="226" y="196" width="14" height="30" rx="5" fill="#39456B"/><rect x="160" y="206" width="70" height="9" rx="4" fill="#8D95AD"/><rect x="142" y="186" width="14" height="48" rx="5" fill="#5B6B8F"/><rect x="234" y="186" width="14" height="48" rx="5" fill="#5B6B8F"/>'+'<path d="M60 70 q7 11 0 17 q-7 -6 0 -17z" fill="#7DC8F7"/><path d="M130 60 q7 11 0 17 q-7 -6 0 -17z" fill="#7DC8F7"/>')
def road(kind):
    o='<rect x="0" y="0" width="256" height="256" rx="28" fill="#CFEBD8"/><rect x="98" y="110" width="60" height="146" fill="#8D95AD"/>'
    if kind=='T': o+='<rect x="0" y="80" width="256" height="60" fill="#8D95AD"/>'
    else: o+='<rect x="98" y="0" width="60" height="120" fill="#8D95AD"/>'
    return o
def arrow(d,col='#FFC531'): return '<path d="%s" fill="none" stroke="%s" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'%(d,col)
X('trai','trái','left', road('T')+arrow('M128 226 V110 H44 M70 84 L44 110 L70 136')+house(206,54,.6))
X('phai','phải','right (side)', road('T')+arrow('M128 226 V110 H212 M186 84 L212 110 L186 136')+house(50,54,.6))
X('thang','thẳng','straight', road('I')+arrow('M128 226 V40 M102 66 L128 40 L154 66')+house(206,150,.6)+house(50,90,.6))
X('giua','giữa','middle; between', shadow(128,104)+box(22,150,60,72)+box(174,150,60,72)+glow(128,190,42)+ball(128,196,24))
X('canh','cạnh','next to', shadow(128,100)+box(40,120,104,102)+glow(186,196,40)+ball(186,198,24))
def tree(cx,by,s=1): return '<g transform="translate(%g %g) scale(%g)"><rect x="-9" y="-70" width="18" height="70" rx="5" fill="#8B5A34"/><circle cx="0" cy="-96" r="46" fill="url(#gr)"/><circle cx="-18" cy="-110" r="14" fill="#fff" opacity=".2"/></g>'%(cx,by,s)
X('truoc','phía trước','in front', shadow(128,90)+tree(128,206,1.25)+glow(128,176,56)+mini(128,232,1.0,'or','smile','stand'))
X('sau','phía sau','behind', shadow(128,90)+glow(160,150,58)+mini(160,222,1.0,'or','smile','stand')+tree(110,232,1.3))
X('doidien','đối diện','opposite', '<rect x="0" y="0" width="256" height="256" rx="28" fill="#CFEBD8"/><rect x="0" y="100" width="256" height="56" fill="#8D95AD"/>'+''.join('<rect x="%g" y="125" width="26" height="6" rx="3" fill="#fff"/>'%x for x in (16,66,116,166,216))+house(128,70,1.05)+house(128,222,1.05)+stroke('M128 104 V152','#FFC531',7)+'<path d="M128 96 l-10 14 h20z M128 160 l-10 -14 h20z" fill="#FFC531"/>')
def floors(up):
    o=shadow(128,100)+'<rect x="48" y="52" width="160" height="176" rx="10" fill="#E9EEF8"/><path d="M36 58 L128 12 L220 58z" fill="url(#or)"/><rect x="48" y="134" width="160" height="10" fill="#B9C6E0"/>'
    y=62 if up else 146; o+='<rect x="56" y="%g" width="144" height="70" rx="8" fill="#FFE27A"/>'%y
    o+=mini(128,(130 if up else 216),.58,'bl','joy','wave')
    y2=146 if up else 62; o+='<rect x="76" y="%g" width="36" height="40" rx="5" fill="#C9D4EA"/><rect x="146" y="%g" width="36" height="40" rx="5" fill="#C9D4EA"/>'%(y2+14,y2+14)
    return o
X('trenlau','trên lầu','upstairs', floors(True)); X('duoilau','dưới lầu','downstairs', floors(False))
def doorway(x): return '<rect x="%g" y="52" width="92" height="178" rx="8" fill="#8B5A34"/><rect x="%g" y="62" width="74" height="168" rx="4" fill="#FFE9A8"/>'%(x,x+9)
X('vao','vào','to go in', shadow(128,104)+doorway(140)+mini(150,228,1.1,'bl','smile','walk')+arrow('M22 150 H92 M72 130 L92 150 L72 170','#1FA57C'))
X('ra','ra','to go out', shadow(128,104)+doorway(24)+mini(120,228,1.1,'or','smile','walk')+arrow('M164 150 H234 M214 130 L234 150 L214 170','#EE5B7E'))
X('tatca','tất cả','all', shadow(128,104)+glow(128,150,104).replace('.45','.35')+''.join(apple(x,y,1.05) for x,y in ((74,196),(128,196),(182,196),(74,140),(128,140),(182,140)))+'<rect x="34" y="96" width="188" height="136" rx="26" fill="none" stroke="#F5B81F" stroke-width="6"/>')
X('vai','vài','a few, some', shadow(128,104)+''.join('<g opacity=".28">'+apple(x,y,1.05)+'</g>' for x,y in ((182,196),(74,140),(128,140),(182,140)))+glow(100,200,56)+apple(74,196,1.05)+apple(128,196,1.05))
X('giong','giống','alike, the same as', shadow(128,104)+house(70,196,1.2)+house(186,196,1.2)+stroke('M108 110 h40','#1FA57C',8)+stroke('M108 130 h40','#1FA57C',8))
X('khac','khác','different', shadow(128,104)+house(70,196,1.2)+'<g transform="translate(186 196)"><rect x="-34" y="-70" width="68" height="94" rx="6" fill="url(#pu)"/><rect x="-22" y="-58" width="16" height="16" rx="3" fill="#FFE27A"/><rect x="6" y="-58" width="16" height="16" rx="3" fill="#FFE27A"/><rect x="-22" y="-30" width="16" height="16" rx="3" fill="#FFE27A"/><rect x="6" y="-30" width="16" height="16" rx="3" fill="#FFE27A"/><rect x="-9" y="-4" width="18" height="28" rx="3" fill="#39456B"/></g>')
X('chiadoi','chia đôi','split in two', shadow(128,100)+'<g transform="translate(84 150) scale(2.6)"><path d="M0 -8 C-22 -18 -24 18 -6 20 q6 2 6 0z" fill="#E8503F"/><path d="M0 -6 C-14 -10 -16 14 -4 16 L0 16z" fill="#FFF3D6"/><circle cx="-4" cy="4" r="1.6" fill="#6B4A2A"/></g><g transform="translate(172 150) scale(2.6)"><path d="M0 -8 C22 -18 24 18 6 20 q-6 2 -6 0z" fill="#E8503F"/><path d="M0 -6 C14 -10 16 14 4 16 L0 16z" fill="#FFF3D6"/><circle cx="4" cy="4" r="1.6" fill="#6B4A2A"/></g>')
X('mo','mơ','to dream', shadow()+bust(cx=96,cy=146,r=32,mood='sleep',shirt='pu')+bubble(134,20,104,78,'<circle cx="186" cy="58" r="20" fill="url(#ye)"/><circle cx="196" cy="50" r="18" fill="#fff"/>'+spark(160,44,.7)+spark(216,78,.6,'#A58BFF'),(-1,1),True)+'<text x="40" y="96" font-family="Arial" font-weight="900" font-size="24" fill="#B9C6E0">z</text>')
X('noroi','no rồi','full (after eating)', shadow()+bust(mood='joy',shirt='gr',la=(110,200,-12),ra=(146,200,12),w=1.25)+'<g transform="translate(206 206)"><path d="M-34 0 h68 q0 24 -34 24 q-34 0 -34 -24z" fill="url(#pk)"/><rect x="-36" y="-5" width="72" height="9" rx="4.5" fill="#FFB3C4"/></g>'+spark(206,170,.9))
X('dau','đầu','head', shadow()+glow(128,92,66)+bust(mood='smile',shirt='bl')+'<circle cx="128" cy="92" r="56" fill="none" stroke="#F5B81F" stroke-width="6" stroke-dasharray="10 9"/>')
X('vai2','vai','shoulder', shadow()+bust(mood='smile',shirt='bl')+glow(176,148,30)+'<circle cx="176" cy="148" r="26" fill="none" stroke="#F5B81F" stroke-width="6" stroke-dasharray="10 9"/>')
X('bung','bụng','belly', shadow()+bust(cy=80,mood='smile',shirt='bl')+glow(128,196,36)+'<circle cx="128" cy="196" r="32" fill="none" stroke="#F5B81F" stroke-width="6" stroke-dasharray="10 9"/>')
X('goi','gối','pillow', shadow(128,96)+'<path d="M36 110 q-14 50 0 100 q92 16 184 0 q14 -50 0 -100 q-92 -16 -184 0z" fill="url(#wh)" stroke="#C9D4EA" stroke-width="4"/><path d="M60 126 q68 -10 136 0" fill="none" stroke="#DCE6F7" stroke-width="5" stroke-linecap="round"/>'+'<text x="176" y="78" font-family="Arial" font-weight="900" font-size="30" fill="#9AA8C7">z</text><text x="204" y="52" font-family="Arial" font-weight="900" font-size="40" fill="#B9C6E0">z</text>')
X('tulanh','tủ lạnh','fridge', shadow(128,70)+'<rect x="68" y="22" width="120" height="206" rx="16" fill="url(#wh)" stroke="#B9C6E0" stroke-width="4"/><rect x="68" y="92" width="120" height="5" fill="#B9C6E0"/><rect x="84" y="46" width="8" height="30" rx="4" fill="#8D95AD"/><rect x="84" y="112" width="8" height="50" rx="4" fill="#8D95AD"/><path transform="translate(150 60) scale(1.3)" d="M0 -12 V12 M-10 -6 L10 6 M-10 6 L10 -6" stroke="#7DC8F7" stroke-width="3.5" stroke-linecap="round"/>')
X('hu','hư','broken', shadow(128,90)+'<path d="M84 60 h88 q10 60 -6 164 h-76 q-16 -104 -6 -164z" fill="url(#bl)"/><rect x="78" y="50" width="100" height="18" rx="8" fill="#5B8DEF"/><path d="M128 66 l-14 34 l22 22 l-18 34 l16 30 l-10 38" fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="round"/><path d="M196 200 l22 8 l-14 16z" fill="#5B8DEF"/><path d="M40 206 l18 -10 l4 22z" fill="#2F6BE0"/>')
X('do','đổ','to spill', shadow(128,100)+'<g transform="translate(96 190) rotate(-78)">'+glass(0,0,1.3,0)+'</g><path d="M120 196 q40 -14 96 6 q20 10 0 20 q-70 14 -110 0 q-10 -10 14 -26z" fill="#7DC8F7"/><ellipse cx="170" cy="208" rx="24" ry="5" fill="#fff" opacity=".45"/>')

# ---- v86: batch 4 (full audit)
def badge(cx,cy,ok,r=26):
    return '<circle cx="%g" cy="%g" r="%g" fill="%s"/>'%(cx,cy,r,'#1FA57C' if ok else '#EE5B7E')+(stroke('M%g %g l%g %g l%g %g'%(cx-r*.45,cy,r*.33,r*.33,r*.6,-r*.66),'#fff',r*.22) if ok else stroke('M%g %g l%g %g M%g %g l%g %g'%(cx-r*.38,cy-r*.38,r*.76,r*.76,cx+r*.38,cy-r*.38,-r*.76,r*.76),'#fff',r*.22))
def qm(x,y,sz=58,col='#7B5CF0'): return '<text x="%g" y="%g" font-family="Arial" font-weight="900" font-size="%g" fill="%s">?</text>'%(x,y,sz,col)
X('chungta','chúng ta','we, us', shadow(128,110)+glow(128,150,112).replace('.45','.4')+mini(66,226,1.0,'gr','joy','stand','long')+mini(190,226,1.0,'or','joy','stand')+mini(128,230,1.12,'bl','joy','stand')+'<ellipse cx="128" cy="150" rx="112" ry="100" fill="none" stroke="#F5B81F" stroke-width="6" stroke-dasharray="12 10"/>')
X('nay','này','this, here', shadow(128,100)+bust(cx=84,cy=110,r=30,mood='smile',shirt='bl',look=4,ra=(140,196,6))+glow(176,204,40)+ball(176,206,22))
X('kia','kia','that, over there', '<path d="M0 232 Q120 170 256 196 V256 H0z" fill="#CFEBD8"/>'+bust(cx=70,cy=130,r=30,mood='smile',shirt='or',look=6,ra=(128,118,-8))+stroke('M144 110 L186 84','#B9C6E0',5).replace('stroke-linecap','stroke-dasharray="3 12" stroke-linecap')+glow(218,62,32)+ball(218,62,13))
X('ai','ai','who', shadow(128,60)+'<g opacity=".9"><circle cx="128" cy="84" r="36" fill="#B9C6E0"/><path d="M70 232 v-50 q0 -40 40 -40 h36 q40 0 40 40 v50z" fill="#B9C6E0"/></g>'+qm(110,104,56,'#fff'))
X('gi','gì','what', shadow(128,90)+box(58,96,140,126)+qm(104,196,96,'#fff')+spark(52,66,1)+spark(210,60,.9))
X('baonhieu','bao nhiêu','how much, how many', shadow(128,104)+''.join(apple(x,y,1.0) for x,y in ((60,206),(98,206),(136,206),(79,170),(117,170),(98,134)))+qm(170,150,110))
X('khinao','khi nào','when', shadow(128,90)+'<rect x="30" y="56" width="150" height="150" rx="18" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/><rect x="30" y="56" width="150" height="42" rx="16" fill="url(#pk)"/>'+''.join('<rect x="%g" y="%g" width="22" height="18" rx="5" fill="#DCE6F7"/>'%(46+i%4*32,112+i//4*28) for i in range(12))+clock(196,186,42,10,10)+qm(182,70,64))
X('duoc','được','OK, can, right', shadow()+bust(mood='joy',shirt='gr',ra=(176,150,12))+badge(200,74,True,34)+spark(52,70,1))
X('sai','sai','wrong, cannot', shadow()+bust(mood='sad',shirt='or')+badge(200,74,False,34))
X('them','thêm','more, extra', shadow(128,104)+'<ellipse cx="128" cy="212" rx="96" ry="14" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+apple(82,190,1.05)+apple(128,190,1.05)+glow(184,150,44)+apple(184,150,1.15)+stroke('M184 60 v34','#B9C6E0',6)+stroke('M162 70 v24','#B9C6E0',5)+stroke('M206 70 v24','#B9C6E0',5)+'<circle cx="222" cy="50" r="22" fill="#1FA57C"/>'+stroke('M210 50 h24 M222 38 v24','#fff',6))
def tl(n):
    o=shadow(128,110,236)
    for i in range(3):
        on=i==n; o+=(glow(48+i*80,176,50) if on else '')+'<rect x="%g" y="140" width="72" height="72" rx="14" fill="%s" stroke="%s" stroke-width="4"/><rect x="%g" y="140" width="72" height="20" rx="10" fill="%s"/>'%(12+i*80,'#FFF7D6' if on else '#EEF2FA','#F5B81F' if on else '#C9D4EA',12+i*80,'url(#or)' if on else '#C9D4EA')
    o+=mini(48+n*80,146,.72,'bl','smile','stand')
    if n==0: o+=arrow('M214 60 H140 M160 40 L140 60 L160 80','#B9C6E0')
    if n==2: o+=arrow('M42 60 H116 M96 40 L116 60 L96 80','#B9C6E0')
    return o
X('qua3','hôm qua','yesterday; before', tl(0)); X('nay3','bây giờ','now; today', tl(1)); X('sau3','sau','later; after', tl(2))
X('dunggio','đúng giờ','on time', shadow(128,70)+clock(118,128,84,9,0)+badge(196,196,True,34))
X('theo','theo','to follow', shadow(128,110)+'<rect x="10" y="226" width="236" height="8" rx="4" fill="#DCE6F7"/>'+mini(176,228,1.15,'or','smile','walk')+mini(78,228,1.0,'bl','smile','walk')+stroke('M112 150 h20','#B9C6E0',6)+stroke('M112 172 h14','#B9C6E0',6))
X('lay','lấy','to take', shadow(128,100)+'<rect x="120" y="150" width="124" height="14" rx="6" fill="#C48A50"/><rect x="232" y="60" width="12" height="170" fill="#A66E3A"/>'+apple(206,130,1.0)+glow(160,128,34)+apple(160,128,1.1)+bust(cx=64,cy=130,r=30,mood='smile',shirt='pu',look=5,ra=(140,134,-10)))
X('dat','đặt','to put down', shadow(128,96)+table(160)+glow(128,134,40)+ball(128,136,22)+stroke('M128 40 v44','#B9C6E0',6)+stroke('M106 52 v30','#B9C6E0',5)+stroke('M150 52 v30','#B9C6E0',5)+arm(200,60,150,120,'#2F6BE0',16,10))
X('doi','đổi','to change, to swap', shadow(128,100)+'<rect x="28" y="118" width="76" height="76" rx="16" fill="url(#bl)"/><rect x="152" y="118" width="76" height="76" rx="16" fill="url(#pk)"/>'+arrow('M70 100 Q128 50 186 100 M166 78 L188 102 L156 106','#1FA57C').replace('stroke-width="18"','stroke-width="11"')+arrow('M186 212 Q128 262 70 212 M90 234 L68 210 L100 206','#F58A1F').replace('stroke-width="18"','stroke-width="11"'))
X('giaithich','giải thích','to explain, to show how', shadow(128,110)+'<rect x="92" y="34" width="150" height="110" rx="10" fill="#2E7D5B"/><rect x="92" y="34" width="150" height="110" rx="10" fill="none" stroke="#C48A50" stroke-width="8"/>'+stroke('M114 66 h70','#fff',5)+stroke('M114 88 h100','#fff',5)+stroke('M114 110 h54','#fff',5)+bust(cx=62,cy=140,r=28,mood='open',shirt='or',look=4,ra=(104,96,-14))+mini(170,230,.62,'bl','smile','stand')+mini(214,230,.62,'pk','smile','stand','long'))
X('de','dễ','easy', shadow(128,70)+mini(120,228,1.3,'gr','joy','stand')+stroke('M140 112 L176 70','#1FA57C',13)+'<circle cx="178" cy="68" r="8" fill="url(#sk)"/>'+box(150,14,62,46)+spark(60,60,1.1)+spark(228,96,.8))
X('kho','khó','hard, difficult', '<path d="M0 256 L256 120 V256z" fill="#CFEBD8"/>'+'<g transform="rotate(-24 96 206)">'+mini(86,214,1.1,'or','tired','walk')+'</g><circle cx="176" cy="126" r="48" fill="#8D95AD"/><circle cx="160" cy="110" r="12" fill="#A9B2C8"/><circle cx="196" cy="140" r="8" fill="#737C98"/>'+stroke('M112 138 L138 132','#F58A1F',13)+'<path d="M60 70 q7 11 0 17 q-7 -6 0 -17z" fill="#7DC8F7"/><path d="M96 50 q7 11 0 17 q-7 -6 0 -17z" fill="#7DC8F7"/>')
X('dep','đẹp','beautiful, nice', shadow(128,60)+'<path d="M96 150 h64 q10 40 -8 78 h-48 q-18 -38 -8 -78z" fill="url(#bl)"/>'+stroke('M128 150 V86','#1FA57C',7)+stroke('M128 150 Q100 120 90 96','#1FA57C',6)+stroke('M128 150 Q156 120 168 100','#1FA57C',6)+''.join('<g transform="translate(%g %g)">'%(x,y)+''.join('<circle cx="%g" cy="%g" r="13" fill="%s"/>'%(dx,dy,c) for dx,dy in ((0,-14),(13,-4),(8,12),(-8,12),(-13,-4)))+'<circle r="8" fill="#FFC531"/></g>' for x,y,c in ((128,70,'#FF8FA8'),(84,88,'#A58BFF'),(174,92,'#FFB45C')))+spark(44,50,1.2)+spark(216,44,1.1)+spark(214,170,.8))
def pencil(x,y,L): return '<g transform="translate(%g %g)"><rect x="0" y="-11" width="%g" height="22" rx="4" fill="url(#ye)"/><path d="M%g -11 l22 11 l-22 11z" fill="#F2C39A"/><path d="M%g -4 l8 4 l-8 4z" fill="#39456B"/><rect x="0" y="-11" width="16" height="22" rx="4" fill="#EE5B7E"/></g>'%(x,y,L,L,L+14)
X('ngan','ngắn','short (length)', shadow(128,104)+pencil(22,96,180)+glow(88,170,62)+pencil(40,170,74))
X('om','ốm','thin', shadow(128,104)+'<g transform="translate(74 0) scale(1.35 1) translate(-74 0)">'+mini(74,228,1.2,'bl','smile','stand')+'</g>'+glow(188,150,60)+'<g transform="translate(188 0) scale(.66 1) translate(-188 0)">'+mini(188,228,1.25,'or','smile','stand')+'</g>')
def tee(cx,cy,fill,s=1): return '<g transform="translate(%g %g) scale(%g)"><path d="M-30 -44 q30 20 60 0 l40 22 l-18 34 l-20 -10 v66 h-64 v-66 l-20 10 l-18 -34z" fill="%s"/></g>'%(cx,cy,s,fill)
X('moi','mới','new', shadow(128,80)+glow(128,136,96).replace('.45','.3')+tee(128,140,'url(#bl)',1.35)+spark(48,60,1.5)+spark(214,70,1.3)+spark(206,206,1))
X('cu','cũ','old (things)', shadow(128,80)+tee(128,140,'#A9B2C8',1.35)+'<rect x="96" y="150" width="30" height="26" rx="3" fill="#8D95AD" stroke="#737C98" stroke-width="2" stroke-dasharray="4 3"/><path d="M150 112 l10 12 l-8 10 l10 12" fill="none" stroke="#737C98" stroke-width="4"/><path d="M86 232 l10 -12 l10 12 l10 -12 l10 12" fill="none" stroke="#A9B2C8" stroke-width="5"/>')
X('lammat','làm mất','to lose (something)', shadow()+bust(cx=92,cy=120,r=32,mood='o',shirt='gr',look=4,la=(60,60,-10),ra=(124,60,10))+'<rect x="160" y="150" width="76" height="70" rx="14" fill="none" stroke="#B9C6E0" stroke-width="4" stroke-dasharray="9 8"/><path d="M180 150 q18 -34 36 0" fill="none" stroke="#B9C6E0" stroke-width="4" stroke-dasharray="9 8"/>'+qm(184,206,46,'#B9C6E0'))
X('quanh','quanh','around', shadow(128,100)+box(88,110,80,80)+''.join(ball(x,y,13) for x,y in ((128,70),(204,110),(210,190),(128,226),(48,190),(52,110)))+'<ellipse cx="128" cy="150" rx="98" ry="86" fill="none" stroke="#F5B81F" stroke-width="5" stroke-dasharray="10 10"/>')
X('mat2','mặt','face', shadow()+bust(mood='smile',shirt='gr')+'<ellipse cx="128" cy="102" rx="34" ry="30" fill="none" stroke="#F5B81F" stroke-width="6" stroke-dasharray="10 9"/>'+glow(128,102,36).replace('.45','.2'))
X('hong','họng','throat', shadow()+bust(cy=84,mood='sad',shirt='bl')+glow(128,124,22)+'<circle cx="128" cy="124" r="20" fill="none" stroke="#EE5B7E" stroke-width="6" stroke-dasharray="8 7"/>')
X('o','ở','to live, to be at', shadow(128,104)+'<path d="M10 232 Q130 216 250 232 V244 H10z" fill="#CFEBD8"/><rect x="50" y="100" width="156" height="128" rx="8" fill="#FFE9C7"/><path d="M30 106 L128 30 L226 106z" fill="url(#or)"/><rect x="150" y="160" width="36" height="68" rx="4" fill="#8B5A34"/><rect x="66" y="120" width="72" height="66" rx="8" fill="#9FD3F5"/>'+'<g transform="translate(102 0)"><clipPath id="wc"><rect x="-36" y="120" width="72" height="66" rx="8"/></clipPath><g clip-path="url(#wc)">'+mini(0,236,.62,'bl','joy','wave')+'</g></g>'+heart(206,60,.9))
X('daso','đa số','most, the majority', shadow(128,104)+''.join((glow(x,y,24) if i<5 else '')+('<g opacity="%s">'%('1' if i<5 else '.25'))+apple(x,y,1.05)+'</g>' for i,(x,y) in enumerate(((74,140),(128,140),(182,140),(74,196),(128,196),(182,196)))))
X('mo2','mở','to open', shadow(128,80)+'<rect x="70" y="40" width="120" height="188" rx="8" fill="#8B5A34"/><rect x="80" y="50" width="100" height="178" fill="#FFE9A8"/><path d="M80 50 l-52 22 v170 l52 -14z" fill="#B67B4A"/><circle cx="40" cy="150" r="6" fill="#FFC531"/>'+spark(130,110,1.3)+spark(156,160,.9))
X('dong','đóng','to close', shadow(128,80)+'<rect x="70" y="40" width="120" height="188" rx="8" fill="#8B5A34"/><rect x="80" y="50" width="100" height="178" rx="3" fill="#B67B4A"/><rect x="92" y="64" width="76" height="60" rx="4" fill="#A66E3A"/><rect x="92" y="138" width="76" height="76" rx="4" fill="#A66E3A"/><circle cx="166" cy="146" r="7" fill="#FFC531"/>')
X('nhay','nhảy','to jump', shadow(128,50,236)+'<g transform="translate(0 -22)">'+mini(128,214,1.05,'pk','joy','up','long')+'</g>'+stroke('M96 206 v22','#B9C6E0',6)+stroke('M128 212 v18','#B9C6E0',6)+stroke('M160 206 v22','#B9C6E0',6)+spark(50,70,1)+spark(210,60,1))

# ---- v86: batch 5 (things, food, road, amounts)
def bottle(cx,by,cap,body,label): return '<g transform="translate(%g %g)"><rect x="-12" y="-150" width="24" height="26" rx="5" fill="%s"/><path d="M-12 -126 h24 q22 14 22 44 v70 q0 12 -12 12 h-44 q-12 0 -12 -12 v-70 q0 -30 22 -44z" fill="%s"/><rect x="-34" y="-70" width="68" height="44" rx="6" fill="#fff"/>%s<rect x="-24" y="-112" width="8" height="30" rx="4" fill="#fff" opacity=".35"/></g>'%(cx,by,cap,body,label)
def dish(cx,cy,col): return '<ellipse cx="%g" cy="%g" rx="44" ry="15" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/><ellipse cx="%g" cy="%g" rx="30" ry="9" fill="%s"/>'%(cx,cy,cx,cy,col)
X('nuocmam','nước mắm','fish sauce', shadow(128,96)+bottle(96,224,'#E8503F','#D98A2B','<path d="M-20 -48 q14 -14 28 0 q-14 14 -28 0z M8 -48 l12 -9 v18z" fill="#2F6BE0"/>')+dish(190,208,'#C9781F')+'<circle cx="182" cy="206" r="4" fill="#E8503F"/><circle cx="198" cy="210" r="3" fill="#E8503F"/>')
X('nuoctuong','nước tương','soy sauce', shadow(128,96)+bottle(96,224,'#1FA57C','#4A2E1F','<ellipse cx="-8" cy="-48" rx="9" ry="12" fill="#E9C46A"/><ellipse cx="10" cy="-48" rx="9" ry="12" fill="#D9B054"/>')+dish(190,208,'#3A2418'))
X('tieu','tiêu','pepper', shadow(128,70)+'<path d="M92 110 h72 l10 110 q0 10 -10 10 h-72 q-10 0 -10 -10z" fill="url(#wh)" stroke="#B9C6E0" stroke-width="4"/><path d="M96 150 h64 l6 66 h-76z" fill="#5A4A42"/><path d="M90 110 q0 -44 38 -44 q38 0 38 44z" fill="#8D95AD"/>'+''.join('<circle cx="%g" cy="%g" r="3.5" fill="#39456B"/>'%(x,y) for x,y in ((116,84),(128,78),(140,84),(122,96),(134,96)))+''.join('<circle cx="%g" cy="%g" r="4" fill="#39456B"/>'%(x,y) for x,y in ((198,214),(212,222),(204,230),(46,222),(58,230))))
X('dauhu','đậu hũ','tofu', shadow(128,96)+'<ellipse cx="128" cy="206" rx="100" ry="22" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+''.join('<g transform="translate(%g %g)"><path d="M-30 -20 l30 -14 l30 14 v34 l-30 14 l-30 -14z" fill="#FFF7E0"/><path d="M-30 -20 l30 14 l30 -14 l-30 -14z" fill="#FFFDF2"/><path d="M0 -6 v34 l30 -14 v-34z" fill="#F1E3BE"/></g>'%(x,y) for x,y in ((92,176),(164,176),(128,140)))+'<circle cx="120" cy="112" r="5" fill="#6CC36A"/><circle cx="136" cy="110" r="4" fill="#6CC36A"/>')
def roll(cx,cy,ang,wrap,inner): return '<g transform="translate(%g %g) rotate(%g)"><rect x="-58" y="-18" width="116" height="36" rx="18" fill="%s" stroke="#D8DEE9" stroke-width="2"/>%s</g>'%(cx,cy,ang,wrap,inner)
shr='<path d="M-30 4 q14 -18 30 0" fill="none" stroke="#F4846B" stroke-width="7" stroke-linecap="round"/><path d="M6 4 q14 -18 30 0" fill="none" stroke="#F4846B" stroke-width="7" stroke-linecap="round"/><rect x="-44" y="6" width="88" height="6" rx="3" fill="#6CC36A" opacity=".8"/>'
X('goicuon','gỏi cuốn','fresh spring roll', shadow(128,104)+'<ellipse cx="128" cy="206" rx="112" ry="22" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+roll(110,150,-8,'#F7F4EA',shr)+roll(122,188,-8,'#F7F4EA',shr)+dish(206,150,'#B5651D').replace('rx="44"','rx="30"').replace('rx="30" ry="9"','rx="20" ry="6"'))
X('banhcuon','bánh cuốn','steamed rice rolls', shadow(128,104)+'<ellipse cx="128" cy="206" rx="112" ry="22" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+''.join(roll(128,y,0,'#FFFFFF','<circle cx="-30" cy="-8" r="5" fill="#B5651D"/><circle cx="-6" cy="-10" r="5" fill="#C9781F"/><circle cx="20" cy="-8" r="5" fill="#B5651D"/><circle cx="38" cy="-6" r="4" fill="#6CC36A"/>') for y in (136,166,196)))
def numtile(n,k): return shadow(128,80)+'<rect x="48" y="40" width="160" height="176" rx="28" fill="url(#bl)"/><text x="128" y="176" text-anchor="middle" font-family="Arial" font-weight="900" font-size="150" fill="#fff">%s</text>'%n+''.join('<circle cx="%g" cy="236" r="7" fill="#F5B81F"/>'%(128-(k-1)*9+i*18) for i in range(k))
X('so9','chín','nine', numtile(9,9)); X('so5','năm','five', numtile(5,5))
X('gapdoi','gấp đôi','double, twice', shadow(128,104)+apple(60,170,1.5)+arrow('M100 170 H140 M124 154 L140 170 L124 186','#B9C6E0').replace('stroke-width="18"','stroke-width="11"')+glow(196,170,56)+apple(178,170,1.5)+apple(218,170,1.5))
X('chiadoi2','chia đôi','split in two', shadow(128,100)+'<path d="M112 70 a84 84 0 0 0 0 168z" fill="url(#ye)"/><path d="M144 70 a84 84 0 0 1 0 168z" fill="url(#ye)"/><path d="M112 92 a62 62 0 0 0 0 124z" fill="#FFF3C4"/><path d="M144 92 a62 62 0 0 1 0 124z" fill="#FFF3C4"/>'+stroke('M128 40 V250','#B9C6E0',5).replace('stroke-linecap','stroke-dasharray="10 10" stroke-linecap'))
def slot(x,y): return '<circle cx="%g" cy="%g" r="26" fill="none" stroke="#B9C6E0" stroke-width="4" stroke-dasharray="8 7"/>'%(x,y)
X('thieu','thiếu','short, missing', shadow(128,104)+'<rect x="24" y="100" width="208" height="110" rx="22" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+apple(62,160,1.2)+apple(106,160,1.2)+apple(150,160,1.2)+slot(194,156)+qm(184,172,34,'#B9C6E0'))
X('du','đủ','enough', shadow(128,104)+'<rect x="24" y="100" width="208" height="110" rx="22" fill="url(#wh)" stroke="#C9D4EA" stroke-width="3"/>'+apple(62,160,1.2)+apple(106,160,1.2)+apple(150,160,1.2)+apple(194,160,1.2)+badge(222,92,True,26))
X('rong','rộng','wide, roomy', '<rect x="14" y="60" width="228" height="176" rx="12" fill="#EEF2FA" stroke="#C9D4EA" stroke-width="4"/><rect x="14" y="206" width="228" height="30" rx="8" fill="#DCE6F7"/>'+mini(128,222,.9,'gr','joy','up')+arrow('M30 96 H96 M46 80 L30 96 L46 112','#B9C6E0').replace('stroke-width="18"','stroke-width="9"')+arrow('M226 96 H160 M210 80 L226 96 L210 112','#B9C6E0').replace('stroke-width="18"','stroke-width="9"'))
X('chat','chật','too tight, cramped', '<rect x="78" y="40" width="100" height="196" rx="10" fill="#EEF2FA" stroke="#8D95AD" stroke-width="6"/>'+mini(128,228,1.3,'or','sad','stand')+arrow('M18 140 H62 M46 124 L62 140 L46 156','#EE5B7E').replace('stroke-width="18"','stroke-width="10"')+arrow('M238 140 H194 M210 124 L194 140 L210 156','#EE5B7E').replace('stroke-width="18"','stroke-width="10"'))
X('sau2','sâu','deep', '<rect x="0" y="0" width="256" height="60" fill="#CFEBD8"/><path d="M40 60 h176 v170 q0 20 -20 20 h-136 q-20 0 -20 -20z" fill="#5B8DEF"/><path d="M40 60 h176 v40 q-44 14 -88 0 q-44 -14 -88 0z" fill="#9FD3F5"/>'+arrow('M128 96 V224 M106 204 L128 226 L150 204','#fff').replace('stroke-width="18"','stroke-width="11"')+ball(190,222,10))
X('xau','xấu','ugly, bad', shadow(128,60)+'<path d="M96 150 h64 q10 40 -8 78 h-48 q-18 -38 -8 -78z" fill="#A9B2C8"/><path d="M120 156 l10 22 l-10 20 l8 24" fill="none" stroke="#737C98" stroke-width="4"/>'+stroke('M128 150 Q124 110 96 96','#8A9A5B',7)+stroke('M128 150 Q140 120 168 122','#8A9A5B',6)+''.join('<g transform="translate(%g %g) rotate(%g)">'%(x,y,r)+''.join('<ellipse cx="%g" cy="%g" rx="9" ry="14" fill="#B59A7A"/>'%(dx,dy) for dx,dy in ((-10,8),(0,12),(10,8)))+'<circle r="7" fill="#8B6F4E"/></g>' for x,y,r in ((92,98,20),(172,126,-30)))+'<ellipse cx="70" cy="222" rx="9" ry="5" fill="#B59A7A"/><ellipse cx="190" cy="226" rx="9" ry="5" fill="#B59A7A"/>')
X('qua','qua','to cross, to go over', '<path d="M0 190 h256 v66 h-256z" fill="#9FD3F5"/><path d="M0 204 q20 -8 40 0 t40 0 t40 0 t40 0 t40 0 t40 0" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/><path d="M0 150 Q128 70 256 150 v22 Q128 96 0 172z" fill="#C48A50"/><rect x="0" y="150" width="34" height="60" fill="#CFEBD8"/><rect x="222" y="150" width="34" height="60" fill="#CFEBD8"/>'+mini(128,116,.8,'bl','smile','walk')+arrow('M60 60 H190 M170 42 L190 60 L170 78','#F5B81F').replace('stroke-width="18"','stroke-width="10"'))
X('queo','quẹo','to turn', '<rect x="0" y="0" width="256" height="256" rx="28" fill="#CFEBD8"/><rect x="98" y="110" width="60" height="146" fill="#8D95AD"/><rect x="98" y="80" width="158" height="60" fill="#8D95AD"/>'+arrow('M128 226 V110 H212 M186 84 L212 110 L186 136')+mini(60,200,.7,'or','smile','stand'))
X('quaylai','quay lại','to turn back, to come back', '<rect x="0" y="0" width="256" height="256" rx="28" fill="#CFEBD8"/><rect x="60" y="40" width="136" height="216" rx="40" fill="#8D95AD"/><rect x="108" y="92" width="40" height="164" fill="#CFEBD8"/>'+arrow('M172 226 V110 Q172 66 128 66 Q84 66 84 110 V206 M60 182 L84 208 L108 182'))
X('khongai','không ai','nobody', shadow(128,104)+''.join('<g transform="translate(%g 0)"><circle cx="0" cy="110" r="24" fill="none" stroke="#B9C6E0" stroke-width="4" stroke-dasharray="8 7"/><path d="M-30 226 v-50 q0 -28 28 -28 h4 q28 0 28 28 v50" fill="none" stroke="#B9C6E0" stroke-width="4" stroke-dasharray="8 7"/></g>'%x for x in (60,128,196)))
X('khuyenmai','khuyến mãi','promotion, sale', shadow(128,80)+'<g transform="translate(128 130) rotate(-14)"><path d="M-80 -50 h110 l50 50 l-50 50 h-110 q-14 0 -14 -14 v-72 q0 -14 14 -14z" fill="url(#pk)"/><circle cx="44" cy="0" r="11" fill="#fff"/><text x="-26" y="26" text-anchor="middle" font-family="Arial" font-weight="900" font-size="70" fill="#fff">%</text></g>'+spark(46,54,1.4)+spark(214,60,1.2)+spark(204,210,1))
X('het','hết rồi','all gone, sold out', shadow(128,100)+'<ellipse cx="128" cy="180" rx="104" ry="34" fill="url(#wh)" stroke="#C9D4EA" stroke-width="4"/><ellipse cx="128" cy="178" rx="68" ry="20" fill="#F6F9FF" stroke="#DCE6F7" stroke-width="3"/>'+slot(128,120)+'<circle cx="96" cy="182" r="3" fill="#D9A066"/><circle cx="150" cy="186" r="2.5" fill="#D9A066"/><circle cx="126" cy="174" r="2" fill="#D9A066"/>')
X('bang','bảng','board; sign', shadow(128,96)+'<rect x="30" y="40" width="196" height="140" rx="10" fill="#2E7D5B"/><rect x="30" y="40" width="196" height="140" rx="10" fill="none" stroke="#C48A50" stroke-width="10"/>'+stroke('M56 80 h100','#fff',6)+stroke('M56 108 h140','#fff',6)+stroke('M56 136 h70','#fff',6)+'<rect x="70" y="184" width="10" height="46" fill="#A66E3A"/><rect x="176" y="184" width="10" height="46" fill="#A66E3A"/><rect x="150" y="172" width="34" height="8" rx="3" fill="#fff"/>')
X('vn','tiếng Việt','Vietnamese', shadow(128,80)+'<rect x="34" y="60" width="188" height="126" rx="14" fill="#DA251D"/><path transform="translate(128 123) scale(2.3)" d="M0 -16 L4.7 -5 L16.2 -5 L7 2.2 L10.4 13.6 L0 6.8 L-10.4 13.6 L-7 2.2 L-16.2 -5 L-4.7 -5z" fill="#FFDD00"/>')
X('dich','dịch','to translate', shadow(128,96)+bubble(18,50,104,84,'<text x="70" y="112" text-anchor="middle" font-family="Arial" font-weight="900" font-size="54" fill="#2F6BE0">A</text>',(-1,1))+bubble(134,96,104,84,'<text x="186" y="158" text-anchor="middle" font-family="Arial" font-weight="900" font-size="54" fill="#EE5B7E">Ă</text>',(1,1))+arrow('M128 40 q30 0 44 30 M158 54 L174 72 L182 48','#1FA57C').replace('stroke-width="18"','stroke-width="8"'))
X('bep','bếp','stove, kitchen', shadow(128,96)+'<rect x="40" y="140" width="176" height="88" rx="10" fill="url(#wh)" stroke="#B9C6E0" stroke-width="4"/><rect x="40" y="128" width="176" height="18" rx="6" fill="#5B6B8F"/><circle cx="84" cy="186" r="9" fill="#8D95AD"/><circle cx="128" cy="186" r="9" fill="#8D95AD"/><circle cx="172" cy="186" r="9" fill="#8D95AD"/>'+'<path d="M66 128 q4 -16 14 -22 q-2 10 6 14 q2 -12 12 -18 q0 14 8 26z" fill="#F58A1F"/><path d="M78 128 q2 -8 8 -12 q2 8 8 12z" fill="#FFE27A"/>'+'<path d="M134 84 h76 v30 q0 14 -14 14 h-48 q-14 0 -14 -14z" fill="#39456B"/><rect x="128" y="78" width="88" height="10" rx="5" fill="#5B6B8F"/><rect x="206" y="92" width="34" height="8" rx="4" fill="#5B6B8F"/>'+stroke('M158 66 q-6 -10 0 -20','#B9C6E0',5)+stroke('M184 66 q-6 -10 0 -20','#B9C6E0',5))
X('khan','khăn','towel', shadow(128,80)+'<rect x="30" y="56" width="196" height="12" rx="6" fill="#8D95AD"/><path d="M70 62 h116 v140 q0 10 -10 10 h-96 q-10 0 -10 -10z" fill="url(#bl)"/><rect x="70" y="170" width="116" height="10" fill="#fff" opacity=".6"/><rect x="70" y="186" width="116" height="6" fill="#fff" opacity=".6"/><path d="M70 62 h116 v16 h-116z" fill="#2F6BE0"/>')
X('ui','ủi','to iron', shadow(128,100)+'<path d="M20 206 h216 l-10 20 h-196z" fill="#DCE6F7"/><path d="M40 196 q4 -70 90 -70 h70 q20 0 20 20 v50z" fill="url(#pu)"/><path d="M40 196 h180 v14 h-186 q-2 -6 6 -14z" fill="#8D95AD"/><path d="M110 110 h70 q22 0 22 22 v6 h-16 v-4 q0 -8 -8 -8 h-68z" fill="#39456B"/>'+stroke('M70 96 q-8 -12 0 -26','#B9C6E0',5)+stroke('M96 86 q-8 -12 0 -26','#B9C6E0',5))
X('hoboi','hồ bơi','swimming pool', '<rect x="10" y="60" width="236" height="176" rx="30" fill="#E9EEF8"/><rect x="28" y="78" width="200" height="140" rx="22" fill="#5BB8F0"/>'+''.join('<path d="M40 %g q16 -10 32 0 t32 0 t32 0 t32 0 t32 0" fill="none" stroke="#fff" stroke-width="4" opacity=".6"/>'%y for y in (112,150,188))+'<path d="M186 50 v60 M212 50 v60 M186 70 h26 M186 92 h26" stroke="#8D95AD" stroke-width="7" fill="none" stroke-linecap="round"/>'+'<circle cx="96" cy="150" r="20" fill="none" stroke="#EE5B7E" stroke-width="12"/><circle cx="96" cy="150" r="20" fill="none" stroke="#fff" stroke-width="12" stroke-dasharray="14 18"/>')
X('viahe','vỉa hè','pavement', '<rect x="0" y="150" width="256" height="106" fill="#8D95AD"/>'+''.join('<rect x="%g" y="210" width="34" height="8" rx="4" fill="#fff"/>'%x for x in (10,74,138,202))+'<rect x="0" y="96" width="256" height="64" fill="#E3D5BC"/>'+''.join('<path d="M%g 96 v64" stroke="#CDBB9A" stroke-width="3"/>'%x for x in (32,64,96,128,160,192,224))+'<path d="M0 128 h256" stroke="#CDBB9A" stroke-width="3"/><rect x="0" y="156" width="256" height="10" fill="#B9C6E0"/>'+glow(128,110,70).replace('.45','.3')+mini(128,150,.85,'bl','smile','walk')+tree(214,128,.6))
X('bungbinh','bùng binh','roundabout', '<rect x="0" y="0" width="256" height="256" rx="28" fill="#CFEBD8"/><rect x="100" y="0" width="56" height="256" fill="#8D95AD"/><rect x="0" y="100" width="256" height="56" fill="#8D95AD"/><circle cx="128" cy="128" r="84" fill="#8D95AD"/><circle cx="128" cy="128" r="40" fill="#6CC36A"/><circle cx="128" cy="128" r="16" fill="#FF8FA8"/>'+'<path d="M128 66 a62 62 0 1 0 62 62" fill="none" stroke="#FFC531" stroke-width="10" stroke-linecap="round"/><path d="M176 112 L190 130 L206 114" fill="none" stroke="#FFC531" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
X('nga3','ngã ba','T-junction', road('T')+''.join('<rect x="%g" y="107" width="26" height="6" rx="3" fill="#fff"/>'%x for x in (16,66,166,216))+'<rect x="125" y="160" width="6" height="26" rx="3" fill="#fff"/><rect x="125" y="210" width="6" height="26" rx="3" fill="#fff"/>'+house(128,44,.6))
X('co','cổ','neck', shadow()+bust(cy=84,mood='smile',shirt='gr')+glow(128,124,22)+'<circle cx="128" cy="124" r="20" fill="none" stroke="#F5B81F" stroke-width="6" stroke-dasharray="8 7"/>')

import sys
out=sys.argv[1]
for k in ('chiadoi','vai2'): D.pop(k,None)   # drawn but not clear enough, left out
for k,(vi,en,body) in D.items(): open(os.path.join(out,'w-'+k+'.svg'),'w',encoding='utf8').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'+DEFS+body+'</svg>')
html='<body style="margin:0;background:#F4F6FD;font-family:Arial"><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;padding:14px;width:1000px">'
for k,(vi,en,body) in D.items(): html+='<div style="background:#fff;border-radius:18px;padding:8px;text-align:center;box-shadow:0 2px 0 #D9E0F0"><img src="w-%s.svg" width="150" height="150"><div style="font-weight:800;font-size:20px;color:#2F6BE0">%s</div><div style="color:#6B7896;font-size:13px">%s</div></div>'%(k,vi,en)
open(os.path.join(out,'sheet.html'),'w',encoding='utf8').write(html+'</div></body>')
print(len(D),'drawings')
