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
    # SVGs here are already cropped to their own viewBox — nothing to trim.
    crest_trim_uri = crest_uri
else:
    crest_uri = f'data:{mime};base64,' + base64.b64encode(raw).decode()
    # wbyc-burgee.webp in particular carries a huge transparent margin — it's
    # sized and positioned for the masthead's negative-margin overlap trick
    # (.bl-mast img{margin-top:-16px;margin-left:-26px}). Used standalone (e.g.
    # the Bear's Log empty-state letterhead) that padding reads as a washed-out
    # logo floating in empty space. Trim to the opaque bounding box, with a
    # small margin kept, for any use that isn't the masthead.
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(raw)).convert('RGBA')
    bbox = im.getbbox()
    if bbox:
        pad = 6
        l, t, r, b = bbox
        l, t = max(0, l - pad), max(0, t - pad)
        r, b = min(im.width, r + pad), min(im.height, b + pad)
        im = im.crop((l, t, r, b))
    buf = io.BytesIO()
    im.save(buf, format='PNG')
    crest_trim_uri = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

values = dict(brand)
values['CREST_SRC'] = crest_uri
values['CREST_TRIM_SRC'] = crest_trim_uri

# ---------------- entry screen: hero photograph and club line ----------------
# The welcome screen's photograph. Optional on purpose: a brand with no photo of
# its own gets an empty url(), a declaration the browser drops, and the entry
# screen falls back to its dark turf gradient rather than a broken image. The
# alternative — inheriting WBYC's 9th green — would put White Bear's course
# behind another club's welcome, which no identity-string guard could see.
welcome_file = brand.get('WELCOME_FILE')
if welcome_file:
    wpath = os.path.join('brands', welcome_file)
    wext = os.path.splitext(wpath)[1].lower()
    wmime = MIME.get(wext) or mimetypes.guess_type(wpath)[0]
    if not wmime:
        sys.exit(f'unknown welcome image type: {wpath}')
    values['WELCOME_SRC'] = (f'data:{wmime};base64,'
                             + base64.b64encode(open(wpath, 'rb').read()).decode())
else:
    values['WELCOME_SRC'] = ''
# The foot of the entry screen: a photograph of real turf, and a feathered patch
# of the same frame carrying the ball that peeks out from under the card. Both
# optional, both empty for a brand that has no photography of its own.
for _key, _tok in (('MID_FILE', 'MID_SRC'), ('GROUND_FILE', 'GROUND_SRC'),
                   ('BALL_FILE', 'BALL_SRC')):
    _f = brand.get(_key)
    if _f:
        _p = os.path.join('brands', _f)
        _m = MIME.get(os.path.splitext(_p)[1].lower()) or mimetypes.guess_type(_p)[0]
        if not _m:
            sys.exit(f'unknown {_key} image type: {_p}')
        values[_tok] = f'data:{_m};base64,' + base64.b64encode(open(_p, 'rb').read()).decode()
    else:
        values[_tok] = ''
# The greeting names the club in full, not the short mark used in the masthead.
values['WELCOME_LINE'] = (brand.get('WELCOME_LINE') or brand.get('club_full')
                          or brand['BRAND'])

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

# Demo banner. A pitch build carries scaled tee yardages and OSM-derived pars;
# if the prospect forwards the link and a member plays off those numbers, that
# is the worst possible first impression. Absent for a real deployment, which
# is also what makes the paid build visibly different from the free one.
banner = brand.get('demo_banner')
_marker = '<!--__DEMO_BANNER__-->'
if out.count(_marker) != 1:
    sys.exit(f'demo banner: expected one {_marker}, found {out.count(_marker)}')
if banner:
    import html as _html
    text = banner if isinstance(banner, str) else \
        'DEMO — yardages not yet verified against the club scorecard'
    # Pinned to the BOTTOM, and deliberately *below* every full-screen overlay.
    # It started at top with z-index 9999, which put it over the Round Log and
    # covered that panel's close button. The engine's overlays run 50–99, so 3
    # keeps the strip above the page and under anything that takes over the
    # screen — when the Round Log opens, the banner simply disappears behind it.
    # The padding-bottom stops it sitting on top of the GPS and WIND controls.
    out = out.replace(_marker,
                      '<style>#app{padding-bottom:58px}</style>'
                      '<div style="background:#7a1533;color:#fff;font:700 11.5px/1.45 '
                      '-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif;'
                      'letter-spacing:.5px;text-align:center;padding:7px 12px;'
                      'position:fixed;bottom:0;left:0;right:0;z-index:3">'
                      + _html.escape(text) + '</div>')
else:
    out = out.replace(_marker + '\n', '')   # take the newline too, no stray blank line

# Per-brand CSS, appended last inside the engine's <style>. A general hook
# rather than a token per tweak: brands want different accent colours, crest
# sizes and control styling, and each of those as its own key would make every
# config longer for no gain. Absent by default.
_css_marker = '/*__BRAND_CSS__*/'
if out.count(_css_marker) != 1:
    sys.exit(f'brand css: expected one {_css_marker}, found {out.count(_css_marker)}')
_bcss = brand.get('css') or ''
if isinstance(_bcss, list):
    _bcss = '\n  '.join(_bcss)
out = out.replace(_css_marker, _bcss)

# Which file the running app may fetch to override its embedded course. Defaults
# to the brand's OWN course file, so a club can still drop an updated scorecard
# beside the app and have it picked up — but can never inherit whatever course
# happens to share a filename on that host. `"live_course": null` disables it.
if 'live_course' in brand:
    live = brand['live_course']
else:
    live = os.path.basename(brand.get('course', 'course_data_v2.json'))
_old_live = "const LIVE_COURSE='course_data_v2.json';"
if out.count(_old_live) != 1:
    sys.exit(f'live-course swap: expected one LIVE_COURSE declaration, found {out.count(_old_live)}')
out = out.replace(_old_live, 'const LIVE_COURSE=%s;'
                  % (json.dumps(live) if live else 'null'))

# Tee colours. The engine's built-in rules key off WBYC's tee names (Blue, White,
# Gold, Red, Green), which are colours by coincidence of that club's card. Any
# other club needs its own map, so this writes rules keyed on the data-tee
# attribute instead of a class: a swatch along the top of every button so the set
# reads at a glance, and the full fill when selected. Absent by default, so no
# club's appearance changes unless its config asks.
_tee_marker = '/*__TEE_COLORS__*/'
if out.count(_tee_marker) != 1:
    sys.exit(f'tee colours: expected one {_tee_marker}, found {out.count(_tee_marker)}')
tee_colors = brand.get('tee_colors') or {}
_css = []
for name, col in tee_colors.items():
    c = col.lstrip('#')
    r, g_, b_ = (int(c[i:i+2], 16) for i in (0, 2, 4))
    # WCAG relative luminance, so pale tees get dark text and vice versa
    lum = 0.2126*r + 0.7152*g_ + 0.0722*b_
    ink = '#141414' if lum > 150 else '#ffffff'
    sel = name.replace('"', '\\"')
    # Selected-state only, matching how the club's own tee colours behave: the
    # chosen tee fills, the rest stay plain. An always-on swatch was tried and
    # read as clutter next to the FRONT/CENTER/BACK panel below it.
    _css.append(f'.tees button.sel[data-tee="{sel}"]{{background:{col};color:{ink};'
                f'border-color:transparent}}')
out = out.replace(_tee_marker, '\n  '.join(_css) if _css else '')

# Keepsake seals. The figure inside every earned seal is a club's own emblem —
# traced from its crest — in that club's colours. Shipping it unchanged puts one
# club's heraldry on another club's keepsake, and no identity guard can see it
# because the payload is an SVG path. A brand supplies its own mark and colours,
# or the seals section is left as-is only for the club it belongs to.
seal = brand.get('seal_mark')
if seal:
    _pairs = [(re.compile(r"const RF_BEAR='[^']*'"), "const RF_BEAR='%s'" % seal['path']),
              (re.compile(r'RF_BW=[\d.]+'), 'RF_BW=%s' % seal['width'])]
    for rx, rep in _pairs:
        if len(rx.findall(out)) != 1:
            sys.exit(f'seal mark: expected one match for {rx.pattern}')
        out = rx.sub(lambda _m: rep, out, count=1)
sealc = brand.get('seal_colors')
if sealc:
    old = "const RF_NAVY='#1638a8', RF_GOLD='#ffd257';"
    if out.count(old) != 1:
        sys.exit('seal colours: RF_NAVY/RF_GOLD declaration not found')
    out = out.replace(old, "const RF_NAVY='%s', RF_GOLD='%s';"
                      % (sealc['ink'], sealc['fill']))

# Ball-flight tracer colour, same plain-value-swap trick. Optional and absent by
# default *on purpose*: WBYC's app is live on members' phones, so a brand that
# wants a different tracer says so in its own config rather than the engine
# changing colour underneath a club that never asked.
tracer = brand.get('tracer')
if tracer:
    old = "const TRACER={main:'#f000c2', bright:'#ffa5eb'};"
    if out.count(old) != 1:
        sys.exit(f'tracer swap: expected exactly one TRACER declaration, found {out.count(old)}')
    out = out.replace(old, "const TRACER={main:'%s', bright:'%s'};"
                      % (tracer['main'], tracer['bright']))

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
# A club that isn't WBYC has neither topo nor aerials of its own, and inheriting
# WBYC's would put White Bear's contours and hole photography inside someone
# else's course — wrong in a way no identity-string guard can see, because the
# payload is numbers and filenames. Set "topo": null / "aerials": null and the
# engine hides the 3D button and disables SAT, which is the honest outcome.
topo_path = brand.get('topo', 'wbyc_topo_data.json')
topo = (json.dumps(json.load(open(topo_path)), separators=(',', ':'), ensure_ascii=False)
        if topo_path else 'null')
aer_path = brand.get('aerials', 'aerials/manifest.json')
aer = (json.dumps(json.load(open(aer_path))['aerials'], separators=(',', ':'))
       if aer_path else 'null')
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
foreign = [s for s in re.findall(r'WBYC|WHITE\s*BEAR|BEAR.S\s*LOG|wbyc_|wbyc-', scan, re.I)
           if brand['BRAND'] != 'WBYC']
if foreign:
    from collections import Counter
    sys.exit('!! another club\'s identity survived: '
             + ', '.join(f'{k}x{v}' for k, v in Counter(foreign).items()))

# ---------------- guard: the built app must actually parse ----------------
# A brand value substituted into a quoted JavaScript string can break out of it.
# MADDEN'S did exactly that — one single-quoted literal became
# 'that file isn't a MADDEN'S Rangefinder…' and the whole script died with
# "Unexpected identifier 'S'". Nothing else caught it: the tokens all resolved,
# no foreign identity survived, the file was the right size, and the page still
# rendered a header. Only the rangefinder underneath was dead. Golf clubs are
# full of apostrophes, so this is a permanent hazard, not a one-off.
scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', out, flags=re.S)
if scripts:
    import subprocess, tempfile
    for i, body in enumerate(scripts):
        if not body.strip():
            continue
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(body)
            p = f.name
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        os.unlink(p)
        if r.returncode != 0:
            msg = (r.stderr or '').strip().splitlines()
            sys.exit(f'!! built app has a JavaScript syntax error in <script> #{i+1}:\n  '
                     + '\n  '.join(msg[:6])
                     + '\n\nMost likely a brand value containing a quote was substituted into a\n'
                       "string literal. Check the apostrophes in: "
                     + ', '.join(f'{k}={v!r}' for k, v in brand.items()
                                 if isinstance(v, str) and ("'" in v or '"' in v)))

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
