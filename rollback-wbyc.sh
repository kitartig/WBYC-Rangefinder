#!/bin/bash
# Roll WBYC back to the build saved in backups/, safely.
#
#   ./rollback-wbyc.sh                 # newest backup
#   ./rollback-wbyc.sh 20260907-2231   # a specific stamp
#
# ## Why this is a script and not "copy the old file back"
#
# The app shell is served CACHE-FIRST by pwa/sw.js — look at the last branch of
# its fetch handler. Once a phone holds the v308 cache it keeps serving that
# index.html and never asks the network again. So restoring the old index.html
# on its own changes nothing on the phone: it will happily go on running the
# build you were trying to undo, and you would have no way of telling.
#
# The only thing that evicts the cache is the service worker's VERSION changing,
# because the activate handler deletes every cache whose name isn't the current
# VERSION. So a rollback has to touch sw.js too.
#
# And it bumps the version FORWARD rather than restoring the old number. Going
# back to v307 would probably work — the browser compares sw.js byte-for-byte,
# not by version — but "probably" is not what you want from the escape hatch.
# Forward is unambiguous on every phone that has ever seen this app.
set -euo pipefail
cd "$(dirname "$0")"

STAMP="${1:-}"
if [ -z "$STAMP" ]; then
  STAMP=$(ls backups/wbyc-rangefinder.PRE-*.html 2>/dev/null \
          | sed 's/.*PRE-[A-Z]*\.\(.*\)\.html/\1/' | sort | tail -1)
fi
[ -n "$STAMP" ] || { echo "no backups found in backups/"; exit 1; }

APP=$(ls backups/wbyc-rangefinder.PRE-*."$STAMP".html 2>/dev/null | head -1)
PWA=$(ls backups/pwa-index.PRE-*."$STAMP".html      2>/dev/null | head -1)
CFG=$(ls backups/wbyc.PRE-*."$STAMP".json           2>/dev/null | head -1)
[ -f "$APP" ] && [ -f "$PWA" ] || { echo "incomplete backup for $STAMP"; exit 1; }

echo "rolling back to $STAMP"
cp "$APP" wbyc-rangefinder.html
cp "$PWA" pwa/index.html
[ -f "$CFG" ] && cp "$CFG" brands/wbyc.json && echo "  brand config restored too"

# bump, never restore, the service worker version
V=$(grep -o "wbyc-v[0-9]*" pwa/sw.js | head -1 | tr -d 'wbyc-v')
NEW=$((V + 1))
sed -i.bak "s/wbyc-v$V/wbyc-v$NEW/" pwa/sw.js && rm -f pwa/sw.js.bak

echo "  wbyc-rangefinder.html, pwa/index.html restored"
echo "  service worker v$V -> v$NEW  (forward, so every phone picks it up)"
echo
echo "Now deploy pwa/ as usual. Your Round Log is untouched — it lives in"
echo "localStorage under the wbyc_ prefix, which no build has ever changed."
