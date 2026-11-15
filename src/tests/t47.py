# 47: teacher page — listen to one speaker's clips, mark good, take one out
import json, urllib.request, struct, math
from playwright.sync_api import sync_playwright
B='http://localhost:8890'; errs=[]
def call(path,method='GET',body=None,headers=None,raw=None):
    h={'Content-Type':'application/json'}; h.update(headers or {})
    r=urllib.request.Request(B+path,method=method,data=raw if raw is not None else (json.dumps(body).encode() if body is not None else None),headers=h)
    with urllib.request.urlopen(r) as f: return json.loads(f.read())
def wav(sec=0.6,sr=16000):
    n=int(sec*sr); d=b''.join(struct.pack('<h',int(8000*math.sin(i*0.07))) for i in range(n))
    return b'RIFF'+struct.pack('<I',36+len(d))+b'WAVEfmt '+struct.pack('<IHHIIHH',16,1,1,sr,sr*2,2,16)+b'data'+struct.pack('<I',len(d))+d
key=call('/api/setup','POST',{})['key']; T={'X-Teacher':key}
vk=call('/api/t/voice-key','POST',{},T)['key']
lines=json.load(open('data/voice-lines.json'))['parts'][0]['lines'][:3]
for l in lines: call('/api/voice/rec?v=%s&who=voice3&id=%s&part=x'%(vk,l['id']),'POST',headers={'Content-Type':'audio/wav','X-Text':urllib.parse.quote(l['vi'])},raw=wav())
print('count before',call('/api/t/voice-key','POST',{},T)['counts'].get('voice3'))
with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--autoplay-policy=no-user-gesture-required'])
    tp=br.new_page(viewport={'width':420,'height':900}); tp.on('pageerror',lambda e: errs.append(str(e)))
    tp.goto(B+'/teacher.html?k='+key); tp.wait_for_timeout(1200); tp.click('text=Thu âm · recording links'); tp.wait_for_timeout(1500)
    tp.locator('button:has-text("listen to their recordings")').first.click(); tp.wait_for_timeout(500)
    t=tp.inner_text('#app'); i=t.find('clips, newest first'); print(t[i-4:i+500])
    src=tp.locator('audio').first.get_attribute('src'); print('src',src)
    print('play ok', tp.evaluate("(s)=>fetch(s).then(r=>r.status+' '+r.headers.get('content-type'))",src))
    tp.locator('button:text-is("Good")').first.click(); print('good ->',tp.locator('button:has-text("✓ Good")').count())
    tp.locator('button:has-text("Play all")').click(); tp.wait_for_timeout(2500); print('after play all:',tp.locator('button:has-text("Play")').first.inner_text())
    rd=tp.locator('button:text-is("Redo")').last; rd.click(); tp.wait_for_timeout(200); tp.locator('button:has-text("Tap again to remove")').click(); tp.wait_for_timeout(1200)
    t=tp.inner_text('#app'); i=t.find('Removed:'); print(t[i:i+100])
    tp.screenshot(path='/tmp/t47.png',full_page=False)
    tp.reload(); tp.wait_for_timeout(1200); tp.click('text=Thu âm · recording links'); tp.wait_for_timeout(1500); tp.locator('button:has-text("listen to their recordings")').first.click(); tp.wait_for_timeout(500)
    print('after reload rows:',tp.locator('audio').count(),' good kept:',tp.locator('button:has-text("✓ Good")').count())
    br.close()
print('count after',call('/api/t/voice-key','POST',{},T)['counts'].get('voice3'))
try: call('/api/voice/clip?w=voice3&i='+lines[0]['id']); print('removed clip still there?')
except Exception as e: print('removed clip gone:',e)
print('ERR',errs or 'none')
