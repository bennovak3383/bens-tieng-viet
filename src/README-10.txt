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

VERSION 21 (14 Nov 2026) - the Ben character, red-star flags, no photos
- src/art/ben.py draws the cartoon of Ben, the red-star bunting, the scooter and the flag-alley welcome scene. It prints JSON with 'ov' (overlay added to the skyline header) and 'alley' (welcome scene); these are stored in v7.js as Z21OV and Z21AL.
- The photos in img/ are no longer shown (z20Photos is switched off). The files are still in the repo.

VERSION 22 (14 Nov 2026) - Thầy Tâm character
- src/art/ben.py also draws tam(): the teacher (black side-swept hair, round face, striped shirt, pointing). He stands next to Ben in the header and in the welcome alley, and his round avatar (Z21TA, z21Av) sits on the teacher's note on Today.
- The avatar is only put next to words the teacher actually wrote (his notes), not next to tips written for the app.

VERSION 24 (14 Nov 2026) - photo of your page from a laptop
- Writing, photo step: two new buttons (z24Extra). "Send it from my phone": the laptop makes a 10-character code, shows it as a QR code (lib/qrcode.js, Kazuhiko Arase, MIT) and polls GET /api/snap?t=CODE. The phone opens snap.html?t=CODE (or types the code at /snap.html), takes the photo and POSTs it. Stored in KV as sn:CODE for 15 minutes and deleted when collected. "Use this computer's camera": webcam preview and Snap.

VERSION 25 (14 Nov 2026) - easier day, hear it mark it, mouth guide
- Easier day: S.set.easy = today's key. z12Stops then returns a review-only route and fcFresh returns no new cards. Button under the time chips on Today.
- Hear it, mark it (z25Mark): one-syllable words that have a recording; six tone choices; shows where the mark goes and why (z25Where: on ơ in ươ; else on the vowel with a hat or hook; else one vowel; two vowels + final consonant = second; two vowels open = first; three = middle). Misses kept in S.set.mk13. On the Sounds page and in the 60 and 90 minute routes (key 'mk').
- Mouth guide (z25Mouth, Z25M): lip shapes and a short note for each vowel, vowel pair, endings and tones. Written for the app, not yet checked by a teacher. Learner's own class notes in S.set.mn13. Each sound lesson shows the matching entries in a fold-out at the top.

Version 26 · starting from zero (beginner path)
- Welcome now asks "Have you studied Vietnamese before?" (S.set.lvl0 = zero | some | more). Existing users are untouched.
- "zero" learners get a 14-step guided path on Today instead of the normal day (data/beginner.json, built by src/beginner/make.py).
  Each step: 2 to 4 short stops, plus a "with your teacher" box. State in S.set.z0 = {s:step, d:{'step:stop':1}, fin}.
- New mini-sessions: z26Explain (read first pages), z26Learn (meet words, then check), z26Quiz (review), z26Tone (which tone did you hear).
  Other stops reuse existing drills (vowels, marks, mouth guide, shadowing, restaurant situation, scene, story, monthly check).
- After step 14 the learner moves to the full app at 30 minutes. Settings has "My level" to switch either way.
- Teacher page: "Người mới · beginner guide" (what to do in class for each step) and the student's current step on their page.
- Recording page: new part z0 (29 beginner lines) after a3.

VERSION 27 (15 Nov 2026) - core course: grammar units that roll out the most common words in order
- Why: a check against a Vietnamese frequency list showed only 26% of word cards were in the top 1,000 words, the commonest glue words (và, nhưng, vì, nếu, đã, sẽ, đang) sat in level 15, and half the word cards appeared in one sentence only.
- Content: src/core/*.txt (format at the top of a1.txt). python3 src/core/make.py . [vn_word_frequencies.tsv] builds data/core.json and checks that every sentence uses only words taught up to that unit. Then run python3 src/voice/make_lines.py . so the recording list picks the lines up.
- 20 units so far (level A1, 275 words, 397 sentences). Drafted by Claude, NOT checked by a Vietnamese speaker.
- App: block "27" at the end of src/v7/v7.js. z27Apply turns each unit's words into cards (deck k01, k02 …; card id k01_1 …) and removes an older, not-yet-started card for the same word. z27Unit runs a unit: z27Gram (explanation + examples), z26Learn (words + quiz), z27Order (build the sentence), z27Gap (missing word), z27Say (say it, then check). State: S.set.k27 = {snd, d:{unitId:{t,o,on,g,gn,s,sn}|{skip}}}.
- A unit's cards open when the unit is done (fcOn is wrapped) and come first among new cards (fcFresh is wrapped).
- z27Rot: once a day each card's example sentence is picked from its own sentence plus up to 5 sentences from finished units that contain the word, so words come back in new sentences everywhere c.xv is used (cards, recall, listening, shadowing).
- Sounds first: the course card on Today asks for the first 8 sound lessons (single vowels and the vowel pairs) unless the learner says they know them (S.set.k27.snd) or finished the beginner path.
- Teacher: teacher.html button "Nền tảng · core course" (core27): edit the explanation, examples, words and class notes of any unit, leave a note, tick "checked". Stored in KV cfg:core via POST /api/t/core, read by the app from GET /api/core. The student page shows core progress and low drill scores.
- Recording: make_lines.py adds one part per unit (k01 …). They are added last so older line ids do not change, then moved up to sit after the beginner part.
- Tests: src/tests/t27.py (learner) and t27b.py (teacher, recording page).
- To rebuild index.html: python3 src/patch10.py OLD_SRC src OLD_INDEX OUT, where OLD_SRC and OLD_INDEX come from the last commit (git archive HEAD src index.html).

VERSION 28 (15 Nov 2026) - core course grows to 45 units (A1 1-20, A2 21-45): 817 words, 1,089 sentences
- New files src/core/a2a.txt (21-30), a2b.txt (31-40), a2c.txt (41-45). Files are read in name order.
- make.py with the frequency file also writes "top" into data/core.json: the top-1,000 words that are a card somewhere in the app (730 now). z27Top counts how many of them the learner has started; shown on the core card and the unit list.
- Of the top 1,000 on the frequency list: 633 are core-course words, 730 are a card somewhere. The rest are mostly film, news and northern words left out on purpose (list them with the script in the handoff doc if needed).
- The "one new thing" check in make.py works on syllables, so a compound made of known syllables passes even if the compound itself is new.

VERSION 29 (15 Nov 2026) - a day plan at the learner's level, and test practice
- Why: Ben said listening and speaking in the app were over his head. The old plan drew questions, stories and scenes from everything.
- z12Stops is wrapped: while z29On() (core course loaded, S.set.k27.full not set, not on the beginner path, not an easy day) the day is: Sharp ears, the next core unit (or a sound lesson until the sounds are done), cards, then Nghe (z27Hear), Nói (z27SayDay), Dấu (z29Write) and at 90 minutes Trả lời (z29Speak). All four draw only on z27Known(): sentences from finished core units. Stops are ticked with zDay('ku'|'kl'|'ks'|'kw'|'kq').
- The switch is a slip under the time buttons on Today (S.set.k27.full = 1 gives the old full plan back). z12Pool is also limited to started cards plus finished-unit sentences while at-my-level is on.
- Test practice (Practice tab, Thi thử): src/exam/make.py builds data/exam.json (9 speaking topics with 41 questions and example answers, 6 reading texts with 24 questions; each has a "gate" = core units needed). Task types follow the first parts of the Vietnamese proficiency test for foreigners; all wording is our own, nothing copied from a test paper, and no school is named.
  z29Hear1 (hear a question, pick the reply), z27Hear (hear a sentence, pick the meaning), z29Read, z29Write (pick the correctly tone-marked word; wrong options are made with z25Put), z29Speak (answer out loud; with the mic on the answer is recorded for the teacher as kind 'exam'). Scores: S.set.k27.ex[part] = {t,r,n}.
- Recording list: parts x1 (questions and example answers) and x2 (reading texts).
- Tests: src/tests/t29.py.

VERSION 30 (15 Nov 2026) - pictures, the questions people ask you every day, a fuller day plan
- Pictures: src/art/draw2.py adds 204 drawings (304 in all) in the same style: people and family words, actions, feelings, places, positions (trên, dưới, trong …), times of day and calendar words, qualities, colours, question words. It is run by draw.py (exec before saving): python3 src/art/draw.py art/cards.json . Helpers: fig() draws a person (feet at y=0, head at y=-92; limbs are point lists), Q() a question mark, bubble(), heart(), arrow(), cal(), clockface(), box(), ball().
  Pictures are keyed by the Vietnamese word, so a word with several meanings (phải, nên, hay, về, chỉ, ký …) is left without one on purpose.
  211 of the 817 core words now have a picture; the rest are grammar words, where the example sentence does the work.
- Everyday questions: data/exam.json "daily" (30 questions people in Saigon ask a foreigner, with one example answer each; written in src/exam/make.py DAILY). They are a card deck "dq" (first among new cards), a day stop "kd" (8 at a time) at 30, 60 and 90 minutes, the first row on the check page, and recording part x0 (right after the beginner part).
- Day plan at my level: 30 = ear, unit, cards, everyday questions; 60 adds listen, say it, marks; 90 adds a sound lesson, a speaking topic and 20 minutes of listening outside the app.
- "Test practice" is now "Kiểm tra · Can I do it?": the same checks, framed as "can you use what you learned". The course follows the research plan; the university test papers were only a reference for task types.
- Tests: src/tests/t30.py.

VERSION 31 — sound lessons: listening in the spelling step, word and sentence in one voice
- Step 3 (spelling rules) now plays the word first, with a big replay button. The word is
  worked out by filling the blank with the right answer (m_t + ắ = mắt). Yes/no rule
  questions have no word, so no sound.
- Recording list: new part v0 "Vần: từ và câu" right after the six tones (265 lines: every
  sound-lesson word, then every example sentence). Once recorded, the word and its sentence
  play in the same real voice. Until then the app may use the woman's computer voice for the
  word and the man's for the sentence (e.g. "me" vs "Tôi thích nước me."), which is why they
  sounded different. Recording list total: 4,385 lines.

VERSION 32 — everyone gets their own account that follows them
- At the end of the welcome screen the app makes a code for the new person automatically
  (POST /api/join). The home page shows it ("Your code · keep it") with Copy and Got it.
- The welcome screen has "Already using the app on another phone or computer? Sign in with
  your code". Signing in loads that person's progress and skips the welcome.
- Devices that were used before this (no code yet) show a "Save your progress online" card
  on the home page with Get my code / sign in.
- Lost code: the teacher page now shows each student's code next to their name (stored as
  metadata c on s:<id>; older students show it after their next save).
- Progress tab: "Start over as a new learner" clears this device and signs out; the old code
  still works online.

VERSION 33 — recording page: pick any part, by size
- Order now follows the line list itself (src/voice/make_lines.py): tones, sound lessons (v0),
  everyday questions, core course, then the older parts. Before this, record.html had its own
  ORDER list that pushed the new parts to the end.
- "Pick a part" list with size buttons: all / short (≤10) / medium (11–20) / long (21+). Each
  part shows lines left and rough minutes (about 20 seconds a line).

VERSION 34 — "A1 only" switch for the core course
- Core course → All units → Show levels: "A1 only" / "A1 + A2". Saved in S.set.k27.max, so it
  follows the learner's code. Default is A1 + A2.
- With A1 only: the card counts "unit x of 20", the list hides the 25 A2 units, A2 words never
  become cards, the day plan has no unit stop once A1 is done, and the card offers "Open A2".

VERSION 35 — levels for everyone, teacher controls A2 (replaces the version 34 learner switch)
- Every learner sees A1 only (20 units). A2 opens by itself when all A1 units are done (done or
  skipped with "I know this").
- Teacher page → a student → "Cấp độ · course level": Automatic / Open A2 now / Keep at A1.
  Stored as lv:<student id> (POST /api/t/level); sent to the app with GET /api/state as j.lv and
  copied into S.set.k27.t after each sync. Only works for learners with a code.
- z27N() = number of units in reach; used by the course card, unit list, end-of-unit screen,
  practice tile and the day plan.

VERSION 36 — grammar units end with "your own sentences" for the teacher
- After the three drills, each core unit asks for 3 sentences of the learner's own with that
  grammar, each with a Record button (record / stop / play back). "Send to my teacher" or
  "Skip for now". The end-of-unit screen has "Write more sentences for my teacher".
- Sends like Write it, say it: POST /api/w with ref 'g<time>' and u (unit id); each recording via
  zRecSave kind 'unit' with the same ref. Without a code it is kept on the device only.
- Teacher page: the piece shows under Writing tagged "grammar", with ▶ Hear it under each recorded
  sentence and the usual written / voice reply. Recordings also have a "Grammar" filter.
- Voice only for now; Ben said no video.
