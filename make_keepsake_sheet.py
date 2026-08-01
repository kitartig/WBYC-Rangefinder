import base64, os
from PIL import ImageFont

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB= "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def w(txt, size, bold=False):
    try: f=ImageFont.truetype(SANSB if bold else SANS, size)
    except Exception: return len(txt)*size*0.55
    return f.getlength(txt)

crest = base64.b64encode(open('/tmp/crest.png','rb').read()).decode()  # cairosvg can't decode webp
W, PAD = 620, 26
L, R = PAD, W-PAD
s = []
def t(x,y,txt,size,fill,fam="DejaVu Sans",weight="normal",style="normal",anchor="start",ls=None):
    a=f' letter-spacing="{ls}"' if ls else ''
    s.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
             f'font-style="{style}" fill="{fill}" text-anchor="{anchor}"{a}>{txt}</text>')
G="EB Garamond"

# ---------- page ----------
H = 1286
s.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="#fffdf7" stroke="#e5dbc4"/>')
s.append(f'<rect x="9" y="9" width="{W-18}" height="{H-18}" rx="12" fill="none" stroke="#ece2c9"/>')

# ---------- masthead ----------
s.append(f'<image x="{L-26}" y="2" width="238" height="158.6" xlink:href="data:image/png;base64,{crest}"/>')
TX = L+182
t(TX, 44, "THE BEAR&#8217;S LOG &#183; WBYC", 11, "#0e6b3a", weight="bold", ls="2.6")
t(TX, 84, "Wednesday, July 29", 32, "#1a1712", fam=G, weight="500")
t(TX, 112, "Kit &#183; Green tees", 16, "#6b6350", fam=G, style="italic")
t(R, 46, "Sunny &#183; 78&#176;F", 12.5, "#1a1712", anchor="end")
t(R, 64, "SW wind 8 mph", 12.5, "#6b6350", anchor="end")
s.append(f'<line x1="{L}" y1="128" x2="{R}" y2="128" stroke="#4d84c4"/>')

# ---------- the score ----------
y=164
t(L, y, "The Score", 18, "#1b3a66", fam=G, weight="500")
t(L, y+58, "78", 64, "#1a1712", fam=G, weight="500")
t(L+82, y+52, "+4", 23, "#f000c2", fam=G, weight="500")
cx=R
for label in ["11 greens","33 putts"]:
    tw=w(label,12.5,True); pw=tw+24
    s.append(f'<rect x="{cx-pw:.1f}" y="{y+22}" width="{pw:.1f}" height="26" rx="13" fill="#fdeef8" stroke="#f2b2df"/>')
    t(cx-pw/2, y+39, label, 12.5, "#b3018f", weight="bold", anchor="middle")
    cx -= pw+8

# ---------- the card ----------
y=260
t(L, y, "The Card", 18, "#1b3a66", fam=G, weight="500")
CY, CH, ROW = y+12, 84, 28
s.append(f'<rect x="{L}" y="{CY}" width="{R-L}" height="{CH}" rx="12" fill="#fff" stroke="#9fc2ea" stroke-width="1.4"/>')
cols = 11
cw = (R-L)/cols
labels = ["HOLE","PAR","KIT"]
holes = ["1","2","3","4","5","6","7","8","9"]
pars  = ["4","4","5","3","4","4","5","3","5"]
you   = [("4",None),("2","eagle"),("6","bog"),("3",None),("3","bird"),("5","bog"),("5",None),("4","bog"),("5",None)]
tots  = ["OUT","37","37"]
for r_i in range(3):
    ry = CY + r_i*ROW
    if r_i: s.append(f'<line x1="{L}" y1="{ry}" x2="{R}" y2="{ry}" stroke="#dceaf6"/>')
    s.append(f'<rect x="{L+0.7}" y="{ry+(0.7 if r_i==0 else 0)}" width="{cw-0.7}" height="{ROW-(0.7 if r_i==0 else 0)}" fill="#f4f9ff"/>')
    s.append(f'<rect x="{R-cw}" y="{ry+(0.7 if r_i==0 else 0)}" width="{cw-0.7}" height="{ROW-(0.7 if r_i==0 else 0)}" fill="#f4f9ff"/>')
    t(L+cw/2, ry+ROW/2+4, labels[r_i], 10.5, "#1b3a66", weight="bold", anchor="middle", ls="0.5")
    t(R-cw/2, ry+ROW/2+4.5, tots[r_i], 12.5, "#1b3a66", weight="bold", anchor="middle")
    for i in range(9):
        x = L+cw*(i+1)+cw/2
        if r_i==0: t(x, ry+ROW/2+4.5, holes[i], 12.5, "#1b3a66", anchor="middle")
        elif r_i==1: t(x, ry+ROW/2+4.5, pars[i], 12.5, "#7a7362", weight="bold", anchor="middle")
        else:
            v,mk = you[i]
            if mk in ("bird","eagle"):
                s.append(f'<circle cx="{x}" cy="{ry+ROW/2}" r="11.5" fill="none" stroke="#f000c2" stroke-width="1.7"/>')
                if mk=="eagle": s.append(f'<circle cx="{x}" cy="{ry+ROW/2}" r="14.9" fill="none" stroke="#f000c2" stroke-width="1.7"/>')
                t(x, ry+ROW/2+4.5, v, 12.5, "#f000c2", weight="bold", anchor="middle")
            elif mk=="bog":
                s.append(f'<rect x="{x-11.5}" y="{ry+ROW/2-11.5}" width="23" height="23" rx="3" fill="none" stroke="#ffa300" stroke-width="1.7"/>')
                t(x, ry+ROW/2+4.5, v, 12.5, "#c9760a", weight="bold", anchor="middle")
            else:
                t(x, ry+ROW/2+4.5, v, 12.5, "#1b3a66", anchor="middle")
for i in range(1, cols):
    s.append(f'<line x1="{L+cw*i}" y1="{CY}" x2="{L+cw*i}" y2="{CY+CH}" stroke="#eaf1fb"/>')

# ---------- the moments ----------
y = CY+CH+38
t(L, y, "The Moments", 18, "#1b3a66", fam=G, weight="500")
moms=[("#f000c2","&#8595;","Eagle on the 2nd","&#160;&#8212; 2 on the par 4."),
      ("#f000c2","&#8595;","Birdie on the 5th","&#160;&#8212; 3 on the par 4."),
      ("#ffa300","D","Longest shot","&#160;&#8212; 277 yards with the D."),
      ("#0e6b3a","P","8 pars","&#160;&#8212; steady stuff.")]
my = y+22
for col,gl,bold,rest in moms:
    s.append(f'<circle cx="{L+10}" cy="{my+6}" r="10" fill="{col}"/>')
    t(L+10, my+10, gl, 11, "#fff", weight="bold", anchor="middle")
    bw=w(bold,14,True)
    t(L+30, my+11, bold, 14, "#1a1712", weight="bold")
    t(L+30+bw, my+11, rest, 14, "#1a1712")
    s.append(f'<line x1="{L+30}" y1="{my+23}" x2="{L+330}" y2="{my+23}" stroke="#e5dbc4" stroke-dasharray="1 3"/>')
    my += 34
# green diagram — the engine's own markup, verbatim, translated into place.
# Its native box is 210x190; the app's gradients are what gives the shading.
GW, GH = 210, 190
gx, gy = R-GW, y+14
s.append(f'<defs>'
  f'<linearGradient id="blt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9bd79a"/><stop offset="1" stop-color="#69bd79"/></linearGradient>'
  f'<radialGradient id="blg" cx="50%" cy="40%" r="62%"><stop offset="0" stop-color="#dff7dd"/><stop offset="1" stop-color="#a6e0b3"/></radialGradient>'
  f'</defs>')
s.append(f'<g transform="translate({gx},{gy})">'
  f'<rect width="210" height="190" rx="12" fill="url(#blt)"/>'
  f'<ellipse cx="106" cy="54" rx="50" ry="35" fill="url(#blg)" stroke="#fff" stroke-width="1.5"/>'
  f'<ellipse cx="166" cy="138" rx="20" ry="12" fill="#ecd39a" opacity=".95"/>'
  f'<path d="M103 164 Q76 102 100 66" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="4.5 4.5" opacity=".9"/>'
  f'<circle cx="103" cy="166" r="5" fill="#fff" stroke="#f5b512" stroke-width="1.4"/>'
  f'<g transform="translate(100,60)"><path d="M0 -11 L3.2 -3.4 L11 -3.4 L4.6 1.6 L7.1 9.3 L0 4.6 L-7.1 9.3 L-4.6 1.6 L-11 -3.4 L-3.2 -3.4 Z" fill="#f000c2" stroke="#fff" stroke-width="1.1"/></g>'
  f'<text x="106" y="112" text-anchor="middle" font-family="EB Garamond" font-style="italic" font-size="14" fill="#0e5a32">the 2nd</text>'
  f'</g>')
t(gx+GW/2, gy+GH+18, "eagle, on the 2nd", 12.5, "#6b6350", fam=G, style="italic", anchor="middle")

# ---------- note bar ----------
y = max(my+18, gy+GH+42)
s.append(f'<path d="M{L} {y} h{R-L-10} a10 10 0 0 1 10 10 v42 a10 10 0 0 1 -10 10 h{-(R-L-10)} z" fill="#fbe3f4"/>')
s.append(f'<rect x="{L}" y="{y}" width="6" height="62" fill="#f000c2"/>')
t(L+22, y+38, "Tap to add a note about your round&#8230;", 19, "#8a8270", fam=G, style="italic")

# ---------- earned today ----------
y += 96
t(L, y, "Earned today", 18, "#1b3a66", fam=G, weight="500")
seals=[("#f000c2","#fdeaf6","#f000c2","3 BIRDIES","pennant"),
       ("#ffa300","#fbeeda","#c9760a","277Y DRIVE","arrow"),
       ("#8fbce0","#eaf3fb","#2f6ea0","SUNNY","sun"),
       ("#5cbf84","#eef8f1","#0e6b3a","18 HOLES","check")]
sy = y+50
span = len(seals)*74 + (len(seals)-1)*16
sx = (W-span)/2 + 37
for bc,bg,cap,label,glyph in seals:
    s.append(f'<circle cx="{sx}" cy="{sy}" r="28" fill="{bg}" stroke="{bc}" stroke-width="2"/>')
    if glyph=="pennant":
        s.append(f'<line x1="{sx-7}" y1="{sy-12}" x2="{sx-7}" y2="{sy+12}" stroke="{bc}" stroke-width="2.6"/>'
                 f'<path d="M{sx-7} {sy-11} L{sx+9} {sy-6} L{sx-7} {sy-1} Z" fill="{bc}"/>')
    elif glyph=="arrow":
        s.append(f'<path d="M{sx-11} {sy+10} L{sx+11} {sy-8}" stroke="{bc}" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="M{sx+3} {sy-9} L{sx+12} {sy-9} L{sx+12} {sy}" fill="none" stroke="{bc}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    elif glyph=="sun":
        s.append(f'<circle cx="{sx}" cy="{sy}" r="8" fill="none" stroke="{cap}" stroke-width="2.6"/>')
        import math
        for k in range(8):
            a=math.radians(k*45); x1,y1=sx+11*math.cos(a),sy+11*math.sin(a); x2,y2=sx+15.5*math.cos(a),sy+15.5*math.sin(a)
            s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{cap}" stroke-width="2.6" stroke-linecap="round"/>')
    else:
        s.append(f'<path d="M{sx-11} {sy+1} L{sx-3} {sy+9} L{sx+12} {sy-9}" fill="none" stroke="{cap}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
    t(sx, sy+44, label, 10, cap, weight="bold", anchor="middle", ls="0.4")
    sx += 90
t(W/2, sy+74, "Earned automatically from your round. Soon you&#8217;ll tap any hole to add your own.", 13, "#6b6350", fam=G, style="italic", anchor="middle")

# ---------- quote ----------
y = sy+104
s.append(f'<rect x="{L}" y="{y}" width="{R-L}" height="96" rx="14" fill="#e4f5f3" stroke="#bfe3df"/>')
t(L+20, y+46, "&#8220;", 60, "#2fb0a8", fam=G, weight="500")
t(W/2, y+46, "An eagle on the card &#8212; a day the 2nd won&#8217;t forget.", 18, "#1a1712", fam=G, style="italic", anchor="middle")
t(W/2, y+72, "&#8212; KEPT FOR KIT BY THE WBYC RANGEFINDER", 13, "#6b6350", anchor="middle", ls="1")

# ---------- photographs ----------
y += 130
t(L, y, "THE PHOTOGRAPHS", 12, "#1b3a66", weight="bold", ls="1.4")
s.append(f'<rect x="{L}" y="{y+14}" width="150" height="112" rx="10" fill="none" stroke="#c3b79a" stroke-width="1.5" stroke-dasharray="5 4"/>')
t(L+75, y+74, "+ add a photograph", 12.5, "#6b6350", weight="bold", anchor="middle")
t(L, y+150, "0 of 4 &#183; 2KB of roughly 5000KB used", 11, "#8a8270")

# ---------- footer ----------
fy = y+186
s.append(f'<line x1="{L}" y1="{fy}" x2="{R}" y2="{fy}" stroke="#e5dbc4"/>')
t(W/2, fy+22, "WHITE BEAR YACHT CLUB &#183; EST. 1889 &#183; WEDNESDAY, JULY 29", 11, "#6b6350", anchor="middle", ls="0.6")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'viewBox="-24 -24 {W+48} {H+48}" width="{W+48}" height="{H+48}">'
       f'<rect x="-24" y="-24" width="{W+48}" height="{H+48}" fill="#f2e7cf"/>' + "".join(s) + '</svg>')
open('/tmp/keepsake.svg','w').write(svg)
print('svg bytes', len(svg), '| page height', H)
