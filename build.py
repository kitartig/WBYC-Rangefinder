#!/usr/bin/env python3
"""Rangefinder build — one neutral engine, one brand config.

    python3 build.py                    # WBYC (default), as before
    python3 build.py brands/tpc.json    # any other brand

The engine (wbyc-rangefinder-template.html) carries no club identity. Everything
club-specific lives in brands/*.json and is substituted here. That inversion is
deliberate: identity used to be baked into the engine and each white-label build
subtracted it with string replacement, which leaked WBYC into other clubs' apps
in five separate places. Nothing to subtract now, so nothing to leak.

Data injection (course / topo / aerials) and the service-worker bump behave as
they always did.
"""
import base64, json, mimetypes, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

brand_path = sys.argv[1] if len(sys.argv) > 1 else 'brands/wbyc.json'
brand = json.load(open(brand_path, encoding='utf-8'))
tpl = open('wbyc-rangefinder-template.html', encoding='utf-8').read()

# ---------------- resolve the crest to a data URI ----------------
crest_file = os.path.join('brands', brand['CREST_FILE'])
# Don't trust mimetypes for these: .webp is absent from the table on some
# systems, which silently yields application/octet-stream and a crest that
# still renders but no longer matches the byte-for-byte original.
MIME = {'.webp': 'image/webp', '.svg': 'image/svg+xml', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}
ext = os.path.splitext(crest_file)[1].lower()
mime = MIME.get(ext) or mimetypes.guess_type(crest_file)[0]
if not mime:
    sys.exit(f'unknown crest image type: {crest_file}')
raw = open(crest_file, 'rb').read()
if mime == 'image/svg+xml':
    import urllib.parse
    crest_uri = 'data:image/svg+xml;utf8,' + urllib.parse.quote(raw.decode('utf-8'))
else:
    crest_uri = f'data:{mime};base64,' + base64.b64encode(raw).decode()

values = dict(brand)
values['CREST_SRC'] = crest_uri

# ---------------- substitute, and refuse to ship a half-built app ----------------
needed = set(re.findall(r'\{\{(\w+)\}\}', tpl))
missing = sorted(needed - set(values))
if missing:
    sys.exit(f'{brand_path}: missing required keys {missing}\n'
             f'The engine needs all of: {sorted(needed)}')

out = tpl
for k in needed:
    out = out.replace('{{%s}}' % k, str(values[k]))

left = re.findall(r'\{\{\w+\}\}', out)
if left:
    sys.exit(f'unsubstituted tokens survived: {sorted(set(left))}')

# accent is a plain value swap, not a token, so the engine stays valid CSS
if brand.get('accent_sun'):
    out = out.replace('--accent:#4a5fae', f"--accent:{brand['accent_sun']}")

# ---------------- data injection (unchanged behaviour) ----------------
# A course file carries club identity of its own — course_name, location,
# scorecard URLs, attribution. Normally that's correct, because each club builds
# from their own course. A brand borrowing someone else's course for a demo must
# set "neutralise_course": true, or the guard below will stop the build.
course_obj = json.load(open(brand.get('course', 'course_data_v2.json')))
if brand.get('neutralise_course'):
    for k in ('course_name', 'location'):
        course_obj[k] = ''
    src = course_obj.get('data_source')
    course_obj['data_source'] = 'OpenStreetMap' if isinstance(src, str) else {}
    course_obj['attribution'] = 'Course geometry © OpenStreetMap contributors (ODbL).'
course = json.dumps(course_obj, separators=(',', ':'), ensure_ascii=False)
topo = json.dumps(json.load(open(brand.get('topo', 'wbyc_topo_data.json'))),
                  separators=(',', ':'), ensure_ascii=False)
aer = json.dumps(json.load(open('aerials/manifest.json'))['aerials'], separators=(',', ':'))
assert out.count('/*__COURSE_DATA__*/null') == 1 and out.count('/*__TOPO_DATA__*/null') == 1 \
    and out.count('/*__AERIALS__*/null') == 1
out = (out.replace('/*__COURSE_DATA__*/null', course)
          .replace('/*__TOPO_DATA__*/null', topo)
          .replace('/*__AERIALS__*/null', aer))

# ---------------- guard: no other brand's identity may survive ----------------
# This is the check that caught the fifth leak. It scans only human-readable
# markup — the crest data URI and the topo polylines are opaque and can contain
# any letter sequence by coincidence.
scan = re.sub(r'data:image/[^"]*', '', out)
scan = re.sub(r'"contours":\[.*?\],"grid"', '', scan, flags=re.S)
scan = re.sub(r'"b64":"[^"]*"', '', scan)
foreign = [s for s in re.findall(r'WBYC|WHITE BEAR|Bear.s Log|wbyc_', scan)
           if brand['BRAND'] != 'WBYC']
if foreign:
    from collections import Counter
    sys.exit('!! another club\'s identity survived: '
             + ', '.join(f'{k}x{v}' for k, v in Counter(foreign).items()))

# ---------------- inline vendored libraries ----------------
# html2canvas powers the keepsake's Share-as-image. Kept as a separate file so the
# template stays readable; injected here so the shipped app is still one offline file.
vendor = open('vendor/html2canvas.min.js', encoding='utf-8').read()
if out.count('/*__VENDOR__*/') != 1:
    sys.exit('vendor marker /*__VENDOR__*/ missing or duplicated in the template')
out = out.replace('/*__VENDOR__*/', vendor)

# ---------------- write ----------------
o = brand.get('outputs', {})
app_path = o.get('app', 'app.html')
open(app_path, 'w', encoding='utf-8').write(out)
wrote = [app_path]
if o.get('pwa'):
    open(o['pwa'], 'w', encoding='utf-8').write(out)
    wrote.append(o['pwa'])
if o.get('bump_sw'):
    sw = open('pwa/sw.js').read()
    v = int(re.search(r"wbyc-v(\d+)", sw).group(1))
    open('pwa/sw.js', 'w').write(sw.replace(f"'wbyc-v{v}'", f"'wbyc-v{v+1}'"))
    wrote.append(f'pwa/sw.js (v{v+1})')

print(f"built {brand['BRAND']} {brand['PRODUCT']} ({len(out)//1024} KB) "
      f"— storage prefix '{brand['STORE']}_'")
print('  wrote: ' + ', '.join(wrote))
