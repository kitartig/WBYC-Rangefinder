# Rangefinder — one engine, many clubs

A GPS rangefinder and round keepsake, built per club from their own course
geometry and elevation. White Bear Yacht Club is the first customer; **Back
Pocket** is the product.

The engine carries **no club identity**. Everything club-specific lives in a
brand config and is substituted at build time. That direction matters: identity
used to be baked into the engine and each white-label build *subtracted* it with
string replacement, which leaked WBYC into other clubs' apps in five separate
places. There is nothing to subtract now, so nothing to leak.

---

## Build

```sh
python3 build.py                       # WBYC → wbyc-rangefinder.html + pwa/ + sw bump
python3 build.py brands/backpocket.json # the product's own demo
python3 build_guide.py                 # user guide → pwa/guide/ + WBYC-Rangefinder-Guide.html
sh tests/run.sh                        # 88 assertions against the built app
```

`build.py` refuses to finish if a brand config is missing a key the engine needs,
or if another club's identity survives into the output. Both guards have caught
real bugs.

## Add a club

1. `course-builder.html` in a browser → `<club>-course-data.json` from OpenStreetMap
2. `python3 fix_course_data.py <course.json> --drop-partial-tees`
   Adds `green.depth_yds`; drops tee sets OSM only mapped on some holes.
3. *(demo only)* `python3 make_demo_tees.py <course.json>` — derives Back/Middle/
   Forward by scaling. **Those yardages are invented**, flagged in the file under
   `synthetic_tees`. Replace with the club's scorecard before anything real.
4. `brands/<club>.json` — copy `brands/wbyc.json`, put the crest in `brands/assets/`
5. `python3 build.py brands/<club>.json`
6. `python3 deploy_demo.py …` → drop-ready folder + zip for Netlify (GPS needs https)

**Topo has no generator.** Without a topo file the 3D button hides itself
(`if(!TOPO) d3Btn.style.display='none'`), contours don't draw and there's no
elevation adjustment. `SAT` likewise needs an `aerials/` folder beside the app.

---

## Source vs generated

Edit the left. The right is overwritten on every build.

| Source | Generated |
|---|---|
| `wbyc-rangefinder-template.html` — the engine | `wbyc-rangefinder.html` |
| `brands/*.json`, `brands/assets/` | `pwa/index.html`, `pwa/sw.js` |
| `wbyc-guide-template.html` | `demo-backpocket.html` |
| `course_data_v2.json`, `wbyc_topo_data.json` | `WBYC-Rangefinder-Guide.html`, `pwa/guide/index.html` |
| `tests/tests.js` | `marketing/back-pocket-tour.mp4` |

Rough guide: wording, colour, layout, behaviour → the engine. Club name, crest,
diary name, storage prefix → that club's brand config. Yardages, pars, tees →
the course data.

## Brand config

Twelve tokens. `build.py` lists any you've missed.

`BRAND` `PRODUCT` `CLUB_LINE` `DIARY` `DIARY_SHORT` `DIARY_BUTTON`
`CREST_FILE` `CREST_STYLE` `CREST_CARD_W` `CREST_CARD_M` `CONTACT_HTML` `STORE`

**`STORE` is the one to leave alone.** It prefixes all 14 localStorage keys.
WBYC's is `wbyc`, matching what shipped — changing it orphans every member's
saved rounds, pins, shots and clubs, with no migration path.

`neutralise_course: true` blanks course name, location and attribution — needed
only when a brand borrows another club's geometry, as the Back Pocket demo does.

## Marketing

`marketing/make_backpocket_video.py` → 21s product tour, 1080×1080, ~1.5MB.
`marketing/make_backpocket_gif.py` → 8s GIF for places that need one. A GIF
can't carry 20s of varied material without passing 5MB and dithering badly.

Re-capturing screens: serve the **repo root** (`python3 -m http.server 8000`) and
open the build with `?nocoach=1` so the first-run card doesn't cover the app.

---

## Known gaps

- **`back-pocket-starter-kit/` is dead.** See `DEPRECATED.md` inside it; delete
  the folder. Its engine copy is stale and would undo the tokenisation.
- **`aerials/` isn't bundled into standalone demos**, so `SAT` disables itself in
  anything handed to a club as a single file.
- **WBYC course-data quirks**, OSM-derived and worth a scorecard pass: holes 7
  and 9 read as par 5s at 450/468 yds, hole 17 as a 255-yd par 3, and stroke
  indexes are placeholders (= hole number) because OSM carries none.
- **Keepsake photographs use localStorage**, a ~5MB budget shared with rounds,
  shots and clubs. Capped at 4 per round, downscaled to 900px/q0.62, with a
  visible budget and an explicit quota error. IndexedDB is the durable answer
  when it fills.
