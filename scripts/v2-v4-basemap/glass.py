import os
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
p=S+'src/template2.html';s=open(p).read()
a=s.index('/* ---------- brand header ---------- */'); b=s.index('/* ---------- map chrome ---------- */')
css=r'''/* ---------- glass cards (brand header + legend) ---------- */
.glass{position:fixed;z-index:800;right:calc(16px + env(safe-area-inset-right,0px));width:344px;max-width:calc(100vw - 32px);direction:rtl;color:var(--night);
  border-radius:22px;isolation:isolate;
  background:linear-gradient(150deg,rgba(255,255,255,.66) 0%,rgba(255,255,255,.42) 55%,rgba(255,255,255,.52) 100%);
  -webkit-backdrop-filter:blur(18px) saturate(175%);backdrop-filter:blur(18px) saturate(175%);
  border:1px solid rgba(255,255,255,.78);
  box-shadow:0 30px 60px -28px rgba(28,31,35,.45),0 10px 24px -12px rgba(28,31,35,.18),inset 0 1px 0 rgba(255,255,255,.95),inset 0 -1px 0 rgba(255,255,255,.3);
  animation:enter .8s cubic-bezier(.2,.8,.2,1) .15s both,float 7s ease-in-out 1.2s infinite;
  transition:box-shadow .35s ease}
.glass:hover{box-shadow:0 38px 70px -28px rgba(28,31,35,.5),0 12px 28px -12px rgba(28,31,35,.2),inset 0 1px 0 rgba(255,255,255,.95),inset 0 -1px 0 rgba(255,255,255,.3)}
.glass::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:-1;
  background:linear-gradient(112deg,transparent 35%,rgba(255,255,255,.65) 48%,transparent 61%) no-repeat;background-size:260% 100%;background-position:160% 0;
  animation:sheen 10s ease-in-out 1.6s infinite}
.glass::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:-2;
  background:radial-gradient(120% 70% at 100% 0%,rgba(242,97,34,.10),transparent 60%)}
@keyframes enter{from{opacity:0;transform:translateX(28px) scale(.97);filter:blur(8px)}to{opacity:1;transform:none;filter:none}}
@keyframes float{0%,100%{translate:0 0}50%{translate:0 -3px}}
@keyframes sheen{0%{background-position:160% 0}24%,100%{background-position:-60% 0}}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.glass{background:rgba(255,255,255,.94)}}

.brandcard{top:calc(16px + env(safe-area-inset-top,0px));padding:18px 20px 18px;display:flex;flex-direction:column;gap:12px}
.head{display:flex;flex-direction:column;gap:14px}
.logo svg{display:block;height:36px;width:auto;--lm:#F26122;--lw:#5E6573}
.brandcard h1{margin:0;font-size:20px;font-weight:800;line-height:1.45;text-wrap:balance;color:var(--night)}
.brandcard h1::after{content:"";display:block;width:40px;height:4px;border-radius:4px;background:var(--or);margin-top:9px;transform-origin:right;animation:grow .7s cubic-bezier(.2,.8,.2,1) .7s both}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.brandcard p{margin:0;color:#4A515E;font-size:12.5px;line-height:1.85}

.search{position:relative}
.search input{width:100%;box-sizing:border-box;font:inherit;font-size:14px;padding:12px 42px 12px 14px;border-radius:13px;border:1px solid rgba(28,31,35,.10);
  background:rgba(255,255,255,.72);color:var(--night);outline:none;box-shadow:inset 0 1px 2px rgba(28,31,35,.06);transition:border-color .2s,box-shadow .2s,background .2s}
.search input::placeholder{color:#7C828D}
.search input:focus{border-color:var(--or);background:rgba(255,255,255,.92);box-shadow:0 0 0 4px rgba(242,97,34,.18)}
.search svg{position:absolute;right:13px;top:50%;transform:translateY(-50%);width:18px;height:18px;stroke:var(--slate);fill:none;stroke-width:1.75;stroke-linecap:round}
.search svg .a{stroke:var(--or)}
.results{position:absolute;inset-inline:0;top:100%;margin-top:8px;color:var(--night);border-radius:14px;max-height:290px;overflow-y:auto;padding:5px;z-index:5;
  background:rgba(255,255,255,.86);-webkit-backdrop-filter:blur(16px) saturate(170%);backdrop-filter:blur(16px) saturate(170%);
  border:1px solid rgba(255,255,255,.8);box-shadow:0 24px 44px -20px rgba(28,31,35,.4)}
.results[hidden]{display:none}
.results button{all:unset;box-sizing:border-box;width:100%;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:9px 10px;border-radius:9px;cursor:pointer;font-size:13.5px}
.results button:hover,.results button:focus-visible{background:rgba(242,97,34,.08)}
.results small{color:var(--gray);font-size:11.5px;margin-inline-start:6px}
.badge{font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;white-space:nowrap}
.b1{background:#E3F4ED;color:var(--z1-ink)}.b2{background:#FFF3C7;color:var(--z2-ink)}.b3{background:#ECEDF0;color:var(--slate)}
.results .empty{padding:10px;color:var(--gray);font-size:13px;line-height:1.7}

/* ---------- legend ---------- */
.legend{bottom:calc(16px + env(safe-area-inset-bottom,0px));padding:14px 14px 12px;display:flex;flex-direction:column;gap:4px;
  animation-delay:.35s,2.4s}
.legend h2{margin:0 6px 4px;font-size:12.5px;font-weight:700;color:#4A515E;display:flex;justify-content:space-between;align-items:center}
.legend h2 button{all:unset;cursor:pointer;color:var(--or-deep);font-size:12px;font-weight:600}
.row{all:unset;box-sizing:border-box;display:grid;grid-template-columns:40px 1fr;gap:2px 12px;align-items:center;padding:9px 8px;border-radius:13px;cursor:pointer;
  transition:background .25s,box-shadow .25s,transform .25s}
.row:hover{background:rgba(255,255,255,.55);transform:translateX(-2px)}
.row.on{background:rgba(255,255,255,.75);box-shadow:inset 0 0 0 1.5px var(--rc),0 6px 16px -10px rgba(28,31,35,.35)}
.row:focus-visible{outline:2px solid var(--or);outline-offset:1px}
.sw{grid-row:span 2;width:40px;height:30px;border-radius:9px;box-sizing:border-box}
.sw1{background:rgba(21,147,106,.22);border:2.5px solid var(--z1)}
.sw2{background:rgba(245,184,0,.32);border:3.5px solid var(--z2);box-shadow:inset 0 0 0 1px rgba(138,100,0,.25)}
.sw3{background:repeating-linear-gradient(135deg,rgba(79,88,104,.45) 0 2px,transparent 2px 6px),rgba(241,242,244,.8);border:1px solid #C9CDD3}
.row b{font-size:13.5px;font-weight:700;line-height:1.5}
.row span{font-size:12px;color:#5A616D;line-height:1.6}
.edge{display:flex;align-items:center;gap:10px;padding:9px 8px 2px;font-size:12px;color:var(--slate)}
.edge i{width:40px;height:6px;border-radius:6px;background:var(--z2);box-shadow:0 0 0 1.5px rgba(138,100,0,.45);flex:none}
.edge i.g{background:var(--z1);height:3px;box-shadow:none}
.edgegrid{display:grid;grid-template-columns:1fr 1fr;gap:0 8px;border-top:1px solid rgba(28,31,35,.08);margin-top:4px}
.legend .collapse{display:none}

'''
s=s[:a]+css+s[b:]
# mobile block
ma=s.index('  .brandcard{top:env(safe-area-inset-top,0px);'); mb=s.index('  .legend .collapse{display:inline}')
mob='''  .glass{right:8px;left:8px;width:auto;max-width:none;border-radius:18px;animation:enter .7s cubic-bezier(.2,.8,.2,1) .1s both}
  .brandcard{top:calc(8px + env(safe-area-inset-top,0px));padding:12px 14px;gap:10px}
  .head{flex-direction:row;align-items:center;justify-content:space-between;gap:10px}
  .logo{order:2}.logo svg{height:24px}
  .brandcard p{display:none}
  .brandcard h1{font-size:15.5px}.brandcard h1::after{display:none}
  .legend{bottom:calc(8px + env(safe-area-inset-bottom,0px));padding:10px 12px;gap:0}
  .row{padding:6px 6px}.row span{font-size:11.5px}.sw{width:32px;height:24px}
'''
s=s[:ma]+mob+s[mb:]
s=s.replace('.leaflet-top .leaflet-control{margin-top:calc(150px + env(safe-area-inset-top,0px))}','.leaflet-top .leaflet-control{margin-top:calc(140px + env(safe-area-inset-top,0px))}')
# markup
ha=s.index('<header class="brandcard">'); hb=s.index('</header>')+len('</header>')
hdr='''<header class="brandcard glass">
  <div class="head">
    <div class="logo" id="logo" aria-label="پیام‌گستر"></div>
    <h1>محدوده پشتیبانی حضوری</h1>
  </div>
  <p>محله، شهر یا منطقه را جستجو کنید یا روی نقشه بزنید تا شرایط اعزام کارشناس را ببینید.</p>
  <div class="search">
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path class="a" d="M16 16l4.5 4.5"/></svg>
    <input id="q" type="search" placeholder="مثلاً سعادت‌آباد، قدس، منطقه ۵" autocomplete="off" aria-label="جستجوی محله، شهر یا منطقه">
    <div class="results" id="results" hidden></div>
  </div>
</header>'''
s=s[:ha]+hdr+s[hb:]
s=s.replace('<aside class="legend" id="legend"','<aside class="legend glass" id="legend"')
s=s.replace('--font:"Vazirmatn",Tahoma','--font:"Yekan Bakh","Vazirmatn",Tahoma')
# inject logo at script start
if "__LOGO_SVG__" not in s:
    s=s.replace("const fa = n => Number(n).toLocaleString('fa-IR');","const fa = n => Number(n).toLocaleString('fa-IR');\nconst LG=document.getElementById('logo'); if(LG) LG.innerHTML='__LOGO_SVG__';",1)
# canvas label fonts follow the brand font
s=s.replace("px Vazirmatn, Tahoma, sans-serif","px 'Yekan Bakh', Vazirmatn, Tahoma, sans-serif")
open(p,'w').write(s)
print('ok')
