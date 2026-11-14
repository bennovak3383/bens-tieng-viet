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

VERSION 13b (14 Nov 2026) - levels, own words, sentence review, listening, weekly mission, monthly check
- Block "13b" at the end of src/v7/v7.js.
- IMPORTANT: the app only saves the top-level keys listed in merge(). New data therefore lives inside S.set:
  S.set.rc13 (sentence review), S.set.lc13 (listening), S.set.wm13 (weekly mission), S.set.chk13 (monthly checks), S.set.myc13 (own words), S.set.lvl (level opened by hand).
- Levels: Z13LV lists the decks in each level. A level opens at 80% learned of the one before (z13Level). fcOn is wrapped; cards already started stay on.
- New words to reach about 1,200 go in as levels 6 and up: add cards to content7 and a row to Z13LV.

VERSION 13c (14 Nov 2026) - 667 more words for foreigners living in Saigon (1,115 total)
- Source: src/words/w1.txt, w2.txt, w3.txt (one line per word: vi|en|sentence|sentence in English; "# n|vi|en" starts a level).
- Built into data/words13.json (levels 6 to 15), fetched at start by z13Words. Words already in the app are dropped when building.
- words.html is a plain page of the new words for the teacher to check.
- These words were drafted by Claude and are NOT yet checked by a teacher. Most have no recording yet and use word clips or the phone voice.

VERSION 13d (14 Nov 2026) - the teacher's side
- Server: GET /api/words (open) and POST /api/t/words (teacher key). Stored in KV as cfg:words = {e:{cardId:[vi,en,sentence,sentenceEn]}, d:{cardId:1}, a:[{id:'tw…',vi,en,xv,xe}]}.
- App: z13Teach applies edits, removals and the teacher's own words (deck 'tw', always open) to every learner.
- teacher.html: "Từ vựng · word list" button (words13) edits any of the words; the student page has a new panel (x13) with level, weekly missions, own words and monthly checks.

VERSION 14 (14 Nov 2026) - voice choice
- audio/index.json: every clip now has a 4th value, 1 = the man's voice (Đức Trí), 0 = the woman's (Kim Thanh). Worked out by measuring pitch (man about 70 to 130 Hz, woman 165 and up).
- 1,034 of the 2,824 texts exist only in the man's voice. To fix his voice for good, those need making again.
- S.set.vx: 'f' woman first (default), 'both', 'm'. The man's clips are not slowed below 0.9 unless S.set.vslow is 1. Settings has the switches.

VERSION 14b (14 Nov 2026) - quiet sound on iPhone
- Cause: the app kept the microphone stream open all the time. An iPhone then plays all sound in "call" mode (quiet, earpiece).
- Fix: the stream is opened only for a recording and closed 0.2 s after it stops (z14Get, z14Free; MediaRecorder.start is wrapped to count live recordings). SPEECH.on still means "the learner wants the mic".
