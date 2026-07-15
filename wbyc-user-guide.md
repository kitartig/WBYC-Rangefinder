# WBYC Rangefinder — Quick User Guide

A GPS rangefinder built for one course: every hole, hazard, and green at WBYC, working offline in your pocket.

## Features at a glance

- **Live GPS distances** to the front / center / back of every green, smoothed over your last 5 fixes
- **Pin sheet (PIN)** — tap where today's pin actually is; every distance, arc, and the 3D flag re-key to it (resets at midnight)
- **"Plays like" numbers** that fold in elevation (USGS 3DEP terrain) and wind — with a per-hole wind arrow
- **Club hints** learned from your own tracked shots (`plays 152 · 7i`)
- **Shot tracking** — one tap per shot; builds your real club distances and draws your round on the map
- **Carry arcs** — dashed rings showing your selected club's reach (and its neighbors) from where you stand
- **Running scorecard** — strokes, putts, fairways; full 18-hole card with stats (putts, FW, GIR)
- **GHIN post helper** — one tap copies your scores and opens ghin.com for posting
- **Your game (STATS)** — round history, best round, averages, and a trend line across rounds
- **Green view (GRN)** — zoom to the green complex with downhill fall-line arrows and micro-contours for reading putts
- **Ball-flight tracer** — a TV-style pink arc of your shot: on the hole map, in a tap-for-it side profile, and animated over 3D terrain with yardage stats at the apex
- **3D terrain view** of every hole; **SAT** aerial imagery overlay
- **Auto hole detection** as you walk the course
- **Hazards & targets panel** — reach / carry distances to every bunker, water hazard, and dogleg
- **Three themes** (dark / sun / dream) with a high-contrast sun mode for bright days
- **Works offline** — installs to your home screen as an app; scorecard and shots survive restarts
- A little hidden whimsy for those who explore

## Your name

Tap **+ your name** (top right, next to the Bar/Dining button) and enter it once. It signs your scorecard title and your GHIN post text, and stays on the device. Tap it again anytime to change it; clear it to go anonymous.

## One-time setup

1. Deploy the `pwa/` folder to Netlify (drag-and-drop at app.netlify.com/drop works).
2. Open the URL on your phone in Safari/Chrome → **Allow location** when prompted.
3. **Add to Home Screen** — this installs it as an app with offline support.
4. Sanity check from anywhere: status bar should go green with `GPS ±Xm · n/5 fixes`. If it says demo mode, GPS isn't coming through.

## On the course

- **Pinch to zoom** anywhere on the hole map — two fingers zoom around your fingertips and drag to pan; pinch back out (or change holes) to snap back to the full hole. GRN remains the one-tap green zoom.
- **Just stand over your ball.** The white golf ball with the glowing gold halo is you. The app averages your last 5 GPS fixes, so stand still a few seconds for best accuracy (±3–5 m typical).
- **AUTO** (on by default) switches holes for you as you walk — it picks whichever hole's centerline you're nearest. Use **‹ ›** to browse manually (this turns AUTO off; tap AUTO to re-enable).
- **Distances** update live: front / **CENTER** / back of green. Under CENTER, the "plays like" line stacks everything the app knows: elevation, wind, and (once shot tracking has data) your club — e.g. `plays 152 (+6 ft, wind +4) · 7i`.
- **Tee buttons** (Blue/White/Gold/Red/Green) set the scorecard yardage shown and demo-mode start point. Red and Green score against women's par and use their own handicap allocations from the 4/2026 card. Heads-up: most Green tee positions are estimated on the line of play until they're GPS-captured — yardages match the card, but the dot on the map may sit a pace or two off the actual pad.
- The screen stays awake during a round (wake lock) — expect battery drain; start charged.

## Buttons

| Button | Does |
|---|---|
| ‹ › | Previous / next hole (disables AUTO) |
| AUTO | Auto-detect hole from GPS |
| SAT | Aerial imagery under the map |
| GRN | Zoom to the green (fall-line arrows appear here) |
| PIN | Drop today's pin: tap PIN, then tap the green — every number re-keys to the actual pin. Long-press to clear. Pins reset at midnight |
| 3D | 3D terrain view with animated shot tracer (drag to rotate, pinch to zoom, TRACE to replay) |
| CENTER box | Tap the big CENTER number to toggle the side-profile flight view |
| ☀ / ✦ / ☾ | Cycle theme: dark → sun → dream |
| SHOT | Mark a shot from where you stand (club picker beside it; long-press = undo) |
| ± ELEV | Elevation-adjusted "plays like" distances (~1 yd per 3 ft) |
| WIND | Wind-adjusted "plays like" — tap to toggle, long-press to set wind manually |
| DEMO MODE | Tap-the-map positioning when GPS is off/unavailable |

## Wind

- **Live wind** loads automatically from Open-Meteo (free, no key) once the app is served from Netlify, refreshing every 15 min. It does nothing when running from a local file.
- **Manual wind**: long-press WIND, enter speed (mph) and the direction it's blowing FROM (compass name or degrees). Works fully offline; shown with a `*` and it overrides live data until reload.
- The button reads like `WIND 12 SW` — speed and where it's coming from.
- **Map arrow** (top-right) points where the wind blows *relative to the hole* — arrow pointing up = tailwind toward the green.
- "Plays like" folds in the head/tail component: headwind adds ~1% of the shot per mph, tailwind subtracts ~0.5%/mph. Crosswind doesn't change distance — that part's still your call.
- **First-round check**: long-press WIND, set something like 10 SW, and sanity-check the arrow against the flag. The live fetch is untested until the Netlify deploy.

## Pin sheet (PIN)

Green-center numbers are good; today's-pin numbers are better. Tap **PIN**, then tap where the pin actually is (GRN view makes this precise) — a white-and-pink flag appears there, the big CENTER box relabels to **PIN**, and everything follows: plays-like, the flight arc and its stats, carry-arc aiming, the profile view, and the 3D flagstick and tracer. FRONT and BACK stay what they are. Long-press PIN to go back to center; pins clear themselves at midnight since the greenkeeper moves them anyway. Set all 18 while your partner putts out and you're carrying a real pin sheet.

## Ball flight (the pink arc)

Your shot to the green shows three ways, all in hot pink:

- **On the hole map**, a pink arc bows off the straight line from your ball to the center, with the flight stats stacked right at its peak — yardage big, then plays-like/club and apex height. The straight line is the ground path (the arc's "shadow"); the small dashed tick ties the arc's high point back to the ground so you can tell it's height, not a hook. It's illustrative — the arc always curves toward the middle of the frame, whichever side that is.
- **Side profile**: tap the big **CENTER** number to open a strip under the map showing the actual terrain cross-section between you and the green — the green's surface highlighted, elevation change labeled (`+12 ft`), and the flight arc over it. This is the picture behind the "plays like" number. Tap CENTER again to hide it; the choice sticks.
- **In 3D**, opening the view fires an animated tracer from your ball (or the tee) to the flag, with small stats pinned at the arc's peak: the raw yardage, the plays-like number with its elevation/wind parts, your suggested club once shot tracking knows you, and apex height. Tap **TRACE** to replay it. With WIND on, a crosswind visibly bends the flight late — just like it does outside.

The profile and 3D stats respect your ± ELEV and WIND toggles, so what they show always matches the numbers up top.

## Reading the green

Tap **GRN** (on the map, next to SAT/3D) to zoom to the green complex. Up close you get fall-line arrows: small dark arrows pointing **downhill**, longer = steeper, plus the pale micro-contour lines and your ball if you're on or near the green. Tap GRN again — or change holes — to jump back to the whole hole.

The arrows come from USGS 3m elevation data, so treat them as the broad break (overall tilt and big shelves), not subtle 6-inch reads. They only appear in GRN view — including over SAT imagery, where they render smaller and pale to sit on the photo. The aerial photos themselves get a saturation boost so the course reads lush rather than flat-survey gray.

## Shot tracking

- Standing at your ball, pick the club (bottom-left of the map) and tap **SHOT** just before you hit. That's the whole flow — one tap per shot.
- Each mark's distance is measured to your next mark on the hole (the last one measures to green center), so the app learns your **real** club distances. Mismarked? **Long-press SHOT to undo.**
- Today's shots draw on the map as numbered dots with a dotted trail from the tee.
- **Carry arcs**: dashed rings from your position show what the selected club reaches (bold arc), with one longer and one shorter club as fainter neighbors. Change the club in the picker to move them. They start from stock distances and switch to *your* numbers once a club has 2+ tracked shots. Arcs show raw carry — the plays-like number handles wind/elevation. Hole view only.
- Open the scorecard and tap **CLUBS** to see your learned median distance per club, across all rounds.
- Once a club has 2+ tracked shots, a club hint appears after "plays like" under CENTER (e.g. `plays 152 · 7i`). More rounds = smarter hints.
- Don't bother marking putts — the scorecard putt counter covers those.

## Scorecard

- The strip below the map is your running card for the current hole: **TOTAL SCORE** (all strokes on the hole, putts included) and **PUTTS** +/−, and **FW** — fairway hit (tap to cycle ✓ hit → ✗ miss → blank; hidden on par 3s).
- The right side shows your running score vs par (`+2 thru 7`) — **tap it to open the full card**: front/back/total, per-hole results, and a stats line (putts, fairways, GIR).
- On the full card, **tap any hole row to jump the app to that hole**; NEW ROUND clears the card (with a confirm).
- The card survives closing the app mid-round (saved on every tap). Red-tee rounds score against women's par automatically.
- **POST** (on the full card) copies your hole-by-hole scores to the clipboard and opens ghin.com — log in, choose hole-by-hole posting, and paste/enter. GHIN doesn't allow direct posting from personal apps, so this is deliberately a two-tap handoff: your GHIN login never touches this app.
- **NEW** banks the finished round into your history (it's saved, not discarded), then clears the card for the next round.

## Your game (STATS)

Tap **STATS** on the scorecard for your profile page: every banked round (date, tee, score vs par, putts, FW%, GIR), a trend line of your last 10 rounds vs par, and a stats footer — best round, plus averages over your last five full rounds. Nine-hole outings are listed and tagged (`(9h)`); bests and averages use full 18s only. The **CLUBS** view next to it is the other half of your profile: your learned distance for every club in the bag.

**Reviewing at home:** the same link works on an iPad or laptop — replay any hole's 3D flyover, walk the card, and browse your stats from the couch. One catch: rounds live on the device that recorded them (there are no accounts, by design), so review your round on the phone that scored it, or use the big screen for course study and replays.

## Tournament play

Turn **± ELEV and WIND off** — adjusted distances aren't allowed under USGA/R&A Rule 4.3a. Plain GPS distances are fine.

## Demo mode

Kicks in automatically if GPS is denied or unavailable (or tap DEMO MODE). Tap anywhere on the map to move yourself. Tapping the map while GPS is live also switches you into demo — tap DEMO MODE again to return to GPS.

## Fun

- Long-press **± ELEV** to cycle gravity: Earth → Moon → Mars distances. Resets on reload.
- In demo mode, landing a tap within 3 yards of the pin on all 18 holes does… something. 

## Known quirks

- **Hole 5, Red tee** yardage is wrong (+90 yds) — that tee isn't mapped in OSM yet. Capture a GPS point there during your round (`gps-walk-checklist.md` has the method).
- GPS lags slightly while walking; it settles when you stop.
- If the app looks stale after an update, close and reopen it twice (service worker updates on second launch).
