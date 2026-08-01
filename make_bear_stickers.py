#!/usr/bin/env python3
"""Prototype bear stickers for The Bear's Log. The bear is the CLUB'S bear —
traced from component #95 of the burgee artwork, not drawn."""
import cairosvg

BEAR = open('bear-path.txt').read()          # viewBox 0 0 49 100, upright bear
BW, BH = float(open('bear-vb.txt').read()), 100.0

def bear(x, y, h, fill, extra=''):
    s = h/BH
    return (f'<g transform="translate({x - BW*s/2:.1f},{y - h:.1f}) scale({s:.4f})">'
            f'<path d="{BEAR}" fill="{fill}"{extra}/></g>')

def disc(cx, cy, r, ring, bg):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{ring}" stroke-width="2"/>'

NAVY='#1638a8'

def wings(cx, cy, ink):
    """swept up and BACK from the shoulders, scalloped along the trailing edge —
    low and angled, or they read as ears"""
    def w(d):
        return (f'<path d="M{cx+d*5:.1f} {cy+3:.1f} '
                f'C{cx+d*13:.1f} {cy-1:.1f} {cx+d*22:.1f} {cy-8:.1f} {cx+d*25:.1f} {cy-17:.1f} '
                f'C{cx+d*22:.1f} {cy-13:.1f} {cx+d*20:.1f} {cy-14:.1f} {cx+d*19:.1f} {cy-10:.1f} '
                f'C{cx+d*17:.1f} {cy-12:.1f} {cx+d*15:.1f} {cy-11:.1f} {cx+d*14:.1f} {cy-7:.1f} '
                f'C{cx+d*12:.1f} {cy-9:.1f} {cx+d*10:.1f} {cy-7:.1f} {cx+d*9:.1f} {cy-3:.1f} Z" fill="{ink}"/>')
    return w(-1)+w(1)

def umbrella(cx, top, ink):
    """canopy r=15 so the whole thing sits inside a 33 disc"""
    return (f'<path d="M{cx-15} {top+8} A15 15 0 0 1 {cx+15} {top+8} '
            f'Q{cx+10} {top+4.5} {cx+5} {top+8} Q{cx} {top+4.5} {cx-5} {top+8} '
            f'Q{cx-10} {top+4.5} {cx-15} {top+8} Z" fill="{ink}"/>'
            f'<path d="M{cx} {top+8} V{top+26}" stroke="{ink}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M{cx} {top+26} q0 4.5 -4.5 4.5" fill="none" stroke="{ink}" stroke-width="2.2" stroke-linecap="round"/>')

def visor(cx, cy, ink):
    """brim + band only — a crown turns it into a bowler hat"""
    return (f'<path d="M{cx-13.5} {cy} q13.5 -7.5 27 0 z" fill="{ink}"/>'
            f'<rect x="{cx-13.5}" y="{cy-0.5}" width="27" height="4.4" rx="2.2" fill="{ink}"/>'
            f'<rect x="{cx-8.5}" y="{cy+6.5}" width="17" height="4.2" rx="2.1" fill="{ink}"/>')

SET = [
  dict(cap='3 BIRDIES', ring='#f000c2', bg='#fdeaf6',
       art=lambda cx,cy: wings(cx, cy-4, NAVY) + bear(cx, cy+22, 44, '#f000c2')),
  dict(cap='RAIN', ring='#5b8db8', bg='#e9f2f9',
       art=lambda cx,cy: bear(cx, cy+23, 40, '#7fb2d8') + umbrella(cx+1, cy-27, NAVY)),
  dict(cap='SUNNY', ring='#f2a413', bg='#fdf0d8',
       art=lambda cx,cy: bear(cx, cy+22, 44, '#f2a413') + visor(cx-0.5, cy-17, NAVY)),
]

def sheet(scale, y0, label, idbase):
    out=[f'<text x="24" y="{y0}" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#6b6350">{label}</text>']
    r=34*scale
    top=y0+24
    pitch=(r*2)+34*scale
    for i,s in enumerate(SET):
        cx=40+r+i*pitch; cy=top+r
        cid=f'{idbase}{i}'
        out.append(f'<clipPath id="{cid}"><circle cx="0" cy="0" r="33"/></clipPath>')
        out.append(f'<g transform="translate({cx},{cy}) scale({scale})">')
        out.append(disc(0,0,34,s['ring'],s['bg']))
        out.append(f'<g clip-path="url(#{cid})">{s["art"](0,0)}</g>')
        out.append('</g>')
        out.append(f'<text x="{cx}" y="{cy+r+16*min(scale,1.3):.0f}" text-anchor="middle" font-family="DejaVu Sans" '
                   f'font-size="{10*min(scale,1.35):.0f}" font-weight="bold" letter-spacing=".4" fill="{s["ring"]}">{s["cap"]}</text>')
    return ''.join(out), top+r*2+30*min(scale,1.4)

body=''
b1,y = sheet(2.4, 40, 'AT 2.4x — how the drawing reads', 'a')
body+=b1
b2,y2 = sheet(1.0, y+46, 'ACTUAL SIZE — 68px disc, as it appears on the keepsake', 'b')
body+=b2
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 {y2+20:.0f}" width="1560" height="{(y2+20)*2:.0f}">'
     f'<rect width="780" height="{y2+20:.0f}" fill="#fffdf7"/>{body}</svg>')
open('bear-stickers.svg','w').write(svg)
cairosvg.svg2png(url='bear-stickers.svg', write_to='bear-stickers.png', output_width=1280)
print('rendered bear-stickers.png')
