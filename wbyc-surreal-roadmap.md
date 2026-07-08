# WBYC Rangefinder — Surreal Enhancement Roadmap

Four phases, ordered so each builds on the last. Phases 1–2 are pure code (free, offline-safe, shippable same-day). Phases 3–4 use AI generation (consumes media credits; produces assets for the app *and* the media brand).

---

## Phase 1 — "Dream Mode" (in-app art theme, pure code)

A third theme in the ☀ cycle: dark → sun → dream.

1. **Palette**: new CSS variable set — deep indigo night sky (#0b0b2a), aurora ramp for the hypsometric tint (teal → violet → magenta instead of greens), contours in luminous cyan.
2. **Animated contours**: SVG `stroke-dasharray` + CSS `stroke-dashoffset` animation so contour lines slowly flow like water around the terrain. One CSS rule; GPU-cheap.
3. **Glow**: SVG `feGaussianBlur` filter on the green and water so they softly pulse; flag ripples via animated path.
4. **Starfield**: sparse animated dots in the map background above the terrain bounds.
5. **3D dream lighting**: in the 3D view, swap hillshade light for a low-angle magenta/cyan dual-light blend.
6. Theme button cycles 3 states; localStorage remembers; time-based default untouched.

*Effort: one working session. No new data, no size cost worth mentioning.*

## Phase 2 — Playful surreal features (small, fun, demoable)

1. **Moon golf**: long-press the ± ELEV button → gravity picker (Earth / Moon ×6.05 / Mars ×2.64). "Plays like 72" on the 433-yd 4th. Physics footnote in the UI.
2. **10× terrain**: exaggeration slider in the 3D view (1.6× → 10×) — WBYC's 86 ft of relief becomes a mountain range.
3. **Night golf**: in dream mode, distances render in a glowing seven-segment style; player dot becomes a firefly with a motion trail.
4. **Easter egg**: enter 18 holes-in-one in demo mode → confetti of tiny golf balls.

*Effort: an afternoon. Pure whimsy, zero risk to the real rangefinder (all gated behind dream mode / long-press).*

## Phase 3 — AI-generated surreal hole artwork

Turn each hole's real aerial + topo into painted, dreamlike art — an "ART" layer next to MAP/SAT, plus a gallery for the brand.

1. **Style exploration**: pick 2–3 style directions (Dalí-melting fairways; Ghibli pastoral; vaporwave topo). I generate test variations of hole 1 from its NAIP aerial as the structural reference.
2. **You pick the winner** (consistency matters — one style across all 18).
3. **Batch generation**: 18 images, each conditioned on its hole's aerial so bunkers/greens stay recognizably *that hole*. Review, regenerate stragglers.
4. **Integrate**: `art/hole01.jpg…` beside `aerials/`, ART button reuses the exact SAT affine-transform pipeline (already built — new layer is ~10 lines).
5. **Brand assets**: same images exported at poster resolution for social/print.

*Effort: 1–2 sessions + generation credits (18–40 images depending on retries). Check credit balance first.*

## Phase 4 — Cinematic hole flyovers (media brand content)

Short surreal flyover clips per hole — app intro screens and social content.

1. **Storyboard one hole**: tee-to-green camera path over the 3D terrain; decide real (NAIP-textured) vs. surreal (Phase 3 art-textured) vs. hybrid (real → melts into surreal).
2. **Pilot clip**: image-to-video generation from the hole's aerial/art frames (5–8 s), or a scripted camera-path capture of the app's own 3D view for full geometric accuracy.
3. **Pick pipeline** based on pilot quality; batch remaining holes.
4. **Assembly**: per-hole clips + one 60–90 s course trailer (music, hole numbers, yardages); vertical crops for Shorts/Reels.
5. **Optional app tie-in**: flyover plays when you open a hole (behind a toggle; skips on cellular).

*Effort: 2–3 sessions + video generation credits (the expensive phase — pilot first, then decide).*

---

**Suggested order**: 1 → 2 (same session), then 3, then 4 — each phase produces something shippable on its own, and 4 reuses 3's art.
