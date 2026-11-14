import json
s=open('/home/claude/v7/index.html',encoding='utf-8').read()
def sub(tagid,blank=False):
    global s
    a=s.find('id="%s">'%tagid)+len('id="%s">'%tagid); b=s.find('</script>',a)
    t=s[a:b]
    if blank:
        d=json.loads(t)
        for sl in d['slots']:
            if sl['k'] in('age','year','building','street'): sl['d']=''
        t=json.dumps(d,ensure_ascii=False).replace('</','<\\/')
    t=t.replace('Gold View','Sông Xanh').replace('gold view','sông xanh').replace('Bến Vân Đồn','Lê Lợi').replace('sinh năm 1983','sinh năm 1990').replace('born in 1983','born in 1990')
    s=s[:a]+t+s[b:]
sub('content6',True); sub('content')
s=s.replace('<title>Ben\'s Tiếng Việt</title>','<title>Tiếng Việt · speak Saigon Vietnamese</title>')
open('/home/claude/repo/index.html','w',encoding='utf-8').write(s); print('ok')
