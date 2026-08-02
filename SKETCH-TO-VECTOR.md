# Sketch → vector

How a shape drawn on paper, or lifted out of existing artwork, becomes a path in
the app. Both bear stickers' key shapes came through here: the bear from the
club burgee, the wing from a pencil sketch Kit photographed.

Use this instead of trying to *generate* an organic shape from curves. Seven
attempts at writing a wing as Béziers produced a leaf, a quill, a paw, a
butterfly and a frond. The traced pencil sketch read as a wing on the first go.

---

## 1. Get a clean bitmap mask

### From a photographed pencil sketch

The problem is the paper, not the pencil: phone photos carry shadow gradients
and vignetting that defeat any global threshold.

```python
a = np.array(Image.open(src).convert('L'), dtype=float)[y0:y1, x0:x1]
bg = ndimage.gaussian_filter(a, sigma=60)      # a blurred copy IS the lighting
flat = a / np.maximum(bg, 1)                   # divide it out
ink = flat < 0.93                              # now a global threshold works
```

Then close the outline and fill it. Pencil lines have gaps; without the closing
step `binary_fill_holes` leaks and you get nothing.

```python
closed = ndimage.binary_closing(ink, structure=np.ones((9,9)), iterations=3)
filled = ndimage.binary_fill_holes(closed)
filled = ndimage.binary_opening(filled, structure=np.ones((7,7)), iterations=2)
lab, n = ndimage.label(filled)                 # keep the largest blob only
```

Interior detail (feather divisions, etc.) is lost to the fill. That's usually
right — a solid silhouette is what survives at sticker size.

### From existing artwork

Classify by colour into masks, then pick the component you want by size and
bounding box. The burgee's white elements split into 237 components; the bear
was #95 at 3258px, 49×101. Print every component's size and bbox and identify
by eye — don't guess an index.

## 2. Smooth, then trace

Source shapes are small (the bear is 49px wide), so the pixel staircase is the
enemy. Upsample, blur, threshold, trace.

```python
UP = 20
up = np.array(Image.fromarray(mask*255).resize((w*UP, h*UP), Image.BICUBIC))/255
sm = ndimage.gaussian_filter(up, sigma=UP) > 0.5          # sigma ~= ONE SOURCE PIXEL
path = potrace.Bitmap(~sm).trace(turdsize=200, alphamax=1.334, opttolerance=0.9)
```

**Read sigma in SOURCE pixels, not upsampled ones.** This is the trap, and it
cost two rounds of "make it sharper" that made no difference. At ×16 upsample,
`sigma=2.3` is 0.14 of a source pixel — it cannot remove a staircase whose step
is a whole pixel. Even `sigma=5.6` is only 0.35. The staircase only goes when
sigma reaches roughly one source pixel: at ×20 that is `sigma=20`. Divide by the
upsample factor before you judge whether a number is large.

**`~sm` — potracer traces the FALSE region.** Hand it the mask un-inverted and
you get the complement: for the whole burgee that came back as only the white
elements with no outer boundary, which cost an afternoon before it was spotted.
Always verify by rendering and counting: the filled fraction of the render
should match `mask.mean()`.

**Sigma is the whole game, and more of it than feels right.** For the 50px
burgee bear: 0.35 source pixels leaves every stair visible, 1.0 gives clean
flowing curves that still resolve the claws and the snout, 1.5 starts melting
the snout and the rear leg. Push `alphamax` to its 1.334 maximum and
`opttolerance` to ~0.9 — the smoother the mask, the more aggressively potrace
can merge segments, and the path gets *smaller*: the bear went from 5,375 to
3,603 characters while looking better.

**Check the bbox before swapping a path in.** Heavier blur can dilate a shape,
which would silently change its size against every placement number already
tuned around it. Measure with `getBBox()` in a real browser; the σ20 bear came
out 49.02 × 99.99 against the old 49.02 × 100.00, so it dropped straight in.

## 3. Emit at a known height

Normalise to 100 units tall and record the width, so callers scale by height and
never have to know the aspect ratio.

```python
sc = 100.0 / H
open('bear-path.txt','w').write(d)
open('bear-vb.txt','w').write(f"{W*sc:.2f}")
```

---

## Rendering the result

`cairosvg` for SVG → PNG. Three traps, each of which silently produced a missing
image rather than an error:

- it honours **`xlink:href`** only, not plain `href`
- it **cannot decode webp** — convert to PNG first
- it **skips any `<image>` without an explicit `height`**

## Debugging a visual glitch

Render the element alone at large scale and **measure the pixels**, rather than
adjusting a number and re-rendering. The umbrella handle "gap" survived two
guesses at its length; a column scan found the handle was fine and the canopy's
scalloped underside lifted at the centre, so the handle began *below* the
canopy edge. The fix was at the top of the line, not the bottom.

```python
a = np.array(Image.open('probe.png').convert('RGB')).astype(int)
col = int(round((x_scene + 34) * px_per_unit))
runs = [r for r in range(a.shape[0]) if is_navy(a[r, col])]
```
