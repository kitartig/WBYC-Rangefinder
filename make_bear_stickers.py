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
    """Wing built the way the reference is drawn: a curved leading edge from the
    shoulder up to the tip, with primaries hanging from points ALONG that edge —
    longest near the tip. Every earlier version fanned everything from one pivot,
    which is why it read as a fan or a butterfly rather than a wing."""
    import math
    S=(cx+9, cy+11)          # shoulder, on the bear's back
    T=(cx-14, cy-21)        # wing tip, up and out
    C1=(cx+2, cy-4)         # leading-edge control points
    C2=(cx-8, cy-20)
    def bez(t):
        mt=1-t
        x=mt**3*S[0]+3*mt*mt*t*C1[0]+3*mt*t*t*C2[0]+t**3*T[0]
        y=mt**3*S[1]+3*mt*mt*t*C1[1]+3*mt*t*t*C2[1]+t**3*T[1]
        return x,y
    out=[]
    # primaries, hung from along the leading edge, drawn outer-first
    for t,L,Wd,ang in [(0.97,23,4.6,150),(0.80,21,4.7,142),(0.62,18,4.6,134),
                       (0.44,15,4.3,126),(0.26,12,3.9,118)]:
        ax,ay=bez(t)
        a=math.radians(ang)
        tx,ty=ax+math.cos(a)*L, ay+math.sin(a)*L
        mx,my=ax+math.cos(a)*L*0.5, ay+math.sin(a)*L*0.5
        px,py=math.cos(a+math.pi/2)*Wd, math.sin(a+math.pi/2)*Wd
        t1=(tx+px*0.3, ty+py*0.3); t2=(tx-px*0.3, ty-py*0.3)
        ox,oy=math.cos(a)*Wd*0.5, math.sin(a)*Wd*0.5
        out.append(f'<path d="M{ax:.1f} {ay:.1f} '
                   f'C{mx+px:.1f} {my+py:.1f} {t1[0]+px*0.3:.1f} {t1[1]+py*0.3:.1f} {t1[0]:.1f} {t1[1]:.1f} '
                   f'Q{tx+ox:.1f} {ty+oy:.1f} {t2[0]:.1f} {t2[1]:.1f} '
                   f'C{mx-px:.1f} {my-py:.1f} {ax-px*0.4:.1f} {ay-py*0.4:.1f} {ax:.1f} {ay:.1f} Z" '
                   f'fill="{GOLD}" stroke="{NAVY}" stroke-width=".85" stroke-linejoin="round"/>')
    # the arm itself: a tapered band along the leading edge, laid over the roots
    arm=(f'<path d="M{S[0]:.1f} {S[1]:.1f} '
         f'C{C1[0]:.1f} {C1[1]:.1f} {C2[0]:.1f} {C2[1]:.1f} {T[0]:.1f} {T[1]:.1f} '
         f'C{T[0]+4:.1f} {T[1]+4:.1f} {C2[0]+7:.1f} {C2[1]+7:.1f} {C1[0]+5:.1f} {C1[1]+8:.1f} '
         f'C{S[0]-1:.1f} {S[1]+5:.1f} {S[0]+2:.1f} {S[1]+3:.1f} {S[0]:.1f} {S[1]:.1f} Z" '
         f'fill="{GOLD}" stroke="{NAVY}" stroke-width=".85" stroke-linejoin="round"/>')
    return ''.join(out)+arm

def umbrella(cx, top, rx=15.5, ry=9.5):
    """flattened canopy — wider than tall"""
    return (f'<g stroke="{NAVY}" stroke-width="1.05" stroke-linejoin="round">'
            f'<path d="M{cx-rx} {top+ry} A{rx} {ry} 0 0 1 {cx+rx} {top+ry} '
            f'Q{cx+rx*0.66:.1f} {top+ry*0.55:.1f} {cx+rx*0.33:.1f} {top+ry} '
            f'Q{cx} {top+ry*0.55:.1f} {cx-rx*0.33:.1f} {top+ry} '
            f'Q{cx-rx*0.66:.1f} {top+ry*0.55:.1f} {cx-rx} {top+ry} Z" fill="{GOLD}"/>'
            f'<path d="M{cx} {top+ry} V{top+ry+30}" stroke-linecap="round" fill="none"/></g>')

def sunburst(cx, cy, r=20, ink="#ef8a17"):
    import math
    rays=''.join(
        f'<path d="M{cx+math.cos(math.radians(a))*r*0.62:.1f} {cy+math.sin(math.radians(a))*r*0.62:.1f} '
        f'L{cx+math.cos(math.radians(a))*r:.1f} {cy+math.sin(math.radians(a))*r:.1f}" '
        f'stroke="{ink}" stroke-width="3" stroke-linecap="round"/>' for a in range(0,360,30))
    return f'<circle cx="{cx}" cy="{cy}" r="{r*0.5:.1f}" fill="{ink}"/>'+rays

GRADS = {
 'g-bird': [('0%','#ff9ceb'),('55%','#e46fe0'),('100%','#a56ae0')],
 'g-rain': [('0%','#c3ecff'),('55%','#7cc2ee'),('100%','#4a8fd0')],
 'g-sun':  [('0%','#fffdf2'),('50%','#fff0c4'),('100%','#ffd98a')],
}
SET=[
 dict(cap='3 BIRDIES', grad='g-bird', art=lambda cx,cy: wings(cx-2, cy-4) + bear(cx+8, cy+26, 42)),
 dict(cap='RAIN',      grad='g-rain', art=lambda cx,cy: umbrella(cx-1, cy-29) + bear(cx-1, cy+26, 40)),
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
