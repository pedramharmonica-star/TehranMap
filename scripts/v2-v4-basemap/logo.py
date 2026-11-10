import os
import numpy as np, potrace
from PIL import Image
S=os.environ.get('TEHRANMAP_WORK', 'work').rstrip('/') + '/'
im=np.array(Image.open(S+'inputs/logo-dark-slogan.png').convert('RGB')).astype(int)
r,g,b=im[...,0],im[...,1],im[...,2]
orange=(r>170)&(g<150)&(b<90)&(r-b>120)
white=(r>150)&(g>150)&(b>150)
reg=np.zeros_like(orange); reg[540:785,:]=True   # logo only, above the rule line
orange&=reg; white&=reg
ys,xs=np.where(orange|white); x0,x1,y0,y1=xs.min()-4,xs.max()+5,ys.min()-4,ys.max()+5
print('bbox',x0,x1,y0,y1)
K=4
def trace(mask):
    m=mask[y0:y1,x0:x1].astype(np.uint8)*255
    big=np.array(Image.fromarray(m).resize((m.shape[1]*K,m.shape[0]*K),Image.LANCZOS))>127
    bm=potrace.Bitmap(~big)
    path=bm.trace(turdsize=8,opticurve=True,alphamax=1.0)
    d=[]
    for c in path:
        s=c.start_point; d.append(f"M{s.x/K:.2f},{s.y/K:.2f}")
        for seg in c.segments:
            if seg.is_corner: d.append(f"L{seg.c.x/K:.2f},{seg.c.y/K:.2f}L{seg.end_point.x/K:.2f},{seg.end_point.y/K:.2f}")
            else: d.append(f"C{seg.c1.x/K:.2f},{seg.c1.y/K:.2f} {seg.c2.x/K:.2f},{seg.c2.y/K:.2f} {seg.end_point.x/K:.2f},{seg.end_point.y/K:.2f}")
        d.append('Z')
    return ''.join(d)
W,H=x1-x0,y1-y0
po,pw=trace(orange),trace(white)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="پیام‌گستر"><path fill-rule="evenodd" style="fill:var(--lm,#F26122)" d="{po}"/><path fill-rule="evenodd" style="fill:var(--lw,#6E747F)" d="{pw}"/></svg>'
open(S+'logo/logo.svg','w').write(svg)
print(W,H,len(svg))
# preview on light and dark
import subprocess
