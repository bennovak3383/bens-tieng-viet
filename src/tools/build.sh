#!/bin/bash
# Build index.html from src using HEAD as OLD, then refresh the test site.
set -e
R=/home/claude/bens-tieng-viet; T=$(mktemp -d)
mkdir -p $T/old/v7 $T/out
for f in v7.js v7.css sections.html; do git -C $R show HEAD:src/v7/$f > $T/old/v7/$f; done
git -C $R show HEAD:index.html > $T/live.html
python3 $R/src/patch10.py $T/old $R/src $T/live.html $T/out
cp $T/out/index.html $R/index.html
node -e "const s=require('fs').readFileSync('$R/index.html','utf8'); const m=[...s.matchAll(/<script(?![^>]*type=\"(?:text\/plain|application\/json)\")[^>]*>([\s\S]*?)<\/script>/g)]; for(const x of m){ try{ new Function(x[1]) }catch(e){ console.log('SYNTAX',e.message); process.exit(1)} } console.log('syntax ok',m.length)"
# test site
S=/home/claude/site; rm -rf $S; mkdir -p $S
cp -r $R/index.html $R/teacher.html $R/record.html $R/words.html $R/snap.html $R/functions $R/audio $R/data $R/art $R/img $R/lib $S/
cp $R/src/site8/devserver.mjs $S/
python3 - <<'PY'
p='/home/claude/site/index.html'; s=open(p,encoding='utf8').read(); i=s.find('function z27Unit(ui,onDone){'); s=s[:i]+'window.__T=function(c){return eval(c)};'+s[i:]; open(p,'w',encoding='utf8').write(s)
PY
pkill -f devserver.mjs || true; sleep 0.5
cd $S && (nohup node devserver.mjs > /tmp/dev.log 2>&1 &); sleep 1.5; curl -s -o /dev/null -w "server %{http_code}\n" localhost:8890/
