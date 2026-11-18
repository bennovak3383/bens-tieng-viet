/* Ben's Tiếng Việt · offline support (version 76).
   Keeps a copy of the app, its lesson data, pictures and sound bundles on the device, so the practice parts open with no internet.
   Never touches /api/ (sync, recordings, AI chat) or the teacher / recording pages: those need the internet and behave as before.
   The app page: internet first (so updates arrive), the saved copy if there is no answer in 3.5 s.
   Lesson data (.json): internet first too (2.5 s), so the page and its data never get out of step.
   Pictures, sounds, fonts: the saved copy, else the internet. */
var C='btv-1';
self.addEventListener('install',function(e){ self.skipWaiting(); e.waitUntil(caches.open(C).then(function(c){ return c.addAll(['./','data/offline.json']).catch(function(){}) })) });
self.addEventListener('activate',function(e){ e.waitUntil(self.clients.claim()) });
function put(req,res){ try{ if(res&&(res.ok||res.type==='opaque')){ var cp=res.clone(); caches.open(C).then(function(c){ c.put(req,cp).catch(function(){}) }) } }catch(x){} return res }
function saved(req){ return caches.match(req,{ignoreSearch:true}) }
function netFirst(req,ms){ return new Promise(function(done){ var settled=false, t=setTimeout(function(){ saved(req).then(function(r){ if(r&&!settled){ settled=true; done(r) } }) },ms);
  fetch(req).then(function(res){ clearTimeout(t); put(req,res); if(!settled){ settled=true; done(res) } }).catch(function(){ clearTimeout(t); saved(req).then(function(r){ if(settled) return; settled=true; if(r){ done(r); return } caches.match('./').then(function(x){ done(x||Response.error()) }) }) }) }) }
function cacheFirst(req){ return caches.match(req).then(function(r){ return r||fetch(req).then(function(res){ return put(req,res) }) }) }
self.addEventListener('fetch',function(e){ var req=e.request; if(req.method!=='GET') return; var u; try{ u=new URL(req.url) }catch(x){ return }
  var same=u.origin===self.location.origin, p=u.pathname;
  if(same&&p.indexOf('/api/')===0) return;
  if(same&&/\/(teacher|record|snap|words)\.html$/.test(p)) return;
  if(same&&(u.search.indexOf('nosw')>=0||String(req.referrer||'').indexOf('nosw=1')>=0)) return;
  if(same&&req.mode==='navigate'){ e.respondWith(netFirst(req,3500)); return }
  if(same&&/\/data\/offline\.json$/.test(p)){ e.respondWith(netFirst(req,3500)); return }
  if(same&&/\.json$/.test(p)){ e.respondWith(netFirst(req,2500)); return }
  if(same&&/\.(webp|png|jpe?g|svg|mp3|js|css|woff2?|webmanifest)$/.test(p)&&!/\/sw\.js$/.test(p)){ e.respondWith(cacheFirst(req)); return }
  if(/(^|\.)fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)){ e.respondWith(cacheFirst(req)); return }
});
/* the page sends the list of files to keep; files already saved are skipped */
self.addEventListener('message',function(e){ var d=e.data||{}; if(d.t!=='save') return; var list=d.files||[], src=e.source, done=0, fail=0;
  function tell(end){ try{ src.postMessage({t:'saved',done:done,total:list.length,fail:fail,id:d.id,end:end?1:0}) }catch(x){} }
  e.waitUntil(caches.open(C).then(function(c){ var i=0;
    function one(){ if(i>=list.length) return Promise.resolve(); var f=list[i++];
      return c.match(f).then(function(r){ if(r) return; return fetch(f,{cache:'no-cache'}).then(function(res){ if(res.ok) return c.put(f,res); fail++ }).catch(function(){ fail++ }) }).then(function(){ done++; if(done%25===0) tell(false); return one() }) }
    return Promise.all([one(),one(),one(),one()]) }).then(function(){ tell(true) })) });
