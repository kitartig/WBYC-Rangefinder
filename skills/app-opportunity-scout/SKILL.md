---
name: app-opportunity-scout
description: Research what app to build next — sweep complaint mines (Reddit, app-store and B2B reviews), spot market gaps, score candidates against the builder's unfair advantages, and deliver a sourced opportunity brief. Use when the user asks "what app should I build", "find a gap / unmet need", "is there an app that…", wants a better version of an existing app, or names domains/URLs they care about and wants opportunities scouted in them.
---

# App Opportunity Scout

Turn "I'd like to build another app" into a sourced, scored opportunity brief. Research is live (web search), never from memory. Never fabricate demand — every claimed complaint or trend needs a real citation.

## 1. Intake (fast — don't gate research on it)

Capture, or infer from context and confirm later:
- **Domains**: 2–3 areas the user cares about. If they paste URLs, treat those as the domains (marketplace URLs = the market; social URLs = their distribution channels).
- **Unfair advantages**: skills, audience, insider access, proven playbooks from past projects. The best idea *fits the builder*, not just the market.
- **Prior wins**: a past project's shape often generalizes (e.g. "hyper-local, data-perfect, no accounts, licensed to the institution that benefits").

Start searching immediately; ask clarifying questions alongside first results, not before.

## 2. Sweep protocol

Run per domain. Reddit's own search is weak — go in through the search engine:

**Complaint / wish mining**
- `"is there an app that" [domain] site:reddit.com`
- `"why is there no app" OR "someone should make an app" [domain] site:reddit.com`
- `"[category leader] alternative" OR "[category leader] sucks" site:reddit.com`
- Standing wish-pools: r/SomebodyMakeThis, r/AppIdeas, request megathreads in r/iosapps and r/androidapps.

**Review mining**
- 1–3 star reviews of the category leaders (App Store "critical" sort, Google Play). The repeated "love it BUT…" is a free spec sheet.
- B2B: Capterra and G2 low-star reviews — complaints from people who pay real money.

**Demand & health signals**
- Google Trends (growing or dying interest).
- AlternativeTo.net (heavy "looking for alternative" traffic on an app = a flare).
- Platform-health news: fee restructures, account purges, curation pivots, revenue declines. A marketplace squeezing its users is a live exodus to catch.

## 3. Gap signals worth acting on

- **Proven demand, bad supply**: big download numbers + mediocre ratings.
- **Squeeze exodus**: incumbents raising fees / purging users *right now* — timing beats size.
- **Upstream pain**: existing tools handle step 2 of the user's workflow but nobody touches step 1 (e.g. schedulers arrange content; nothing *generates* it).
- **Ownership gap**: platforms that keep the customer relationship hostage.
- **Craft gap**: a category where everything works but nothing is *beautiful* or trustworthy.

## 4. Score candidates

Rate each 1–5 on: pain frequency (weekly beats yearly) · willingness to pay (already paying someone badly?) · fit to the builder's unfair advantages · solo-buildability (PWA / zero-backend / API-rails preferred) · timing (is there a live exodus or trend). Kill anything scoring low on advantage-fit no matter how good the market — a better idea that doesn't fit the builder loses to a good idea that does.

Prefer candidates where **the builder is user zero** (eat your own cooking): it guarantees taste, testing, and the first case study.

## 5. Deliver the brief (a committed .md file, not just chat)

Template:
- **The finding, in one paragraph** — the market story with the squeeze/gap named plainly.
- **Concept cards** (2–3 max): The gap · The product · Moat · Watch out for.
- **Why they combine** (if they do — traffic + destination pairs are common).
- **Validation plan before heavy building**: user-zero build, waitlist landing page (pair with an indie-launch/waitlist skill if installed), build-in-public (pair with a content-engine skill if installed), and explicit go/no-go thresholds (e.g. 100 waitlist signups or 10 pre-pay betas).
- **Open questions for the user** — the 2–3 answers that change the plan.
- **Sources** — every claim traceable.

End by asking the user which direction to chase (multi-select), then deepen only the chosen ones.

## Rules

- Search first, always; summaries of vibes are not evidence.
- 2–3 concepts maximum in a brief — more is indecision wearing a costume.
- Note API/platform risks early (posting limits, ToS allergies like Reddit self-promotion norms).
- Save the brief in the user's project folder and commit it if the folder is a repo; record a pointer in memory so "the next app" resumes from the brief, not from scratch.
