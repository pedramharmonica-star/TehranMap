import os
import re
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
b=open(S+'supportmap/bundle.html').read()
styles=re.findall(r'<style[^>]*>.*?</style>',b,re.S)
scripts=re.findall(r'<script[^>]*>.*?</script>',b,re.S)
head='''<title>نقشه محدوده پشتیبانی پیام‌گستر</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap">
'''
import base64
emb=''.join('<script type="application/octet-stream" id="%s">%s</script>\n'%(i,base64.b64encode(open(S+'out2/'+fn,'rb').read()).decode()) for i,fn in [('bm-base','base.json.gz'),('bm-minor','minor.json.gz')])
out=head+'\n'.join(styles)+'\n<div id="root"></div>\n'+emb+'\n'.join(scripts)
open(S+'pub/payamgostar-support-map.html','w').write(out)
open(S+'pub/test.html','w').write('<!doctype html><html lang="fa"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body style="margin:0">'+out+'</body></html>')
print(len(out), len(styles), len(scripts))
