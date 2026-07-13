# Project Brief — WBYC Rangefinder

A GPS rangefinder app for White Bear Yacht Club (Dellwood, MN), built as an inception project before expanding to other courses. This file is the onboarding context — read this first before continuing any work in this project.

---

## Course Facts

- **Name:** White Bear Yacht Club
- **Location:** Dellwood, MN 55110 (56 Dellwood Ave, White Bear Lake per official site)
- **Architect:** Donald J. Ross
- **Opened:** 1920
- **Par:** 72 (men) / 74 (women — holes 1 and 15 play as par 5 from the Reds)
- **Clubhouse anchor coordinate (approx):** 45.0910462, -92.9734125

### Tee sets (official scorecard, fetched 2026-07-03)

| Tee | Yardage | Rating/Slope |
|---|---|---|
| Blue | 6,471 | 72.1 / 132 (M) |
| White | 6,266 | 71.2 / 131 (M) |
| Gold | 5,823 | 69.0 / 127 (M) |
| Red | 5,658 | 73.3 / 134 (W) |

> Historical note: an earlier version of this brief labeled the 5,823 yardages as "Men's tees" — they are the **Gold** tees.

---

## Data Status — Read This Carefully

**As of 2026-07-03, all placeholder coordinates have been replaced with real geometry from OpenStreetMap** (© OpenStreetMap contributors, ODbL 1.0 — attribution is embedded in the data file and must be kept in any distributed output).

| Data | Status | Source |
|---|---|---|
| Par, yardage, handicap (all 18 holes, all 4 tee sets, M+W) | ✅ REAL | Official scorecard (wbyc.clubhouseonline-e3.net) |
| Green front/center/back + full green polygons + depth | ✅ REAL | OSM |
| Hole centerlines (dogleg geometry) | ✅ REAL | OSM |
| Bunkers (69 polygons) + water hazards (5 polygons) | ✅ REAL | OSM |
| Tee box coordinates | ✅ REAL, with gaps below | OSM |

### Known coordinate gaps (per-hole `yardage_delta` flags these in the data)

1. **Hole 5 Red tee (290 yds) is NOT mapped in OSM** — it's currently assigned the forward pad measuring 380 yds (+90). Needs a real pin-drop or GPS capture. This is the only materially wrong coordinate.
2. Holes **1, 3, 7, 14, 18** have a single mapped tee pad shared by all four colors. Measured distances are within ~15 yds of the official card, so this is cosmetic, but back-tee pads could be refined.

Validation: measured playing distance (tee → dogleg vertices → green center) matches the official scorecard within ±16 yds on every tee except hole 5 Red. Each `tee_boxes[]` entry carries `measured_yds` and `yardage_delta` so mixed-quality data stays visible.

---

## Data Schema (course_data_v2.json)

```
Course
 ├─ course_name, location, architect, year_opened, par, par_women
 ├─ tees[]              (name, gender, total_yardage, rating, slope)
 ├─ attribution          (ODbL — keep in any output)
 └─ holes[]
     ├─ hole_number, par, par_women, handicap_index, handicap_index_women
     ├─ tee_boxes[]      (name, yardage, lat, lng, measured_yds, yardage_delta)
     ├─ tee_positions_osm[]  (raw mapped pads: lat, lng, measured_yds)
     ├─ green            (front/center/back {lat,lng}, depth_yds, polygon[])
     ├─ centerline[]     (tee → dogleg vertices → green; real hole shape)
     ├─ hazards[]        (type: bunker|water, subtype, points[] polygon, osm_id)
     └─ coordinates_source
```

---

## Files In This Project

- **`wbyc-rangefinder.html`** — standalone mobile web app. Self-contained (HTML/CSS/JS, no build step, no dependencies); course data is embedded at build and also re-fetched from `course_data_v2.json` when served over HTTP. Browser Geolocation API with 5-fix rolling average; SVG overhead hole map rendered from the real polygons; auto-hole detection from centerlines; demo mode (tap the map to move) when GPS is unavailable.
- **`course_data_v2.json`** — the course data file (real scorecard + real OSM geometry), matching the schema above.
- **`wbyc_topo_data.json`** — elevation package from USGS 3DEP lidar (public domain), fetched 2026-07-03: 1,839 contour polylines at 2-ft intervals (index every 10 ft) — base 10m grid for the full course plus 18 high-res 3m patches covering each green complex (120m boxes; some have 40-55 ft of relief). App renders per-hole hypsometric tinting + hillshading from the grids; `elevFt()` prefers 3m patches over the base grid for "plays like". Embedded into the app at build; the app renders USGS-style contours under each hole map and uses bilinear grid lookups for "plays like" distances (~1 yd per 3 ft, toggleable via ± ELEV for tournament compliance).
- **`aerials/`** — 18 NAIP aerial JPEGs (~1 m/px, USGS public domain) + manifest with per-hole geo bounds. Rendered via the SAT toggle as an affine-transformed base layer under the contours/features. Duplicated in `pwa/aerials/`.
- **`pwa/`** — deployable PWA package: `index.html` (same app), `sw.js` (offline-first service worker: app shell cache-first, course data stale-while-revalidate), `manifest.webmanifest`, icons, and a copy of the data file. Deploy this folder to any HTTPS static host (Netlify Drop, GitHub Pages), then Add to Home Screen on the phone. The app also requests a screen wake lock so the display stays on during a round. To ship an update, bump `VERSION` in `sw.js`.
- **`gps-walk-checklist.md`** — field guide for capturing coordinates on foot. Still useful for the hole 5 Red tee and back-tee refinements. *(Note: not present in the folder as of 2026-07-03 — restore from wherever it lives if needed.)*

---

## What's Left To Do

1. **Hole 5 Red tee coordinate** — the one real data bug. Pin-drop via Google Earth or GPS capture on site.
2. **Back-tee pads on holes 1, 3, 7, 14, 18** — currently one shared pad per hole; refine if back-tee accuracy matters.
3. **Layup/dogleg target points** — centerline vertices exist; consider named targets with carry distances (e.g., "corner: 230 to reach").
4. ~~Elevation-adjusted "plays like" distance~~ — ✅ done, with USGS-style topo contour layer. The ± ELEV toggle satisfies tournament compliance (off = plain distances only).
5. ~~PWA packaging~~ — ✅ done (`pwa/` folder); just needs deploying to an HTTPS host.
6. **Broader course support** — still explicitly deferred until WBYC is validated end-to-end on the course.

## Build Pipeline (added 2026-07-03)

**Never edit `wbyc-rangefinder.html` or `pwa/index.html` directly** — they're generated. Edit `wbyc-rangefinder-template.html` (has `/*__COURSE_DATA__*/null`, `/*__TOPO_DATA__*/null`, `/*__AERIALS__*/null` placeholders), then run `python3 build.py`, which injects the three data files and auto-bumps the service-worker cache version.

Session 2026-07-03 additions beyond the data work: sun + dream themes (3-way toggle), hillshading + histogram-equalized hypsometric tint, smooth Bézier features, water ripples/gradients, on-green micro-contour reading lines, NAIP SAT layer (rotation-proof enlarged photos), dependency-free 3D terrain view (EXAG slider, anti-aliased features, shimmering water, hairline contours), portrait view clamp with interior-nudge, whole-course neighbor-feature rendering, moon/Mars gravity long-press, demo-dot snap-to-tee. See `wbyc-surreal-roadmap.md` for pending Phases 3–4 (AI art layer, flyovers) and their asset checklist.

## Pitch Deck (added 2026-07-12)

**`WBYC-Rangefinder-Pitch.pptx`** — 12-slide draft proposing to license the app to WBYC in trade for annual dues, with free reasonable revisions/updates included. Kit's goal: establish an estimated value and present the elegance of the build.

- **Fonts:** Didot (headers) + Raleway (body), per Kit. Didot ships with macOS; Raleway is a free Google Font — install it on the presenting machine, or embed fonts on save / present the PDF if using a Windows PC (it has neither).
- **Palette:** the app's own — dark forest `#0E2A1C`, lush green `#1E7A4A`, hot pink tracer `#F000C2`. Motif: the pink tracer arc; on the title slide its apex dot lands as a period after "RANGEFINDER" (intentional).
- **Valuation anchors (researched 2026-07-12):** consumer golf apps $50–100/yr (Golfshot Pro, 18Birdies, GolfLogix, Arccos — ScoringZone/Birvix surveys); custom GPS app build $45K–$75K (Business of Apps, TopFlight, USM Systems guides); WBYC dues from public reporting only — 2020 tiers $374–$960/mo (Press Publications), initiation raised $50K→$65K in 2025 after the $6M renovation (MSPBJ). Ask framed as est. $8K–$12K/yr dues in trade.
- **Placeholders Kit must replace before presenting:** actual annual dues figure (slide 8) and real golfing-member count (slides 6 & 8 assume ~300 × $60/yr ≈ $18K/yr member value).
- **Honesty features:** barter-tax caveat (slide 9); rounds are stored per-device, phone-to-iPad sync listed on the 2027 roadmap (slides 5 & 11); slide 5 sells the zero-signup loop — score a hole or mark a shot and the round saves itself, home replay is the reward.
- **Regenerating:** built with pptxgenjs + sharp (SVG art rasterized). Generator scripts live in `deck-src/` (`art.js` builds the three PNGs, `deck.js` builds the .pptx — adjust the path constants at the top, see `deck-src/README.md`). Possible next pass: replace slide 4's stylized three-view art with real app screenshots.

## Working Agreements

- Never fabricate coordinates and present them as real — flag data quality explicitly, per-hole (`measured_yds` / `yardage_delta` serve this now).
- Prefer official/verifiable sources (scorecards, OSM, on-site GPS capture) over estimates.
- Keep OSM attribution intact in the data file and any user-facing output (ODbL requirement).
- Keep the app usable as a single-course MVP; don't over-engineer for multi-course support until WBYC has been validated on the course.
