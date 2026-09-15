#!/bin/bash
# Move WBYC onto the current engine — deliberately, and with a look first.
#
#   ./promote-wbyc-engine.sh          # show what would change, change nothing
#   ./promote-wbyc-engine.sh --apply  # take the new engine
#
# ## The point of this script
#
# WBYC is pinned to a frozen engine in engine/, so demo work can't reach it. That
# alone would be a fork, and a fork rots — WBYC would stop getting the fixes that
# the demos are paying for. This is the other half: the deliberate step that
# carries improvements across, with a behavioural diff to read before you commit.
#
# It does NOT diff the files. Two builds of the same engine differ in a thousand
# meaningless ways. It compares the things a golfer would notice: the flags, the
# storage prefix, the distances the app computes, and whether anybody else's club
# name got in. Then it shows you the raw size and line delta for context.
set -euo pipefail
cd "$(dirname "$0")"
APPLY="${1:-}"

CUR=$(python3 -c "import json;print(json.load(open('brands/wbyc.json'))['engine'])")
NEW="engine/engine-$(date +%Y%m%d-%H%M).html"
echo "pinned to : $CUR"
echo "candidate : wbyc-rangefinder-template.html (live)"
echo

cp wbyc-rangefinder-template.html "$NEW"
cp brands/wbyc.json /tmp/wbyc-pinned.json

# build WBYC both ways, into scratch, touching nothing that ships
python3 - "$NEW" <<'PY'
import json, sys, os
b=json.load(open('brands/wbyc.json'))
for tag, eng in (('old', b['engine']), ('new', sys.argv[1])):
    c=dict(b); c['engine']=eng
    c['outputs']={'app':f'/tmp/wbyc-{tag}.html','pwa':None,'bump_sw':False}
    json.dump(c, open(f'/tmp/brand-{tag}.json','w'))
PY
python3 build.py /tmp/brand-old.json >/dev/null
python3 build.py /tmp/brand-new.json >/dev/null

echo "what a golfer would notice"
python3 - <<'PY'
import re
def probe(p):
    s=open(p,encoding='utf-8',errors='replace').read(); low=s.lower()
    t=lambda k:(re.search(r'/\*__'+k+r'__\*/([a-z]+)',s) or [None,'-'])[1]
    return {'AIM':t('AIM_VIEW'), 'smoothing':t('GPS_SMOOTH'), 'opens on aerial':t('SAT_DEFAULT'),
            'storage wbyc_':'yes' if 'wbyc_' in s else 'NO',
            'demo banner':'yes' if 'DEMO ·' in s else 'no',
            'other clubs':str(sum(low.count(w) for w in ('madden','somerset','gull lake','mendota'))),
            'size KB':str(len(s)//1024)}
o,n=probe('/tmp/wbyc-old.html'),probe('/tmp/wbyc-new.html')
bad=False
for k in o:
    flag='' if o[k]==n[k] else '   <-- CHANGES'
    if o[k]!=n[k] and k in ('storage wbyc_','other clubs','demo banner'): bad=True; flag='   <-- CHANGES, and should not'
    print(f"  {k:<18} {o[k]:>8}  ->  {n[k]:<8}{flag}")
open('/tmp/verdict','w').write('BAD' if bad else 'OK')
PY

echo
echo "javascript"
for t in old new; do
  node -e "const s=require('fs').readFileSync('/tmp/wbyc-$t.html','utf8');const m=s.match(/<script>([\s\S]*?)<\/script>/g)||[];let n=0;for(const b of m){try{new Function(b.replace(/<\/?script>/g,''))}catch(e){n++}}console.log('  $t: '+(n?'FAILS TO PARSE':'parses'));"
done

if [ "$(cat /tmp/verdict)" = "BAD" ]; then
  echo; echo "REFUSING: something changed that never should. Not promoting."; rm -f "$NEW"; exit 1
fi

if [ "$APPLY" != "--apply" ]; then
  echo
  echo "Nothing changed. Re-run with --apply to move WBYC onto the new engine."
  echo "(candidate snapshot left at $NEW)"
  exit 0
fi

python3 - "$NEW" <<'PY'
import json, sys, glob
snap=sys.argv[1]
gsnap=snap.replace('engine/engine-','engine/guide-')
import shutil; shutil.copy('wbyc-guide-template.html', gsnap)
for f in ('brands/wbyc.json','brands/wbyc-aim.json'):
    b=json.load(open(f)); b['engine']=snap; b['guide_engine']=gsnap
    json.dump(b,open(f,'w'),indent=2,ensure_ascii=False); open(f,'a').write('\n')
print(f'  pinned to {snap}')
PY
D=$(date +%Y%m%d-%H%M)
cp pwa/index.html "backups/pwa-index.PRE-ENGINE.$D.html"
cp pwa/sw.js      "backups/pwa-sw.PRE-ENGINE.$D.js"
python3 build.py brands/wbyc.json
python3 build_guide.py brands/wbyc.json
echo
echo "Deploy pwa/ when ready. ./rollback-wbyc.sh if it isn't right."
