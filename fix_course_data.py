#!/usr/bin/env python3
"""Repair course files produced by course-builder.html.

Two fixes:

1. green.depth_yds — the rangefinder template renders `${g.depth_yds}` in the
   HAZARDS & TARGETS panel, but convert() in course-builder.html never emits it,
   so every built course shows "Green depth: undefined yds". Depth is simply the
   distance from the green's front point to its back point.

2. incomplete tee sets (optional, --drop-partial-tees) — OSM rarely has every
   tee box mapped, so sets like "Middle" can total 814 yards across 18 holes.
   Honest for QA, but it reads as broken in a demo. This drops any tee set not
   present on every hole, and prints what it removed.

Usage:  python3 fix_course_data.py <course.json> [--drop-partial-tees] [-o out.json]
"""
import json, math, sys, argparse

D = math.pi / 180
R = 6371000


def yards(a, b):
    la1, la2 = a['lat'] * D, b['lat'] * D
    dla = (b['lat'] - a['lat']) * D
    dlo = (b['lng'] - a['lng']) * D
    x = math.sin(dla / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlo / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x)) * 1.09361


ap = argparse.ArgumentParser()
ap.add_argument('course')
ap.add_argument('--drop-partial-tees', action='store_true')
ap.add_argument('-o', '--out')
args = ap.parse_args()

d = json.load(open(args.course))
holes = d['holes']

# --- fix 1: green depth ---
added = 0
for h in holes:
    g = h['green']
    if 'depth_yds' not in g and 'front' in g and 'back' in g:
        g['depth_yds'] = round(yards(g['front'], g['back']))
        added += 1
depths = [h['green']['depth_yds'] for h in holes if 'depth_yds' in h['green']]
print(f"green.depth_yds added to {added} holes "
      f"(min {min(depths)}, median {sorted(depths)[len(depths)//2]}, max {max(depths)} yds)")

# --- fix 2: partial tee sets ---
if args.drop_partial_tees:
    n = len(holes)
    coverage = {}
    for h in holes:
        for t in h['tee_boxes']:
            coverage[t['name']] = coverage.get(t['name'], 0) + 1
    partial = {k for k, v in coverage.items() if v < n}
    if partial:
        for name in sorted(partial):
            print(f"dropping tee set {name!r} — mapped on only {coverage[name]}/{n} holes")
        for h in holes:
            h['tee_boxes'] = [t for t in h['tee_boxes'] if t['name'] not in partial]
        d['tees'] = [t for t in d.get('tees', []) if t['name'] not in partial]
    else:
        print("all tee sets complete — nothing dropped")

out = args.out or args.course
json.dump(d, open(out, 'w'), separators=(',', ':'), ensure_ascii=False)
print(f"wrote {out}")
