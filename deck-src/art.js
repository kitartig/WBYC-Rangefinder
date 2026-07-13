const sharp = require('sharp');
const path = '/sessions/kind-great-lovelace/deck/';

// palette (the app's own)
const PINK='#f000c2', PINKL='#ffa5eb', GRN='#1fee75', GRNM='#2fbf71', GRND='#0b2e1c', GRND2='#123b26', PALE='#9af6ba';

function contours(seed, n, w, h, col, op){
  let s='', rnd=(()=>{let x=seed;return()=>{x=(x*1664525+1013904223)>>>0;return x/4294967296;};})();
  for(let i=0;i<n;i++){
    const cy=h*0.15+rnd()*h*0.75, amp=8+rnd()*30, ph=rnd()*6.28, per=180+rnd()*260;
    let d='M-20 '+cy.toFixed(0);
    for(let x=0;x<=w+40;x+=40) d+=` Q${x+20} ${(cy+Math.sin((x/per)+ph)*amp).toFixed(0)} ${x+40} ${(cy+Math.sin(((x+40)/per)+ph)*amp*0.7).toFixed(0)}`;
    s+=`<path d="${d}" fill="none" stroke="${col}" stroke-width="${i%4===0?2.2:1}" opacity="${op*(i%4===0?1.5:1)}"/>`;
  }
  return s;
}
// tracer arc through (x0,y0)->(x1,y1) with apex lift
function tracer(x0,y0,x1,y1,lift,wCore,wGlow){
  const mx=(x0+x1)/2, my=(y0+y1)/2-lift;
  const d=`M${x0} ${y0} Q${mx} ${my} ${x1} ${y1}`;
  const ax=(x0+2*mx+x1)/4, ay=(y0+2*my+y1)/4;
  return `<path d="${d}" fill="none" stroke="${PINK}" stroke-width="${wGlow}" opacity=".33" filter="url(#blur)"/>`
    +`<path d="${d}" fill="none" stroke="${PINKL}" stroke-width="${wCore}"/>`
    +`<circle cx="${ax}" cy="${ay}" r="${wCore*2.2}" fill="#ffffff"/>`
    +`<circle cx="${x0}" cy="${y0}" r="${wCore*2.6}" fill="#ffffff" stroke="#f5b512" stroke-width="${wCore*0.7}"/>`;
}
const defs=`<defs><filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="${GRND}"/><stop offset="100%" stop-color="${GRND2}"/></linearGradient>
<radialGradient id="grn" cx="45%" cy="40%" r="75%"><stop offset="0%" stop-color="${GRN}"/><stop offset="100%" stop-color="${GRNM}"/></radialGradient></defs>`;

// ---- 1. hero (2000x1125, dark) ----
const hero=`<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1125" viewBox="0 0 2000 1125">
${defs}<rect width="2000" height="1125" fill="url(#bg)"/>
${contours(7,26,2000,1125,'#3f8f5f',0.16)}
<ellipse cx="1590" cy="300" rx="150" ry="105" fill="url(#grn)" opacity=".92" transform="rotate(-18 1590 300)"/>
<ellipse cx="1466" cy="404" rx="40" ry="22" fill="#e8d9a8" opacity=".85" transform="rotate(24 1466 404)"/>
<ellipse cx="1712" cy="412" rx="34" ry="19" fill="#e8d9a8" opacity=".85" transform="rotate(-30 1712 412)"/>
<rect x="930" y="960" width="40" height="40" rx="9" fill="#35c8ff" opacity=".9"/>
<path d="M950 980 L1240 760 Q1420 560 1590 300" fill="none" stroke="#cfe8d5" stroke-width="4" stroke-dasharray="14 16" opacity=".4"/>
${tracer(950,980,1596,306,400,7,26)}
<line x1="1590" y1="300" x2="1590" y2="212" stroke="#ffffff" stroke-width="5"/>
<path d="M1590 212 L1544 228 L1590 244 Z" fill="${PINK}"/>
</svg>`;

// ---- 2. three-view strip (2460x780, transparent, three dark rounded panels) ----
function panel(x,inner){return `<g transform="translate(${x} 0)"><rect x="0" y="0" width="780" height="780" rx="34" fill="url(#bg)"/>${inner}</g>`;}
// p1: overhead hole map with arc
const p1=contours(11,12,780,780,'#3f8f5f',0.2)
 +`<ellipse cx="540" cy="170" rx="108" ry="76" fill="url(#grn)" opacity=".95" transform="rotate(-15 540 170)"/>`
 +`<ellipse cx="425" cy="255" rx="34" ry="18" fill="#e8d9a8" transform="rotate(28 425 255)"/>`
 +`<rect x="150" y="640" width="34" height="34" rx="8" fill="#35c8ff"/>`
 +`<path d="M167 657 Q300 420 543 176" fill="none" stroke="#cfe8d5" stroke-width="3.4" stroke-dasharray="11 13" opacity=".45"/>`
 +tracer(167,657,545,178,190,5,18);
// p2: side profile
const p2=`<path d="M0 780 L0 560 Q140 520 260 545 Q420 575 560 500 Q670 445 780 470 L780 780 Z" fill="#2fbf71" opacity=".5"/>
 <path d="M0 560 Q140 520 260 545 Q420 575 560 500 Q670 445 780 470" fill="none" stroke="${PALE}" stroke-width="4" opacity=".8"/>
 <path d="M620 486 Q700 462 760 468" fill="none" stroke="${GRN}" stroke-width="9" opacity=".95"/>
 ${tracer(60,548,724,462,300,5,18)}
 <line x1="724" y1="462" x2="724" y2="368" stroke="#ffffff" stroke-width="4"/>
 <path d="M724 368 L684 382 L724 396 Z" fill="${PINK}"/>
 <text x="52" y="120" font-family="Arial" font-size="42" font-weight="bold" fill="${PALE}" opacity=".9">+12 ft</text>`;
// p3: 3D mesh + tracer + stats
let mesh='';
for(let i=0;i<=10;i++){ // perspective grid
  const t=i/10, y=430+t*310, xl=120-90*t, xr=660+90*t;
  mesh+=`<path d="M${xl} ${y} Q390 ${y-40-60*(1-t)} ${xr} ${y}" fill="none" stroke="#4fae74" stroke-width="1.6" opacity="${0.25+0.25*t}"/>`;
}
for(let i=0;i<=8;i++){ const t=i/8, xt=150+t*480, xb=30+t*720;
  mesh+=`<line x1="${xt}" y1="415" x2="${xb}" y2="740" stroke="#4fae74" stroke-width="1.3" opacity=".22"/>`;}
const p3=mesh
 +`<ellipse cx="560" cy="452" rx="86" ry="34" fill="url(#grn)" opacity=".9"/>`
 +tracer(150,700,560,452,330,5,18)
 +`<line x1="560" y1="452" x2="560" y2="360" stroke="#ffffff" stroke-width="4"/>`
 +`<path d="M560 360 L522 373 L560 386 Z" fill="${PINK}"/>`
 +`<text x="330" y="300" font-family="Arial" font-size="46" font-weight="bold" fill="${PINKL}">172 yds</text>`
 +`<text x="330" y="352" font-family="Arial" font-size="30" fill="#dceee2" opacity=".85">plays 180 · apex 96 ft · 5i</text>`;
const strip=`<svg xmlns="http://www.w3.org/2000/svg" width="2460" height="780" viewBox="0 0 2460 780">${defs}
${panel(0,p1)}${panel(840,p2)}${panel(1680,p3)}</svg>`;

// ---- 3. small arc motif (transparent, light-slide corner art) ----
const motif=`<svg xmlns="http://www.w3.org/2000/svg" width="900" height="330" viewBox="0 0 900 330">
<defs><filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter></defs>
<path d="M40 300 Q450 -60 860 290" fill="none" stroke="${PINK}" stroke-width="20" opacity=".22" filter="url(#blur)"/>
<path d="M40 300 Q450 -60 860 290" fill="none" stroke="${PINK}" stroke-width="6"/>
<circle cx="450" cy="120" r="11" fill="${PINK}"/>
<circle cx="40" cy="300" r="13" fill="#ffffff" stroke="#f5b512" stroke-width="4"/>
</svg>`;

(async()=>{
  await sharp(Buffer.from(hero)).png().toFile(path+'hero.png');
  await sharp(Buffer.from(strip)).png().toFile(path+'views.png');
  await sharp(Buffer.from(motif)).png().toFile(path+'motif.png');
  console.log('art done');
})();
