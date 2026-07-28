#!/usr/bin/env python3
"""Compose the Back Pocket demo GIF — full-height app screens, charcoal canvas.

Each beat shows the WHOLE app screen (header through hazards), stitched from two
scroll captures, so nothing is clipped mid-map. The flight profile inset is on,
which is the arc under the map: trajectory drawn over a terrain cross-section.

Type is Liberation Sans Narrow Bold throughout. Headlines carry explicit line
breaks rather than auto-wrapping, so phrases break where they should ("Your
course, / in your back pocket." never splits "back pocket").

Usage:  python3 make_backpocket_gif.py
Output: back-pocket-demo-dark.gif (1080x1080)
"""
import os, subprocess, shutil, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'demo-assets')
WORK = '/tmp/bp/frames_v3'
OUT_GIF = os.path.join(HERE, 'back-pocket-demo-dark.gif')

PITCH = ['A GPS caddie in your club’s colors.',
         'Built from your course’s own ground.']

CHAR = (20, 23, 26)
CREAM = (242, 231, 207)
MINT = (123, 233, 187)     # midpoint of the L1 ramp #5CE4EA -> #9BEE8C
MUTED = (150, 158, 166)
RULE = (44, 49, 56)

W = H = 1080
CARD_H = 880
CARD_W = 351                # 0.3994 aspect, matching the stitched screens
CARD_X, CARD_Y = W - 64 - CARD_W, 100
COL_X, COL_R = 64, 620

F_B = '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
F_R = '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf'
# Liberation Sans Narrow has no ★ glyph — it renders as tofu. DejaVu does.
F_SYM = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(p, s):
    return ImageFont.truetype(p, s)


def track(d, xy, text, f, fill, spacing=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + spacing


def track_w(d, text, f, spacing):
    return sum(d.textlength(c, font=f) + spacing for c in text) - spacing


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def mark(size):
    svg = open(os.path.join(HERE, '..', 'brands', 'assets', 'backpocket-mark.svg'), encoding='utf-8').read()
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert('RGBA')


def card(img):
    im = img.resize((CARD_W, CARD_H), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (CARD_W, CARD_H), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, CARD_W - 1, CARD_H - 1), radius=22, fill=255)
    im.putalpha(m)
    return im


def glow(c, box, radius=22):
    x0, y0, x1, y1 = box
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle((x0 - 6, y0 - 4, x1 + 6, y1 + 10), radius=radius + 4,
                                        fill=(120, 210, 180, 44))
    c.alpha_composite(g.filter(ImageFilter.GaussianBlur(22)))


def build(shot, beat, progress):
    c = Image.new('RGBA', (W, H), CHAR + (255,))
    d = ImageDraw.Draw(c)

    if beat.get('bleed'):
        # 3D terrain fills the frame. The arc only reads with the camera rotated,
        # which makes the composition wide — so this beat breaks the portrait-card
        # rhythm deliberately, as the climax.
        im = shot.convert('RGB')
        sc = max(W / im.width, (H - 150) / im.height)
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        c.alpha_composite(im.convert('RGBA'),
                          ((W - im.width) // 2, (H - 150 - im.height) // 2))
        veil = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(veil).rectangle((0, H - 300, W, H), fill=(20, 23, 26, 215))
        c.alpha_composite(veil.filter(ImageFilter.GaussianBlur(28)))
        f_h, f_s = font(F_B, 58), font(F_R, 26)
        y = H - 250
        for ln in beat['headline']:
            d.text((COL_X, y), ln, font=f_h, fill=CREAM); y += 66
        for ln in wrap(d, beat['sub'], f_s, W - 2 * COL_X):
            d.text((COL_X, y + 6), ln, font=f_s, fill=MUTED); y += 34
        bx0, bx1, by = COL_X, W - COL_X, 1030
        d.rounded_rectangle((bx0, by, bx1, by + 6), radius=3, fill=RULE)
        if progress > 0:
            d.rounded_rectangle((bx0, by, bx0 + int((bx1 - bx0) * progress), by + 6),
                                radius=3, fill=MINT)
        return c.convert('RGB')

    if shot is not None:
        glow(c, (CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H))
        c.alpha_composite(card(shot), (CARD_X, CARD_Y))

    if beat.get('end'):
        m = mark(250)
        f = font(F_B, 70)
        f2 = font(F_B, 26)
        lines = beat['headline']
        block = m.height + 66 + len(lines) * 82 + 38 + 32
        y = (H - block) / 2 - 10
        c.alpha_composite(m, ((W - m.width) // 2, int(y)))
        y += m.height + 66
        for ln in lines:
            d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=CREAM)
            y += 82
        y += 38
        track(d, ((W - track_w(d, beat['sub'], f2, 6)) / 2, y), beat['sub'], f2, MINT, spacing=6)
    else:
        c.alpha_composite(mark(64), (COL_X, 92))
        track(d, (COL_X + 84, 114), 'BACK POCKET', font(F_B, 23), CREAM, spacing=3.4)
        f_p = font(F_R, 25)
        py = 178
        for ln in PITCH:
            d.text((COL_X, py), ln, font=f_p, fill=MUTED)
            py += 32

        f_h, f_s = font(F_B, 62), font(F_R, 27)
        f_b = font(F_SYM, 118) if beat.get('sym') else font(F_B, 132)
        hl = beat['headline']
        sl = wrap(d, beat['sub'], f_s, COL_R - COL_X)
        block = len(hl) * 72 + 34 + 158 + len(sl) * 38
        y = 300 + max(0, (900 - 300 - block) / 2)

        for ln in hl:
            d.text((COL_X, y), ln, font=f_h, fill=CREAM)
            y += 72
        y += 34
        d.text((COL_X, y), beat['big'], font=f_b, fill=MINT)
        y += 158
        for ln in sl:
            d.text((COL_X, y), ln, font=f_s, fill=MUTED)
            y += 38

        d.line((COL_X, 918, COL_R, 918), fill=RULE, width=2)
        track(d, (COL_X, 940), 'HOLE 1 · PAR 4 · 388 YDS', font(F_B, 21), CREAM, spacing=1.6)
        d.text((COL_X, 972), 'Elevation: USGS 3DEP · contours every 2 ft',
               font=font(F_R, 21), fill=MUTED)

    bx0, bx1, by = COL_X, W - COL_X, 1030
    d.rounded_rectangle((bx0, by, bx1, by + 6), radius=3, fill=RULE)
    if progress > 0:
        d.rounded_rectangle((bx0, by, bx0 + int((bx1 - bx0) * progress), by + 6), radius=3, fill=MINT)
    return c.convert('RGB')


def main():
    beats = [
        dict(img='bp4_A.png', headline=['Stand on', 'the tee.'], big='388',
             sub='to the center. Plays 407 — five feet uphill, plus seventeen for the wind.', hold=18),
        dict(img='bp4_B.png', headline=['Move up', 'the fairway.'], big='264',
             sub='Plays 286 — thirty-three feet of climb, drawn as an arc over the real ground.', hold=18),
        dict(img='bp4_C.png', headline=['Drop', 'today’s pin.'], big='258',
             sub='Every distance re-keys to it, and the flight profile redraws with them.', hold=18),
        dict(img='bp4_D.png', headline=['Mark the shot', 'you’ll retell.'], big='★', sym=True,
             sub='Pinned to the spot. It comes back every time you play the hole, and it’s kept in the Round Log.', hold=20),
        dict(orbit=['bp4_3d0.png', 'bp4_3d1.png', 'bp4_3d2.png', 'bp4_3d3.png', 'bp4_3d4.png'],
             bleed=True, headline=['Then see the ground itself.'],
             sub='Contours every two feet from USGS elevation, with the shot flown over real terrain.',
             hold=16),
        dict(img=None, end=True, headline=['Your course,', 'in your back pocket.'],
             sub='BACK POCKET', hold=14),
    ]

    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK, exist_ok=True)
    total = sum(b['hold'] for b in beats)
    n = 0
    for b in beats:
        if b.get('orbit'):
            frames = [Image.open(os.path.join(ASSETS, f)) for f in b['orbit']]
            seq = frames + frames[-2:0:-1]          # ping-pong, no jump at the loop
            for i in range(b['hold']):
                build(seq[i % len(seq)], b, n / (total - 1)).save(f'{WORK}/f{n:04d}.png')
                n += 1
            continue
        shot = Image.open(os.path.join(ASSETS, b['img'])) if b.get('img') else None
        for _ in range(b['hold']):
            build(shot, b, n / (total - 1)).save(f'{WORK}/f{n:04d}.png')
            n += 1
    print(f'rendered {n} frames ({n/12.5:.1f}s at 12.5fps)')

    pal = f'{WORK}/palette.png'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '12.5',
                    '-i', f'{WORK}/f%04d.png',
                    '-vf', 'scale=880:880:flags=lanczos,palettegen=max_colors=128:stats_mode=diff', pal], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '12.5',
                    '-i', f'{WORK}/f%04d.png', '-i', pal,
                    '-lavfi', '[0:v]scale=880:880:flags=lanczos[s];[s][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
                    '-loop', '0', OUT_GIF], check=True)
    print(f'wrote {OUT_GIF}  {os.path.getsize(OUT_GIF)/1e6:.2f} MB')


if __name__ == '__main__':
    main()
