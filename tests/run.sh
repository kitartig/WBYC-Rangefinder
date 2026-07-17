#!/bin/sh
# Build + run the DOM-stub harness. Usage: sh tests/run.sh   (from the project root)
node -e "
const fs=require('fs');
const m=fs.readFileSync('wbyc-rangefinder.html','utf8').match(/<script>([\s\S]*)<\/script>/);
fs.writeFileSync('/tmp/wbyc-app.js', m[1]);
"
cat tests/stubs.js /tmp/wbyc-app.js tests/tests.js > /tmp/wbyc-run.js
node /tmp/wbyc-run.js
