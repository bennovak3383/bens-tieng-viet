# v84: our own drawings for words an emoji cannot show. 256x256, soft colours, same people look as the app.
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
D['ban']=('bạn','friend', shadow(128,96)+mini(92,226,1.25,'bl','joy','stand')+mini(164,226,1.25,'gr','joy','stand','long')+stroke('M108 118 Q128 104 150 118','#2F6BE0',13)+heart(128,44,1.1))
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
X('dua','đưa','to hand over', shadow(128,106)+mini(64,226,1.15,'bl','smile','stand')+mini(196,226,1.15,'gr','joy','stand','long')+stroke('M80 124 L112 138','#2F6BE0',12)+stroke('M180 124 L150 140','#1FA57C',12)+box(108,112,46,40)+'<circle cx="112" cy="140" r="7" fill="url(#sk)"/><circle cx="150" cy="142" r="7" fill="url(#sk)"/>')
X('cam','cầm','to hold', shadow()+bust(mood='smile',shirt='gr')+box(92,150,72,60)+'<circle cx="92" cy="186" r="10" fill="url(#sk)"/><circle cx="164" cy="186" r="10" fill="url(#sk)"/>')
X('khoe','khỏe','healthy, strong', shadow(128,60)+mini(128,228,1.4,'gr','joy','stand').replace('</g>','')+stroke('M-14 -88 L-40 -92 L-40 -122','#1FA57C',12)+stroke('M14 -88 L40 -92 L40 -122','#1FA57C',12)+'<circle cx="-40" cy="-124" r="7" fill="url(#sk)"/><circle cx="40" cy="-124" r="7" fill="url(#sk)"/></g>'+spark(44,60,1.1)+spark(214,66,1))
X('te','té','to fall over', shadow(128,90)+'<g transform="rotate(62 128 190)">'+mini(128,214,1.2,'or','o','up')+'</g>'+spark(60,70,1.1,'#FF8FA8')+spark(96,44,.8)+stroke('M190 96 l14 -16','#B9C6E0',6)+stroke('M210 122 l20 -8','#B9C6E0',6))
X('gap','gặp','to meet', shadow(128,106)+mini(72,226,1.2,'bl','joy','wave')+'<g transform="translate(256 0) scale(-1 1)">'+mini(72,226,1.2,'pk','joy','wave','long')+'</g>')
X('oi','ơi','hey! (calling someone)', shadow()+bust(cx=104,mood='open',shirt='or',look=5,ra=(150,112,16))+stroke('M178 84 l26 -14','#F58A1F',7)+stroke('M184 108 h30','#F58A1F',7)+stroke('M178 132 l26 14','#F58A1F',7))
X('day','đẩy','to push', shadow(128,110)+'<g transform="rotate(14 80 226)">'+mini(80,226,1.15,'bl','flat','walk')+'</g>'+stroke('M96 132 L140 140','#2F6BE0',13)+'<circle cx="142" cy="140" r="8" fill="url(#sk)"/>'+box(146,112,92,112)+stroke('M20 150 h26','#B9C6E0',6)+stroke('M14 176 h32','#B9C6E0',6))
X('keo','kéo','to pull', shadow(128,110)+'<g transform="rotate(-16 70 226)">'+mini(70,226,1.15,'pu','flat','walk')+'</g>'+stroke('M92 146 L160 176','#8B5A34',5)+'<circle cx="94" cy="146" r="8" fill="url(#sk)"/>'+box(158,136,84,88))
X('nang','nâng','to lift', shadow(128,60)+mini(128,228,1.3,'bl','flat','up')+box(84,24,88,50))
X('roi','rơi','to fall, to drop', shadow(128,70)+'<rect x="26" y="20" width="204" height="14" rx="7" fill="#8B5A34"/><ellipse cx="80" cy="30" rx="58" ry="26" fill="#4CC9A0"/><ellipse cx="180" cy="26" rx="62" ry="24" fill="#3DB58D"/>'+stroke('M128 58 v36','#B9C6E0',6)+stroke('M108 70 v24','#B9C6E0',5)+stroke('M148 70 v24','#B9C6E0',5)+apple(128,140,1.7))
X('xephang','xếp hàng','to queue', shadow(120,110)+mini(48,226,.95,'gr','flat','stand')+mini(104,226,.95,'or','smile','stand','long')+mini(160,226,.95,'bl','flat','stand')+'<rect x="204" y="150" width="44" height="76" rx="6" fill="#E9EEF8"/><rect x="198" y="140" width="56" height="16" rx="7" fill="url(#pu)"/>')
X('hop','họp','meeting', shadow(128,110)+mini(60,196,.85,'bl','smile','stand')+mini(128,190,.85,'pk','open','stand','long')+mini(196,196,.85,'gr','smile','stand')+'<path d="M28 176 h200 q10 0 10 10 v8 H18 v-8 q0 -10 10 -10z" fill="#C48A50"/><rect x="40" y="194" width="14" height="36" rx="5" fill="#A66E3A"/><rect x="202" y="194" width="14" height="36" rx="5" fill="#A66E3A"/><rect x="100" y="162" width="56" height="16" rx="3" fill="#fff" stroke="#C9D4EA" stroke-width="2"/>')

import sys
out=sys.argv[1]
for k,(vi,en,body) in D.items(): open(os.path.join(out,'w-'+k+'.svg'),'w',encoding='utf8').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'+DEFS+body+'</svg>')
html='<body style="margin:0;background:#F4F6FD;font-family:Arial"><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;padding:14px;width:1000px">'
for k,(vi,en,body) in D.items(): html+='<div style="background:#fff;border-radius:18px;padding:8px;text-align:center;box-shadow:0 2px 0 #D9E0F0"><img src="w-%s.svg" width="150" height="150"><div style="font-weight:800;font-size:20px;color:#2F6BE0">%s</div><div style="color:#6B7896;font-size:13px">%s</div></div>'%(k,vi,en)
open(os.path.join(out,'sheet.html'),'w',encoding='utf8').write(html+'</div></body>')
print(len(D),'drawings')
