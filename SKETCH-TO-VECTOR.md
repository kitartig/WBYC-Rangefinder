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
up = np.array(Image.fromarray(mask*255).resize((w*16, h*16), Image.BICUBIC))/255
sm = ndimage.gaussian_filter(up, sigma=2.3) > 0.5
path = potrace.Bitmap(~sm).trace(turdsize=30, alphamax=0.62, opttolerance=0.15)
```

**`~sm` — potracer traces the FALSE region.** Hand it the mask un-inverted and
you get the complement: for the whole burgee that came back as only the white
elements with no outer boundary, which cost an afternoon before it was spotted.
Always verify by rendering and counting: the filled fraction of the render
should match `mask.mean()`.

**Sigma is the whole game.** 0.9 keeps the source's pixel staircase and the
edges look jagged — "sharp" in the wrong sense. 3.2 rounds off the claws and
the snout. 2.3 with `alphamax` around 0.6 erases the stairs while potrace still
resolves true corners.

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
