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

VERSION 37 (15 Nov 2026) - audit fix 1: one spine on Home
- Block "37" at the end of src/v7/v7.js. Only when the core course is on, not the beginner path, not the full plan (z37Spine).
- Z37.gate = units finished before an extra shows: weekly mission 5, monthly-check nudge 3, hands-free Speak now 5, Practice: Stories 5 and Games 5, real-life situations 10, "More ways to practise" folded until 20.
- Core card moved to the top of Home, under the code card. A line on it says what opens next.
- Situations: pet shop, girlfriend's family and gym (Z37.personal) sit under "More situations".
- More tab: the in-app "Thầy" tile (the student's own recordings view, #teach) renamed "Ghi âm · my recordings".
- Home sound line now says the course opens after the first 8 sound lessons and the rest are extra.

VERSION 38 (15 Nov 2026) - audit fix 2: A2 re-levelled, B1 preview, five plain A2 units
- Units u26 (although), u27 (càng…càng), u31 (việc/cách/điều/sự), u39 (về/theo/đối với), u41 (do/nhờ/tại/khỏi) moved to src/core/b1.txt with level B1 ("B1 preview"). Their words that are now taught earlier (giá, mắc, rẻ, ký, vui tính) were dropped from them.
- New A2 units: u46 days and dates (before u25 clock time), u48 shopping and bargaining (start of a2b), u47 describing people and places (in a2c before u42), u49 doctor and pharmacy, u50 phone, Grab and pickup (end of a2c). 50 units, 868 words, 1,170 sentences, 0 sentences with an untaught word.
- tiền mặt and mặc dropped from u37 (now taught in u48). A few sentences reworded so no sentence uses a word from the B1 units.
- z27N: A1 → A1+A2 → all. Teacher level can be A1, A2 or B1 (server accepts B1; teacher page button "Open B1 preview"). z27Lv(lv), z27LvDone(lv).
- Recording list rebuilt: 4,474 lines; new parts k46 to k50 sit inside the A2 order, B1 parts after the A2 ones.

VERSION 39 (15 Nov 2026) - audit fix 3: words come back more; graded stories
- src/core/extra.txt: extra review sentences per unit ("## uid" then "& vi|en"), 213 lines. make.py puts them in unit.xs and checks them for untaught words.
- src/core/stories.txt: 9 graded stories (g1 to g9) about Mike, one after units 5, 10, 15, 20, 26, 30, 35, 40, 45 (field "at" = position in the course). "+ word|English" lines are the few new words a story may add. make.py writes them to core.json "st" and checks every line.
- Words added to units so stories and sentences can use them: bà (u01), cười (u03), phòng and chợ (u05), vợ and chồng (u30), mươi and lăm (u46), bán (u48). Added at the END of each unit's word list so card ids do not move.
- A2 words seen 3+ times in the course text: 155 -> 304 of 497. Of the 10 most common words in each A2 unit: most now 3+.
- Block 38 in v7.js: z27Apply also feeds unit.xs into Z27.sent (card sentence rotation, at-my-level drills). z38Story turns a graded story into the normal story reader format; z38Open (all units up to "at" done); zStories lists unlocked graded stories first and hides locked ones; the core card on Home shows "Truyện mới · new story" when one is unlocked and unread. Core words are added to the tap-a-word glossary.
- Recording list: 4,840 lines. Each story is part g1..g9, placed right after the unit it follows; extra sentences are inside each unit's part.

VERSION 40 (15 Nov 2026) - audit fix 4: must-know words, each learned inside its sentence
- make.py writes unit.m = indices of the must-know words. A1 units: every word. A2 and B1 units: up to 12, picked in this order: the unit's key grammar words, words its example sentences use, a short ESSENTIAL list (make.py), then the most common words. 638 must-know, 239 optional.
- Block 39 in v7.js. z39Learn replaces the word step of a core unit: one must-know word per screen with its picture, meaning and its example sentence with the word highlighted (both play), then the 8-question check on must-know words, then an "Also in this unit · optional" screen with the other words (tap to hear), "Add these to my cards" (S.set.k27.opt[unitId]) and "Always add the extra words" (S.set.k27.optall).
- fcOn: an optional word only becomes a card if added (or already started). z39IsOpt(card). The unit card says "N must-know words (and M optional)" and a longer, more honest time.
- z26Learn is wrapped: when called by z27Unit (Z39.u set by the z27Unit wrapper) it hands over to z39Learn; the beginner path still uses the old screen.

VERSION 41 (15 Nov 2026) - audit fix 5: the Say step is recorded, compared and sent
- Block 40 in v7.js replaces z27Say. For the first 3 lines (Z40.rec) of a unit's Say step: after "I said it · show me" the learner records the line (z36Rec), sees their pitch line next to the model (z13Pitch, z13Graph), and the clip is saved with kind 'unit' and prompt "Unit N · say it: …" so it uploads to the teacher like the own sentences. The 4th line is not recorded. Score buttons unchanged.
- Teacher page: every recording with a text now has "Tone off:" chips (ngang, huyền, sắc, hỏi/ngã, nặng). A tap saves a note "Tone to fix: <tone>" about that line (existing t/note endpoint; toneTag in teacher.html).
- Student app: notes that start "Tone to fix:" show on Today as "Thầy cô · tones to fix" with a "Fix them now" button that runs shadowing on those lines (z13Shadow with items). Done lines are remembered in S.set.tf40 (note time).

VERSION 42 (15 Nov 2026) - audit fix 6: "Ngoài đường · on the street"
- src/core/street.txt: 79 lines, at least one per unit: "~ street form|course form|English|note" (tui, hông, dạ/dzậy, bữa nay, ổng/bả, kêu, xài, quẹo, mắc, ghê, dữ, chục, xíu…). make.py puts them in unit.street (not checked for untaught words on purpose: they are for understanding).
- Block 41 in v7.js: z41Street draws a panel under the examples on each unit's How-it-works screen, each line with a play button, the course form, English and a note.
- Teacher page core editor: new rows "Ngoài đường · on the street" (3 boxes + note, one empty row to add); saved as street in cfg:core; the server accepts it; z27Apply uses the teacher's version.
- Recording list: street lines are inside each unit's part, with the English marked "(Saigon street talk: say it casually)" so speakers read them the casual way. 4,917 lines.
- The unit's first button now says "Next · the N words" with the must-know count.

VERSION 43 (15 Nov 2026) - audit fix 7: who is who (xưng hô), and women learners
- New A1 unit u51 "anh · chị · em · chú · cô · bác · ông · bà" placed 7th (after u06). Words ông, chú, bác, cháu, ơi, tuổi; chú, bác, cháu, ơi, tuổi were removed from u36/u33 (A2) so they are not taught twice. A1 is now 21 units. Stories' "at" moved up by one. Street lines added for u51.
- Block 42 in v7.js. Welcome (z26Ask wrapper) asks "How should people address you?": As a man (anh) / As a woman (chị) -> S.set.g42 = 'm' | 'f'.
- z42Q(text): for women, a question's "anh" that means "you" becomes "chị" (not anh ấy / anh trai / anh + name / tiếng Anh / người Anh / nước Anh), vợ -> chồng, bạn gái -> bạn trai. z42Apply runs on Home render and rewrites Z29 everyday questions and speaking topics, C6.pairs questions and the everyday-question cards (keeps originals in _o, so switching back works). The first-three-minutes question uses it too.
- Recording list: new part x0c, the 28 everyday questions that change when asked to a woman. 4,954 lines.
- The family-tree picture for this unit comes with fix 8.

VERSION 44 (15 Nov 2026) - audit fix 8: teaching pictures
- Block 43 in v7.js, drawn in code (SVG/HTML, light and dark themes via currentColor), styles .z43* in v7.css:
  z43Tones (Saigon tone pitch lines, hỏi = ngã, nặng lifts at the end) on the beginner "The six tones" page and the Dấu page;
  z43Marks (where the tone mark goes, with examples) on the beginner "Two kinds of marks" page and the Dấu page;
  z43Family (who-is-who age ladder: you call them / you call yourself) on the beginner "you" page and unit u51;
  z43Time (đã, rồi, vừa, đang, sắp, sẽ on a line; chưa) on units u08, u09, u10, u11, u24, u45;
  z43Vowels (vowel chart: tongue forward/back, closed/open, round lips circled) in the mouth guide and folded inside the single-vowel sound lessons.
  Hooks: z26Explain pages call z43For(title); z27Gram, renderTones, z25Mouth and vanOpen are wrapped.
- Card drawings (src/art/draw2.py, art/cards.json): hôm qua, hôm nay, mai and tuần are now a strip of days with today pinned (days()), not near-identical calendars; uống has a glass of water at the mouth.
- nặng description fixed for Saigon (src/beginner/make.py, rebuilt data/beginner.json; and the mouth note in v7.js): low and short, lifts a little, no hard stop.

VERSION 45 (15 Nov 2026) - audit fix 9: A1 and A2 level checks with teacher sign-off
- Block 44 in v7.js. When all A1 (or A2) units are done and that check has not been taken (z44Due), the core card on Today shows "Kiểm tra A1 · level check". z44Open(lv): part 1 = 20 listening items (sentences from that level's units, pick the meaning out of 3); part 2 = 8 questions out loud (A1: the everyday questions; A2: 8 questions about past, plans, home, Saigon, health, shopping, friends, learning), each answer recorded with kind 'check' and prompt "A1 check · …" so it uploads to the teacher. Result in S.set.k27.lc44[lv] = {t, l, ln, s, sn} (synced with the state).
- Teacher page, student view: a "Kiểm tra A1 · level check" panel per check taken: listening score, answers recorded, a 6-item can-do checklist (Z44.can), and "Passed · open A2" / "Not yet · keep at A1" (A2 -> B1 preview). Marking sends a note to the student ("Level check A1: passed. Listening x/20. You can: … I have opened A2.") and sets the course level with the existing t/level endpoint. Recordings filter "Level checks" added.
- A2 still opens by itself when the A1 units are done (Ben's version 35 decision); the check is the teacher's sign-off and can hold a student at A1.

VERSION 46 (15 Nov 2026) - audit fix 10: the teacher's week, at a glance
- teacher.html, x45(): a "Tuần này · this week, for class" panel at the top of each student's page: recordings in the last 7 days by kind; words that keep slipping (core cards with 2+ lapses, word and meaning from data/core.json); grammar to go over (units with low drill scores); tones the teacher has marked (from "Tone to fix:" notes, most frequent first); and a numbered plan for the next class (warm-up, fix the weak words and tone, go back over a weak unit, the next unit with its in-class note, speaking task 1 = the unit's task, speaking task 2 = a role-play from a street line) with "Copy the plan".
- Tests for versions 37 to 46 are in src/tests (t37a, t38, t38b, t39, t40, t44, t45). t40, t44, t45 and t27b each need a fresh dev server (the teacher key can only be made once per run).

VERSION 46b (15 Nov 2026) - teacher page, recording links: a speaker's name and man/woman now save on their own (when you leave the box, press Enter or pick man/woman), not only with the Save button; the heading changes to the name straight away and says "Saved ✓".

VERSION 47 — teacher page: listen to each speaker's recordings
On Thu âm · recording links, each person with recordings has "▶ Nghe lại · listen to their recordings".
It lists their clips newest first: Vietnamese line, English, which part, and a player. "Play all" plays them one after another.
"Good" marks a clip as checked (saved in that browser only). "Redo" (tap twice) removes the clip from the server
(new endpoint t/voice-del, teacher key only); the app stops using it right away and the line goes back on the recording list.
Test: src/tests/t47.py.

VERSION 48 — welcome questions, a personal plan, and why that much study
Home card "Kế hoạch · your plan" → 14 one-tap questions (why, level, address, 3-month goal, 1–5 ratings for understanding
and speaking, hears Vietnamese daily?, weekly situations, hardest thing, time of day, minutes + days, classes a week,
practice partner, tried before, a date to work toward, their why in their own words). Saved in S.set.in48.
Plan screen: path (Sounds first / Living here / Family / Steady), 3-month can-do goal (5 lines), daily minutes and
new cards (10→5, 30→10, 60→15, 90→20), how to split the day, "why this much" (adds lines for what they said is hard),
rough time to A1 (~150 h) and A2 (~420 h), and what is realistic by their date. Applies S.set.mins and S.set.fcn,
puts their situations first in "I am about to…", and keeps "meeting the family" visible for the family path.
The unit order does NOT change: each unit only uses words already taught.
Home card after: goal ticks, this month's days, their own "why" when they missed 2 of the last 3 days,
a 2-tap re-rating every 4 weeks. Teacher page: "Kế hoạch · their plan" panel at the top of each student.
Test: src/tests/t48.py.

VERSION 49 — story loop: listen → read → retell
Home "story of the week" card for the graded stories (g1–g9): day 1 listen with the text blurred, day 2 read and listen,
day 3 retell out loud (60-second clock, "don't stop" rule, the learner's focus words shown, a "peek at how it starts"
hint), sent to the teacher as kind 'retell'. Then an optional second retell in 45 seconds (the 4/3/2 fluency idea:
same content, less time). One step a day by default, with "do it now anyway". The next graded story card shows only
after the retell. In any story, only the first 4 tapped words become cards (S.w with cid); more taps still show the
meaning. State: S.set.sl49[cid] = {d1, d2, r, rd, r2}. Teacher recordings have a "Retells" filter. Test: src/tests/t49.py.

VERSION 50 — "Ask Thầy why" and the weekly voice note
"?" next to every unit example and "? Ask Thầy" after tapping a word in any story: pick a ready question (word order,
why this word, when to use it, do Saigon people say it, another way to say it) and/or type one. Saved in S.set.ask50.
Teacher page: "Câu hỏi · their questions" panel with an answer box; the answer is a teacher note with about='ask:<t>',
so it reaches the student through the normal notes pull. Home shows "your teacher answered" until they read it
(S.set.seen50). Voice note of the week (once A1 is done or the teacher opened A2): 14 rotating topics, record about a
minute, sent as kind 'vnote' (S.set.vn50[week]). Teacher recordings: "Voice notes" filter; retells and voice notes no
longer show "not understood". The 14 topic questions need a check by a Saigon speaker. Test: src/tests/t50.py.

VERSION 51 — speak without freezing (from the speaking flow audit)
- Start-talking bar: zHear is wrapped, so wherever the app listens (questions, speak now, recall, scenes, story
  questions) a 3-second bar shows under "Your turn"; it turns green with "started in X s" when speech begins, and
  after 3 s says "say anything: a word, ừm…, a lifeline". Time to first speech is logged per day in S.set.lat51
  ({day:[sum ms, count]}), shown on the Home week panel (this week vs last, goal under 2 s) and the teacher's page.
  Only where the browser's speech recognition works (Chrome); not checked on iPhone.
- Soft 5-second clock on every "I said it · show me" prompt (English shown, say it in Vietnamese). Never fails you.
- Lifelines: 10 "when you're stuck" lines (Dạ?, Nói lại giùm được không?, Nói chậm chậm được không?, Ừm… để tôi
  nghĩ chút, Cái này tiếng Việt kêu là gì?, …). One-time Home slip after unit 2, a drill (uses z27Say), a Practice
  tile, and a "Stuck? Lifelines" fold on retell, voice note and speak-now screens. Need a Saigon speaker check.
- Home tidy: plan card moved under today's route; its goal list folds; the month grid is gone (the week panel
  already tracks days and minutes).
Test: src/tests/t51.py.

VERSION 52 — slow first, speed later (Ben: "hear things slow, get reps, then speed up")
Pace follows the level (S.set.pace52: 'slow' | 'auto' | 'push', in Settings). Auto: units 1–10 no clocks at all;
rest of A1 gentle clocks (start-talking 6 s, say-it 8 s); A2 on 3 s / 5 s. Time-to-start is still logged quietly.
"Reps" (Lặp lại): known sentences, each played slow three times (stage 1) or slow, slow, normal (stage 2+), with a
pause after each to say it; hands-free, no marking. In the day route after cards during A1, and on Practice.
Say-it prompts: when the microphone works, "🎤 Say it" listens first and then shows the answer; "Show me without
speaking" is still there. Brave ladder (7 weekly real-world steps) on the plan card for learners who said speaking
makes them nervous or who live here (S.set.brave52). Test: src/tests/t52.py (t51 now runs with pace 'push').
The mic version of say-it was not tested (no speech recognition in the test browser).

VERSION 53 — the teacher's course plan drives the app (E1/E2, 6 lessons each)
data/plan.json = the default plan; the teacher's saved plan (KV cfg:plan, GET /api/plan, POST t/plan) replaces it.
Level names: A1/A2 are shown as plan.names (E1/E2) by a text replacer in the app and on the teacher page; data keys
stay A1/A2, so no progress is touched. A lesson = a run of the existing units (lesson.last = id of its last unit);
unit order never changes. Parts per lesson, in the teacher's own order: Phát âm, Hội thoại, Từ vựng, Mẫu câu,
Thực hành nói, Thực hành viết, Đọc hiểu, Thực hành nghe, Thực tế (real-life task, ours).
Release: plan.rel (whole class) or KV rl:<student> via POST t/rel (one student) = {open: lessons open (0 = automatic),
next: lesson id, hw: note, hp: hidden parts}. z27N() is capped by it. The student's own setting comes back with
GET state as rl → S.set.rl53. Home: #z53 lesson card above the core card; "Lộ trình" course map; per-lesson part
counts in S.set.ls53. Teacher page: "Khóa học · course plan" (names, class release, each lesson: title, where it
ends, parts shown, real-life task, note, dialogues, video links) and "Lộ trình · their lessons" on each student.
Test: src/tests/t53.py (t44 selectors now say E1/E2).

VERSION 54 — the teacher's exercise types, made interactive (lesson.acts in the plan)
sub = swap-one-word drill (oral) · fix = build / transform the sentence, reusing z27Order (written) · reply = hear it,
choose the reply · tone = hear it, choose the tone marks (listening) · tf = short reading, tap a sentence for audio +
English, true/false (reading). Dialogues (lesson.dlg, "Name: Vietnamese | English", "# title | English"): tap a line
for audio + English, hear all, or play a role with your own lines hidden until you say them.
Bài 1 carries a full sample set modelled on Thầy Tâm's sample lesson "Xin lỗi, chị tên là gì?" — same teaching
points and exercise types, in sentences written for the app. Ben confirmed (17 Nov) that Thầy Tâm wrote his
sample lesson himself, so his own dialogues and sentences can go into the plan as they are. The samples use the
computer voice until recorded, and need his check. acts are edited in data/plan.json for now (the teacher page
keeps them on save and edits dialogues). Test: src/tests/t54.py.

VERSION 55 — cards: tap to record, tap to stop, record again
On the "say it" side of a card the microphone no longer starts by itself (it used to listen for 5 seconds as soon as
the card appeared). Now: "🎤 Tap to record" → "■ Tap to stop" → the result, and "↻ Record again" as often as wanted,
also after the answer is shown. No auto-stop on a pause (SPEECH.fast=60000 while recording; 20 s hard cap). Only the
last try is saved for the teacher, when the card is graded. If speech recognition gives up by itself, the card keeps
recording the sound until the learner taps stop and shows a player instead of "it heard".
Tests: src/tests/t55.py (no recognition) and t55b.py (recognition that fails at once). Not tested with real speech
recognition or on a phone.

VERSION 56 — one way to record everywhere: tap to record, tap to stop, try again
z56Btn(o) is the shared button (label, again, cap, start, interim, done). While it records: SPEECH.fast=60000 (no cut on
a pause), hard cap 20 s (45 s speaking topics, 60 s reading a paragraph, 15 s shadowing). If speech recognition ends by
itself with nothing heard, a plain MediaRecorder keeps recording until the tap (res.plain=true).
Now using it: recall (English → Vietnamese), unit say-it "🎤 Say it", first three minutes, shadowing, tongue twisters,
story "Read it", questions after a story (no longer starts by itself; "Show the answer" is there too), sound-lesson
sentence step (no longer starts by itself), speaking topics (record as often as you like; only the last one is sent,
when you tap "show an example").
z56Gate: the screens that listen by themselves (everyday question cards zCard, scenes zOpenScene, speak now z7Speak)
wait for a "🎤 Tap to answer" button while z52Stage()===1 (units 1–10, or pace "Slow and steady"); from stage 2 they
listen by themselves as before. Not gated: AI conversation, the timed say-it-three-times in writing (both call
zHear56), rapid fire and the games (they call listenFor directly).
Guards: listenFor wrapper clears a stale SPEECH.fast=60000; closeSheet stops any recording and sets SPEECH.fast=0
(this also fixes an old leak where "speak now" left SPEECH.fast at 1500 after closing).
Tests: src/tests/t56.py (run with "norec" = no speech recognition; without = recognition that fails at once) and
t56b.py (scene and question-card gates). t40 selector updated for the "Show me without speaking" label.
Not tested with real speech recognition or on a phone.

VERSION 57 — user guides, with pictures, for students and for the teacher
data/guide.json = both guides ({student, teacher}: sections of text, steps, lists, two-column rows and pictures).
Pictures: img/guide/*.jpg (14 screenshots of the real screens with a made-up student, "Anna").
To retake them after a design change: bash build.sh, then python3 src/tests/guide_shots.py (it seeds a local test
server; nothing real is used).
Student side: More → "Hướng dẫn · How the app works", a button at the bottom of Home, and the link …/#guide.
Teacher side: "Hướng dẫn · guide" button on the first page, with two tabs: For teachers / For students.
To change the wording, edit data/guide.json (no code change needed). Test: src/tests/t57.py.

VERSION 58 — "open everything" for one account
Teacher page → a student → "Lộ trình · their lessons" → tick "Open everything for this student" → Save. Stored as
rel.all=true in KV rl:<id>. In the app (z58All): z27N() = all units (B1 preview included), every lesson and graded
story open, the hidden tiles (Stories, Games, more ways to practise) shown, the weekly voice note on. Nothing is
marked as done and no progress changes. "Follow the class again" turns it off. Level checks still wait for a
finished level. Test: src/tests/t58.py.

TOOLS FOR THE NEXT CHAT (17 Nov) — src/tools/
build.sh  = builds index.html from src (uses the last commit as OLD), checks the script syntax, copies the site to
            /home/claude/site with the test hook (window.__T) and restarts the local test server on port 8890.
            It expects the repo at /home/claude/bens-tieng-viet; change R= at the top if it is somewhere else.
            Run it before every test in src/tests (each run gives a fresh server, so /api/setup works again).
chkst.py, recyc.py = story word check and word-recycling counts used when the stories were written.
Tests: python3 src/tests/tNN.py (Playwright, Chromium at /opt/pw-browsers/chromium-1243/chrome-linux64/chrome).
The frequency list for src/core/make.py is vn_word_frequencies.tsv from github.com/tabidots/vn-freqs.

VERSION 59 — new look and a Home hub (Ben: "too much, overwhelming; bigger boxes, colour, simple; a cartoon of the teacher saying welcome to your lesson")
Look: "Sáng · Bright" is the default (S.set.look59 = 'bright' | 'old'). It rides on the dusk skin (z19Skin returns 'dusk') and adds
data-look="bright" on <html>; all its CSS is under :root[data-look="bright"] at the end of v7.css. Font: Nunito (link added by JS).
Settings → Look still offers Night, Dusk and Classic (picking one sets look59='old').
Hub: new view 'hub' (#v-hub in sections.html, drawn by z59Hub). It is the landing page when the link has no #, and the first tab
(Trang chủ · Home). The Practice tab is hidden (the page is still at #prac and behind "Tất cả · All practice").
Order: Thầy Tâm's welcome (the cartoon from Z21TA, full body) → six tiles (Z59.tiles; a later block sets the action with
Z59.act[key]=fn; a tile with no action shows "Soon") → "Bài hôm nay · today's lesson" (z59Today): a ring with the level's percent,
bars for this lesson / the level / the week, Thầy's note for the student (rel.hw or lesson.note) when there is one, the 10/30/60/90
picker (S.set.mins) and Start (opens Today and presses its start button).
Today (#home) is unchanged except that, in the bright look, the mission, situations, outside listening and week panels fold under
one button (S.set.more59=1 keeps them open).

VERSION 60 — games on one clean screen (Wordwall idea: one set of words, many games)
z60Menu: pick a set (each open lesson = its units' words and sentences, plus "Tất cả · everything so far"), then a game.
Games: Match up (z60Match), Flash cards (z60Flash), Unjumble (z60Unj), Find the match (z60Find), Listen and choose (z60Listen).
Every game ends on the same screen: stars, score, time, play again, the same words in another game. Best scores: S.set.g60.
Other blocks add sets with Z60.extra.push(function(){ return [ {id,t,en,words:[{vi,en,ex,exen}],sents:[{vi,en}]} ] }).
z60Ears = the Nghe tile: the listening game for this lesson and for everything, story by ear, reps, listen-and-understand, playlist.
Test: src/tests/t60.py (hub + every game played to the end). Not tested: sound, a real phone.

VERSION 61 — stories you can read straight away
z61List (the Truyện tile): every story as a card, chapters as buttons, locked graded stories shown greyed with their unit.
z61Read(story, chapter): the text is visible from the start. Tap a word → a card with the word, its meaning, a play button, the whole
sentence with its English (tap to hear) and "+ Save to my cards" (S.w, the same store as before). "Nghe · play the story" reads it
sentence by sentence with the sentence lit; "English" shows the translation under each paragraph; "Slow" sets S.set.speed .75 / 1.
Questions fold open one at a time; "Xong" marks the chapter read (S.st[cid].n). Meanings: C6.gloss, topped up once with every core
unit word (z61Gloss). The Home "story of the week" loop (49) and the old #story page are unchanged.

VERSION 62 — Âm: letters and sounds as boards
data/sounds.json = letters (letter, sound name, example word), letter pairs, tones (with the Saigon contour path).
The vowel-pair boards come from C7.chart. z62Menu → z62Board(id, mode): Chạm · touch, Lật · one by one (swipe, arrows), Kiểm tra · test.
A tile plays its example word; once the sound itself has a recording (it.s, e.g. "bờ", "ia") that plays first (z62Play).
Seen and best: S.set.s62[boardId]. The 17 sound lessons (#van) are one tap below the boards.
Recording list: part "ab" (69 lines: sound names and vowel pairs on their own) is now FIRST in data/voice-lines.json.
record.html: a recording link with &part=ab opens straight on that part (any part id works).

VERSION 63 — Cảnh: tap-around scenes (from Thầy Tâm's "Ai? – Who?" sheets; Ben confirmed we may use them)
data/scenes.json: scenes (people with a "look", position, the action they are doing; actions; a model dialogue) and places.
Drawings are made in code: z63Person(look) draws a person (hair short / short2 / grey / bun / long / pony / kid, glasses, coat,
shirt colour), z63Bg / z63Fg the room, z63Svg the whole picture. To add a scene: add it to data/scenes.json; a new room needs a
case in z63Bg / z63Fg (otherwise it gets the classroom).
z63Scene(id, mode): Khám phá (tap a person: name tag, "Đây là …", "… đang …"), Kiểm tra (tap who you hear → "Đây là ai?" →
"… đang làm gì?", first-try score, S.set.s63[id].best), Mẫu câu (patterns, dialogue, every sentence, and the same words as a set
in the games: Z60.extra, set id 'S'+scene id). Three scenes built: family, hospital, school. Recording parts sc_fam, sc_hos,
sc_sch, sc_pl (55 lines) come right after "ab".

VERSION 64 — Mẫu câu: sentence builder, stage 1 of 5
z64Build: three structures (Đây là ai? · Đây là đâu? · … đang làm gì?). Tap a slot, pick a person / place / action, hear the
sentence; switch between Answer, Question and "…, phải không?". Words come from the scenes and data/scenes.json places.
Sentences made: S.set.b64 {n, seen}. Stages 2–5 are listed on the screen (from Thầy Tâm's "Structure 1" sheet) but not built.
Built sentences have no recording of their own: they play from word clips or the phone voice.
Test for 61–64: src/tests/t61.py.
NOT built: Google sign-in (needs a Google client ID that only Ben can create), more scenes, builder stages 2–5, new guide pictures.

VERSION 65 — six more scenes, better drawings, movement (Ben: "keep adding the next sections, keep making the pictures a bit better, add some animation")
Scenes: company, restaurant, transport (taxi), store, park, hotel added to data/scenes.json (9 in all), from the same "Ai? – Who?"
sheets. A person with "back":1 is drawn behind the furniture (z63Fg 'mid'); everyone else stands in front and is cut by 'top'.
z63Person: shading, eyebrows, hair shine, eye highlights, blinking (.z63eye), gentle breathing (.z63br), and new look options:
hat 'chef' | 'cap' | 'sun' (hatc = colour), tie (colour), apron, must (moustache), hc (hair colour).
Rooms (z63Bg / z63Fg) move: clock hands, clouds in the windows, the IV drip, chalk line, office chart, steam over the pot, taxi wheels
and road, sun rays, a bouncing ball, the desk bell. They use SVG <animate>, so they also run inside the small menu pictures.
Home: Thầy Tâm waves (an extra arm added in z59Tam), tile icons move a little; confetti (z60Conf) on any three-star result.
Scene menu is two columns on a phone.

VERSION 66 — sentence builder, stages 1 to 3 (nine structures)
z64Structs(D) lists the structures; each has slots, forms, opts, txt(), pic(), mk(values, form) → {p: parts, en}. To add one, add an
object there; the word lists are in data/scenes.json → build (things with their classifier, animals, rides, lands, goes).
Stage 1: Đây là ai? · Đây là đâu? · … đang làm gì?   Stage 2: Đó là cái gì? · Kia là con gì? · Đây là phương tiện gì?
Stage 3: … phải không? (jobs; with "Dạ phải" and "Không phải … không phải là …") · Anh là người nước nào? (eight flags, drawn in
Z64FL) · Em đến … để làm gì?
A stage opens after 10 different sentences in the stage before (S.set.b64.st[stage]); "Open it now" skips the wait (b64.open);
an "everything open" account has all three. Stages 4 and 5 (time and dates; prices, food, age) are named on the screen, not built.
Recording list: parts sc_com … sc_hot and sc_zb (builder questions, words and the stage-3 sentences) follow "ab". Total 5,196 lines.
Test: src/tests/t61.py covers all nine scenes and stages 1–3.

VERSION 67 — the games, lifted (Ben, after playing Match up on his iPhone: go through every game, better pictures and graphics,
make sure they all work, an elevated level)
Menu: two columns of cards, each with a drawn preview of the game (Z60G[].pv) and the stars you earned on that set.
Game bar: the game's icon and name, ✓ and ✗ counts that update as you play, a sound switch (S.set.fx60; z60Fx makes the chimes
with the Web Audio API, no files). Wrong answers also buzz on phones that support vibration.
Pictures: z60Pic puts every drawing in a soft colour tile; z60Take picks about two pictured words in three, so rounds look alive.
Match up: one grid, so a word and the meaning beside it are always the same height; each matched pair takes its own colour.
Flash cards: the card turns over in 3D; swipe a turned card right (got it) or left (again); "Card n of N".
Unjumble and the new Fill the gap (z60Gap, Điền từ) move whole words: z60Chunks keeps "cà phê", "Sài Gòn" and the like in one piece.
Find the match: coloured tiles, bigger picture clue. Listen and choose: a pulsing speaker.
End screen: Thầy Tâm with a speech bubble, stars, time and misses, confetti on three stars, the same words in another game.
All game buttons: touch-action manipulation (no double-tap zoom on an iPhone), no text selection, no grey tap flash.
Six games now: match, flash, unj, find, gap, listen. Test: src/tests/t60.py plays every one to the end.
Checked at phone size (393 px, touch) in the lab browser for anything running off the screen: games, listening corner, sound
boards, a scene check, the builder, the story reader. Not checked: a real iPhone, sound.
