#!/usr/bin/env python3
"""Screenshot the built app in a real browser, at phone size.

There IS no browser in the sandbox by default and apt is blocked, so every
proof was rendered by cairosvg — which silently ignores things browsers honour
(vector-effect, most notably; that cost a shipped bug). Setup, once per session:

    pip install playwright --break-system-packages
    PATH=$PATH:~/.local/bin playwright install chromium     # downloads fine
    gcc -shared -fPIC -o ~/libs/libXdamage.so.1 tools/xdamage_stub.c
    export LD_LIBRARY_PATH=$HOME/libs

The only missing system library is libXdamage.so.1, and headless Chromium never
calls its four symbols without an X display, so a no-op stub satisfies the
loader. apt can't help: the proxy allows pypi and npm, not ubuntu ports.

    python3 tools/shoot.py out.png [--at "Earned today"] [--w 390]
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

out = sys.argv[1] if len(sys.argv) > 1 else 'shot.png'
at  = sys.argv[sys.argv.index('--at')+1] if '--at' in sys.argv else None
w   = int(sys.argv[sys.argv.index('--w')+1]) if '--w' in sys.argv else 390

SEED = """() => {
  tee='Green'; pname='Kit';
  card=blankCard(); card.start='2026-07-29';
  const par=i=>holePar(course.holes[i]);
  [0,-2,1,0,-1,1,0,1,0, 1,0,-1,0,2,0,1,0,1].forEach((d,i)=>{ card.holes[i]={s:par(i)+d,p:d<0?1:2,f:null}; });
  weather.code=0; weather.day=1; weather.temp=78;
  shots.length=0;
  shots.push({d:'2026-07-29',h:1,lat:45.07970,lng:-92.99020,t:Date.now()-7e6,club:'D'});
  shots.push({d:'2026-07-29',h:1,lat:45.08188,lng:-92.98925,t:Date.now()-6.9e6,club:'D'});
  openBearLog();
}"""

url = 'file://' + str(pathlib.Path('wbyc-rangefinder.html').resolve())
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox', '--disable-dev-shm-usage'])
    pg = b.new_page(viewport={'width': w, 'height': 844}, device_scale_factor=3)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(1200)
    pg.evaluate(SEED); pg.wait_for_timeout(1000)
    if at:
        pg.evaluate("""(t) => { const s=[...document.querySelectorAll('#bearlog .bl-sec')]
            .find(x=>x.textContent.includes(t));
            if(s) document.getElementById('bearlog').scrollTop = s.offsetTop - 70; }""", at)
        pg.wait_for_timeout(400)
    pg.screenshot(path=out)
    if errs: print('page errors:', errs[:3])
    print('wrote', out)
    b.close()
