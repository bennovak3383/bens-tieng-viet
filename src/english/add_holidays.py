# Adds the Holidays decks (src/english/holidays.py) to english/index.html. Safe to run once; refuses to run twice.
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__));from holidays import DECKS
p='english/index.html';s=open(p,encoding='utf-8').read()
assert '"id": "xmas"' not in s,'already added'
packs=[dict(id=d['id'],g='hol',t=d['t'],d=d['d'],art='h-'+d['id'],w=d['w']) for d in DECKS]
anchor='(()=>{const seen={};PACKS.forEach'
assert s.count(anchor)==1
s=s.replace(anchor,'/* ---------- Holidays (Nov 2026): Christmas, Thanksgiving, Valentine\'s, Halloween, New Year\'s ---------- */\nPACKS.push(...'+json.dumps(packs,ensure_ascii=False)+');\n'+anchor)
old="const GROUPS=[['rel','Relationships'],"
assert s.count(old)==1;s=s.replace(old,"const GROUPS=[['rel','Relationships'],['hol','Holidays'],")
old='const GOF={'
assert s.count(old)==1;s=s.replace(old,'const GOF={'+''.join('"%s": "hol", '%d['id'] for d in DECKS))
old='const HOMEART={'
assert s.count(old)==1;s=s.replace(old,'const HOMEART={'+''.join("%s:'h-%s',"%(d['id'],d['id']) for d in DECKS))
open(p,'w',encoding='utf-8').write(s);print('ok')
