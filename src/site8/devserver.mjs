import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { onRequest } from './functions/api/[[path]].js';
class KV { constructor(){ this.m=new Map() }
  async get(k,t){ const v=this.m.get(k); if(!v) return null; const s=typeof v.v==='string'?v.v:null; if(t==='json') return JSON.parse(s??new TextDecoder().decode(v.v)); if(t==='arrayBuffer') return v.v; return s??new TextDecoder().decode(v.v) }
  async getWithMetadata(k){ const v=this.m.get(k); return {value:v?v.v:null,metadata:v?v.md:null} }
  async delete(k){ this.m.delete(k) }
  async put(k,v,o){ if(o&&o.metadata&&Buffer.byteLength(JSON.stringify(o.metadata))>1024) throw new Error('metadata too big'); this.m.set(k,{v,md:o&&o.metadata}) }
  async list({prefix,limit}){ return {keys:[...this.m.keys()].filter(k=>k.startsWith(prefix)).sort().slice(0,limit||1000).map(k=>({name:k,metadata:this.m.get(k).md})),list_complete:[...this.m.keys()].filter(k=>k.startsWith(prefix)).length<=(limit||1000)} } }
const env={KV:new KV(),ANTHROPIC_API_KEY:'test'}; const rf=globalThis.fetch; let n=0; globalThis.fetch=async(u,o)=>{ if(String(u).includes('api.anthropic.com')){ const b=JSON.parse(o.body); const hint=b.system.includes('TASK NOW'); const lines=['Chào anh! Anh uống gì?','Dạ, nóng hay đá anh?','Dạ, ba mươi ngàn nha anh.']; const txt=hint?'{"hints":[{"vi":"Cho tôi một ly cà phê sữa đá.","en":"An iced milk coffee, please."},{"vi":"Có trà đá không?","en":"Do you have iced tea?"}]}':JSON.stringify({vi:lines[n++%3],en:'(English here)',fix:b.messages.length>1?'Cho tôi một ly cà phê.':'',note:b.messages.length>1?'Add the counter word ly.':''}); return new Response(JSON.stringify({content:[{type:'text',text:txt}]}),{status:200}) } return rf(u,o) }; const T={'.html':'text/html; charset=utf-8','.json':'application/json','.mp3':'audio/mpeg','.js':'text/javascript'};
http.createServer(async (req,res)=>{ const u=new URL(req.url,'http://localhost:8890');
  if(u.pathname.startsWith('/api/')){ const chunks=[]; for await(const c of req) chunks.push(c); const body=Buffer.concat(chunks);
    const r=await onRequest({request:new Request(u,{method:req.method,headers:req.headers,body:['GET','HEAD'].includes(req.method)?undefined:body}),env,waitUntil:(p)=>p}); res.writeHead(r.status,Object.fromEntries(r.headers)); res.end(Buffer.from(await r.arrayBuffer())); return }
  let f=path.join('.',u.pathname==='/'?'index.html':decodeURIComponent(u.pathname)); if(!path.extname(f)&&fs.existsSync(f+'.html')) f+='.html';
  if(!fs.existsSync(f)){ res.writeHead(404); res.end('nf'); return } res.writeHead(200,{'Content-Type':T[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(res) }).listen(8890);
