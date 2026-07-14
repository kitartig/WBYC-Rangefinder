# Opportunity Brief: The Artist's Escape Stack
*Initial recon, 2026-07-14. Domains chosen by Kit: Fine Art America + X / LinkedIn / Reddit distribution. Directions chosen: artist promo engine + artist-owned gallery PWA. Lives in the WBYC folder for now — spin up a fresh project folder when we start building.*

---

## The finding, in one paragraph

The print-on-demand art marketplaces are squeezing their artists simultaneously: Society6 is purging thousands of artist accounts as it pivots to a "curated" model; Redbubble's Sept 2025 fee restructure made low-volume selling roughly unprofitable; Fine Art America still leads the category but has ~700,000 artists competing for organic discovery and estimated revenue down 10–20% in 2025. The complaint underneath every thread is identical: **the platforms print and ship, but they don't market you; you must bring your own traffic; and you never own your buyers.** Artists are being pushed onto social media to survive, and most do it badly or hate doing it. That's two products: the traffic machine, and the home the traffic lands on.

## Concept A — Artist Promo Engine

**The gap:** every "scheduler for artists" (Later, Buffer, Pallyy, Metricool, Post Planner…) assumes the artist already *made* the content — they only arrange it on a calendar. Nobody starts from the artwork itself. The actual pain is upstream: turning a finished painting into two weeks of platform-native material.

**The product:** portfolio in → content out. From one artwork: room-mockup shots, detail crops, a process/story narrative in the artist's voice, platform-shaped variants (X thread, LinkedIn post, Reddit-safe share for the right subs), every one linking back to a page the artist owns. The artist approves a queue; the engine keeps the drumbeat going.

**Moat:** this is an editorial product wearing an app costume — taste, sequencing, voice. That's Kit's profession, not a scheduler company's. AI generation makes it buildable solo.

**Watch out for:** platform API posting costs/limits (X API tiers); Reddit's allergy to self-promotion (engine must generate *community-appropriate* shares, not spam — this is a feature, and hard for competitors to copy).

## Concept B — Artist-Owned Gallery PWA

**The gap:** leaving a marketplace today means Shopify-plus-plugins (generic, monthly fees, ecommerce-ugly) or Fourthwall (creator-merch flavored). Nothing feels like a *gallery* — and nothing is zero-backend.

**The product:** the WBYC playbook, verbatim. One gorgeous, fast, offline-capable gallery PWA — beautiful typography, room previews, provenance/story per piece — with checkout fulfilled by a POD API and the customer list landing in the artist's hands, not a platform's. Build **Kit's own gallery first** (kitartig.com is sitting right there), perfect it, then template/license it to other artists — the same "one perfect instance, then the institution/next customer" move as the club deal.

**Fulfillment rails (researched):** Prodigi for gallery-grade archival giclée (the quality story vs. marketplace prints); Gelato (cheapest base costs, ~10–20% under Printful, local production in 30+ countries); Printful (most stable pricing). All offer APIs — the gallery stays static + API calls, no inventory, near-zero backend.

**Moat:** design quality + the no-platform pitch ("your gallery, your buyers, no middleman account") + Concept A feeding it traffic.

## Why they're one system

A = the traffic. B = the destination that converts it and banks the buyer relationship. Marketplaces fail at exactly these two things; each concept also makes the other more valuable. Ship B first for Kit (it's the WBYC muscle, mostly frontend craft), grow it with A used manually-then-productized — which doubles as building the case studies A's customers will want to see.

## Validation plan (before heavy building)

1. **Kit's own gallery + engine as case study zero** — sales and audience numbers become the marketing.
2. **Waitlist landing page** for each concept (the installed indie-launch-kit skill scaffolds page + form + free hosting) — pitch to artists in the Society6-purge threads, where the pain is hottest right now.
3. **Build in public** on X/LinkedIn (installed build-in-public-engine skill) — the audience for the tool is the audience Kit is already building.
4. Signal thresholds before committing: ~100+ waitlist signups or 10 artists who'll pre-pay/beta with real portfolios.

## Open questions for Kit

- Does Kit currently sell on FAA — existing portfolio and sales data to seed case study zero?
- Pricing instinct: subscription (contra-positioning vs. Redbubble-style fee creep favors flat + honest) vs. % of sales?
- Which social platform matters most to the target artist? (Instagram is the elephant not in Kit's URL list — its API is the gnarliest; decide early if it's v1 or v2.)

## Sources

- FAA reality checks: topbubbleindex.com/blog/fine-art-america-worth-it-for-artists · haileyherrera.com (2025-03 "Reality of Selling on FAA") · pisnak.com/is-fine-art-america-legit
- Marketplace squeeze: catcoq.com/blog/society6-shutting-down-artist-accounts · lavaritte.com (Redbubble 2025 fee tiers) · medium.com/@jdvgraphics (decline of RB/S6/TeePublic) · fourthwall.com/blog/society6-alternatives
- Scheduler landscape: ginangiela.com/best-social-media-scheduler-for-artists · buffer.com/resources/social-media-scheduling-tools · orphiq.com/resources/social-media-tools-artists
- POD rails: printful.com/printful-vs-gelato · gelato.com/blog/gelato-vs-printful-wall-art · bootstrappingecommerce.com/best-print-on-demand-sites-for-high-quality-prints (Prodigi giclée)
