#!/usr/bin/env python3
"""Bear stickers v2 — one white bear (the club's own, traced from the burgee),
navy keyline, gold props, three gradient fields, navy rule."""
import cairosvg
BEAR=open('bear-path.txt').read(); BW=float(open('bear-vb.txt').read()); BH=100.0
NAVY='#1638a8'; GOLD='#ffd257'

def bear(cx, baseline, h):
    s=h/BH
    return (f'<g transform="translate({cx-BW*s/2:.2f},{baseline-h:.2f}) scale({s:.4f})">'
            f'<path d="{BEAR}" fill="#ffffff" stroke="{NAVY}" stroke-width="{2.0/s:.2f}" '
            f'stroke-linejoin="round" paint-order="stroke"/></g>')

def wings(cx, cy):
    """Both wings on the bear's back — its LEFT in frame, since it faces right.
    Long enough to read as wings: a swept leading edge out to a tip, then three
    scallops back along the trailing edge."""
    def w(ax, ay, span, rise, sc):
        tipx, tipy = ax-span, ay-rise
        s1x, s1y = ax-span*0.68, ay-rise*0.30
        s2x, s2y = ax-span*0.44, ay-rise*0.10
        s3x, s3y = ax-span*0.20, ay+rise*0.06
        return (f'<path d="M{ax:.1f} {ay:.1f} '
                f'C{ax-span*0.30:.1f} {ay-rise*0.55:.1f} {ax-span*0.72:.1f} {ay-rise*0.98:.1f} {tipx:.1f} {tipy:.1f} '
                f'Q{s1x+span*0.10:.1f} {s1y-rise*0.10:.1f} {s1x:.1f} {s1y:.1f} '
                f'Q{s2x+span*0.10:.1f} {s2y-rise*0.16:.1f} {s2x:.1f} {s2y:.1f} '
                f'Q{s3x+span*0.09:.1f} {s3y-rise*0.16:.1f} {s3x:.1f} {s3y:.1f} Z" '
                f'fill="{GOLD}" stroke="{NAVY}" stroke-width="{1.2*sc:.1f}" stroke-linejoin="round"/>')
    return w(cx-1, cy+9, 27, 25, 1) + w(cx-3, cy+14, 22, 18, 1)

def umbrella(cx, top, r=13):
    return (f'<g stroke="{NAVY}" stroke-width="1.2" stroke-linejoin="round">'
            f'<path d="M{cx-r} {top+r*0.52} A{r} {r} 0 0 1 {cx+r} {top+r*0.52} '
            f'Q{cx+r*0.66} {top+r*0.28} {cx+r*0.33} {top+r*0.52} '
            f'Q{cx} {top+r*0.28} {cx-r*0.33} {top+r*0.52} '
            f'Q{cx-r*0.66} {top+r*0.28} {cx-r} {top+r*0.52} Z" fill="{GOLD}"/>'
            f'<path d="M{cx} {top+r*0.52} V{top+r*2.0}" stroke-linecap="round" fill="none"/></g>')

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
 dict(cap='3 BIRDIES', grad='g-bird', art=lambda cx,cy: wings(cx-1, cy-8) + bear(cx+5, cy+23, 46)),
 dict(cap='RAIN',      grad='g-rain', art=lambda cx,cy: umbrella(cx+3, cy-26) + bear(cx-1, cy+23, 44)),
 dict(cap='SUNNY',     grad='g-sun',  art=lambda cx,cy: sunburst(cx+2, cy-9) + bear(cx, cy+23, 46)),
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
                   f'<circle cx="0" cy="0" r="34" fill="none" stroke="{NAVY}" stroke-width="2.4"/></g>')
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
