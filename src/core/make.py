# Builds data/core.json from src/core/*.txt (the core course: grammar units with their common words).
# Usage: python3 src/core/make.py REPO [FREQ_TSV]
#   FREQ_TSV (optional) = vn_word_frequencies.tsv from github.com/tabidots/vn-freqs, for the coverage report.
# It also checks "one new thing at a time": every sentence should use only words taught up to that unit.
import sys, re, json, glob, unicodedata, os
repo = sys.argv[1]
N = lambda s: unicodedata.normalize('NFC', s.strip())
units = []
for f in sorted(glob.glob(repo + '/src/core/*.txt')):
    u = None
    for ln, raw in enumerate(open(f, encoding='utf-8'), 1):
        line = N(raw)
        if not line or (line.startswith('#') and not line.startswith('##')): continue
        tag, rest = line[:2].strip(), line[2:].strip()
        p = [x.strip() for x in rest.split('|')]
        if tag == '##':
            assert len(p) == 5, (f, ln, line)
            u = {'id': p[0], 'lv': p[1], 'vi': p[2], 'en': p[3], 'key': [k.strip() for k in p[4].split(',') if k.strip()], 'how': [], 'ex': [], 'w': [], 'teach': '', 'tg': ''}
            units.append(u)
        elif tag == '?': u['how'].append(rest)
        elif tag == '=': assert len(p) == 2, (f, ln, line); u['ex'].append(p)
        elif tag == '+': assert len(p) == 4, (f, ln, line); u['w'].append(p)
        elif tag == 'T': u['teach'] = rest
        elif tag == 'C': u['tg'] = rest
        else: raise SystemExit('bad line %s:%d %s' % (f, ln, line))
ids = [u['id'] for u in units]; assert len(ids) == len(set(ids)), 'duplicate unit id'
seen = {}
for u in units:
    assert u['how'] and len(u['ex']) >= 4 and len(u['w']) >= 6 and u['teach'] and u['tg'], u['id']
    for w in u['w']:
        k = w[0].lower()
        if k in seen: print('NOTE word twice:', w[0], seen[k], u['id'])
        seen.setdefault(k, u['id'])
os.makedirs(repo + '/data', exist_ok=True)
json.dump({'v': 1, 'units': units}, open(repo + '/data/core.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
nw = sum(len(u['w']) for u in units); ns = sum(len(u['ex']) + len(u['w']) for u in units)
print('units', len(units), '| words', nw, '| sentences', ns)

# ---- one new thing at a time ----
def syl(s): return [x for x in re.sub(r'[“”"…·,.!?;:()/–—-]', ' ', N(s).lower()).split() if x]
base = set('ben lan nam mai tâm việt mỹ anh sài gòn huế hà nội một hai ba bốn năm sáu bảy tám chín mười'.split())
try:
    B = json.load(open(repo + '/data/beginner.json', encoding='utf-8'))
    for st in B['steps']:
        for sp in st['stops']:
            for it in sp.get('items', []): base.update(syl(it[0]))
except Exception as e: print('no beginner list', e)
known = set(base); bad = 0
for u in units:
    for w in u['w']: known.update(syl(w[0]))
    for vi, en in u['ex'] + [[w[2], w[3]] for w in u['w']]:
        miss = [x for x in syl(vi) if x not in known]
        if miss: bad += 1; print('  NEW-WORD CHECK', u['id'], '|', vi, '| not yet taught:', ', '.join(sorted(set(miss))))
print('sentences with a word not yet taught:', bad, 'of', ns)

# ---- coverage of the most common words ----
if len(sys.argv) > 2:
    fr = [N(l.split('\t')[2]).lower() for l in open(sys.argv[2], encoding='utf-8') if len(l.split('\t')) > 2]
    heads = set(seen)
    for n in (100, 300, 500, 1000): print('top %d: %d are core-course words' % (n, sum(1 for w in fr[:n] if w in heads)))
    other = set()
    try:
        page = open(repo + '/index.html', encoding='utf-8').read()
        C7 = json.loads(re.search(r'<script[^>]*id="content7"[^>]*>(.*?)</script>', page, re.S).group(1))
        other.update(N(c['vi']).lower() for c in C7['cards'] if c['c'] not in ('p75', 'say', 'pat'))
        for L in json.load(open(repo + '/data/words13.json', encoding='utf-8'))['levels']: other.update(N(c['vi']).lower() for c in L['cards'])
    except Exception as e: print('no other cards', e)
    top = [w for w in fr[:1000] if w in heads or w in other]
    print('top 1000 words that are a card somewhere in the app:', len(top))
    d = json.load(open(repo + '/data/core.json', encoding='utf-8')); d['top'] = top; d['topn'] = 1000
    json.dump(d, open(repo + '/data/core.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
