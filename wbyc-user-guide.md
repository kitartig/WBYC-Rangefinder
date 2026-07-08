# WBYC Rangefinder — Quick User Guide

## One-time setup

1. Deploy the `pwa/` folder to Netlify (drag-and-drop at app.netlify.com/drop works).
2. Open the URL on your phone in Safari/Chrome → **Allow location** when prompted.
3. **Add to Home Screen** — this installs it as an app with offline support.
4. Sanity check from anywhere: status bar should go green with `GPS ±Xm · n/5 fixes`. If it says demo mode, GPS isn't coming through.

## On the course

- **Just stand over your ball.** The white golf ball with the glowing gold halo is you. The app averages your last 5 GPS fixes, so stand still a few seconds for best accuracy (±3–5 m typical).
- **AUTO** (on by default) switches holes for you as you walk — it picks whichever hole's centerline you're nearest. Use **‹ ›** to browse manually (this turns AUTO off; tap AUTO to re-enable).
- **Distances** update live: front / **CENTER** / back of green, with "plays like" under center when elevation adjustment is on.
- **Tee buttons** (Blue/White/Gold/Red) set the scorecard yardage shown and demo-mode start point.
- The screen stays awake during a round (wake lock) — expect battery drain; start charged.

## Buttons

| Button | Does |
|---|---|
| ‹ › | Previous / next hole (disables AUTO) |
| AUTO | Auto-detect hole from GPS |
| SAT | Aerial imagery under the map |
| 3D | 3D terrain view of the hole (drag to rotate, pinch to zoom) |
| ☀ / ✦ / ☾ | Cycle theme: dark → sun → dream |
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

## Scorecard

- The strip below the map is your running card for the current hole: **SCORE** and **PUTTS** +/−, and **FW** (tap to cycle ✓ hit → ✗ miss → blank; hidden on par 3s).
- The right side shows your running score vs par (`+2 thru 7`) — **tap it to open the full card**: front/back/total, per-hole results, and a stats line (putts, fairways, GIR).
- On the full card, **tap any hole row to jump the app to that hole**; NEW ROUND clears the card (with a confirm).
- The card survives closing the app mid-round (saved on every tap). Red-tee rounds score against women's par automatically.

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
