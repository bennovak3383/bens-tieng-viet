#!/usr/bin/env python3
# Word pictures from Microsoft's Fluent Emoji set (3D style, MIT licence).
#   python3 src/art/pics.py <path to a checkout of github.com/microsoft/fluentui-emoji> .
# A name written  custom:<name>  uses our own drawing src/art/custom/<name>.png instead (v77; first one: bàn = table).
# Reads src/art/pics_map.txt, copies each picture it names to img/p/<slug>.webp (256 px) and writes data/pics.json
# {map: {Vietnamese word: slug}, emo: {emoji: slug}, tile: {menu tile title: slug}}.  The checkout can be a sparse, blob-less clone: this script asks git for just the files it needs.
import sys, os, re, json, subprocess
from PIL import Image
src, repo = sys.argv[1], sys.argv[2]
SIZE = 256   # v77: was 160. 256 is the full size of the Fluent 3D pictures, so they stay sharp on phone screens
files = subprocess.run(['git','-C',src,'ls-tree','-r','--name-only','HEAD'],capture_output=True,text=True).stdout.split('\n')
by = {}
for f in files:
    m = re.match(r'assets/([^/]+)/(?:Default/)?3D/.+\.png$', f)
    if m: by.setdefault(m.group(1).lower(), f)
pairs, want, miss, tiles, custom = [], {}, [], {}, {}
for l in open(os.path.join(repo,'src/art/pics_map.txt'),encoding='utf8'):
    l = l.strip()
    if not l or l[0] == '#': continue
    vi, nm = [x.strip() for x in l.split('|')]
    if nm.lower().startswith('custom:'):                        # v77: our own drawing, src/art/custom/<name>.png (256 px, see-through background)
        cn = re.sub(r'[^a-z0-9]+','-',nm[7:].lower()).strip('-'); cf = os.path.join(repo,'src/art/custom',cn+'.png')
        if not os.path.exists(cf): miss.append(nm); continue
        slug = 'x-'+cn; custom[slug] = cf
        pairs.append((vi, slug)); continue
    f = by.get(nm.lower())
    if not f: miss.append(nm); continue
    slug = re.sub(r'[^a-z0-9]+','-',nm.lower()).strip('-')
    want[slug] = f
    if vi[0] == '=': tiles[vi[1:].strip().lower()] = slug      # a menu tile title, not a word
    else: pairs.append((vi, slug))
if miss: print('NOT FOUND:', sorted(set(miss)))
# the app's older content marks many cards and menu tiles with an emoji; give each of those the matching picture too (map "emo": emoji → slug)
emo = {}
try:
    import glob
    gl = {}
    for f in glob.glob(os.path.join(src,'assets/*/metadata.json')):
        try: md = json.load(open(f,encoding='utf8'))
        except Exception: continue
        g = (md.get('glyph') or '').replace('\ufe0f','')
        if g: gl[g] = os.path.basename(os.path.dirname(f))
    text = open(os.path.join(repo,'index.html'),encoding='utf8').read()
    for f in glob.glob(os.path.join(repo,'data/*.json')):
        if not f.endswith('pics.json'): text += open(f,encoding='utf8').read()
    text = text.replace('\ufe0f','')
    for g, nm in sorted(gl.items(), key=lambda x: -len(x[0])):
        if len(g) == 1 and ord(g) < 0x2190: continue          # plain characters (digits, #, *) are not pictures
        if g in text and nm.lower() in by:
            slug = re.sub(r'[^a-z0-9]+','-',nm.lower()).strip('-'); emo[g] = slug; want[slug] = by[nm.lower()]
except Exception as e: print('emoji pass skipped:', e)
need = [f for f in want.values() if not os.path.exists(os.path.join(src,f))]
if need:
    subprocess.run(['git','-C',src,'sparse-checkout','set','--no-cone','/LICENSE','/assets/*/metadata.json']+['/'+f for f in want.values()],check=True)
out = os.path.join(repo,'img/p'); os.makedirs(out,exist_ok=True); n = 0; total = 0
for slug, f in sorted(want.items()):
    dst = os.path.join(out, slug+'.webp')
    stale = False
    if os.path.exists(dst):
        try: stale = Image.open(dst).size[0] != SIZE
        except Exception: stale = True
    if stale or not os.path.exists(dst):
        im = Image.open(os.path.join(src,f)).convert('RGBA')
        if im.size != (SIZE,SIZE): im = im.resize((SIZE,SIZE), Image.LANCZOS)
        im.save(dst,'WEBP',quality=88,method=6); n += 1
    total += os.path.getsize(dst)
for slug, cf in sorted(custom.items()):
    dst = os.path.join(out, slug+'.webp'); im = Image.open(cf).convert('RGBA')
    if im.size != (SIZE,SIZE): im = im.resize((SIZE,SIZE), Image.LANCZOS)
    im.save(dst,'WEBP',quality=88,method=6); total += os.path.getsize(dst)
keep = set(want) | set(custom)
for f in os.listdir(out):
    if f.endswith('.webp') and f[:-5] not in keep: os.remove(os.path.join(out,f))
m = {}
for vi, slug in pairs: m[vi.lower()] = slug
# v83: pictures that are a symbol, a face or a hand sign, not a thing you can point at. In games a word with one of these shows its
# English meaning instead (z83Vague in v7.js), because "🧠 = to understand" or "⁉ = hả" is a riddle, not a hint.
vague = []; sym = []; kw = {}   # kw: what each picture shows, in the emoji set's own words (name + keywords). The app compares it with the word's English meaning.
try:
    grp = {}; used = set(m.values())|set(emo.values())
    for f in glob.glob(os.path.join(src,'assets/*/metadata.json')):
        md = json.load(open(f,encoding='utf8')); name = os.path.basename(os.path.dirname(f)); sl = re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-'); grp[sl] = md.get('group','')
        if sl in used: kw[sl] = ' '.join(sorted(set(re.findall(r'[a-z]{3,}',(' '.join(md.get('keywords',[]))+' '+md.get('cldr','')+' '+md.get('tts','')+' '+name).lower()))))
    HAND = re.compile(r'hand|finger|thumb|fist|clap|palm|pinch|victory|vulcan|wave|call-me|love-you|crossed|index-pointing|brain|speaking-head|bust|footprints|eyes?$|mouth|tongue|flexed')
    COLOUR = re.compile(r'-(circle|square)$|^(red|blue|green|yellow|orange|purple|brown|black|white)-')   # a coloured dot is a fine picture for a colour word
    for sl in sorted(set(m.values())|set(emo.values())):
        g = grp.get(sl,'')
        if COLOUR.search(sl): continue
        if g in ('Smileys & Emotion','Symbols','Flags') or (g=='People & Body' and HAND.search(sl)): vague.append(sl)
        if g=='Symbols': sym.append(sl)   # arrows, marks, signs: never a picture hint, whatever the keywords say
except Exception as e: print('vague list skipped:',e)
print('vague pictures',len(vague))
json.dump({'v':2,'note':'Pictures: Microsoft Fluent Emoji (MIT licence), see img/p/LICENSE.txt','map':m,'emo':emo,'tile':tiles,'vague':vague,'sym':sym,'kw':kw}, open(os.path.join(repo,'data/pics.json'),'w'), ensure_ascii=False, separators=(',',':'))
lic = os.path.join(src,'LICENSE')
if os.path.exists(lic): open(os.path.join(out,'LICENSE.txt'),'w').write('The pictures in this folder come from Fluent Emoji by Microsoft (https://github.com/microsoft/fluentui-emoji), resized.\n\n'+open(lic).read())
print('words',len(m),'| emoji',len(emo),'| tiles',len(tiles),'| pictures',len(want),'| new files',n,'| size %.1f MB'%(total/1e6))
