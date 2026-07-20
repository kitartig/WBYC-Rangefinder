#!/usr/bin/env python3
# Builds the styled user guide from wbyc-guide-template.html by injecting the app's
# real embedded EB Garamond faces + burgee logo (extracted from the app template),
# so the guide is a self-contained, pixel-true match to the app.
# Outputs: pwa/guide/index.html  (deploys at /guide)  +  WBYC-Rangefinder-Guide.html (folder copy)
import re, os

here = os.path.dirname(os.path.abspath(__file__))
app = open(os.path.join(here, 'wbyc-rangefinder-template.html'), encoding='utf-8').read()
tpl = open(os.path.join(here, 'wbyc-guide-template.html'), encoding='utf-8').read()

# --- extract the two EB Garamond @font-face blocks ---
faces = re.findall(r"@font-face\{[^}]*?'EB Garamond'[^}]*?\}", app)
assert len(faces) >= 2, f"expected >=2 EB Garamond faces, found {len(faces)}"
fonts_css = "\n".join(faces[:2])

# --- extract the burgee data URI from the header logo img ---
m = re.search(r'id="logo"\s+src="(data:image/webp;base64,[^"]+)"', app)
assert m, "burgee logo data URI not found"
burgee = m.group(1)

out = tpl.replace('/*__FONTS__*/', fonts_css).replace('__BURGEE__', burgee)
assert '/*__FONTS__*/' not in out and '__BURGEE__' not in out, "placeholders not fully replaced"

os.makedirs(os.path.join(here, 'pwa', 'guide'), exist_ok=True)
with open(os.path.join(here, 'pwa', 'guide', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(out)
with open(os.path.join(here, 'WBYC-Rangefinder-Guide.html'), 'w', encoding='utf-8') as f:
    f.write(out)

print(f"guide built ({len(out)//1024} KB) — pwa/guide/index.html + WBYC-Rangefinder-Guide.html")
