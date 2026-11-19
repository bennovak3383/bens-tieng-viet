// Sign-in gate for /english/ (An's English app). Everything under /english/ needs the code once per device.
// The code itself is not stored here, only its SHA-256 (with a fixed prefix). To change the code, set a new CODE_HASH:
//   printf '%s' "english-with-ben|NEW-CODE" | sha256sum
// If the Pages project has an ENGLISH_CODE variable, that code is used instead of CODE_HASH.
const CODE_HASH='bdff1a0f8cf88fd3c164e564fad72371b7e5da9f4a495c5ce1c5585c7c9c8974';
const PRE='english-with-ben|';
async function sha(s){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')}
const page=(msg)=>`<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>English with Ben</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#F1F3FA;color:#1B2148;font-family:system-ui,-apple-system,sans-serif}form{background:#fff;border:2px solid #DDE1F0;border-radius:22px;box-shadow:0 5px 0 #DDE1F0;padding:24px;width:min(340px,88vw);text-align:center}h1{font-size:1.5rem;margin:0 0 6px}p{color:#5A6285;margin:0 0 14px}input{width:100%;box-sizing:border-box;font-size:1.1rem;padding:12px;border:2px solid #DDE1F0;border-radius:14px;text-align:center}button{margin-top:12px;width:100%;font-size:1.1rem;font-weight:700;color:#fff;background:#3F78EA;border:0;border-radius:16px;padding:13px;box-shadow:0 4px 0 #2C5BC4}.e{color:#E0566F;font-weight:700}</style></head>
<body><form method="post" action="/english/__in"><h1>English with Ben</h1><p>Nhập mã để vào · Enter your code</p>${msg?`<p class="e">${msg}</p>`:''}<input name="code" autocomplete="off" autocapitalize="none" spellcheck="false" autofocus required><button>Open</button></form></body></html>`;
const html=(msg,status)=>new Response(page(msg),{status,headers:{'content-type':'text/html; charset=utf-8','cache-control':'no-store'}});
export async function onRequest(ctx){
  const {request,env,next}=ctx,url=new URL(request.url);
  const want=env.ENGLISH_CODE?await sha(PRE+String(env.ENGLISH_CODE).trim().toLowerCase()):CODE_HASH;
  const token=await sha(want+'|cookie');
  const cookie=request.headers.get('cookie')||'';
  if(cookie.split(/;\s*/).includes('en_in='+token))return next();
  if(url.pathname==='/english/__in'&&request.method==='POST'){
    const ip=request.headers.get('cf-connecting-ip')||'x',key='en:try:'+ip;let tries=0;
    try{if(env.KV)tries=+(await env.KV.get(key))||0}catch(e){}
    if(tries>=10)return html('Too many tries. Wait ten minutes.',429);
    let code='';try{code=String((await request.formData()).get('code')||'')}catch(e){}
    if(await sha(PRE+code.trim().toLowerCase())===want)
      return new Response(null,{status:303,headers:{location:'/english/','set-cookie':'en_in='+token+'; Path=/english; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax','cache-control':'no-store'}});
    try{if(env.KV)await env.KV.put(key,String(tries+1),{expirationTtl:600})}catch(e){}
    return html('That code is not right.',401)}
  const nav=request.method==='GET'&&(request.headers.get('accept')||'').includes('text/html');
  return nav?html('',401):new Response('Sign in first.',{status:401,headers:{'cache-control':'no-store'}})}
