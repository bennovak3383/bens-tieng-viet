# Ben's Tiếng Việt

A Vietnamese speaking app (Southern / Saigon accent): sound lessons, Sharp ears, picture cards, Speak now (both ways), Write it say it, stories, scenes, AI conversation, and a teacher page.

- Live: https://bens-tieng-viet.pages.dev · teacher page: /teacher.html (needs the private teacher key)
- Hosting: Cloudflare Pages, project `bens-tieng-viet`. Every commit to `main` goes live in about a minute. No build step on Cloudflare.

## What is where
- `index.html` — the whole app (about 0.7 MB).
- `teacher.html` — teacher page.
- `functions/api/[[path]].js` — the server (Cloudflare Pages Function, Workers KV bound as `KV`).
- `audio/index.json` + `a00–a13.mp3`, `m00–m11.mp3` — voice clips, found by byte position. Never add anything to the front of a bundle.
- `audio/e6a.b64`, `e6b.b64` — more clips, stored as base64 text on purpose (binary files saved on a Mac get a header added).
- `src/` — the build source (v7 layer, content scripts, TTS scripts, local test server, tests). Read `src/README-10.txt` first.

## How to change the app
1. Edit `src/v7/v7.js`, `v7.css` or `sections.html`.
2. Run `python3 src/patch10.py OLD_SRC src index.html OUT` (OLD_SRC = a copy of `src/` from before your edit) to swap the new files into `index.html`.
3. Test with `src/site8/devserver.mjs` and the Playwright scripts in `src/tests/`.
4. Commit. Cloudflare puts it live.

Secrets (AI key) live in Cloudflare only, never in this repo.

## Recording lines (native speakers)
- `data/voice-lines.json` is the list speakers record from. It is built from the app's own content by `python3 src/voice/make_lines.py .` — **run it again after any change to the words, phrases, situations or stories** and commit the result. The recording page picks up the new list straight away.
- Recordings count by their words, not by line number, so rebuilding the list never loses one. A changed line becomes a gap again; a new line is a gap; a removed line just drops off the list.
- Approved speaker fixes: `GET /api/voice/linefix` lists them (old → new wording). Put the new wording into the app content, then rebuild the list.

## English with Ben (An's English app)
- Live at `/english/`. A separate vocabulary app: spaced-review cards (53 decks), eight games, speaking prompts and a page for Ben.
- `english/index.html` is the whole app; `english/img/` holds its photos and the painted pictures it reuses from `img/p/`.
- Home page cover: the `PH` list in `english/index.html` sets the cover pictures (`english/img/an-N.jpg`), their caption and where An's face is in each (x, y as a share of the picture); `fitH` zooms and shifts each picture so her face sits in the middle of the cover. Cartoon pictures only: Ben does not want real photos of An on the site.
- No server part yet: progress is kept in the browser (localStorage key `ewb2`). It shares nothing with the Vietnamese app.
- Sign-in gate: `functions/english/_middleware.js` asks for a code once per device before serving anything under `/english/` (cookie `en_in`, one year). Only the code's hash is in the file; an `ENGLISH_CODE` variable on the Pages project overrides it. Wrong tries are limited to 10 per 10 minutes per address (KV keys `en:try:`). The gate covers the site only: while this repo is public, the files in `english/` can still be read on GitHub.
- Voices: `english/audio/` holds one clip per word (`NNNw.mp3`) and per example sentence (`NNNs.mp3`), listed in `english/audio/index.json` by their text. Made with Kokoro (voices af_heart and am_michael, alternating by card).
- The site's offline worker (`sw.js`) saves pictures the first time they load and never refreshes them, so give a changed picture a new file name.

## Zelus (training and food log) — taken off the site for now
- Removed on 2026-11-19 at Ben's request, to come back later in its own home. The last version is in git history: commit `3820409` has `zelus/` and `functions/zelus/`.
- Its saved data was not touched: it is still in the `KV` namespace under keys starting `zl:`.
