#!/usr/bin/env python3
# v77 · Drawn Saigon places (our own cartoon drawings, not photos and not traced from one).
#   python3 src/art/sg.py .      → writes data/sgart.json  {"art": {Vietnamese name: svg string}}
# Each drawing is a 320×200 SVG. Moving parts carry a class (z77cl cloud, z77fl flag, z77bt boat, z77bk blink, z77pl plane,
# z77sw sway, z77rd rider, z77wv water) that src/v7/v7.css animates. With "reduce motion" on they simply stand still.
import sys, os, json
OUT = {}
def sky(a, b, uid): return '<defs><linearGradient id="g%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs><rect width="320" height="200" fill="url(#g%s)"/>' % (uid, a, b, uid)
def cloud(x, y, s=1, o=.95, slow=''): return '<g class="z77cl%s" opacity="%s"><g transform="translate(%s %s) scale(%s)"><ellipse cx="0" cy="0" rx="22" ry="9" fill="#fff"/><ellipse cx="-10" cy="-6" rx="11" ry="8" fill="#fff"/><ellipse cx="7" cy="-8" rx="13" ry="10" fill="#fff"/></g></g>' % (slow, o, x, y, s)
def sun(x, y, c='#FFD75E'): return '<circle class="z77sn" cx="%s" cy="%s" r="16" fill="%s"/><circle cx="%s" cy="%s" r="24" fill="%s" opacity=".25"/>' % (x, y, c, x, y, c)
def flag(x, y, h=26): return '<path d="M%s %s v-%s" stroke="#7A6A55" stroke-width="2" stroke-linecap="round"/><g class="z77fl" style="transform-origin:%spx %spx"><rect x="%s" y="%s" width="20" height="13" rx="1.5" fill="#DA251D"/><path d="M%s %s l1.6 3.4 3.7 .3 -2.8 2.4 .9 3.6 -3.4 -2 -3.4 2 .9 -3.6 -2.8 -2.4 3.7 -.3z" fill="#FFDD00" transform="scale(.62)" style="transform-origin:%spx %spx"/></g>' % (x, y, h, x, y - h, x, y - h, x + 10, y - h + 2.2, x + 10, y - h + 6.5)
def arch(x, y, w, h, fill): return '<path d="M%s %s v-%s a%s %s 0 0 1 %s 0 v%s z" fill="%s"/>' % (x, y, h - w / 2, w / 2, w / 2, w, h - w / 2, fill)
def tree(x, y, s=1, c='#2E9E6B'): return '<g transform="translate(%s %s) scale(%s)"><rect x="-2" y="-14" width="4" height="14" rx="1" fill="#7A5236"/><g class="z77sw" style="transform-origin:0 -14px"><circle cx="0" cy="-24" r="13" fill="%s"/><circle cx="-8" cy="-18" r="9" fill="%s"/><circle cx="8" cy="-18" r="9" fill="%s"/><circle cx="-3" cy="-28" r="5" fill="#fff" opacity=".18"/></g></g>' % (x, y, s, c, c, c)
def palm(x, y, s=1): return '<g transform="translate(%s %s) scale(%s)"><path d="M0 0 q-3 -22 2 -40" stroke="#8A5A3A" stroke-width="4" fill="none" stroke-linecap="round"/><g class="z77sw" style="transform-origin:2px -40px" stroke="#2E9E6B" stroke-width="5" fill="none" stroke-linecap="round"><path d="M2 -40 q-14 -8 -22 2"/><path d="M2 -40 q14 -8 22 2"/><path d="M2 -40 q-8 -14 -18 -12"/><path d="M2 -40 q8 -14 18 -12"/><path d="M2 -40 q0 -14 2 -18"/></g></g>' % (x, y, s)
def bike(y, c='#E2434B', d=''): return '<g class="z77rd%s"><g transform="translate(0 %s)"><circle cx="-9" cy="0" r="5" fill="#2B2233"/><circle cx="11" cy="0" r="5" fill="#2B2233"/><circle cx="-9" cy="0" r="2" fill="#C9CFDA"/><circle cx="11" cy="0" r="2" fill="#C9CFDA"/><path d="M-11 -3 h14 l5 -9 h4 l2 9" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/><rect x="-10" y="-9" width="11" height="4" rx="2" fill="#2B2233"/><path d="M-3 -9 v-9 l7 3" stroke="#3B4A7A" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="-3" cy="-22" r="4.2" fill="#F1C7A3"/><path d="M-7.6 -22.5 a4.6 4.6 0 0 1 9.2 0 z" fill="#FFC83D"/></g></g>' % (d, y, c, c)
def road(y=176, c='#59607A'): return '<rect x="0" y="%s" width="320" height="%s" fill="%s"/><path d="M0 %s h320" stroke="#fff" stroke-width="2" stroke-dasharray="14 12" opacity=".55"/>' % (y, 200 - y, c, y + 13)
def wrap(k, body, label): OUT[k] = '<svg viewBox="0 0 320 200" role="img" aria-label="%s">%s</svg>' % (label, body)
def wins(x0, y, n, dx, w, h, fill, fn=None):
    return ''.join((fn or (lambda x: '<rect x="%s" y="%s" width="%s" height="%s" rx="1.5" fill="%s"/>' % (x, y, w, h, fill)))(x0 + i * dx) for i in range(n))

# 1 · Chợ Bến Thành
b = sky('#8FD3FF', '#E8F7FF', 'a') + sun(270, 40) + cloud(60, 38) + cloud(190, 26, .7, .8, ' s2')
b += '<rect x="14" y="118" width="292" height="58" fill="#F6E7C8"/><path d="M8 118 h304 l-14 -22 h-276z" fill="#C8553D"/><path d="M22 96 h276" stroke="#A8402C" stroke-width="2"/>'
b += wins(26, 132, 4, 26, 16, 30, '#7A5236', lambda x: arch(x, 176, 18, 40, '#8A5E3C')) + wins(206, 132, 4, 26, 16, 30, '#7A5236', lambda x: arch(x, 176, 18, 40, '#8A5E3C'))
b += '<rect x="132" y="62" width="56" height="114" fill="#FBF0D6"/><path d="M126 62 h68 l-10 -16 h-48z" fill="#C8553D"/><rect x="150" y="34" width="20" height="14" fill="#FBF0D6"/><path d="M146 34 h28 l-14 -12z" fill="#C8553D"/>'
b += '<circle cx="160" cy="84" r="13" fill="#fff" stroke="#7A5236" stroke-width="2.5"/><g class="z77ck" style="transform-origin:160px 84px"><path d="M160 84 v-8" stroke="#2B2233" stroke-width="2" stroke-linecap="round"/></g><path d="M160 84 h6" stroke="#2B2233" stroke-width="2" stroke-linecap="round"/>'
b += arch(144, 176, 32, 62, '#6E4A2E') + '<rect x="120" y="102" width="80" height="13" rx="3" fill="#1F6FD6"/><text x="160" y="112" text-anchor="middle" font-size="8.5" font-weight="900" fill="#fff" font-family="system-ui,sans-serif">CHỢ BẾN THÀNH</text>'
b += road() + bike(170) + bike(190, '#2F7BF6', ' r')
wrap('Chợ Bến Thành', b, 'Drawing of Bến Thành Market')

# 2 · Nhà thờ Đức Bà
b = sky('#9AD8FF', '#EAF8FF', 'b') + cloud(50, 50, .9) + cloud(270, 34, .7, .85, ' s2')
def tower(x): return '<rect x="%s" y="70" width="40" height="106" fill="#C0553F"/><path d="M%s 70 h48 l-24 -56z" fill="#EDEFF3"/><path d="M%s 14 v-10 M%s 8 h8" stroke="#8A8F9C" stroke-width="2"/>' % (x, x - 4, x + 20, x + 16) + arch(x + 12, 112, 16, 30, '#5B2C22') + arch(x + 12, 152, 16, 26, '#5B2C22') + '<path d="M%s 70 h40" stroke="#9E3F2D" stroke-width="3"/>' % x
b += tower(88) + tower(192) + '<rect x="128" y="96" width="64" height="80" fill="#CC6048"/><path d="M124 96 h72 l-36 -30z" fill="#B24A36"/>'
b += '<circle cx="160" cy="110" r="12" fill="#FFF3D0" stroke="#5B2C22" stroke-width="3"/><path d="M160 98 v24 M148 110 h24 M152 102 l16 16 M168 102 l-16 16" stroke="#5B2C22" stroke-width="1.2"/>' + arch(146, 176, 28, 46, '#5B2C22')
b += '<rect x="0" y="176" width="320" height="24" fill="#8FCF8A"/><rect x="120" y="176" width="80" height="24" fill="#D9D2C4"/>' + tree(40, 180, 1.2) + tree(282, 180, 1.2)
b += '<g class="z77bd"><path d="M20 60 q4 -5 8 0 q4 -5 8 0" fill="none" stroke="#3B4A7A" stroke-width="2" stroke-linecap="round"/><path d="M44 48 q3 -4 6 0 q3 -4 6 0" fill="none" stroke="#3B4A7A" stroke-width="1.6" stroke-linecap="round"/></g>'
wrap('Nhà thờ Đức Bà', b, 'Drawing of Notre-Dame Cathedral of Saigon')

# 3 · Bưu điện Thành phố
b = sky('#8FD3FF', '#F2FAFF', 'c') + sun(52, 40) + cloud(250, 40, .9)
b += '<rect x="20" y="92" width="280" height="84" fill="#F7C948"/><rect x="20" y="86" width="280" height="8" fill="#fff"/><rect x="20" y="170" width="280" height="6" fill="#E3B02F"/>'
b += wins(32, 112, 4, 22, 14, 34, '#fff', lambda x: arch(x, 150, 14, 36, '#2F8F6B') + '<path d="M%s 126 h14 M%s 116 v34" stroke="#F7C948" stroke-width="1.5"/>' % (x, x + 7))
b += wins(214, 112, 4, 22, 14, 34, '#fff', lambda x: arch(x, 150, 14, 36, '#2F8F6B') + '<path d="M%s 126 h14 M%s 116 v34" stroke="#F7C948" stroke-width="1.5"/>' % (x, x + 7))
b += '<rect x="118" y="60" width="84" height="116" fill="#FAD35E"/><path d="M112 60 h96 l-12 -14 h-72z" fill="#fff"/><rect x="118" y="56" width="84" height="6" fill="#E3B02F"/>'
b += arch(132, 176, 56, 96, '#FFF4CC') + arch(140, 176, 40, 70, '#3A7D6A') + '<path d="M140 136 h40 M160 110 v66" stroke="#FFF4CC" stroke-width="2"/>'
b += '<circle cx="160" cy="96" r="10" fill="#fff" stroke="#7A5236" stroke-width="2.5"/><g class="z77ck" style="transform-origin:160px 96px"><path d="M160 96 v-6" stroke="#2B2233" stroke-width="2" stroke-linecap="round"/></g><path d="M160 96 h4.5" stroke="#2B2233" stroke-width="2" stroke-linecap="round"/>'
b += flag(160, 46, 24) + '<rect x="0" y="176" width="320" height="24" fill="#D9D2C4"/>' + tree(14, 182, 1.1) + tree(306, 182, 1.1) + bike(192, '#12A26E')
wrap('Bưu điện Thành phố', b, 'Drawing of the Saigon Central Post Office')

# 4 · Dinh Độc Lập
b = sky('#8FD3FF', '#F2FAFF', 'd') + cloud(60, 36) + cloud(250, 50, .8, .85, ' s2')
b += '<rect x="30" y="84" width="260" height="70" fill="#F4F1EA"/><rect x="24" y="78" width="272" height="9" fill="#fff"/><rect x="24" y="150" width="272" height="6" fill="#D8D2C4"/><rect x="42" y="92" width="236" height="52" fill="#5C6B8A"/>'
b += ''.join('<rect x="%s" y="90" width="5" height="56" rx="2" fill="#FBF9F4"/><circle cx="%s" cy="104" r="3.4" fill="#FBF9F4"/><circle cx="%s" cy="118" r="3.4" fill="#FBF9F4"/><circle cx="%s" cy="132" r="3.4" fill="#FBF9F4"/>' % (x, x + 2.5, x + 2.5, x + 2.5) for x in range(46, 276, 13))
b += '<rect x="118" y="66" width="84" height="14" fill="#F4F1EA"/><rect x="112" y="62" width="96" height="6" fill="#fff"/><rect x="136" y="120" width="48" height="34" fill="#39445E"/>' + flag(160, 62, 30)
b += '<rect x="0" y="154" width="320" height="46" fill="#7CC97A"/><ellipse cx="160" cy="180" rx="62" ry="15" fill="#69B867"/><ellipse cx="160" cy="180" rx="26" ry="7" fill="#9EDBFF"/><g class="z77ft"><path d="M160 180 v-16 M160 166 q-7 -4 -10 6 M160 166 q7 -4 10 6" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/></g>'
b += tree(22, 168, 1.3) + tree(298, 168, 1.3) + '<path d="M0 154 h320" stroke="#3E4658" stroke-width="2" stroke-dasharray="2 6"/>'
wrap('Dinh Độc Lập', b, 'Drawing of Independence Palace')

# 5 · Landmark 81
b = sky('#3B4FA0', '#FFB37A', 'e') + '<circle cx="250" cy="120" r="26" fill="#FFD9A0" opacity=".9"/>' + cloud(70, 60, .9, .5) + cloud(260, 44, .6, .4, ' s2')
b += ''.join('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (x, 150 - h, w, h, c) for x, w, h, c in [(8, 26, 44, '#32407F'), (38, 20, 62, '#2A3670'), (60, 30, 36, '#3A4A8E'), (212, 24, 54, '#2A3670'), (238, 30, 38, '#32407F'), (272, 22, 70, '#2A3670'), (296, 24, 30, '#3A4A8E')])
b += ''.join('<rect x="%s" y="%s" width="3" height="3" fill="#FFE39A" class="z77bk%s"/>' % (x, y, ' d' + str(i % 3)) for i, (x, y) in enumerate([(14, 116), (22, 126), (44, 98), (50, 120), (68, 124), (78, 130), (218, 106), (226, 124), (246, 122), (278, 90), (284, 112), (302, 130), (278, 132)]))
for x, w, top in [(136, 48, 96), (142, 36, 66), (148, 24, 40), (154, 12, 22)]: b += '<rect x="%s" y="%s" width="%s" height="%s" fill="#7FB6F2"/><rect x="%s" y="%s" width="%s" height="%s" fill="#A8D1FA"/>' % (x, top, w, 150 - top, x, top, w / 3.0, 150 - top)
b += ''.join('<path d="M136 %s h48" stroke="#5C93D6" stroke-width="1" opacity=".7"/>' % y for y in range(102, 150, 8)) + '<path d="M160 22 v-14" stroke="#DCE8FF" stroke-width="2.5" stroke-linecap="round"/><circle class="z77bk" cx="160" cy="7" r="3" fill="#FF5A5A"/>'
b += '<rect x="0" y="150" width="320" height="50" fill="#2C4A9A"/><path class="z77wv" d="M-40 164 q10 -4 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0" stroke="#7FA2E8" stroke-width="2" fill="none" opacity=".7"/><path class="z77wv b" d="M-40 182 q10 -4 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0" stroke="#7FA2E8" stroke-width="2" fill="none" opacity=".5"/><rect x="150" y="152" width="20" height="40" fill="#A8D1FA" opacity=".25"/>'
wrap('Landmark 81', b, 'Drawing of the Landmark 81 tower')

# 6 · Phố đi bộ Nguyễn Huệ
b = sky('#8FD3FF', '#F2FAFF', 'f') + cloud(60, 30, .8) + cloud(260, 36, .7, .85, ' s2')
b += '<rect x="112" y="70" width="96" height="46" fill="#F9DB7A"/><rect x="108" y="66" width="104" height="6" fill="#fff"/><path d="M146 66 h28 l-4 -14 h-20z" fill="#F9DB7A"/><path d="M150 52 h20 l-10 -22z" fill="#7C8AA5"/>' + wins(118, 84, 6, 15, 8, 20, '#fff', lambda x: arch(x, 108, 9, 22, '#7A5236')) + flag(160, 30, 16)
b += '<path d="M0 200 L112 116 H208 L320 200z" fill="#E7E0D2"/><path d="M60 200 L138 116 H182 L260 200z" fill="#F4EFE4"/><path d="M160 116 V200" stroke="#D5CCB9" stroke-width="2" stroke-dasharray="8 8"/>'
b += '<path d="M0 116 H112 L0 200z" fill="#B9C3D6"/><path d="M320 116 H208 L320 200z" fill="#B9C3D6"/><rect x="0" y="60" width="60" height="70" fill="#9FB0CC"/><rect x="260" y="50" width="60" height="80" fill="#9FB0CC"/>' + wins(8, 70, 3, 16, 9, 12, '#DCE8FF') + wins(268, 62, 3, 16, 9, 12, '#DCE8FF') + wins(8, 92, 3, 16, 9, 12, '#DCE8FF') + wins(268, 86, 3, 16, 9, 12, '#DCE8FF')
b += tree(98, 132, .7) + tree(222, 132, .7) + tree(70, 156, 1) + tree(250, 156, 1) + tree(34, 190, 1.4) + tree(286, 190, 1.4)
b += '<ellipse cx="160" cy="150" rx="20" ry="6" fill="#9EDBFF"/><g class="z77ft"><path d="M160 150 v-14 M160 138 q-6 -3 -9 5 M160 138 q6 -3 9 5" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/></g>'
b += ''.join('<g class="z77wk%s"><circle cx="%s" cy="%s" r="3" fill="#F1C7A3"/><rect x="%s" y="%s" width="5" height="9" rx="2" fill="%s"/></g>' % (' b' if i % 2 else '', x, y, x - 2.5, y + 3, c) for i, (x, y, c) in enumerate([(128, 168, '#E2434B'), (196, 176, '#2F7BF6'), (144, 184, '#12A26E'), (184, 160, '#FF8A1F')]))
wrap('Phố đi bộ Nguyễn Huệ', b, 'Drawing of Nguyễn Huệ walking street')

# 7 · Nhà hát Thành phố
b = sky('#FFC9A8', '#FFF1DC', 'h') + sun(266, 52, '#FFB14A') + cloud(60, 40, .9, .8)
b += '<rect x="46" y="96" width="228" height="76" fill="#F6ECDA"/><rect x="40" y="90" width="240" height="8" fill="#fff"/><path d="M96 90 q64 -70 128 0z" fill="#EADBC0"/><path d="M110 90 q50 -52 100 0z" fill="#FBF4E6"/>'
b += arch(122, 172, 76, 96, '#C9B48E') + arch(130, 172, 60, 84, '#5E4A3A') + '<path d="M130 132 h60 M160 96 v76 M145 100 v72 M175 100 v72" stroke="#C9B48E" stroke-width="1.6"/>'
b += wins(56, 112, 3, 22, 12, 36, '#fff', lambda x: arch(x, 150, 13, 34, '#8A6F52')) + wins(210, 112, 3, 22, 12, 36, '#fff', lambda x: arch(x, 150, 13, 34, '#8A6F52'))
b += '<circle cx="110" cy="84" r="5" fill="#fff"/><rect x="106" y="86" width="8" height="10" rx="3" fill="#fff"/><circle cx="210" cy="84" r="5" fill="#fff"/><rect x="206" y="86" width="8" height="10" rx="3" fill="#fff"/>'
b += '<path d="M30 172 h260 v6 h-266 z M22 178 h276 v6 h-282z" fill="#E3D6BD"/><rect x="0" y="184" width="320" height="16" fill="#C9BFAE"/>' + palm(24, 184, .9) + palm(296, 184, .9)
b += '<g class="z77nt"><text x="74" y="70" font-size="16" fill="#B4472E">♪</text></g><g class="z77nt b"><text x="236" y="76" font-size="13" fill="#B4472E">♫</text></g>'
wrap('Nhà hát Thành phố', b, 'Drawing of the Saigon Opera House')

# 8 · Nhà thờ Tân Định
b = sky('#8FD3FF', '#FDEFF5', 'i') + cloud(84, 60, .9) + cloud(262, 30, .7, .85, ' s2') + sun(40, 34)
P, PD, W = '#F58FB0', '#D96A90', '#fff'
b += '<rect x="96" y="112" width="128" height="64" fill="%s"/><path d="M92 112 h136 l-20 -18 h-96z" fill="%s"/>' % (P, PD)
b += '<rect x="138" y="58" width="44" height="118" fill="%s"/><path d="M134 58 h52 l-26 -50z" fill="%s"/><path d="M160 8 v-8 M156 3 h8" stroke="#8A8F9C" stroke-width="2"/><path d="M138 58 h44 M138 92 h44" stroke="%s" stroke-width="3"/>' % (P, PD, W)
for x in (102, 206): b += '<rect x="%s" y="90" width="12" height="24" fill="%s"/><path d="M%s 90 h16 l-8 -22z" fill="%s"/>' % (x, P, x - 2, PD)
b += arch(151, 86, 18, 22, W) + arch(153, 86, 14, 18, '#7A3550') + '<circle cx="160" cy="106" r="8" fill="%s" stroke="#7A3550" stroke-width="2.5"/>' % W + arch(146, 176, 28, 44, W) + arch(150, 176, 20, 38, '#7A3550')
b += wins(106, 130, 2, 18, 10, 26, W, lambda x: arch(x, 160, 11, 28, W) + arch(x + 2, 160, 7, 24, '#7A3550')) + wins(186, 130, 2, 18, 10, 26, W, lambda x: arch(x, 160, 11, 28, W) + arch(x + 2, 160, 7, 24, '#7A3550'))
b += '<rect x="0" y="176" width="320" height="24" fill="#D9D2C4"/>' + tree(50, 182, 1.2) + tree(270, 182, 1.2) + bike(192, '#7A54E8')
wrap('Nhà thờ Tân Định', b, 'Drawing of the pink Tân Định Church')

# 9 · Chợ Lớn
b = sky('#FFC08A', '#FFEFD6', 'j') + '<rect x="0" y="70" width="80" height="106" fill="#E8B96A"/><rect x="240" y="60" width="80" height="116" fill="#D99A5B"/>' + wins(10, 84, 3, 22, 14, 20, '#7A5236') + wins(250, 76, 3, 22, 14, 20, '#7A5236') + wins(10, 116, 3, 22, 14, 20, '#7A5236') + wins(250, 110, 3, 22, 14, 20, '#7A5236')
b += '<rect x="96" y="92" width="12" height="84" fill="#C8372D"/><rect x="212" y="92" width="12" height="84" fill="#C8372D"/><rect x="88" y="80" width="144" height="14" fill="#C8372D"/>'
b += '<path d="M70 80 q10 -4 18 -16 h144 q8 12 18 16z" fill="#2F8F6B"/><path d="M92 62 q8 -3 14 -14 h108 q6 11 14 14z" fill="#37A37B"/><rect x="104" y="64" width="112" height="16" fill="#FFD75E"/><text x="160" y="76.500" text-anchor="middle" font-size="10" font-weight="900" fill="#C8372D" font-family="system-ui,sans-serif">CHỢ LỚN</text>'
def lan(x, y, d=''): return '<g class="z77ln%s" style="transform-origin:%spx %spx"><path d="M%s %s v8" stroke="#7A5236" stroke-width="1.5"/><ellipse cx="%s" cy="%s" rx="8" ry="10" fill="#E2332B"/><path d="M%s %s v20" stroke="#FFD75E" stroke-width="1.2" opacity=".8"/><rect x="%s" y="%s" width="8" height="3" fill="#FFD75E"/><path d="M%s %s v7" stroke="#FFD75E" stroke-width="2"/></g>' % (d, x, y, x, y, x, y + 18, x, y + 8, x - 4, y + 6.5, x, y + 28)
b += lan(126, 94) + lan(160, 94, ' b') + lan(194, 94) + '<rect x="0" y="176" width="320" height="24" fill="#8C7B6B"/>' + bike(186, '#E2434B') + bike(196, '#2F7BF6', ' r')
wrap('Chợ Lớn', b, 'Drawing of a gate with red lanterns in Chợ Lớn')

# 10 · sông Sài Gòn
b = sky('#FF9E7A', '#FFE2B8', 'k') + '<circle cx="160" cy="112" r="30" fill="#FFF0C2"/>' + cloud(60, 40, 1, .6) + cloud(250, 30, .8, .5, ' s2')
b += ''.join('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (x, 120 - h, w, h, c) for x, w, h, c in [(0, 24, 30, '#7A5C8E'), (26, 18, 50, '#6A4E82'), (46, 26, 36, '#7A5C8E'), (76, 14, 76, '#5E4477'), (92, 24, 44, '#6A4E82'), (200, 22, 40, '#6A4E82'), (224, 16, 64, '#5E4477'), (242, 28, 34, '#7A5C8E'), (272, 20, 54, '#6A4E82'), (294, 26, 28, '#7A5C8E')])
b += '<path d="M83 44 l-4 -12" stroke="#5E4477" stroke-width="2"/><rect x="0" y="120" width="320" height="80" fill="#3F7FBF"/><rect x="120" y="120" width="80" height="80" fill="#FFE2B8" opacity=".22"/>'
W1 = 'q10 -4 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0'
b += '<path class="z77wv" d="M-40 136 %s" stroke="#BFE0FF" stroke-width="2" fill="none" opacity=".7"/><path class="z77wv b" d="M-40 158 %s" stroke="#BFE0FF" stroke-width="2" fill="none" opacity=".55"/><path class="z77wv" d="M-40 184 %s" stroke="#BFE0FF" stroke-width="2.4" fill="none" opacity=".5"/>' % (W1, W1, W1)
b += '<g class="z77bt"><g transform="translate(0 150)"><path d="M-34 0 h68 l-10 14 h-48z" fill="#fff"/><path d="M-34 0 h68" stroke="#E2434B" stroke-width="4"/><rect x="-20" y="-14" width="36" height="14" rx="2" fill="#FBF4E6"/><rect x="-15" y="-10" width="6" height="6" fill="#3F7FBF"/><rect x="-5" y="-10" width="6" height="6" fill="#3F7FBF"/><rect x="5" y="-10" width="6" height="6" fill="#3F7FBF"/><rect x="-2" y="-24" width="7" height="10" fill="#E2434B"/></g></g>'
wrap('sông Sài Gòn', b, 'Drawing of the Saigon River at sunset')

# 11 · Bùi Viện
b = sky('#1B1F4B', '#4A2B7A', 'l') + ''.join('<circle class="z77bk d%s" cx="%s" cy="%s" r="1.2" fill="#fff"/>' % (i % 3, x, y) for i, (x, y) in enumerate([(30, 20), (90, 12), (150, 26), (210, 10), (280, 22), (250, 40), (60, 44)]))
b += '<path d="M0 60 H110 L130 176 H0z" fill="#2B2F66"/><path d="M320 50 H210 L190 176 H320z" fill="#2B2F66"/><path d="M130 176 L150 96 h20 L190 176z" fill="#3B3F7A"/><rect x="0" y="176" width="320" height="24" fill="#23264F"/>'
def neon(x, y, w, c, t, d=''): return '<g class="z77bk%s"><rect x="%s" y="%s" width="%s" height="18" rx="5" fill="none" stroke="%s" stroke-width="2.5"/><text x="%s" y="%s" text-anchor="middle" font-size="10" font-weight="900" fill="%s" font-family="system-ui,sans-serif">%s</text></g>' % (d, x, y, w, c, x + w / 2.0, y + 13, c, t)
b += neon(10, 72, 58, '#FF5AC8', 'BIA HƠI') + neon(44, 104, 52, '#5AF0FF', 'CÀ PHÊ', ' d1') + neon(238, 66, 66, '#FFE24A', 'BÙI VIỆN', ' d2') + neon(226, 100, 52, '#7CFF8A', 'PHỞ', ' d1') + neon(16, 138, 44, '#FFE24A', 'BAR', ' d2') + neon(246, 134, 64, '#FF5AC8', 'KARAOKE')
b += '<path d="M110 70 Q160 84 210 62" stroke="#8A8FC0" stroke-width="1" fill="none"/>' + ''.join('<circle class="z77bk d%s" cx="%s" cy="%s" r="3" fill="%s"/>' % (i % 3, x, y, c) for i, (x, y, c) in enumerate([(122, 73, '#FF5AC8'), (138, 76, '#FFE24A'), (154, 77, '#5AF0FF'), (170, 76, '#7CFF8A'), (186, 72, '#FF5AC8'), (200, 67, '#FFE24A')]))
for x in (92, 228): b += '<ellipse cx="%s" cy="182" rx="15" ry="4" fill="#C8372D"/><rect x="%s" y="182" width="2" height="10" fill="#8A8FC0"/><rect x="%s" y="174" width="5" height="7" rx="1" fill="#FFC83D"/><rect x="%s" y="173" width="5" height="2" fill="#fff"/>' % (x, x - 1, x - 6, x - 6)
b += bike(190, '#FF5AC8')
wrap('Bùi Viện', b, 'Drawing of Bùi Viện street at night with neon signs')

# 12 · sân bay Tân Sơn Nhất
b = sky('#7CC8FF', '#EAF7FF', 'm') + sun(48, 44) + cloud(110, 60, 1) + cloud(260, 80, .8, .85, ' s2')
b += '<rect x="20" y="126" width="200" height="40" fill="#EEF2F8"/><path d="M14 126 q106 -30 212 0z" fill="#C9D6EA"/>' + wins(30, 134, 9, 21, 14, 22, '#7FB6F2') + '<rect x="56" y="110" width="128" height="12" rx="3" fill="#1F6FD6"/><text x="120" y="119.500" text-anchor="middle" font-size="8.5" font-weight="900" fill="#fff" font-family="system-ui,sans-serif">TÂN SƠN NHẤT</text>'
b += '<rect x="262" y="84" width="12" height="82" fill="#DCE3EE"/><path d="M252 84 h32 l-4 -16 h-24z" fill="#7FB6F2"/><rect x="250" y="64" width="36" height="5" rx="2" fill="#C9D6EA"/><circle class="z77bk" cx="268" cy="60" r="2.5" fill="#FF5A5A"/>'
b += '<rect x="0" y="166" width="320" height="34" fill="#6B7285"/><path d="M0 184 h320" stroke="#fff" stroke-width="2.5" stroke-dasharray="20 14" opacity=".7"/>'
b += '<g class="z77pl"><g transform="rotate(-14)"><path d="M-30 0 q0 -6 8 -6 h38 q14 0 16 6 q-2 6 -16 6 h-38 q-8 0 -8 -6z" fill="#fff"/><path d="M-4 -4 l-12 -18 h8 l18 18z M-4 4 l-12 14 h8 l18 -14z" fill="#DCE3EE"/><path d="M-28 -4 l-6 -12 h6 l8 12z" fill="#E2434B"/><path d="M18 -3 h8" stroke="#7FB6F2" stroke-width="2.5" stroke-linecap="round"/><path d="M-18 -1 h28" stroke="#7FB6F2" stroke-width="1.5" stroke-dasharray="2 3"/></g></g>'
wrap('sân bay Tân Sơn Nhất', b, 'Drawing of Tân Sơn Nhất airport with a plane taking off')

repo = sys.argv[1] if len(sys.argv) > 1 else '.'
p = os.path.join(repo, 'data/sgart.json')
json.dump({'v': 1, 'note': 'Drawn Saigon places (v77). Our own drawings, made by src/art/sg.py. Not photos.', 'art': OUT}, open(p, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('drawings', len(OUT), '| size', round(os.path.getsize(p) / 1024.0, 1), 'KB')
