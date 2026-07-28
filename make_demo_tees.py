#!/usr/bin/env python3
"""Generate DEMO-ONLY tee sets for a course file.

OSM rarely maps every tee box, so a built course often has one complete set and
a couple of ragged ones (WBYC: Championship 18/18, Back 11/18, Middle 3/18).
Dropping the ragged sets is honest but leaves a single tee button, which doesn't
look like a real club deployment.

This derives Back / Middle / Forward from the complete set by proportional
scaling, and places each new tee ON the hole — along the bearing from the green
back toward the real tee, at the scaled distance — so the geometry stays
self-consistent rather than being a number with no position behind it.

THE YARDAGES ARE INVENTED. The file records that under "synthetic_tees" so it
can't be mistaken for surveyed data. Never ship this to a club's live app;
replace it with their scorecard.

Usage:  python3 make_demo_tees.py <course.json> [-o out.json]
"""
import argparse, json, math

D = math.pi / 180
R = 6371000
M_PER_YD = 0.9144

# Rough but conventional spreads off the championship tee.
SETS = [('Back', 0.940), ('Middle', 0.865), ('Forward', 0.755)]


def yards(a, b):
    la1, la2 = a['lat'] * D, b['lat'] * D
    dla, dlo = (b['lat'] - a['lat']) * D, (b['lng'] - a['lng']) * D
    h = math.sin(dla / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlo / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h)) / M_PER_YD


def move_toward(origin, target, yds):
    """Point at `yds` from origin, along the origin->target bearing."""
    m = yds * M_PER_YD
    mlat = 111320.0
    mlng = 111320.0 * math.cos(origin['lat'] * D)
    dx = (target['lng'] - origin['lng']) * mlng
    dy = (target['lat'] - origin['lat']) * mlat
    n = math.hypot(dx, dy) or 1.0
    return {'lat': round(origin['lat'] + (dy / n) * m / mlat, 6),
            'lng': round(origin['lng'] + (dx / n) * m / mlng, 6)}


ap = argparse.ArgumentParser()
ap.add_argument('course')
ap.add_argument('-o', '--out')
a = ap.parse_args()

d = json.load(open(a.course))
holes = d['holes']

base_name = d['tees'][0]['name'] if d.get('tees') else 'Championship'
totals = {}
for h in holes:
    base = next((t for t in h['tee_boxes'] if t['name'] == base_name), None)
    if not base:
        continue
    green = h['green']['center']
    origin = {'lat': base['lat'], 'lng': base['lng']}
    keep = [t for t in h['tee_boxes'] if t['name'] == base_name]
    totals[base_name] = totals.get(base_name, 0) + base['yardage']
    for name, f in SETS:
        yds = max(70, int(round(base['yardage'] * f)))
        p = move_toward(green, origin, yds)          # back from the green
        keep.append({'name': name, 'lat': p['lat'], 'lng': p['lng'], 'yardage': yds})
        totals[name] = totals.get(name, 0) + yds
    h['tee_boxes'] = keep

order = [base_name] + [n for n, _ in SETS]
d['tees'] = [{'name': n, 'gender': 'men', 'total_yardage': totals[n]} for n in order if n in totals]
d['synthetic_tees'] = {
    'generated': [n for n, _ in SETS],
    'method': f'proportional scaling from {base_name}, placed along the green->tee bearing',
    'warning': 'DEMO ONLY — these yardages are invented. Replace with the club scorecard.',
}

json.dump(d, open(a.out or a.course, 'w'), separators=(',', ':'), ensure_ascii=False)
for t in d['tees']:
    real = ' (surveyed)' if t['name'] == base_name else ' (INVENTED)'
    print(f"  {t['name']:14s} {t['total_yardage']:5d} yds{real}")
print(f"wrote {a.out or a.course}")
