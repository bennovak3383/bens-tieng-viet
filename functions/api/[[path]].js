// Cloudflare Pages Function: accounts, online saving, teacher view. Storage: one KV namespace bound as KV.
const J = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
const ALPH = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
function rnd(n) { const a = new Uint8Array(n); crypto.getRandomValues(a); let s = ''; for (let i = 0; i < n; i++) s += ALPH[a[i] % ALPH.length]; return s; }
const clean = (s, n) => String(s == null ? '' : s).replace(/[\u0000-\u001f]/g, ' ').slice(0, n);
async function student(env, request) {
  const code = clean(request.headers.get('X-Code') || '', 20).toUpperCase().replace(/[^A-Z0-9]/g, '');
  if (code.length < 8) return null;
  const u = await env.KV.get('u:' + code, 'json'); return u ? { id: u.id, name: u.name, code } : null;
}
async function teacher(env, request, url) {
  const k = clean(request.headers.get('X-Teacher') || url.searchParams.get('k') || '', 64);
  if (k.length < 16) return false; const t = await env.KV.get('cfg:teacher'); return !!t && t === k;
}
export async function onRequest(context) {
  const { request, env } = context; const url = new URL(request.url); const path = url.pathname.replace(/^\/api\/?/, '').replace(/\/$/, ''); const m = request.method;
  if (!env.KV) return J({ error: 'Storage is not connected yet.' }, 503);
  try {
    if (path === 'ping') return J({ ok: true });
    if (path === 'join' && m === 'POST') {
      const b = await request.json().catch(() => ({})); const name = clean(b.name, 40) || 'Student';
      const id = rnd(10), code = rnd(8);
      await env.KV.put('u:' + code, JSON.stringify({ id, name, created: Date.now() }));
      await env.KV.put('s:' + id, '{}', { metadata: { n: name, last: Date.now(), sum: {} } });
      return J({ id, code, name });
    }
    if (path === 'state') {
      const s = await student(env, request); if (!s) return J({ error: 'That code was not found.' }, 401);
      if (m === 'GET') { const [st, notes] = await Promise.all([env.KV.get('s:' + s.id, 'json'), env.KV.get('n:' + s.id, 'json')]); return J({ id: s.id, name: s.name, state: st || {}, notes: notes || [] }); }
      if (m === 'PUT') {
        const text = await request.text(); if (text.length > 3_000_000) return J({ error: 'Too large.' }, 413);
        let st; try { st = JSON.parse(text); } catch (e) { return J({ error: 'Bad data.' }, 400); }
        let sum = {}; try { sum = JSON.parse(decodeURIComponent(request.headers.get('X-Sum') || '%7B%7D')); } catch (e) {}
        const name = clean((st.me && st.me.name) || s.name, 40);
        const safe = {}; for (const k of ['d', 'fc', 'q', 'van', 'st', 'sp', 'day']) if (typeof sum[k] === 'number') safe[k] = sum[k];
        await env.KV.put('s:' + s.id, text, { metadata: { n: name, last: Date.now(), sum: safe } });
        return J({ ok: true });
      }
    }
    if (path === 'rec' && m === 'POST') {
      const s = await student(env, request); if (!s) return J({ error: 'That code was not found.' }, 401);
      const buf = await request.arrayBuffer(); if (!buf.byteLength || buf.byteLength > 1_500_000) return J({ error: 'Recording too large.' }, 413);
      let meta = {}; try { meta = JSON.parse(decodeURIComponent(request.headers.get('X-Meta') || '%7B%7D')); } catch (e) {}
      const md = { t: Date.now(), k: clean(meta.kind, 12), ref: clean(meta.ref, 40), tg: clean(meta.target, 80), hd: clean(meta.heard, 80), pr: clean(meta.prompt, 60), ok: meta.ok ? 1 : 0, sc: Number(meta.score) || 0, ms: Number(meta.ms) || 0, ty: clean(request.headers.get('Content-Type') || 'audio/webm', 40) };
      const key = 'r:' + s.id + ':' + String(9999999999999 - md.t).padStart(13, '0');   // newest first when listed
      await env.KV.put(key, buf, { metadata: md, expirationTtl: 60 * 60 * 24 * 90 });
      return J({ ok: true });
    }

    if (path === 'chat' && m === 'POST') {
      const s = await student(env, request); if (!s) return J({ error: 'Sign in with your code first.', code: 'signin' }, 401);
      if (!env.ANTHROPIC_API_KEY && !env.OPENAI_API_KEY) return J({ error: 'AI conversation is not connected on this website yet.', code: 'nokey' }, 503);
      if (!(await env.KV.get('a:' + s.id))) return J({ error: 'AI conversation is not turned on for you yet. Ask your teacher to switch it on.', code: 'off' }, 403);
      const day = new Date().toISOString().slice(0, 10), ck = 'c:' + s.id + ':' + day, used = parseInt((await env.KV.get(ck)) || '0', 10) || 0, cap = parseInt(env.CHAT_DAILY || '200', 10) || 200;
      if (used >= cap) return J({ error: 'That is the limit for today (' + cap + ' turns). Come back tomorrow.', code: 'cap' }, 429);
      const b = await request.json().catch(() => ({}));
      const hist = (Array.isArray(b.history) ? b.history : []).slice(-16).map(t => ({ role: t.role === 'assistant' ? 'assistant' : 'user', content: clean(t.content, 400) })).filter(t => t.content);
      if (!hist.length || hist[0].role !== 'user') hist.unshift({ role: 'user', content: '(start the conversation)' });
      const you = clean(b.you, 12) || 'anh', them = clean(b.them, 12) || 'em', name = clean(b.name, 30) || 'the learner';
      const mode = b.mode === 'hint' ? 'hint' : 'talk', open = !!b.open;
      const system = [
        'You are a friendly Vietnamese conversation partner for a beginner (level A1 to A2) who lives in Ho Chi Minh City.',
        'Scene: ' + (clean(b.scene, 400) || 'Free small talk about daily life.'),
        'Speak natural Southern (Saigon) Vietnamese: dạ, nha, hông/không, mắc, quẹo, coi, vô, trễ. Use only very common words.',
        'The learner is called ' + name + '. Call the learner "' + you + '" and call yourself "' + them + '".',
        open
          ? 'Rules: reply with ONE or TWO short sentences, at most 18 words in total. React to what the learner said, add a little about yourself, then ask ONE follow-up question so the conversation keeps going. Follow the learner\'s topic, whatever it is, and never end the conversation yourself.'
          : 'Rules: reply with ONE or TWO short sentences, at most 12 words in total, and usually end with ONE simple question so the learner has something to answer. Stay in the scene.',
        'Keep talking in Vietnamese. Do not give in to English: if the learner seems lost, first say it again in simpler Vietnamese. Never write English inside "vi".',
        'If the learner writes in English, or asks what something means or how to say something: answer that briefly in English in "help" (at most 30 words, include the Vietnamese words they need), then carry on the conversation in Vietnamese in "vi". Otherwise leave "help" empty.',
        'Correct lightly: fill "fix" only when a mistake changes or hides the meaning, or is a very common beginner error. Ignore small slips. Most turns "fix" should be empty. Never correct an English question.',
        'The learner\'s lines come from speech recognition, so ignore missing tone marks and small recognition errors; only correct real mistakes in grammar or word choice.',
        'Do not think out loud and do not explain. Output the JSON object only, no words before or after it. Keep "note" under 15 words.',
        mode === 'hint'
          ? 'TASK NOW: do not continue the conversation. Give the learner two short things THEY could say next, as a JSON object: {"hints":[{"vi":"...","en":"..."},{"vi":"...","en":"..."}]}'
          : 'Reply ONLY with a JSON object and nothing else: {"vi":"your reply in Vietnamese","en":"English translation of your reply","fix":"the learner\'s last line rewritten correctly in Vietnamese, or an empty string","note":"one short tip in English about that fix, or an empty string","help":"a short English answer if the learner asked something in English, or an empty string"}'
      ].join('\n');
      let text = '';
      if (env.ANTHROPIC_API_KEY) {
        const models = [env.AI_MODEL || 'claude-haiku-5-5', 'claude-haiku-4-5']; let r = null;
        for (const model of models) {
          r = await fetch('https://api.anthropic.com/v1/messages', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' }, body: JSON.stringify({ model, max_tokens: 2000, system, messages: hist }) });
          if (r.status !== 404 && r.status !== 400) break;
        }
        if (!r.ok) return J({ error: r.status === 401 ? 'The AI key was not accepted. Check the key in Cloudflare.' : (r.status === 429 || r.status === 529 ? 'The AI is busy. Try again in a moment.' : 'The AI did not answer (' + r.status + ').'), code: 'ai' }, 502);
        const j = await r.json(); text = (j.content || []).map(c => c.text || '').join('');
      } else {
        const r = await fetch('https://api.openai.com/v1/chat/completions', { method: 'POST', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + env.OPENAI_API_KEY }, body: JSON.stringify({ model: env.AI_MODEL || 'gpt-4o-mini', max_tokens: 2000, messages: [{ role: 'system', content: system }].concat(hist) }) });
        if (!r.ok) return J({ error: r.status === 401 ? 'The AI key was not accepted. Check the key in Cloudflare.' : 'The AI did not answer (' + r.status + ').', code: 'ai' }, 502);
        const j = await r.json(); text = (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '';
      }
      let out = null; const a = text.indexOf('{'), z = text.lastIndexOf('}');
      if (a >= 0 && z > a) { try { out = JSON.parse(text.slice(a, z + 1)); } catch (e) {} }
      if (!out && mode !== 'hint') {   // cut-off or untidy reply: pull the fields out by hand
        const pick = (k) => { const m = text.match(new RegExp('"' + k + '"\\s*:\\s*"((?:[^"\\\\]|\\\\.)*)"')); if (!m) return ''; try { return JSON.parse('"' + m[1] + '"'); } catch (e) { return m[1]; } };
        const vi = pick('vi'); if (vi) out = { vi, en: pick('en'), fix: pick('fix'), note: pick('note'), help: pick('help') };
        else if (text && text.indexOf('{') < 0) out = { vi: clean(text, 200), en: '', fix: '', note: '' };
      }
      if (!out) { if (mode === 'hint') out = { hints: [] }; else return J({ error: 'The AI answer came back garbled. Tap Speak or press Enter to try again.', code: 'ai' }, 502); }
      if (mode !== 'hint' && !clean(out.vi, 240)) return J({ error: 'The AI answer came back empty. Try again.', code: 'ai' }, 502);
      context.waitUntil(env.KV.put(ck, String(used + 1), { expirationTtl: 60 * 60 * 48 }));
      if (mode === 'hint') return J({ hints: (Array.isArray(out.hints) ? out.hints : []).slice(0, 3).map(x => ({ vi: clean(x && x.vi, 120), en: clean(x && x.en, 120) })) });
      return J({ vi: clean(out.vi, 240), en: clean(out.en, 240), fix: clean(out.fix, 200), note: clean(out.note, 200), help: clean(out.help, 300), left: cap - used - 1 });
    }

    // 10: writing practice. wi:ID = list of pieces (newest first), wp:ID:t = photo (data URL), wv:ID:t = teacher voice reply
    if (path === 'w') {
      const s = await student(env, request); if (!s) return J({ error: 'Sign in with your code first (Progress page).', code: 'signin' }, 401);
      if (m === 'GET') return J({ items: (await env.KV.get('wi:' + s.id, 'json')) || [] });
      if (m === 'POST') {
        const text = await request.text(); if (text.length > 2_500_000) return J({ error: 'Too large. Try the photo again a little further away.' }, 413);
        let b; try { b = JSON.parse(text); } catch (e) { return J({ error: 'Bad data.' }, 400); }
        const t = Date.now(), lines = (Array.isArray(b.lines) ? b.lines : []).slice(0, 12).map(x => clean(x, 300).trim()).filter(Boolean);
        const photo = (typeof b.photo === 'string' && /^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(b.photo)) ? b.photo : '';
        if (!lines.length && !photo) return J({ error: 'Nothing to send yet.' }, 400);
        const item = { t, q: clean(b.q, 200), qEn: clean(b.qEn, 200), mode: b.mode === 'type' ? 'type' : 'hand', lines, photo: !!photo, recs: Math.min(10, Number(b.recs) || 0) };
        if (photo) await env.KV.put('wp:' + s.id + ':' + t, photo, { expirationTtl: 60 * 60 * 24 * 180 });
        const items = (await env.KV.get('wi:' + s.id, 'json')) || []; items.unshift(item);
        await env.KV.put('wi:' + s.id, JSON.stringify(items.slice(0, 100)));
        return J({ ok: true, t });
      }
    }
    if (path === 'w-voice' && m === 'GET') {
      const s = await student(env, request); if (!s) return J({ error: 'Sign in first.' }, 401);
      const t = parseInt(url.searchParams.get('t') || '0', 10); const r = await env.KV.getWithMetadata('wv:' + s.id + ':' + t, 'arrayBuffer');
      if (!r.value) return J({ error: 'Not found.' }, 404);
      return new Response(r.value, { headers: { 'Content-Type': (r.metadata && r.metadata.ty) || 'audio/webm', 'Cache-Control': 'private, max-age=3600' } });
    }
    if (path === 'words' && m === 'GET') { const w = await env.KV.get('cfg:words', 'json'); return J(w || { e: {}, d: {}, a: [] }); }
    if (path === 'setup' && m === 'POST') {
      if (await env.KV.get('cfg:teacher')) return J({ error: 'Teacher access is already set up.' }, 409);
      const k = rnd(24); await env.KV.put('cfg:teacher', k); return J({ key: k });
    }
    if (path.startsWith('t/')) {
      if (!(await teacher(env, request, url))) return J({ error: 'Teacher link not recognised.' }, 401);
      if (path === 't/students') { const l = await env.KV.list({ prefix: 's:', limit: 1000 }); return J({ students: l.keys.map(k => ({ id: k.name.slice(2), ...(k.metadata || {}) })) }); }
      if (path === 't/words' && m === 'POST') {
        const b = await request.json().catch(() => null); if (!b || typeof b !== 'object') return J({ error: 'Bad data.' }, 400);
        const row = r => [clean(r[0], 80).trim(), clean(r[1], 120).trim(), clean(r[2], 160).trim(), clean(r[3], 200).trim()];
        const out = { e: {}, d: {}, a: [], t: Date.now() };
        for (const k of Object.keys(b.e || {}).slice(0, 2000)) { const r = b.e[k]; if (Array.isArray(r) && r.length === 4) { const v = row(r); if (v[0] && v[1]) out.e[clean(k, 24)] = v; } }
        for (const k of Object.keys(b.d || {}).slice(0, 2000)) if (b.d[k]) out.d[clean(k, 24)] = 1;
        for (const r of (Array.isArray(b.a) ? b.a : []).slice(0, 600)) { if (!r || typeof r !== 'object') continue; const v = row([r.vi, r.en, r.xv, r.xe]); const id = clean(r.id, 24).replace(/[^a-z0-9_]/gi, ''); if (v[0] && v[1] && /^tw/.test(id)) out.a.push({ id, vi: v[0], en: v[1], xv: v[2], xe: v[3] }); }
        await env.KV.put('cfg:words', JSON.stringify(out)); return J({ ok: true, words: out });
      }
      const id = clean(url.searchParams.get('id') || '', 12).replace(/[^A-Z0-9]/g, '');
      if (path === 't/student') {
        const [st, notes, recs, ai, wi] = await Promise.all([env.KV.get('s:' + id, 'json'), env.KV.get('n:' + id, 'json'), env.KV.list({ prefix: 'r:' + id + ':', limit: 300 }), env.KV.get('a:' + id), env.KV.get('wi:' + id, 'json')]);
        if (st == null) return J({ error: 'No such student.' }, 404);
        return J({ id, state: st, notes: notes || [], ai: !!ai, aiReady: !!(env.ANTHROPIC_API_KEY || env.OPENAI_API_KEY), recs: recs.keys.map(k => ({ key: k.name, ...(k.metadata || {}) })), writing: wi || [] });
      }

      if (path === 't/w-photo') {
        const t = parseInt(url.searchParams.get('t') || '0', 10); const p = await env.KV.get('wp:' + id + ':' + t);
        return p ? J({ photo: p }) : J({ error: 'Photo not found (photos are kept 180 days).' }, 404);
      }
      if (path === 't/w-voice' && m === 'GET') {
        const t = parseInt(url.searchParams.get('t') || '0', 10); const r = await env.KV.getWithMetadata('wv:' + id + ':' + t, 'arrayBuffer');
        if (!r.value) return J({ error: 'Not found.' }, 404);
        return new Response(r.value, { headers: { 'Content-Type': (r.metadata && r.metadata.ty) || 'audio/webm', 'Cache-Control': 'no-store' } });
      }
      if ((path === 't/w-reply' || path === 't/w-voice' || path === 't/w-del') && m === 'POST') {
        const t = parseInt(url.searchParams.get('t') || '0', 10);
        const items = (await env.KV.get('wi:' + id, 'json')) || []; const it = items.find(x => x.t === t); if (!it) return J({ error: 'That piece of writing was not found.' }, 404);
        if (path === 't/w-del') {
          const rest = items.filter(x => x.t !== t);
          await Promise.all([rest.length ? env.KV.put('wi:' + id, JSON.stringify(rest)) : env.KV.delete('wi:' + id), env.KV.delete('wp:' + id + ':' + t), env.KV.delete('wv:' + id + ':' + t)]);
          return J({ ok: true, writing: rest });
        }
        it.reply = it.reply || {};
        if (path === 't/w-reply') { const b = await request.json().catch(() => ({})); it.reply.text = clean(b.text, 1500); it.reply.t = Date.now(); }
        else {
          const buf = await request.arrayBuffer(); if (!buf.byteLength || buf.byteLength > 1_500_000) return J({ error: 'Recording too large (keep it under about a minute).' }, 413);
          await env.KV.put('wv:' + id + ':' + t, buf, { metadata: { ty: clean(request.headers.get('Content-Type') || 'audio/webm', 40) }, expirationTtl: 60 * 60 * 24 * 180 });
          it.reply.voice = true; it.reply.t = Date.now();
        }
        it.seen = 0; await env.KV.put('wi:' + id, JSON.stringify(items));
        return J({ ok: true, writing: items });
      }
      if (path === 't/audio') {
        const key = clean(url.searchParams.get('key') || '', 60); if (!/^r:[A-Z0-9]+:\d+$/.test(key)) return J({ error: 'Bad key.' }, 400);
        const r = await env.KV.getWithMetadata(key, 'arrayBuffer'); if (!r.value) return J({ error: 'Recording not found.' }, 404);
        return new Response(r.value, { headers: { 'Content-Type': (r.metadata && r.metadata.ty) || 'audio/webm', 'Cache-Control': 'private, max-age=3600' } });
      }
      if (path === 't/ai' && m === 'POST') {
        const b = await request.json().catch(() => ({})); const sid = clean(b.id, 12).replace(/[^A-Z0-9]/g, ''); if (!sid || (await env.KV.get('s:' + sid)) == null) return J({ error: 'No such student.' }, 404);
        if (b.on) await env.KV.put('a:' + sid, '1'); else await env.KV.delete('a:' + sid);
        return J({ ok: true, ai: !!b.on });
      }
      if (path === 't/note' && m === 'POST') {
        const b = await request.json().catch(() => ({})); const sid = clean(b.id, 12).replace(/[^A-Z0-9]/g, ''); const text = clean(b.text, 600); if (!sid || !text) return J({ error: 'Nothing to save.' }, 400);
        if ((await env.KV.get('s:' + sid)) == null) return J({ error: 'No such student.' }, 404);
        const notes = (await env.KV.get('n:' + sid, 'json')) || []; notes.unshift({ t: Date.now(), text, about: clean(b.about, 140) }); await env.KV.put('n:' + sid, JSON.stringify(notes.slice(0, 200)));
        return J({ ok: true, notes: notes.slice(0, 200) });
      }
      if (path === 't/note-del' && m === 'POST') {
        const b = await request.json().catch(() => ({})); const sid = clean(b.id, 12).replace(/[^A-Z0-9]/g, ''); if (!sid) return J({ error: 'No such student.' }, 404);
        let notes = (await env.KV.get('n:' + sid, 'json')) || []; notes = b.all ? [] : notes.filter(n => n.t !== b.t);
        if (notes.length) await env.KV.put('n:' + sid, JSON.stringify(notes)); else await env.KV.delete('n:' + sid);
        return J({ ok: true, notes });
      }
      if (path === 't/rec-del' && m === 'POST') {
        const b = await request.json().catch(() => ({})); const sid = clean(b.id, 12).replace(/[^A-Z0-9]/g, ''); if (!sid) return J({ error: 'No such student.' }, 404);
        if (b.all) { const l = await env.KV.list({ prefix: 'r:' + sid + ':', limit: 200 }); await Promise.all(l.keys.map(k => env.KV.delete(k.name))); return J({ ok: true, more: !l.list_complete }); }
        const key = clean(b.key, 60); if (!/^r:[A-Z0-9]+:\d+$/.test(key) || key.indexOf('r:' + sid + ':') !== 0) return J({ error: 'Bad key.' }, 400);
        await env.KV.delete(key); return J({ ok: true });
      }
      if (path === 't/student-del' && m === 'POST') {
        const b = await request.json().catch(() => ({})); const sid = clean(b.id, 12).replace(/[^A-Z0-9]/g, ''); if (!sid) return J({ error: 'No such student.' }, 404);
        const l = await env.KV.list({ prefix: 'r:' + sid + ':', limit: 200 }); await Promise.all(l.keys.map(k => env.KV.delete(k.name)));
        if (!l.list_complete) return J({ ok: true, more: true });
        const c = await env.KV.list({ prefix: 'c:' + sid + ':', limit: 100 }); await Promise.all(c.keys.map(k => env.KV.delete(k.name)));
        const us = await env.KV.list({ prefix: 'u:', limit: 1000 });
        for (const k of us.keys) { const u = await env.KV.get(k.name, 'json'); if (u && u.id === sid) await env.KV.delete(k.name); }
        for (const pre of ['wp:', 'wv:']) { const w = await env.KV.list({ prefix: pre + sid + ':', limit: 200 }); await Promise.all(w.keys.map(k => env.KV.delete(k.name))); }
        await Promise.all([env.KV.delete('n:' + sid), env.KV.delete('a:' + sid), env.KV.delete('s:' + sid), env.KV.delete('wi:' + sid)]);
        return J({ ok: true, more: false });
      }
    }
    return J({ error: 'Not found.' }, 404);
  } catch (e) { return J({ error: 'Something went wrong on the server.' }, 500); }
}
