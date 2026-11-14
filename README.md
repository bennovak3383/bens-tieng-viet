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
