import { onRequest } from './functions/api/[[path]].js';
class KV { constructor(){ this.m=new Map() }
  async get(k,t){ const v=this.m.get(k); if(!v) return null; if(t==='json') return JSON.parse(typeof v.v==='string'?v.v:new TextDecoder().decode(v.v)); if(t==='arrayBuffer') return v.v; return typeof v.v==='string'?v.v:new TextDecoder().decode(v.v) }
  async getWithMetadata(k,t){ const v=this.m.get(k); return {value:v?v.v:null,metadata:v?v.md:null} }
  async put(k,v,o){ this.m.set(k,{v,md:o&&o.metadata}) }
  async delete(k){ this.m.delete(k) }
  async list({prefix,limit}){ return {keys:[...this.m.keys()].filter(k=>k.startsWith(prefix)).sort().slice(0,limit||1000).map(k=>({name:k,metadata:this.m.get(k).md}))} } }
const env={KV:new KV()};
const call=async(p,o={})=>{ const r=await onRequest({request:new Request('https://x.test/api/'+p,o),env,waitUntil:(p)=>p}); const ct=r.headers.get('Content-Type'); return {s:r.status,b:ct.includes('json')?await r.json():(await r.arrayBuffer()).byteLength} };
let r=await call('join',{method:'POST',body:JSON.stringify({name:'Ben'})}); console.log('join',r.s,Object.keys(r.b)); const code=r.b.code,id=r.b.id;
r=await call('state',{headers:{'X-Code':'WRONG123'}}); console.log('bad code',r.s);
r=await call('state',{method:'PUT',headers:{'X-Code':code.toLowerCase(),'X-Sum':encodeURIComponent(JSON.stringify({d:3,fc:12}))},body:JSON.stringify({me:{name:'Ben'},updatedAt:5,q:{a:1}})}); console.log('put',r.s,r.b);
r=await call('state',{headers:{'X-Code':code}}); console.log('get',r.s,r.b.state.updatedAt,r.b.notes.length);
r=await call('rec',{method:'POST',headers:{'X-Code':code,'Content-Type':'audio/webm','X-Meta':encodeURIComponent(JSON.stringify({kind:'q',ref:'ten',target:'Tôi tên là Ben.',heard:'tôi tên là ben',ok:true,score:.93,ms:900,prompt:'Anh tên gì?'}))},body:new Uint8Array(5000)}); console.log('rec',r.s,r.b);
r=await call('t/students'); console.log('teacher no key',r.s);
r=await call('setup',{method:'POST'}); const tk=r.b.key; console.log('setup',r.s,tk.length); r=await call('setup',{method:'POST'}); console.log('setup again',r.s);
r=await call('t/students',{headers:{'X-Teacher':tk}}); console.log('students',r.s,JSON.stringify(r.b));
r=await call('t/student?id='+id,{headers:{'X-Teacher':tk}}); console.log('student',r.s,r.b.recs.length,JSON.stringify(r.b.recs[0]));
r=await call('t/audio?key='+encodeURIComponent(r.b.recs[0].key),{headers:{'X-Teacher':tk}}); console.log('audio',r.s,r.b);
r=await call('t/note',{method:'POST',headers:{'X-Teacher':tk},body:JSON.stringify({id,text:'Nói chậm hơn ở chữ "tên".',about:'Anh tên gì?'})}); console.log('note',r.s,r.b.notes.length);
r=await call('state',{headers:{'X-Code':code}}); console.log('student sees notes',r.b.notes[0].text);
r=await call('t/student?id=ZZZ',{headers:{'X-Teacher':tk}}); console.log('missing student',r.s);

// chat
r=await call('chat',{method:'POST',headers:{'X-Code':code},body:'{}'}); console.log('chat no key',r.s,r.b.code);
env.ANTHROPIC_API_KEY='k'; r=await call('chat',{method:'POST',headers:{'X-Code':code},body:'{}'}); console.log('chat not approved',r.s,r.b.code);
r=await call('t/ai',{method:'POST',headers:{'X-Teacher':tk},body:JSON.stringify({id,on:true})}); console.log('ai on',r.s,r.b);
const realFetch=globalThis.fetch; let seen=null;
globalThis.fetch=async(u,o)=>{ seen=JSON.parse(o.body); if(seen.model==='claude-haiku-5-5') return new Response('{}',{status:404}); return new Response(JSON.stringify({content:[{type:'text',text:'Sure! {"vi":"Dạ, anh uống gì?","en":"What would you like to drink?","fix":"Cho tôi một ly cà phê.","note":"Add ly."}'}]}),{status:200}) };
r=await call('chat',{method:'POST',headers:{'X-Code':code},body:JSON.stringify({scene:'At a café',you:'anh',them:'em',name:'Ben',history:[{role:'assistant',content:'Chào anh!'},{role:'user',content:'cho tôi cà phê'}]})}); console.log('chat',r.s,JSON.stringify(r.b),'| model used',seen.model,'| first role',seen.messages[0].role,'| msgs',seen.messages.length);
r=await call('chat',{method:'POST',headers:{'X-Code':code},body:JSON.stringify({mode:'hint',history:[]})}); console.log('hint',r.s,JSON.stringify(r.b));
r=await call('t/student?id='+id,{headers:{'X-Teacher':tk}}); console.log('student ai flag',r.b.ai,r.b.aiReady);

// cut-off reply from the AI
globalThis.fetch=async(u,o)=>new Response(JSON.stringify({content:[{type:'text',text:'{"vi":"Dạ, anh uống gì ạ? Cà phê hay trà nha?","en":"Yes, what would you like? Coffee or tea?","fix":"An'}]}),{status:200});
r=await call('chat',{method:'POST',headers:{'X-Code':code},body:JSON.stringify({history:[{role:'user',content:'em'}]})}); console.log('cut-off',r.s,JSON.stringify(r.b));
globalThis.fetch=async(u,o)=>new Response(JSON.stringify({content:[{type:'text',text:'{"v'}]}),{status:200});
r=await call('chat',{method:'POST',headers:{'X-Code':code},body:JSON.stringify({history:[{role:'user',content:'em'}]})}); console.log('garbled',r.s,JSON.stringify(r.b));
