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

VERSION 15 (14 Nov 2026) - first real voice
- 108 lines recorded by a real Saigon speaker (75 everyday phrases, 21 short sayings, 12 tone words) are in audio/r00.mp3, flagged 2 in audio/index.json.
- src/voice/build_voice.py REPO part1 part2 part3 cuts recordings at the pauses, evens the loudness and rebuilds r00.mp3. Run it again with new files to replace the voice. The original recordings are not kept in the repo.
- S.set.vx: 'r' real voice first (default), 'f' computer woman, 'm' computer man, 'both' mix.

VERSION 16 (14 Nov 2026) - mission rehearsals and the first three minutes
- z13Rehearse(missionIndex): the four phrases for that mission (Z13RH, all from recorded lines), copy them out loud (z13Shadow with a fixed list), then a mock run with a matching scene, then "go and do it".
- z13First(): what a new learner does straight after the welcome: answer "Anh tên gì?" out loud, copy two phrases and see the tone line, take away one street sentence. Then the first day starts.

VERSION 17 (14 Nov 2026) - recording page
- record.html?v=VOICEKEY&who=voice1|thay|voice2 : a speaker reads a line, taps record, it trims the silence, evens the loudness, saves a small WAV and uploads it. No files to send.
- Lines to record: data/voice-lines.json (1,076 lines, built by src/voice/make_lines.py from the app's own content, in priority order). Lines with {placeholders} (the question drills and scenes) are not in it yet.
- Server: cfg:voice = the recording key (made by POST /api/t/voice-key, teacher only). vo:<who>:<lineId> = the WAV. vo:index = {who:{lineId:[time,text]}}. vo:flags = lines a speaker marked as not natural. GET /api/voice/index and /api/voice/clip are open; POST /api/voice/rec and /flag need the key.
- App: block 17 reads /api/voice/index at start and plays those recordings first (real voice). Nothing has to be rebuilt when someone records.
- Teacher page: "Thu âm · recording links" shows the three links, the counts and the flagged lines.

VERSION 18 (14 Nov 2026) - ready-made situations, more lines to record, dusk skyline look
- Situations: src/situations/situations.txt (one block per situation: "# id|vi|en|tip", then "me|vi|en" or "them|vi|en" lines) -> data/situations.json. Written once, no AI cost at run time. To add one: add a block, rebuild the json (see the script in this commit), run src/voice/make_lines.py . so its lines join the recording list.
- App: block 18. z18Card on Today, z18Open (lines + tip), z18Mock (they talk, you answer). Learner suggestions go to POST /api/suggest (KV cfg:suggest), shown on the teacher's recording screen.
- Recording list is now 2,478 lines: adds the 8 situations (right after the 12 patterns) and the 667 new words with their sentences (at the end). Old line ids did not change.
- Look: new header (dusk skyline with the old yellow building in front) and a Saigon-at-night dark theme.

VERSION 19 (14 Nov 2026) - skins
- S.set.skin: 'night' (default), 'dusk', 'classic'. Set on <html data-skin>. Colours are CSS variables in block 19 of v7.css. Settings has a Look switch (z19Panel). The night header is made from the dusk one by z19Night().

VERSION 20 (14 Nov 2026) - Ben's own photos
- img/hero.jpg (sunrise skyline, Today header), img/alley.jpg (welcome screen), img/stall.jpg (situations card), img/river.jpg (outside listening card). Used in the night and dusk looks only; classic keeps the drawing. All four are Ben's own photos, cropped and shrunk to about 100 KB each.
