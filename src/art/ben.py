# Draws the "Ben" caricature and the two scenes that use him. Prints a JS snippet.
import math, json
INK='#1B1230'
def star(cx,cy,r,fill='#FFD23F'):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.42; pts.append('%.1f %.1f'%(cx+rr*math.cos(a),cy+rr*math.sin(a)))
    return '<path d="M'+' L'.join(pts)+' Z" fill="%s"/>'%fill
def flag(x,y,w,h,rot=0):
    return '<g transform="translate(%.1f %.1f) rotate(%.0f)"><path d="M0 0 h%.1f v%.1f l-%.1f -%.1f l-%.1f %.1f Z" fill="#E0263C" stroke="%s" stroke-width=".6"/>%s</g>'%(x,y,rot,w,h,w/2,h*0.28,w/2,h*0.28,INK,star(w/2,h*0.42,w*0.26))
def bunting(x1,y1,x2,y2,n,sag,w=11,h=12):
    out='<path d="M%.0f %.0f Q%.0f %.0f %.0f %.0f" fill="none" stroke="%s" stroke-width="1"/>'%(x1,y1,(x1+x2)/2,(y1+y2)/2+2*sag,x2,y2,INK)
    for i in range(n):
        t=(i+0.5)/n; x=(1-t)**2*x1+2*(1-t)*t*(x1+x2)/2+t*t*x2; y=(1-t)**2*y1+2*(1-t)*t*((y1+y2)/2+2*sag)+t*t*y2
        out+=flag(x-w/2,y,w,h,(-6 if i%2 else 5))
    return out
def ben(x,y,s,wave=True,stroke=INK):
    # origin at the feet; about 118 units tall before scaling. Tall, big grin, swept reddish-blond hair, stubble, black tee, backpack.
    st='stroke="%s" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"'%stroke
    arm_r=('<path d="M15 -84 q10 -4 16 -16 l3 -12" fill="none" stroke="#1F1F24" stroke-width="9" stroke-linecap="round"/><path d="M30 -99 l5 -15" fill="none" stroke="#F0BE98" stroke-width="7" stroke-linecap="round"/><circle cx="36" cy="-118" r="5.5" fill="#F0BE98" %s/><path d="M31.5 -108 l6 2" stroke="#15151A" stroke-width="2.6" stroke-linecap="round"/>'%st) if wave else ('<path d="M15 -84 q8 10 7 26" fill="none" stroke="#1F1F24" stroke-width="9" stroke-linecap="round"/><path d="M22 -58 l0 14" fill="none" stroke="#F0BE98" stroke-width="7" stroke-linecap="round"/><circle cx="22" cy="-41" r="5" fill="#F0BE98" %s/>'%st)
    g=f'''<g transform="translate({x} {y}) scale({s})">
<ellipse cx="2" cy="1" rx="26" ry="4" fill="#000" opacity=".28"/>
<path d="M-13 -50 L-15 -4 h11 L-2 -50 Z M2 -50 L7 -4 h11 L14 -50 Z" fill="#4A463F" {st}/>
<path d="M-19 -4 h15 v5 h-17 q-2 -4 2 -5 Z M5 -4 h15 q4 1 2 5 h-17 Z" fill="#B5622B" {st}/><path d="M-21 1 h17 M5 1 h17" stroke="#F6F1E7" stroke-width="1.6"/>
<path d="M-12 -96 q-10 6 -12 18 l-6 30" fill="none" stroke="#17171B" stroke-width="7" stroke-linecap="round"/>
<path d="M-18 -90 q18 -9 36 0 l-2 42 q-16 5 -32 0 Z" fill="#1F1F24" {st}/>
<path d="M-17 -84 q-9 10 -8 26" fill="none" stroke="#1F1F24" stroke-width="9" stroke-linecap="round"/><path d="M-25 -58 l-1 14" fill="none" stroke="#F0BE98" stroke-width="7" stroke-linecap="round"/><circle cx="-26" cy="-41" r="5" fill="#F0BE98" {st}/><path d="M-29 -50 h7" stroke="#8A5A32" stroke-width="2.2" stroke-linecap="round"/>
{arm_r}
<path d="M-6 -92 q8 -6 14 2" fill="none" stroke="#2C2C33" stroke-width="3" stroke-linecap="round"/>
<rect x="-5" y="-98" width="10" height="10" fill="#E8B48E"/>
<path d="M-13 -116 q0 -15 13 -15 q13 0 13 15 q0 13 -5 18 q-8 6 -16 0 q-5 -5 -5 -18 Z" fill="#F0BE98" {st}/>
<path d="M-12.5 -110 q1 10 4.5 13.5 q8 6 16 0 q3.5 -3.5 4.5 -13.5 q-3 9 -12.5 9 q-9.500 0 -12.5 -9 Z" fill="#B97A4E" opacity=".55"/>
<path d="M-14 -117 q-3 -15 9 -19 q10 -5 18 2 q5 5 2 15 q-3 -8 -9 -9 q-11 -2 -20 11 Z" fill="#C98A3F" {st}/>
<circle cx="-5" cy="-114" r="1.5" fill="{INK}"/><circle cx="5.500" cy="-114" r="1.5" fill="{INK}"/><path d="M-8 -118.500 h6 M3 -118.500 h6" stroke="#9A6A34" stroke-width="1.4" stroke-linecap="round"/>
<path d="M-6 -106 q6 7 12.500 0 Z" fill="#fff" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>
</g>'''
    return g.replace('\n','')
def tam(x,y,s,point=True):
    # Thầy Tâm: shorter, round friendly face, black side-swept hair, striped collared shirt, pointing like a teacher.
    st='stroke="%s" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"'%INK
    arm=('<path d="M15 -66 q10 -2 16 -12 l4 -8" fill="none" stroke="#D9D6EE" stroke-width="9" stroke-linecap="round"/><path d="M15 -66 q10 -2 16 -12 l4 -8" fill="none" stroke="#2D3A78" stroke-width="1.6" stroke-dasharray="1 4"/><circle cx="36" cy="-89" r="5" fill="#F3C9A2" %s/><path d="M38 -93 l4 -8" stroke="#F3C9A2" stroke-width="3.4" stroke-linecap="round"/>'%st) if point else ''
    g=f'''<g transform="translate({x} {y}) scale({s})">
<ellipse cx="1" cy="1" rx="24" ry="4" fill="#000" opacity=".28"/>
<path d="M-13 -40 L-14 -4 h11 L-2 -40 Z M2 -40 L6 -4 h11 L14 -40 Z" fill="#2B2D42" {st}/>
<path d="M-18 -4 h15 v5 h-17 q-2 -4 2 -5 Z M4 -4 h15 q4 1 2 5 h-17 Z" fill="#15151A" {st}/>
<path d="M-19 -72 q19 -8 38 0 l-2 36 q-17 5 -34 0 Z" fill="#D9D6EE" {st}/>
<path d="M-12 -74 V-38 M-6 -76 V-37 M6 -76 V-37 M12 -74 V-38" stroke="#2D3A78" stroke-width="2"/><path d="M0 -76 V-36" stroke="#8C7FC0" stroke-width="1.2"/>
<path d="M-18 -66 q-8 9 -7 22" fill="none" stroke="#D9D6EE" stroke-width="9" stroke-linecap="round"/><path d="M-25 -44 l0 8" fill="none" stroke="#F3C9A2" stroke-width="7" stroke-linecap="round"/><circle cx="-25" cy="-33" r="5" fill="#F3C9A2" {st}/>
{arm}
<path d="M-9 -77 l9 8 l9 -8 l-3 -5 h-12 Z" fill="#3C4A94" {st}/>
<rect x="-5" y="-84" width="10" height="8" fill="#EDBE95"/>
<path d="M-16 -100 q0 -17 16 -17 q16 0 16 17 q0 12 -6 17 q-10 6 -20 0 q-6 -5 -6 -17 Z" fill="#F3C9A2" {st}/>
<path d="M-16.500 -100 q-3 -19 12 -21 q12 -3 20 6 q3 5 1 14 q-3 -9 -8 -11 q-10 0 -17 -3 q-6 4 -8 15 Z" fill="#17161C" {st}/>
<circle cx="-6" cy="-99" r="1.6" fill="{INK}"/><circle cx="6" cy="-99" r="1.6" fill="{INK}"/><path d="M-9.500 -104 h7 M2.500 -104 h7" stroke="#17161C" stroke-width="1.5" stroke-linecap="round"/>
<path d="M-5 -90 q5 4 10 0" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/><circle cx="-10" cy="-93" r="2.600" fill="#F2A08A" opacity=".5"/><circle cx="10" cy="-93" r="2.600" fill="#F2A08A" opacity=".5"/>
</g>'''
    return g.replace('\n','')
def scooter(x,y,s):
    return f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"><circle cx="0" cy="-8" r="8" fill="#F6F1E7"/><circle cx="38" cy="-8" r="8" fill="#F6F1E7"/><path d="M12 -20 h22 q6 0 8 10 h-14 q-2 -6 -10 -6 h-6 Z" fill="#3A8C8C"/><rect x="14" y="-26" width="20" height="6" rx="3" fill="{INK}"/><path d="M4 -34 q-5 14 0 26 h6 q-3 -12 0 -26 Z" fill="#F6F1E7"/><path d="M0 -36 h10" stroke-width="2.4" stroke-linecap="round" fill="none"/></g>'
# overlay for the skyline header (viewBox 390x150)
ov=('<path d="M0 137 h390 v13 h-390 Z" fill="#231A45"/><path d="M0 137 h390" stroke="#F7B655" stroke-width="1.2" opacity=".8"/>'
    '<path d="M366 137 V70 q0 -8 -10 -8" fill="none" stroke="#0E0F33" stroke-width="2.4" stroke-linecap="round"/><circle cx="354" cy="63" r="3.4" fill="#FFE9A8"/><path d="M354 64 L318 137 H384 Z" fill="#FFE9A8" opacity=".20"/>'
    +bunting(-4,4,200,2,8,9)+bunting(190,2,394,6,8,9)+scooter(226,147,.62)+tam(296,146,.60)+ben(340,146,.60))
# welcome scene: the flag alley (viewBox 390x220)
al=('<svg viewBox="0 0 390 220" aria-hidden="true"><rect width="390" height="220" fill="#CFE6E8"/>'
 '<path d="M150 0 h90 v120 h-90 Z" fill="#E9F3EE"/><path d="M168 30 h54 v90 h-54 Z" fill="#B9D7CF"/>'
 '<path d="M0 0 H150 V132 L0 196 Z" fill="#E8B23A" stroke="#1B1230" stroke-width="1.6"/><path d="M390 0 H240 V132 L390 196 Z" fill="#F3DFA6" stroke="#1B1230" stroke-width="1.6"/>'
 '<path d="M0 196 L150 132 H240 L390 196 V220 H0 Z" fill="#9A958C" stroke="#1B1230" stroke-width="1.6"/><path d="M196 134 L214 220 M150 150 H240" stroke="#7F7A72" stroke-width="1.2" fill="none"/>'
 '<path d="M22 70 h40 v104 l-40 17 Z" fill="#1F5A45" stroke="#1B1230" stroke-width="1.6"/><path d="M42 70 V182 M22 100 h40 M22 132 h40" stroke="#0F3A2C" stroke-width="1.2"/>'
 '<path d="M86 60 h36 v50 h-36 Z" fill="#3A8C8C" stroke="#1B1230" stroke-width="1.6"/><path d="M104 60 v50 M86 76 h36 M86 92 h36" stroke="#CFE6E8" stroke-width="1"/>'
 '<path d="M300 52 h44 v62 h-44 Z" fill="#3A8C8C" stroke="#1B1230" stroke-width="1.6"/><path d="M322 52 v62 M300 72 h44 M300 92 h44" stroke="#CFE6E8" stroke-width="1"/>'
 '<path d="M262 74 h22 v54 h-22 Z" fill="#B5432B" stroke="#1B1230" stroke-width="1.6"/>'
 '<path d="M0 22 Q120 60 240 30 M60 0 Q150 46 300 8 M130 10 Q230 50 390 40" fill="none" stroke="#1B1230" stroke-width="1.4"/>'
 +bunting(-6,26,180,44,7,10,15,17)+bunting(170,46,396,22,8,10,15,17)+bunting(40,86,200,96,5,8,12,14)+bunting(196,96,372,80,6,8,12,14)
 +'<g transform="translate(300 176)" stroke="#1B1230" stroke-width="1.6" fill="none"><circle cx="0" cy="0" r="15"/><circle cx="42" cy="0" r="15"/><path d="M0 0 L16 -24 H36 L42 0 M16 -24 L24 0 H0 M32 -32 h10 M12 -30 h10"/></g>'
 +ben(182,214,1.42,True)+'</svg>')
av='<svg viewBox="-27 -127 54 54" aria-hidden="true"><defs><clipPath id="z21c"><circle cx="0" cy="-100" r="27"/></clipPath></defs><circle cx="0" cy="-100" r="27" fill="#FFC24A"/><g clip-path="url(#z21c)">'+tam(0,6,1.12,False)+'</g><circle cx="0" cy="-100" r="26" fill="none" stroke="#1B1230" stroke-width="2"/></svg>'
al=al.replace('</svg>',tam(92,212,1.3)+'</svg>')
print(json.dumps({'ov':ov,'alley':al,'av':av},ensure_ascii=False))
