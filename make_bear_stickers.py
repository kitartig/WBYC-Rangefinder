#!/usr/bin/env python3
"""Bear stickers v2 — one white bear (the club's own, traced from the burgee),
navy keyline, gold props, three gradient fields, navy rule."""
import cairosvg
BEAR=open('bear-path.txt').read(); BW=float(open('bear-vb.txt').read()); BH=100.0
WING=open('wing-path.txt').read(); WW=float(open('wing-vb.txt').read())
CLUB=open('club-path.txt').read(); CW=float(open('club-vb.txt').read())
WANG=float(open('wing-angle.txt').read())   # the drawing's long axis
NAVY='#1638a8'; GOLD='#ffd257'

def bear(cx, baseline, h):
    s=h/BH
    return (f'<g transform="translate({cx-BW*s/2:.2f},{baseline-h:.2f}) scale({s:.4f})">'
            f'<path d="{BEAR}" fill="#ffffff" stroke="{NAVY}" stroke-width="{0.75/s:.2f}" '
            f'stroke-linejoin="round" paint-order="stroke"/></g>')

def wings(cx, cy, h=40, kx=1.0, root=None):
    """Kit's traced sketch, CONDENSED — narrowed on x while keeping full height,
    like condensed type, so it stands tall and thick. (Earlier passes squashed y,
    or squashed across the wing's own axis; both made it flatter, which is the
    opposite of what's wanted.)"""
    sc=h/100.0
    if root is not None: cx = root - WW*sc*kx/2     # align the wing's root edge, not its centre
    return (f'<g transform="translate({cx:.2f},{cy:.2f}) scale({kx:.3f},1) '
            f'translate({-WW*sc/2:.2f},{-h/2:.2f}) scale({sc:.4f})">'
            f'<path d="{WING}" fill="{GOLD}" stroke="{NAVY}" stroke-width="{0.7/sc:.2f}" '
            f'vector-effect="non-scaling-stroke" stroke-linejoin="round"/></g>')


def club(cx, cy, h=30):
    """Kit's traced club — head and shaft as one drawn silhouette. Placed so the
    grip end tucks behind the bear's shoulder."""
    sc=h/100.0
    return (f'<g transform="translate({cx-CW*sc/2:.2f},{cy-h/2:.2f}) scale({sc:.4f})">'
            f'<path d="{CLUB}" fill="{GOLD}" stroke="{NAVY}" stroke-width="{0.7/sc:.2f}" '
            f'vector-effect="non-scaling-stroke" stroke-linejoin="round"/></g>')

def umbrella(cx, top, rx=15.5, ry=9.5):
    """flattened canopy — wider than tall"""
    return (f'<g stroke="{NAVY}" stroke-width="0.7" stroke-linejoin="round">'
            f'<path d="M{cx-rx} {top+ry} A{rx} {ry} 0 0 1 {cx+rx} {top+ry} '
            f'Q{cx+rx*0.66:.1f} {top+ry*0.55:.1f} {cx+rx*0.33:.1f} {top+ry} '
            f'Q{cx} {top+ry*0.55:.1f} {cx-rx*0.33:.1f} {top+ry} '
            f'Q{cx-rx*0.66:.1f} {top+ry*0.55:.1f} {cx-rx} {top+ry} Z" fill="{GOLD}"/>'
            f'<path d="M{cx} {top+ry*0.78:.1f} V{top+ry+18}" stroke-linecap="round" fill="none"/></g>')

def sunburst(cx, cy, r=20, ink="#fff36b"):
    import math
    rays=''.join(
        f'<path d="M{cx+math.cos(math.radians(a))*r*0.62:.1f} {cy+math.sin(math.radians(a))*r*0.62:.1f} '
        f'L{cx+math.cos(math.radians(a))*r:.1f} {cy+math.sin(math.radians(a))*r:.1f}" '
        f'stroke="{ink}" stroke-width="3" stroke-linecap="round"/>' for a in range(0,360,30))
    return f'<circle cx="{cx}" cy="{cy}" r="{r*0.5:.1f}" fill="{ink}"/>'+rays

GRADS = {
 'g-bird': [('0%','#ff4fd0'),('55%','#d95fe4'),('100%','#a56ae0')],
 'g-rain': [('0%','#c3ecff'),('55%','#7cc2ee'),('100%','#4a8fd0')],
 'g-sun':  [('0%','#f2ffa8'),('50%','#c2ee63'),('100%','#5cb861')],
 'g-drive':[('0%','#f26fae'),('50%','#ffb3d1'),('100%','#ffe98a')],
}
SET=[
 dict(cap='3 BIRDIES', grad='g-bird', art=lambda cx,cy: wings(cx, cy-4, 18, 1.0, root=cx-8.2) + bear(cx, cy+23, 42)),
 dict(cap='RAIN',      grad='g-rain', art=lambda cx,cy: umbrella(cx, cy-25) + bear(cx, cy+27, 40)),
 dict(cap='SUNNY',     grad='g-sun',  art=lambda cx,cy: sunburst(cx+1, cy-21, 17) + bear(cx, cy+22.5, 41)),
 dict(cap='277Y DRIVE', grad='g-drive', art=lambda cx,cy: club(cx-14, cy-8, 32) + bear(cx, cy+23, 42)),
]

def defs():
    out=['<defs>']
    for k,stops in GRADS.items():
        out.append(f'<linearGradient id="{k}" x1="0" y1="0" x2="0.35" y2="1">'
                   +''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in stops)+'</linearGradient>')
    for i in range(len(SET)):
        out.append(f'<clipPath id="cl{i}"><circle cx="0" cy="0" r="33"/></clipPath>')
    out.append('</defs>')
    return ''.join(out)

def sheet(scale, y0, label):
    out=[f'<text x="26" y="{y0}" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#6b6350">{label}</text>']
    r=34*scale; top=y0+26; pitch=r*2+26*scale
    for i,s in enumerate(SET):
        cx=44+r+i*pitch; cy=top+r
        out.append(f'<g transform="translate({cx},{cy}) scale({scale})">'
                   f'<circle cx="0" cy="0" r="34" fill="url(#{s["grad"]})"/>'
                   f'<g clip-path="url(#cl{i})">{s["art"](0,0)}</g>'
                   f'<circle cx="0" cy="0" r="34" fill="none" stroke="{NAVY}" stroke-width="1.1"/></g>')
        out.append(f'<text x="{cx}" y="{cy+r+15*min(scale,1.3):.0f}" text-anchor="middle" font-family="DejaVu Sans" '
                   f'font-size="{10*min(scale,1.3):.0f}" font-weight="bold" letter-spacing=".4" fill="{NAVY}">{s["cap"]}</text>')
    return ''.join(out), top+r*2+30*min(scale,1.4)

b1,y=sheet(2.4, 42, 'AT 2.4x')
b2,y2=sheet(1.0, y+44, 'ACTUAL SIZE — 68px')
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {y2+18:.0f}" width="1800" height="{(y2+18)*2:.0f}">'
     f'<rect width="900" height="{y2+18:.0f}" fill="#fffdf7"/>{defs()}{b1}{b2}</svg>')
open('bear-stickers.svg','w').write(svg)
cairosvg.svg2png(url='bear-stickers.svg', write_to='bear-stickers.png', output_width=1400)
print('rendered')
