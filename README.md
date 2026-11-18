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

## Zelus (training and food log) — temporary home
- Live at `/zelus/`. A separate app that lives here until it moves to its own repo and Pages project.
- `zelus/` — the whole app (`index.html`), its own offline worker (`sw.js`, scoped to `/zelus/` only) and icons.
- `functions/zelus/api/[[path]].js` — its server. Uses this project's `KV` binding with every key prefixed `zl:`, so it never touches the Vietnamese app's data. If a namespace is bound as `ZELUS` it uses that instead, with no prefix.
- Meal estimates use the same `ANTHROPIC_API_KEY`. Optional `INVITE` variable limits who can create an account.
- Nothing in `zelus/` depends on the Vietnamese app, and the reverse.
