#!/usr/bin/env python3
"""WBYC Rangefinder build: injects course/topo/aerial data into the template,
writes the standalone app + pwa/index.html, and bumps the service-worker version.
Run from the project folder: python3 build.py"""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
tpl = open('wbyc-rangefinder-template.html').read()
course = json.dumps(json.load(open('course_data_v2.json')), separators=(',',':'), ensure_ascii=False)
topo = json.dumps(json.load(open('wbyc_topo_data.json')), separators=(',',':'), ensure_ascii=False)
aer = json.dumps(json.load(open('aerials/manifest.json'))['aerials'], separators=(',',':'))
assert tpl.count('/*__COURSE_DATA__*/null')==1 and tpl.count('/*__TOPO_DATA__*/null')==1 and tpl.count('/*__AERIALS__*/null')==1
out = (tpl.replace('/*__COURSE_DATA__*/null', course)
          .replace('/*__TOPO_DATA__*/null', topo)
          .replace('/*__AERIALS__*/null', aer))
open('wbyc-rangefinder.html','w').write(out)
open('pwa/index.html','w').write(out)
sw = open('pwa/sw.js').read()
v = int(re.search(r"wbyc-v(\d+)", sw).group(1))
open('pwa/sw.js','w').write(sw.replace(f"'wbyc-v{v}'", f"'wbyc-v{v+1}'"))
print(f"built ({len(out)//1024} KB), service worker v{v+1}")
