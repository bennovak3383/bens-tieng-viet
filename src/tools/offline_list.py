#!/usr/bin/env python3
# Writes data/offline.json: the files the app keeps on the device so the practice parts work with no internet.
#   python3 src/tools/offline_list.py .
# Run it again after adding pictures or data files (src/art/pics.py does not do it for you).
import sys, os, json, glob
repo = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(repo)
files = ['./', 'manifest.webmanifest', 'lib/qrcode.js', 'art/cards.json', 'audio/index.json']
files += sorted(f for f in glob.glob('data/*.json') if os.path.basename(f) not in ('offline.json', 'voice-lines.json'))
files += sorted(glob.glob('img/*.jpg')) + sorted(glob.glob('img/icon-*.png')) + sorted(glob.glob('img/p/*.webp')) + sorted(glob.glob('img/home/*.webp'))
files = [f for f in files if f == './' or os.path.exists(f)]
audio = []
try: audio = ['audio/' + b for b in json.load(open('audio/index.json')).get('bundles', [])]
except Exception as e: print('no audio index:', e)
audio = [a for a in audio if os.path.exists(a)]
size = lambda L: sum(os.path.getsize(f) for f in L if f != './')
core, snd = size(files) + os.path.getsize('index.html'), size(audio)
json.dump({'v': '%d-%d-%d' % (len(files) + len(audio), core, snd), 'mb': round(core / 1e6, 1), 'audio_mb': round(snd / 1e6, 1), 'files': files, 'audio': audio},
          open('data/offline.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('offline list: %d files (%.1f MB) + %d sound files (%.1f MB)' % (len(files), core / 1e6, len(audio), snd / 1e6))
