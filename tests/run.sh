#!/bin/sh
# Build + run the DOM-stub harness. Usage: sh tests/run.sh   (from the project root)
#
# NOTE: this used to stage into /tmp. Don't. A /tmp left over from another
# session goes EACCES, node's writeFileSync fails, and the harness then runs
# happily against the STALE copy — 88 green ticks for code you didn't build.
# mktemp -d is per-run and always writable.
set -e
T=$(mktemp -d)
node -e "
const fs=require('fs');
const m=fs.readFileSync('wbyc-rangefinder.html','utf8').match(/<script>([\s\S]*)<\/script>/);
fs.writeFileSync('$T/wbyc-app.js', m[1]);
"
cat tests/stubs.js "$T/wbyc-app.js" tests/tests.js > "$T/wbyc-run.js"
node "$T/wbyc-run.js"
