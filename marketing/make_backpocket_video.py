#!/usr/bin/env python3
"""Compose the ~20s Back Pocket product tour as MP4.

Why MP4 and not GIF: at 20 seconds of varied material a GIF lands at 5–8 MB and
dithers badly. H.264 does the same 20s at 1080p for 1–2 MB, and lets the orbit
and the crossfades actually be smooth.

Structure: five portrait "card" beats (the hole, played through), then three
full-bleed beats (3D terrain, scorecard, Round Log) for contrast, then the end
card. Crossfades between beats — cheap in video, ruinous in GIF.

Usage:  python3 make_backpocket_video.py
Output: back-pocket-tour.mp4 (1080x1080, 24fps)
"""
import os, subprocess, shutil, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'demo-assets')
WORK = '/tmp/bp/frames_mp4'
OUT = os.path.join(HERE, 'back-pocket-tour.mp4')

PITCH = ['A GPS caddie in your club’s colors.',
         'Built from your course’s own ground.']

CHAR = (20, 23, 26); CREAM = (242, 231, 207); MINT = (123, 233, 187)
MUTED = (150, 158, 166); RULE = (44, 49, 56)

W = H = 1080
FPS = 24
CARD_H, CARD_W = 880, 351
CARD_X, CARD_Y = W - 64 - CARD_W, 100
COL_X, COL_R = 64, 620

F_B = '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
F_R = '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf'
F_SYM = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(p, s): return ImageFont.truetype(p, s)


def track(d, xy, text, f, fill, sp=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + sp


def track_w(d, t, f, sp): return sum(d.textlength(c, font=f) + sp for c in t) - sp


def wrap(d, text, f, maxw):
    out, cur = [], ''
    for w_ in text.split():
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = w_
    if cur: out.append(cur)
    return out


def mark(size):
    svg = open(os.path.join(HERE, '..', 'brands', 'assets', 'backpocket-mark.svg'), encoding='utf-8').read()
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),
                                                  output_width=size, output_height=size))).convert('RGBA')


def rounded(img, w, h, r=22):
    im = img.resize((w, h), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255)
    im.putalpha(m); return im


def glow(c, box, r=22):
    x0, y0, x1, y1 = box
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle((x0 - 6, y0 - 4, x1 + 6, y1 + 10), radius=r + 4,
                                        fill=(120, 210, 180, 44))
    c.alpha_composite(g.filter(ImageFilter.GaussianBlur(22)))


def chrome(c, d, progress):
    bx0, bx1, by = COL_X, W - COL_X, 1030
    d.rounded_rectangle((bx0, by, bx1, by + 6), radius=3, fill=RULE)
    if progress > 0:
        d.rounded_rectangle((bx0, by, bx0 + int((bx1 - bx0) * progress), by + 6), radius=3, fill=MINT)


def build(shot, beat, progress):
    c = Image.new('RGBA', (W, H), CHAR + (255,))
    d = ImageDraw.Draw(c)

    if beat.get('bleed'):
        im = shot.convert('RGB')
        # orbit fills the frame; the scorecard and Round Log are landscape-ish
        # overlays that lose their edge columns if cropped, so those fit instead.
        fn = min if beat.get('fit') else max
        sc = fn(W / im.width, (H - 250) / im.height)
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        c.alpha_composite(im.convert('RGBA'), ((W - im.width) // 2, (H - 150 - im.height) // 2))
        veil = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(veil).rectangle((0, H - 300, W, H), fill=(20, 23, 26, 218))
        c.alpha_composite(veil.filter(ImageFilter.GaussianBlur(28)))
        f_h, f_s = font(F_B, 56), font(F_R, 26)
        y = H - 252
        for ln in beat['headline']:
            d.text((COL_X, y), ln, font=f_h, fill=CREAM); y += 64
        for ln in wrap(d, beat['sub'], f_s, W - 2 * COL_X):
            d.text((COL_X, y + 6), ln, font=f_s, fill=MUTED); y += 34
        chrome(c, d, progress); return c.convert('RGB')

    if shot is not None:
        glow(c, (CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H))
        c.alpha_composite(rounded(shot, CARD_W, CARD_H), (CARD_X, CARD_Y))

    if beat.get('end'):
        m = mark(250); f = font(F_B, 70); f2 = font(F_B, 26)
        block = m.height + 66 + len(beat['headline']) * 82 + 38 + 32
        y = (H - block) / 2 - 10
        c.alpha_composite(m, ((W - m.width) // 2, int(y))); y += m.height + 66
        for ln in beat['headline']:
            d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=CREAM); y += 82
        y += 38
        track(d, ((W - track_w(d, beat['sub'], f2, 6)) / 2, y), beat['sub'], f2, MINT, sp=6)
    else:
        c.alpha_composite(mark(64), (COL_X, 92))
        track(d, (COL_X + 84, 114), 'BACK POCKET', font(F_B, 23), CREAM, sp=3.4)
        f_p = font(F_R, 25); py = 178
        for ln in PITCH:
            d.text((COL_X, py), ln, font=f_p, fill=MUTED); py += 32

        f_h, f_s = font(F_B, 62), font(F_R, 27)
        f_b = font(F_SYM, 118) if beat.get('sym') else font(F_B, 132)
        hl, sl = beat['headline'], wrap(d, beat['sub'], f_s, COL_R - COL_X)
        block = len(hl) * 72 + 34 + 158 + len(sl) * 38
        y = 300 + max(0, (900 - 300 - block) / 2)
        for ln in hl:
            d.text((COL_X, y), ln, font=f_h, fill=CREAM); y += 72
        y += 34
        d.text((COL_X, y), beat['big'], font=f_b, fill=MINT); y += 158
        for ln in sl:
            d.text((COL_X, y), ln, font=f_s, fill=MUTED); y += 38
        d.line((COL_X, 918, COL_R, 918), fill=RULE, width=2)
        track(d, (COL_X, 940), 'HOLE 1 · PAR 4 · 388 YDS', font(F_B, 21), CREAM, sp=1.6)
        d.text((COL_X, 972), 'Elevation: USGS 3DEP · contours every 2 ft', font=font(F_R, 21), fill=MUTED)

    chrome(c, d, progress); return c.convert('RGB')


BEATS = [
    dict(img='bp4_A.png', headline=['Stand on', 'the tee.'], big='388',
         sub='to the center. Plays 407 — five feet uphill, plus seventeen for the wind.', secs=2.2),
    dict(img='bp4_B.png', headline=['Move up', 'the fairway.'], big='264',
         sub='Plays 286 — thirty-three feet of climb, drawn as an arc over the real ground.', secs=2.2),
    dict(img='bp4_C.png', headline=['Drop', 'today’s pin.'], big='258',
         sub='Every distance re-keys to it, and the flight profile redraws with them.', secs=2.2),
    dict(img='bp4_GRN.png', headline=['Read', 'the green.'], big='27',
         sub='yards front to back, with the slope arrows showing which way a putt will run.', secs=2.4),
    dict(img='bp4_D.png', headline=['Mark the shot', 'you’ll retell.'], big='★', sym=True,
         sub='Pinned to the spot. It comes back every time you play the hole.', secs=2.2),
    dict(orbit=[f'bp4_3d{i}.png' for i in range(5)], bleed=True,
         headline=['Then see the ground itself.'],
         sub='Contours every two feet from USGS elevation, with the shot flown over real terrain.', secs=3.2),
    dict(img='bp4_CARD.png', bleed=True, fit=True, headline=['The card keeps itself.'],
         sub='Strokes, putts, fairways and greens in regulation — totalled as you play.', secs=2.4),
    dict(img='bp4_LOG.png', bleed=True, fit=True, headline=['And the round becomes a keepsake.'],
         sub='The Round Log: your score, the weather, the moments — and the shot you pinned.', secs=2.6),
    dict(img=None, end=True, headline=['Your course,', 'in your back pocket.'],
         sub='BACK POCKET', secs=2.0),
]


def main():
    shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK, exist_ok=True)
    XF = int(0.28 * FPS)                      # crossfade length
    seqs = []
    for b in BEATS:
        n = int(b['secs'] * FPS)
        if b.get('orbit'):
            fr = [Image.open(os.path.join(ASSETS, f)) for f in b['orbit']]
            seq = fr + fr[-2:0:-1]
            imgs = [seq[i % len(seq)] for i in range(n)]
        else:
            one = Image.open(os.path.join(ASSETS, b['img'])) if b.get('img') else None
            imgs = [one] * n
        seqs.append((b, imgs))

    total = sum(len(i) for _, i in seqs)
    frames, n = [], 0
    for b, imgs in seqs:
        for im in imgs:
            frames.append(build(im, b, n / (total - 1))); n += 1

    # crossfade across beat boundaries
    bounds, acc = [], 0
    for _, imgs in seqs[:-1]:
        acc += len(imgs); bounds.append(acc)
    for bnd in bounds:
        for k in range(XF):
            i = bnd - XF // 2 + k
            if 0 < i < len(frames) - 1:
                a = frames[bnd - XF // 2 - 1] if bnd - XF // 2 - 1 >= 0 else frames[0]
                bfr = frames[min(bnd + XF // 2, len(frames) - 1)]
                frames[i] = Image.blend(a, bfr, (k + 1) / (XF + 1))

    for i, f in enumerate(frames):
        f.save(f'{WORK}/f{i:05d}.png')
    print(f'rendered {len(frames)} frames ({len(frames)/FPS:.1f}s at {FPS}fps)')

    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
                    '-i', f'{WORK}/f%05d.png', '-c:v', 'libx264', '-preset', 'slow',
                    '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], check=True)
    print(f'wrote {OUT}  {os.path.getsize(OUT)/1e6:.2f} MB')


if __name__ == '__main__':
    main()
