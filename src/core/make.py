# Builds data/core.json from src/core/*.txt (the core course: grammar units with their common words).
# Usage: python3 src/core/make.py REPO [FREQ_TSV]
#   FREQ_TSV (optional) = vn_word_frequencies.tsv from github.com/tabidots/vn-freqs, for the coverage report.
# It also checks "one new thing at a time": every sentence should use only words taught up to that unit.
import sys, re, json, glob, unicodedata, os
repo = sys.argv[1]
N = lambda s: unicodedata.normalize('NFC', s.strip())
units = []
for f in sorted(glob.glob(repo + '/src/core/*.txt')):
    if f.endswith('stories.txt') or f.endswith('extra.txt') or f.endswith('street.txt'): continue
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
# 38: extra review sentences per unit (src/core/extra.txt: "## uid" then "& vi|en"), so the common words come back more often
byid = {u['id']: u for u in units}
for u in units: u['xs'] = []
# 41: "on the street" lines (src/core/street.txt: "## uid" then "~ street|course form|English|note"); not checked for untaught words on purpose
for u in units: u['street'] = []
sf2 = repo + '/src/core/street.txt'
if os.path.exists(sf2):
    cu = None
    for ln, raw in enumerate(open(sf2, encoding='utf-8'), 1):
        line = N(raw)
        if not line or (line.startswith('#') and not line.startswith('##')): continue
        if line.startswith('## '): cu = byid[line[3:].strip()]; continue
        assert line.startswith('~'), (sf2, ln); p = [x.strip() for x in line[1:].split('|')]; assert len(p) == 4, (sf2, ln, line); cu['street'].append(p)
print('street lines:', sum(len(u['street']) for u in units), '| units without one:', [u['id'] for u in units if not u['street']])
xf = repo + '/src/core/extra.txt'
if os.path.exists(xf):
    cu = None
    for ln, raw in enumerate(open(xf, encoding='utf-8'), 1):
        line = N(raw)
        if not line or (line.startswith('#') and not line.startswith('##')): continue
        if line.startswith('## '): cu = byid[line[3:].strip()]; continue
        assert line.startswith('&'), (xf, ln); p = [x.strip() for x in line[1:].split('|')]; assert len(p) == 2, (xf, ln); cu['xs'].append(p)
seen = {}
for u in units:
    assert u['how'] and len(u['ex']) >= 4 and len(u['w']) >= 6 and u['teach'] and u['tg'], u['id']
    for w in u['w']:
        k = w[0].lower()
        if k in seen: print('NOTE word twice:', w[0], seen[k], u['id'])
        seen.setdefault(k, u['id'])
os.makedirs(repo + '/data', exist_ok=True)
json.dump({'v': 1, 'units': units}, open(repo + '/data/core.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
nw = sum(len(u['w']) for u in units); ns = sum(len(u['ex']) + len(u['w']) + len(u['xs']) for u in units)
print('units', len(units), '| words', nw, '| sentences', ns)

# ---- one new thing at a time ----
def syl(s): return [x for x in re.sub(r'[“”"…·,.!?;:()/–—-]', ' ', N(s).lower()).split() if x]
base = set('ben lan nam mai tâm việt mỹ anh sài gòn huế hà nội một hai ba bốn năm sáu bảy tám chín mười mike úc'.split())
try:
    B = json.load(open(repo + '/data/beginner.json', encoding='utf-8'))
    for st in B['steps']:
        for sp in st['stops']:
            for it in sp.get('items', []): base.update(syl(it[0]))
except Exception as e: print('no beginner list', e)
known = set(base); bad = 0
for u in units:
    for w in u['w']: known.update(syl(w[0]))
    for vi, en in u['ex'] + [[w[2], w[3]] for w in u['w']] + u['xs']:
        miss = [x for x in syl(vi) if x not in known]
        if miss: bad += 1; print('  NEW-WORD CHECK', u['id'], '|', vi, '| not yet taught:', ', '.join(sorted(set(miss))))
print('sentences with a word not yet taught:', bad, 'of', ns)

# ---- 38: graded stories, one after every few units; only words taught so far, plus a few new words listed with "+" ----
known_at = []; k2 = set(base)
for u in units:
    for w in u['w']: k2.update(syl(w[0]))
    known_at.append(set(k2))
stories = []; sb = 0
sf = repo + '/src/core/stories.txt'
if os.path.exists(sf):
    st = None
    for ln, raw in enumerate(open(sf, encoding='utf-8'), 1):
        line = N(raw)
        if not line or (line.startswith('#') and not line.startswith('##')): continue
        tag, rest = line[:2].strip(), line[2:].strip(); p = [x.strip() for x in rest.split('|')]
        if tag == '##':
            assert len(p) == 4, (sf, ln); st = {'id': p[0], 'at': int(p[1]), 't': p[2], 'en': p[3], 'new': [], 'lines': [], 'qs': []}; stories.append(st); kn = set(known_at[st['at'] - 1])
        elif tag == '+': st['new'].append([p[0], p[1]]); kn.update(syl(p[0]))
        elif tag == '=': st['lines'].append({'vi': p[0], 'en': p[1]})
        elif tag == '?': st['qs'].append({'q': p[0], 'a': p[1], 'en': p[2]})
        else: raise SystemExit('bad story line %d' % ln)
        if tag in '=?':
            for vi in ([p[0]] if tag == '=' else [p[0], p[1]]):
                miss = [x for x in syl(vi) if x not in kn]
                if miss: sb += 1; print('  STORY CHECK', st['id'], '|', vi, '| not yet taught:', ', '.join(sorted(set(miss))))
    d = json.load(open(repo + '/data/core.json', encoding='utf-8')); d['st'] = stories
    json.dump(d, open(repo + '/data/core.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('stories', len(stories), '| lines', sum(len(x['lines']) for x in stories), '| story lines with a word not yet taught:', sb)

# ---- 39: must-know words: about 10 per unit (the unit's key grammar words, then the most common); the rest are optional ----
MUST = 12   # A2 units only; A1 units are short (12 to 16 words) and every word is must-know
ESSENTIAL = set('trưa|chiều|rưỡi|tuần rồi|năm sau|mươi|hoa|điện|học sinh|việc làm|bánh|thịt|câu chuyện|họp|lễ|bán|tiền mặt|chồng|vợ|cha|mẹ|đồ ăn|chụp|quan trọng|đêm|đúng giờ|giải thích|tai nạn'.split('|'))
rank = {}
if len(sys.argv) > 2:
    for i, l in enumerate(open(sys.argv[2], encoding='utf-8')):
        p = l.split('\t')
        if len(p) > 2: rank.setdefault(N(p[2]).lower(), i)
d = json.load(open(repo + '/data/core.json', encoding='utf-8'))
for u in d['units']:
    keys = set(k.lower() for k in u['key'])
    idx = list(range(len(u['w'])))
    exs = ' '.join(' ' + ' '.join(syl(e[0])) + ' ' for e in u['ex'])
    first = [i for i in idx if u['w'][i][0].lower() in keys]
    first += [i for i in idx if i not in first and ' ' + ' '.join(syl(u['w'][i][0])) + ' ' in exs]   # words the examples use
    first += [i for i in idx if i not in first and u['w'][i][0].lower() in ESSENTIAL]
    first = first[:MUST]
    rest = sorted([i for i in idx if i not in first], key=lambda i: rank.get(u['w'][i][0].lower(), 10 ** 6))
    rest = [i for i in rest if i not in first]
    u['m'] = idx if u['lv'] == 'A1' or len(u['w']) <= MUST else sorted((first + rest)[:MUST])
if rank: json.dump(d, open(repo + '/data/core.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('must-know words:', sum(len(u['m']) for u in d['units']), '| optional:', sum(len(u['w']) - len(u['m']) for u in d['units']))
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
