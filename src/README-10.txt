Ben's Tiếng Việt · build source 10 (14 Nov 2026)

What changed in 10: games tile + "Want more?" games row, Listen more card (daily southern podcast/YouTube pick),
Viết · Write it, say it (handwrite + photo, or type with Telex; four "make it longer" rounds; say it 3x with 30/20/12 s;
send to teacher), teacher page Writing panel (photo, text reply, voice reply), Progress page shows replies,
Nghe kỹ · Sharp ears (3-min vowel/tone pick-the-word drill, both voices, misses come back next day; first step of Today),
Speak now goes both ways (every 2nd item: hear the answer, ask the question; "Both ways" chip to switch off).

HOW TO BUILD 10 (or later): python3 patch10.py OLD_SRC NEW_SRC LIVE_INDEX OUT_DIR
 - OLD_SRC = the source folder whose v7 files are inside LIVE_INDEX now (for 10 that was build-source-9-2).
 - It swaps v7/v7.js, v7/v7.css, v7/sections.html into the live index.html.
 - First time only: it also moved the embedded clips (script tag audio6, 6.3 MB) out to audio/e6a.b64 and audio/e6b.b64.
   They are base64 TEXT on purpose: any mp3/binary file saved on Ben's Mac gets a 5,822-byte label added at the front,
   which shifts every clip. Text files are left alone. Page is now about 0.7 MB instead of 7 MB.
 - For the next version: download index.html from the repo, use build-source-10 as OLD_SRC. The audio6 step is skipped.

New server endpoints (functions/api/[[path]].js): w (GET/POST, student), w-voice (GET, student),
t/w-photo, t/w-voice (GET/POST), t/w-reply, t/w-del (teacher). KV keys: wi:ID (list), wp:ID:t (photo, 180 days),
wv:ID:t (teacher voice, 180 days). Student remove also deletes these.

Tests: tests/*.py with Playwright against site8/devserver.mjs (copy index.html, teacher.html, functions/, audio/ next to it).
The app script is inside a closure; the tests add  window.__T=function(c){ return eval(c) };  to a TEST copy only.

VERSION 11 (14 Nov 2026): AI conversation "Nói gì cũng được · Talk about anything" (first tile in Trò chuyện).
Optional topic (typed or a chip). Server prompt now: follow the learner's topic (open mode, up to 18 words),
keep speaking Vietnamese (simpler Vietnamese before any English), light corrections only, and a new "help" field:
a short English answer when the learner asks something in English. Applies to the 8 scenes too.
"🇬🇧 Ask in English" chip: listens once in en-US (base fix in patch10.py: r.lang=SPEECH.lang||'vi-VN').
Build for 11: python3 src/patch10.py <copy of src before the edit> src index.html OUT

VERSION 12 (14 Nov 2026) - classic Saigon look, time-based day
- All v12 code is the "12" block at the end of src/v7/v7.js and src/v7/v7.css.
- Card drawings: src/art/draw.py makes art/cards.json (100 drawings, keyed by the card's Vietnamese word).
  Run: python3 src/art/draw.py art/cards.json . The app fetches art/cards.json at start (z12Pic).
- Emoji are stripped from the interface at run time (z12Clean). The old Library (#today) keeps its emoji: they are the pictures in those games.
- Today: S.set.mins (10/30/60/90) picks the route (z12Stops). Practice seconds: S.d6[day].sec. Outside listening minutes: S.d6[day].out.
- New sessions: z12Recall (English to Vietnamese sentences), z12Playlist (listen only).
- Build: same as before (python3 src/patch10.py OLD_SRC src index.html OUT_DIR).

VERSION 13a (14 Nov 2026) - shadowing with a tone picture
- Block "13a" at the end of src/v7/v7.js. z13Shadow(onDone,n): plays the model clip, records you, plays both, draws both pitch lines.
- z13Pitch: autocorrelation pitch track, shown in semitones around each speaker's own middle, so a low and a high voice can be compared.
- In the 60 and 90 minute routes (key 'sh') and on the Practice tab.
