#!/usr/bin/env python3
"""Builds the styled user guide, pixel-true to the app it documents.

    python3 build_guide.py                    # WBYC (default)
    python3 build_guide.py brands/tpc.json    # any other brand

Previously this reached into the app template and extracted the crest from
`id="logo" src="data:image/webp;base64,…"`. Since the engine was made neutral
that attribute holds {{CREST_SRC}}, so the crest now comes from the brand config
— the same source build.py uses. The guide is per-brand as a result, which is
what you want anyway: a club shouldn't be handed another club's guide.

Outputs (WBYC): pwa/guide/index.html  +  WBYC-Rangefinder-Guide.html
"""
import base64, json, os, re, sys, urllib.parse

here = os.path.dirname(os.path.abspath(__file__))
brand_path = sys.argv[1] if len(sys.argv) > 1 else 'brands/wbyc.json'
brand = json.load(open(os.path.join(here, brand_path), encoding='utf-8'))

app = open(os.path.join(here, 'wbyc-rangefinder-template.html'), encoding='utf-8').read()
tpl = open(os.path.join(here, 'wbyc-guide-template.html'), encoding='utf-8').read()

# --- typeface: still embedded in the engine, so still extracted from it ---
faces = re.findall(r"@font-face\{[^}]*?'EB Garamond'[^}]*?\}", app)
assert len(faces) >= 2, f"expected >=2 EB Garamond faces, found {len(faces)}"
fonts_css = "\n".join(faces[:2])

# --- crest: from the brand config, matching build.py exactly ---
MIME = {'.webp': 'image/webp', '.svg': 'image/svg+xml', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}
crest_file = os.path.join(here, 'brands', brand['CREST_FILE'])
ext = os.path.splitext(crest_file)[1].lower()
mime = MIME.get(ext)
assert mime, f'unknown crest image type: {crest_file}'
raw = open(crest_file, 'rb').read()
crest = ('data:image/svg+xml;utf8,' + urllib.parse.quote(raw.decode('utf-8'))
         if mime == 'image/svg+xml'
         else f'data:{mime};base64,' + base64.b64encode(raw).decode())

out = (tpl.replace('/*__FONTS__*/', fonts_css)
          .replace('__BURGEE__', crest)
          .replace('{{BRAND}}', brand['BRAND'])
          .replace('{{PRODUCT}}', brand['PRODUCT'])
          .replace('{{DIARY}}', brand['DIARY']))
assert '/*__FONTS__*/' not in out and '__BURGEE__' not in out, "placeholders not fully replaced"

outputs = brand.get('guide_outputs') or ['pwa/guide/index.html', 'WBYC-Rangefinder-Guide.html']
for rel in outputs:
    p = os.path.join(here, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(out)

print(f"guide built for {brand['BRAND']} ({len(out)//1024} KB) — " + ', '.join(outputs))
