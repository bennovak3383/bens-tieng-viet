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
      const mode = b.mode === 'hint' ? 'hint' : 'talk';
      const system = [
        'You are a friendly Vietnamese conversation partner for a beginner (level A1 to A2) who lives in Ho Chi Minh City.',
        'Scene: ' + (clean(b.scene, 400) || 'Free small talk about daily life.'),
        'Speak natural Southern (Saigon) Vietnamese: dạ, nha, hông/không, mắc, quẹo, coi, vô, trễ. Use only very common words.',
        'The learner is called ' + name + '. Call the learner "' + you + '" and call yourself "' + them + '".',
        'Rules: reply with ONE or TWO short sentences, at most 12 words in total, and usually end with ONE simple question so the learner has something to answer. Never switch to English in "vi". Stay in the scene. If the learner is silent or says they do not understand, say the same thing again in simpler words.',
        'The learner\'s lines come from speech recognition, so ignore missing tone marks and small recognition errors; only correct real mistakes in grammar or word choice.',
        mode === 'hint'
          ? 'TASK NOW: do not continue the conversation. Give the learner two short things THEY could say next, as a JSON object: {"hints":[{"vi":"...","en":"..."},{"vi":"...","en":"..."}]}'
          : 'Reply ONLY with a JSON object and nothing else: {"vi":"your reply in Vietnamese","en":"English translation of your reply","fix":"the learner\'s last line rewritten correctly in Vietnamese, or an empty string if it was fine or there was no line","note":"one short tip in English about that fix, or an empty string"}'
      ].join('\n');
      let text = '';
      if (env.ANTHROPIC_API_KEY) {
        const models = [env.AI_MODEL || 'claude-haiku-5-5', 'claude-haiku-4-5']; let r = null;
        for (const model of models) {
          r = await fetch('https://api.anthropic.com/v1/messages', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' }, body: JSON.stringify({ model, max_tokens: 400, system, messages: hist }) });
          if (r.status !== 404 && r.status !== 400) break;
        }
        if (!r.ok) return J({ error: r.status === 401 ? 'The AI key was not accepted. Check the key in Cloudflare.' : (r.status === 429 || r.status === 529 ? 'The AI is busy. Try again in a moment.' : 'The AI did not answer (' + r.status + ').'), code: 'ai' }, 502);
        const j = await r.json(); text = (j.content || []).map(c => c.text || '').join('');
      } else {
        const r = await fetch('https://api.openai.com/v1/chat/completions', { method: 'POST', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + env.OPENAI_API_KEY }, body: JSON.stringify({ model: env.AI_MODEL || 'gpt-4o-mini', max_tokens: 400, messages: [{ role: 'system', content: system }].concat(hist) }) });
        if (!r.ok) return J({ error: r.status === 401 ? 'The AI key was not accepted. Check the key in Cloudflare.' : 'The AI did not answer (' + r.status + ').', code: 'ai' }, 502);
        const j = await r.json(); text = (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '';
      }
      let out = null; const a = text.indexOf('{'), z = text.lastIndexOf('}');
      if (a >= 0 && z > a) { try { out = JSON.parse(text.slice(a, z + 1)); } catch (e) {} }
      if (!out) out = mode === 'hint' ? { hints: [] } : { vi: clean(text, 200), en: '', fix: '', note: '' };
      context.waitUntil(env.KV.put(ck, String(used + 1), { expirationTtl: 60 * 60 * 48 }));
      if (mode === 'hint') return J({ hints: (Array.isArray(out.hints) ? out.hints : []).slice(0, 3).map(x => ({ vi: clean(x && x.vi, 120), en: clean(x && x.en, 120) })) });
      return J({ vi: clean(out.vi, 240), en: clean(out.en, 240), fix: clean(out.fix, 200), note: clean(out.note, 200), left: cap - used - 1 });
    }
    if (path === 'setup' && m === 'POST') {
      if (await env.KV.get('cfg:teacher')) return J({ error: 'Teacher access is already set up.' }, 409);
      const k = rnd(24); await env.KV.put('cfg:teacher', k); return J({ key: k });
    }
    if (path.startsWith('t/')) {
      if (!(await teacher(env, request, url))) return J({ error: 'Teacher link not recognised.' }, 401);
      if (path === 't/students') { const l = await env.KV.list({ prefix: 's:', limit: 1000 }); return J({ students: l.keys.map(k => ({ id: k.name.slice(2), ...(k.metadata || {}) })) }); }
      const id = clean(url.searchParams.get('id') || '', 12).replace(/[^A-Z0-9]/g, '');
      if (path === 't/student') {
        const [st, notes, recs, ai] = await Promise.all([env.KV.get('s:' + id, 'json'), env.KV.get('n:' + id, 'json'), env.KV.list({ prefix: 'r:' + id + ':', limit: 300 }), env.KV.get('a:' + id)]);
        if (st == null) return J({ error: 'No such student.' }, 404);
        return J({ id, state: st, notes: notes || [], ai: !!ai, aiReady: !!(env.ANTHROPIC_API_KEY || env.OPENAI_API_KEY), recs: recs.keys.map(k => ({ key: k.name, ...(k.metadata || {}) })) });
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
    }
    return J({ error: 'Not found.' }, 404);
  } catch (e) { return J({ error: 'Something went wrong on the server.' }, 500); }
}
