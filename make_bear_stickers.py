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
    """Built from overlapping feathers rather than one outline — a single path
    kept collapsing into a quill shape. Five teardrops fanned from the shoulder,
    longest at the top, each a rotated ellipse-with-a-point."""
    import math
    ax, ay = cx+4, cy+16                       # shoulder pivot
    out=[]
    for i,(ang,L,Wd) in enumerate([(-108,34,7.5),(-96,31,7.2),(-84,27,6.8),(-72,22,6.2),(-60,17,5.6)]):
        a=math.radians(ang)
        tx,ty = ax+math.cos(a)*L, ay+math.sin(a)*L
        # perpendicular offset for the feather's belly
        px,py = math.cos(a+math.pi/2)*Wd, math.sin(a+math.pi/2)*Wd
        out.append(
          f'<path d="M{ax:.1f} {ay:.1f} '
          f'C{ax+px*0.9:.1f} {ay+py*0.9:.1f} {tx+px*0.75:.1f} {ty+py*0.75:.1f} {tx:.1f} {ty:.1f} '
          f'C{tx-px*0.75:.1f} {ty-py*0.75:.1f} {ax-px*0.9:.1f} {ay-py*0.9:.1f} {ax:.1f} {ay:.1f} Z" '
          f'fill="{GOLD}" stroke="{NAVY}" stroke-width=".95" stroke-linejoin="round"/>')
    return ''.join(out)

def umbrella(cx, top, rx=15.5, ry=9.5):
    """flattened canopy — wider than tall"""
    return (f'<g stroke="{NAVY}" stroke-width="1.05" stroke-linejoin="round">'
            f'<path d="M{cx-rx} {top+ry} A{rx} {ry} 0 0 1 {cx+rx} {top+ry} '
            f'Q{cx+rx*0.66:.1f} {top+ry*0.55:.1f} {cx+rx*0.33:.1f} {top+ry} '
            f'Q{cx} {top+ry*0.55:.1f} {cx-rx*0.33:.1f} {top+ry} '
            f'Q{cx-rx*0.66:.1f} {top+ry*0.55:.1f} {cx-rx} {top+ry} Z" fill="{GOLD}"/>'
            f'<path d="M{cx} {top+ry} V{top+ry+17}" stroke-linecap="round" fill="none"/></g>')

def sunburst(cx, cy, r=20):
    import math
    rays=''.join(
        f'<path d="M{cx+math.cos(math.radians(a))*r*0.62:.1f} {cy+math.sin(math.radians(a))*r*0.62:.1f} '
        f'L{cx+math.cos(math.radians(a))*r:.1f} {cy+math.sin(math.radians(a))*r:.1f}" '
        f'stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>' for a in range(0,360,30))
    return f'<circle cx="{cx}" cy="{cy}" r="{r*0.5:.1f}" fill="{GOLD}"/>'+rays

GRADS = {
 'g-bird': [('0%','#ff4fd8'),('55%','#c026d3'),('100%','#6d28d9')],
 'g-rain': [('0%','#7dd3fc'),('55%','#2f7fce'),('100%','#12377f')],
 'g-sun':  [('0%','#ffe9a8'),('50%','#ffb020'),('100%','#f2600c')],
}
SET=[
 dict(cap='3 BIRDIES', grad='g-bird', art=lambda cx,cy: wings(cx-7, cy-8) + bear(cx+7, cy+22, 42)),
 dict(cap='RAIN',      grad='g-rain', art=lambda cx,cy: umbrella(cx+3, cy-27) + bear(cx-1, cy+22, 41)),
 dict(cap='SUNNY',     grad='g-sun',  art=lambda cx,cy: sunburst(cx+2, cy-17) + bear(cx, cy+22, 43)),
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
