# WBYC Rangefinder

White Bear Yacht Club's GPS rangefinder and round keepsake, built from the club's
own course geometry and elevation. **This folder is WBYC's app.**

The engine itself carries **no club identity** — everything club-specific lives in
a brand config and is substituted at build time. That's a code-quality decision,
not a change of purpose: identity used to be baked into the engine and each build
*subtracted* it with string replacement, which leaked WBYC into other clubs' apps
in five separate places. There is nothing to subtract now, so nothing to leak.

---

## Where Back Pocket lives

Back Pocket is the product built on this engine, and it is **a separate project in
a separate folder**. It got separated because the two overlapped badly enough that
Back Pocket's internal naming (`BP_` prefixes) shipped inside the club's app,
including in the localStorage key on members' phones.

The rule that keeps them apart:

- **Product and marketing material does not live here.** Tour video, GIF, captured
  screens, promo calendar, sell sheet, demo-capture skill → the Back Pocket folder.
- **The engine is shared and must not be copied.** `brands/backpocket.json` stays
  here as a build target and the demo is built here, because a second copy of
  `wbyc-rangefinder-template.html` would drift within a working session. That has
  already happened once — see `WORKING-NOTES.md` §2.

So: one engine, in this folder. Two products, in two folders. If you find yourself
about to copy the engine, don't.

---

## Build

```sh
python3 build.py                        # WBYC → wbyc-rangefinder.html + pwa/ + sw bump
python3 build.py brands/backpocket.json # Back Pocket's demo build (demo-backpocket.html)
python3 build_guide.py                  # user guide → pwa/guide/ + WBYC-Rangefinder-Guide.html
sh tests/run.sh                         # 88 assertions against the built app
```

`build.py` refuses to finish if a brand config is missing a key the engine needs,
or if another club's identity survives into the output. Both guards have caught
real bugs.

`build_guide.py` refuses to write WBYC's guide paths for any other brand — pass a
brand without `guide_outputs` and it stops rather than overwriting the club's live
guide. That has also happened once.

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
| `wbyc-guide-template.html` — the user guide | `pwa/index.html`, `pwa/sw.js` |
| `brands/*.json`, `brands/assets/` | `pwa/guide/index.html` |
| `course_data_v2.json`, `wbyc_topo_data.json` | `WBYC-Rangefinder-Guide.html` |
| `tests/tests.js`, `tests/stubs.js` | `demo-backpocket.html` |

Rough guide: wording, colour, layout, behaviour → the engine. Club name, crest,
diary name, storage prefix → that club's brand config. Yardages, pars, tees →
the course data.

## Brand config

Twelve tokens. `build.py` lists any you've missed.

`BRAND` `PRODUCT` `CLUB_LINE` `DIARY` `DIARY_SHORT` `DIARY_BUTTON`
`CREST_FILE` `CREST_STYLE` `CREST_CARD_W` `CREST_CARD_M` `CONTACT_HTML` `STORE`

**`STORE` is the one to leave alone.** It prefixes all 14 localStorage keys.
WBYC's is `wbyc`, matching what shipped — changing it orphans every member's
saved rounds, pins, shots, notes, photographs and clubs, with no migration path.

`neutralise_course: true` blanks course name, location and attribution — needed
only when a brand borrows another club's geometry, as the Back Pocket demo does.

---

See **`WORKING-NOTES.md`** before doing anything git-related from Cowork — the
file mount can't delete or replace files, which breaks `checkout`, `reset` and
`merge` in ways that look like data loss and aren't, and `mv` doesn't get you out
of it either.

## Known gaps

- **`aerials/` isn't bundled into standalone demos**, so `SAT` disables itself in
  anything handed to a club as a single file.
- **WBYC course-data quirks**, OSM-derived and worth a scorecard pass: holes 7
  and 9 read as par 5s at 450/468 yds, hole 17 as a 255-yd par 3, and stroke
  indexes are placeholders (= hole number) because OSM carries none.
- **Keepsake photographs use localStorage**, a ~5MB budget shared with rounds,
  shots, notes and clubs. Capped at 4 per round, downscaled to 900px/q0.62, with
  a visible budget and an explicit quota error. IndexedDB is the durable answer
  when it fills.
- **A fairways chip with no way to fill it.** The FW logger came off the score
  strip at v118, but the keepsake still shows `0/N fairways` and the scorecard
  footer still prints `FW n/m`. Either drop both readouts or put the logger back.
- **The tour video predates memories and keepsake photographs**, so it shows the
  old flow. Re-shoot lives with Back Pocket now.
