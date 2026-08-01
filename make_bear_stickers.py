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
    """Angel-wing pose from Kit's reference: covert shoulder LOW, primaries
    sweeping UP and outward, longest at the top. (I had it inverted — coverts
    high with primaries falling, which is a folded wing, not a spread one.)"""
    import math
    sx, sy = cx+7, cy+14                    # shoulder, low on the bear's back
    out=[]
    # up-left in SVG's y-down space is 190-240 deg; longest feather highest
    prim=[(232,34,4.4),(222,31,4.2),(212,27,4.0),(202,22,3.7),(193,17,3.3)]
    for ang,L,Wd in prim:
        a=math.radians(ang)
        tx,ty = sx+math.cos(a)*L*0.86, sy+math.sin(a)*L - L*0.10
        mx,my = sx+math.cos(a)*L*0.52, sy+math.sin(a)*L*0.46
        px,py = math.cos(a+math.pi/2)*Wd, math.sin(a+math.pi/2)*Wd
        out.append(
          f'<path d="M{sx:.1f} {sy:.1f} '
          f'C{mx+px:.1f} {my+py:.1f} {tx+px*0.55:.1f} {ty+py*0.55:.1f} {tx:.1f} {ty:.1f} '
          f'C{tx-px*0.55:.1f} {ty-py*0.55:.1f} {mx-px:.1f} {my-py:.1f} {sx:.1f} {sy:.1f} Z" '
          f'fill="{GOLD}" stroke="{NAVY}" stroke-width=".9" stroke-linejoin="round"/>')
    # covert cap over the roots, now sitting UNDER the fan
    cov=(f'<path d="M{sx+2:.1f} {sy-5:.1f} '
         f'C{sx+3:.1f} {sy+6:.1f} {sx-6:.1f} {sy+11:.1f} {sx-13:.1f} {sy+8:.1f} '
         f'Q{sx-9:.1f} {sy+4:.1f} {sx-12:.1f} {sy+1:.1f} '
         f'Q{sx-7:.1f} {sy-1:.1f} {sx-9:.1f} {sy-4:.1f} '
         f'Q{sx-4:.1f} {sy-5:.1f} {sx-5:.1f} {sy-8:.1f} Z" '
         f'fill="{GOLD}" stroke="{NAVY}" stroke-width=".9" stroke-linejoin="round"/>')
    return ''.join(out)+cov

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
 'g-bird': [('0%','#ff9ceb'),('55%','#e46fe0'),('100%','#a56ae0')],
 'g-rain': [('0%','#c3ecff'),('55%','#7cc2ee'),('100%','#4a8fd0')],
 'g-sun':  [('0%','#fff4d2'),('50%','#ffd166'),('100%','#ffa23e')],
}
SET=[
 dict(cap='3 BIRDIES', grad='g-bird', art=lambda cx,cy: wings(cx-4, cy-4) + bear(cx+8, cy+26, 42)),
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
