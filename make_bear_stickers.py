#!/usr/bin/env python3
"""Bear stickers v2 — one white bear (the club's own, traced from the burgee),
navy keyline, gold props, three gradient fields, navy rule."""
import cairosvg
BEAR=open('bear-path.txt').read(); BW=float(open('bear-vb.txt').read()); BH=100.0
NAVY='#1638a8'; GOLD='#ffd257'

def bear(cx, baseline, h):
    s=h/BH
    return (f'<g transform="translate({cx-BW*s/2:.2f},{baseline-h:.2f}) scale({s:.4f})">'
            f'<path d="{BEAR}" fill="#ffffff" stroke="{NAVY}" stroke-width="{1.15/s:.2f}" '
            f'stroke-linejoin="round" paint-order="stroke"/></g>')

def wings(cx, cy):
    """Spread wing, high on the shoulder. Shorter and blunter than v5 — the tips
    are rounded rather than converging to a point, which is what made it read as
    spikes."""
    import math
    sx, sy = cx+7, cy+3                     # shoulder, up between the shoulders
    out=[]
    prim=[(230,24,5.4),(220,22,5.2),(210,19,5.0),(199,16,4.6),(188,13,4.1)]
    for ang,L,Wd in prim:
        a=math.radians(ang)
        tx,ty = sx+math.cos(a)*L*0.88, sy+math.sin(a)*L - L*0.06
        mx,my = sx+math.cos(a)*L*0.50, sy+math.sin(a)*L*0.46
        px,py = math.cos(a+math.pi/2)*Wd, math.sin(a+math.pi/2)*Wd
        t1x,t1y = tx+px*0.34, ty+py*0.34     # blunt tip: two points, not one
        t2x,t2y = tx-px*0.34, ty-py*0.34
        ox,oy = math.cos(a)*Wd*0.55, math.sin(a)*Wd*0.55
        out.append(
          f'<path d="M{sx:.1f} {sy:.1f} '
          f'C{mx+px:.1f} {my+py:.1f} {t1x+px*0.35:.1f} {t1y+py*0.35:.1f} {t1x:.1f} {t1y:.1f} '
          f'Q{tx+ox:.1f} {ty+oy:.1f} {t2x:.1f} {t2y:.1f} '
          f'C{mx-px:.1f} {my-py:.1f} {sx-px*0.3:.1f} {sy-py*0.3:.1f} {sx:.1f} {sy:.1f} Z" '
          f'fill="{GOLD}" stroke="{NAVY}" stroke-width=".9" stroke-linejoin="round"/>')
    cov=(f'<path d="M{sx+2:.1f} {sy-4:.1f} '
         f'C{sx+3:.1f} {sy+5:.1f} {sx-5:.1f} {sy+9:.1f} {sx-11:.1f} {sy+6.5:.1f} '
         f'Q{sx-7.5:.1f} {sy+3:.1f} {sx-10:.1f} {sy+0.5:.1f} '
         f'Q{sx-6:.1f} {sy-1:.1f} {sx-7.5:.1f} {sy-3.5:.1f} '
         f'Q{sx-3.5:.1f} {sy-4.5:.1f} {sx-4:.1f} {sy-7:.1f} Z" '
         f'fill="{GOLD}" stroke="{NAVY}" stroke-width=".9" stroke-linejoin="round"/>')
    return ''.join(out)+cov

def umbrella(cx, top, rx=15.5, ry=9.5):
    """flattened canopy — wider than tall"""
    return (f'<g stroke="{NAVY}" stroke-width="1.05" stroke-linejoin="round">'
            f'<path d="M{cx-rx} {top+ry} A{rx} {ry} 0 0 1 {cx+rx} {top+ry} '
            f'Q{cx+rx*0.66:.1f} {top+ry*0.55:.1f} {cx+rx*0.33:.1f} {top+ry} '
            f'Q{cx} {top+ry*0.55:.1f} {cx-rx*0.33:.1f} {top+ry} '
            f'Q{cx-rx*0.66:.1f} {top+ry*0.55:.1f} {cx-rx} {top+ry} Z" fill="{GOLD}"/>'
            f'<path d="M{cx} {top+ry} V{top+ry+20}" stroke-linecap="round" fill="none"/></g>')

def sunburst(cx, cy, r=20):
    import math
    rays=''.join(
        f'<path d="M{cx+math.cos(math.radians(a))*r*0.62:.1f} {cy+math.sin(math.radians(a))*r*0.62:.1f} '
        f'L{cx+math.cos(math.radians(a))*r:.1f} {cy+math.sin(math.radians(a))*r:.1f}" '
        f'stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>' for a in range(0,360,30))
    return f'<circle cx="{cx}" cy="{cy}" r="{r*0.5:.1f}" fill="{GOLD}"/>'+rays

GRADS = {
 'g-bird': [('0%','#ff9ceb'),('55%','#e46fe0'),('100%','#a56ae0')],
 'g-rain': [('0%','#c3ecff'),('55%','#7cc2ee'),('100%','#4a8fd0')],
 'g-sun':  [('0%','#fff6cf'),('45%','#ffc247'),('100%','#f2760c')],
}
SET=[
 dict(cap='3 BIRDIES', grad='g-bird', art=lambda cx,cy: wings(cx-3, cy-6) + bear(cx+8, cy+26, 42)),
 dict(cap='RAIN',      grad='g-rain', art=lambda cx,cy: umbrella(cx+3, cy-29) + bear(cx-1, cy+26, 40)),
 dict(cap='SUNNY',     grad='g-sun',  art=lambda cx,cy: sunburst(cx+2, cy-19) + bear(cx, cy+26, 41)),
]

def defs():
    out=['<defs>']
    for k,stops in GRADS.items():
        out.append(f'<linearGradient id="{k}" x1="0" y1="0" x2="0.35" y2="1">'
                   +''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in stops)+'</linearGradient>')
    for i in range(3):
        out.append(f'<clipPath id="cl{i}"><circle cx="0" cy="0" r="33"/></clipPath>')
    out.append('</defs>')
    return ''.join(out)

def sheet(scale, y0, label):
    out=[f'<text x="26" y="{y0}" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#6b6350">{label}</text>']
    r=34*scale; top=y0+26; pitch=r*2+40*scale
    for i,s in enumerate(SET):
        cx=44+r+i*pitch; cy=top+r
        out.append(f'<g transform="translate({cx},{cy}) scale({scale})">'
                   f'<circle cx="0" cy="0" r="34" fill="url(#{s["grad"]})"/>'
                   f'<g clip-path="url(#cl{i})">{s["art"](0,0)}</g>'
                   f'<circle cx="0" cy="0" r="34" fill="none" stroke="{NAVY}" stroke-width="1.6"/></g>')
        out.append(f'<text x="{cx}" y="{cy+r+15*min(scale,1.3):.0f}" text-anchor="middle" font-family="DejaVu Sans" '
                   f'font-size="{10*min(scale,1.3):.0f}" font-weight="bold" letter-spacing=".4" fill="{NAVY}">{s["cap"]}</text>')
    return ''.join(out), top+r*2+30*min(scale,1.4)

b1,y=sheet(2.4, 42, 'AT 2.4x')
b2,y2=sheet(1.0, y+44, 'ACTUAL SIZE — 68px')
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 790 {y2+18:.0f}" width="1580" height="{(y2+18)*2:.0f}">'
     f'<rect width="790" height="{y2+18:.0f}" fill="#fffdf7"/>{defs()}{b1}{b2}</svg>')
open('bear-stickers.svg','w').write(svg)
cairosvg.svg2png(url='bear-stickers.svg', write_to='bear-stickers.png', output_width=1400)
print('rendered')
