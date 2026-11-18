// Zelus API: sign-in codes, offline-first sync, friends feed and meal estimates.
// Runs as a Cloudflare Pages Function. Uses a KV namespace bound as ZELUS, or the site's KV binding with a prefix.
// Optional settings: INVITE (code people must enter to create an account),
// ANTHROPIC_API_KEY (switches on meal estimates), ZELUS_MODEL (model for estimates).
function mergeDoc(id,a,b){if(!a)return b;if(!b)return a;const A=a.data||{},B=b.data||{},u=Math.max(a.u||0,b.u||0);
  if(id.indexOf('w-')===0){const gone=Object.assign({},A.gone||{});Object.keys(B.gone||{}).forEach(k=>{gone[k]=Math.max(gone[k]||0,B.gone[k])});const items={},st=w=>w.u||w.end||w.start||0;
    [A.items||{},B.items||{}].forEach(src=>Object.keys(src).forEach(k=>{const w=src[k];if(!items[k]||st(w)>st(items[k]))items[k]=w}));
    Object.keys(gone).forEach(k=>{if(items[k]&&gone[k]>=st(items[k]))delete items[k]});return {u,data:{items,gone}}}
  if(id.indexOf('f-')===0){const days={},du={};[A,B].forEach(src=>Object.keys(Object.assign({},src.days||{},src.du||{})).forEach(d=>{const t=(src.du||{})[d]||0;if(!(d in days)||t>(du[d]||0)){days[d]=(src.days||{})[d]||[];du[d]=t}}));return {u,data:{days,du}}}
  return (b.u||0)>=(a.u||0)?b:a}

const J=(o,s=200)=>new Response(JSON.stringify(o),{status:s,headers:{'content-type':'application/json','cache-control':'no-store'}});
async function sha(s){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')}
function newCode(){const a='ABCDEFGHJKMNPQRSTUVWXYZ23456789',r=crypto.getRandomValues(new Uint8Array(12));let s='';r.forEach((x,i)=>{s+=a[x%a.length];if(i%4===3&&i<11)s+='-'});return s}
const normCode=c=>String(c||'').toUpperCase().replace(/[^A-Z0-9]/g,'').replace(/(.{4})(?=.)/g,'$1-');
const PROMPT='Estimate the nutrition of this meal for a food log. Reply with JSON only, in this shape: {"items":[{"name":"short food name","kcal":0,"p":0,"c":0,"f":0}]}. One item per distinct food. p, c and f are grams of protein, carbohydrate and fat. If a portion is not given, assume one typical serving.\nMeal: ';
export async function onRequest({request,env,params}){
  // Own namespace (ZELUS) when bound; otherwise share the site's KV under a "zl:" prefix so nothing collides.
  const raw=env.ZELUS||env.KV;if(!raw)return J({error:'Storage is not connected yet.'},500);const px=env.ZELUS?'':'zl:';
  const KV={get:(k,t)=>raw.get(px+k,t),put:(k,v,o)=>raw.put(px+k,v,o),delete:k=>raw.delete(px+k),
    list:async o=>{const l=await raw.list(Object.assign({},o,{prefix:px+(o.prefix||'')}));return {keys:l.keys.map(k=>({name:k.name.slice(px.length),metadata:k.metadata})),list_complete:l.list_complete,cursor:l.cursor}}};
  const path=[].concat(params.path||[]).join('/'),m=request.method;let body={};
  if(m==='POST'){try{body=await request.json()}catch(e){return J({error:'Bad request.'},400)}}
  if(path==='signup'&&m==='POST'){
    if(env.INVITE&&String(body.invite||'').trim().toLowerCase()!==String(env.INVITE).trim().toLowerCase())return J({error:'That invite code is not right.'},403);
    const name=String(body.name||'').trim().slice(0,40);if(!name)return J({error:'Enter your name.'},400);
    const code=newCode(),token=await sha(code),uid='u'+token.slice(0,16);
    await KV.put('tok:'+token,JSON.stringify({uid,name,t:Date.now()}));return J({uid,name,code,token})}
  if(path==='signin'&&m==='POST'){
    const code=normCode(body.code);if(code.length<14)return J({error:'Enter the full sign-in code.'},400);
    const token=await sha(code),u=await KV.get('tok:'+token,'json');if(!u)return J({error:'That code was not found. Check it and try again.'},404);
    return J({uid:u.uid,name:u.name,code,token})}
  if(path==='preset'&&m==='GET'){const c=(new URL(request.url).searchParams.get('c')||'').toUpperCase();if(!/^[A-Z0-9]{6,12}$/.test(c))return J({error:'Not found.'},404);
    const d=await KV.get('preset:'+c,'json');return d?J({data:d}):J({error:'Not found.'},404)}
  const tok=(request.headers.get('authorization')||'').replace(/^Bearer\s+/i,'');
  const user=/^[a-f0-9]{64}$/.test(tok)?await KV.get('tok:'+tok,'json'):null;if(!user)return J({error:'Sign in again.'},401);
  if(path==='sync'&&m==='POST'){
    const now=Date.now(),since=+body.since||0,inc=body.docs&&typeof body.docs==='object'?body.docs:{},out={},ids=Object.keys(inc).slice(0,120).filter(id=>/^[A-Za-z0-9_-]{1,60}$/.test(id));
    for(const id of ids){const d=inc[id];if(!d||typeof d.data!=='object'||d.data===null)continue;const key='doc:'+user.uid+':'+id,incoming={u:+d.u||now,data:d.data};
      const cur=await KV.get(key,'json'),merged=cur?mergeDoc(id,cur,incoming):incoming,str=JSON.stringify(merged);if(str.length>900000)continue;
      if(!cur||JSON.stringify(cur)!==str)await KV.put(key,str,{metadata:{m:now}});
      if(JSON.stringify(merged.data)!==JSON.stringify(d.data))out[id]=merged}
    let cursor;do{const l=await KV.list({prefix:'doc:'+user.uid+':',cursor});
      for(const k of l.keys){const id=k.name.slice(('doc:'+user.uid+':').length);if(out[id]||ids.includes(id))continue;if(((k.metadata||{}).m||0)>since){const v=await KV.get(k.name,'json');if(v)out[id]=v}}
      cursor=l.list_complete?null:l.cursor}while(cursor);
    return J({docs:out,now:now-120000,ai:!!env.ANTHROPIC_API_KEY,name:user.name})}
  if(path==='preset'&&m==='POST'){const str=JSON.stringify(body.data||null);if(!body.data||str.length>150000)return J({error:'Too large.'},413);
    const code=newCode().replace(/-/g,'').slice(0,8);await KV.put('preset:'+code,str);return J({code})}
  if(path==='share'&&m==='POST'){
    if(!body.doc){await KV.delete('share:'+user.uid);return J({ok:true})}
    const str=JSON.stringify(body.doc);if(str.length>60000)return J({error:'Too large.'},413);
    await KV.put('share:'+user.uid,JSON.stringify({name:user.name,doc:body.doc}));return J({ok:true})}
  if(path==='friends'&&m==='GET'){
    const people=[];let cursor;do{const l=await KV.list({prefix:'share:',cursor});for(const k of l.keys){const v=await KV.get(k.name,'json');if(v)people.push({id:k.name.slice(6),name:v.name,doc:v.doc})}cursor=l.list_complete?null:l.cursor}while(cursor&&people.length<200);
    return J({people})}
  if(path==='estimate'&&m==='POST'){
    if(!env.ANTHROPIC_API_KEY)return J({error:'Meal estimates are not switched on.'},503);
    const dk='cap:'+user.uid+':'+new Date().toISOString().slice(0,10),n=+(await KV.get(dk))||0;if(n>=40)return J({error:'You have reached today\'s limit for meal estimates. Use Quick add.'},429);
    await KV.put(dk,String(n+1),{expirationTtl:172800});
    const content=[];if(body.image&&typeof body.image.data==='string'&&body.image.data.length<1400000)content.push({type:'image',source:{type:'base64',media_type:'image/jpeg',data:body.image.data}});
    content.push({type:'text',text:PROMPT+(String(body.text||'').slice(0,600)||'shown in the photo')});
    const r=await fetch('https://api.anthropic.com/v1/messages',{method:'POST',headers:{'x-api-key':env.ANTHROPIC_API_KEY,'anthropic-version':'2023-06-01','content-type':'application/json'},body:JSON.stringify({model:env.ZELUS_MODEL||env.AI_MODEL||'claude-haiku-5-5',max_tokens:800,messages:[{role:'user',content}]})});
    if(!r.ok)return J({error:'The estimate service did not answer.'},502);
    const j=await r.json(),txt=((j.content||[]).find(c=>c.type==='text')||{}).text||'',mm=txt.match(/\{[\s\S]*\}/);let val={items:[]};try{val=JSON.parse(mm[0])}catch(e){}
    return J({items:Array.isArray(val.items)?val.items.slice(0,12):[]})}
  return J({error:'Not found.'},404)}
