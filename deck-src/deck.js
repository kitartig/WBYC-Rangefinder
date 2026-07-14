const pptxgen = require('pptxgenjs');
const P = '/sessions/kind-great-lovelace/deck/';

// palette
const INK='0E2A1C', GRN='1E7A4A', GRNL='E9F7EE', GRNXL='F4FBF6', PINK='F000C2', DIM='5F7468', WHT='FFFFFF', PALE='C9EED9';
const HF='Didot', BF='Raleway';

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5

const foot = (s, n) => s.addText(`WBYC Rangefinder · a member-built proposal · ${n}`,
  {x:0.55,y:7.08,w:6,h:0.3,fontFace:BF,fontSize:9,color:DIM,margin:0});

// ---------- S1 TITLE ----------
let s = pres.addSlide();
s.background = {path: P+'hero.png'};
s.addText('WBYC RANGEFINDER', {x:0.7,y:2.15,w:9.6,h:1.2,fontFace:HF,fontSize:54,bold:true,color:WHT,charSpacing:3,margin:0});
s.addText('A digital twin of the club’s Donald Ross classic — built by a member, for the members.',
  {x:0.72,y:3.35,w:7.6,h:0.9,fontFace:BF,fontSize:19,color:PALE,italic:true,margin:0});
s.addText([
  {text:'A proposal to trade craft for dues', options:{bold:true,color:'FFA5EB'}},
  {text:'   ·   Kit Artig   ·   July 2026', options:{color:PALE}},
],{x:0.72,y:6.55,w:8,h:0.4,fontFace:BF,fontSize:14,margin:0});
s.addNotes('Open with the story: 1920 Ross course, 2026 tool. Everything on screen tonight runs offline on any phone.');

// ---------- S2 WHAT THE CLUB WOULD OWN ----------
s = pres.addSlide();
s.background = {color:WHT};
s.addText('What the club would own', {x:0.55,y:0.42,w:9,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
const feats = [
  ['GPS rangefinder', 'Front / center / back to every green — or tap in today’s actual pin and every number re-keys to it. Live hazard carries, dogleg targets.'],
  ['“Plays like” physics', 'USGS lidar elevation (+ live wind) adjusts every number. One tap returns it to tournament-legal raw yardage.'],
  ['3D flyover + shot tracer', 'TV-style ball flight over real terrain, with yardage, apex and club stats pinned to the arc.'],
  ['Scorecard & stats', 'Strokes, putts, fairways, GIR, club distances learned from real shots, and a one-tap GHIN posting helper.'],
  ['Green reading', 'Fall-line arrows and 2-ft contours on every green complex, from survey-grade lidar.'],
  ['Offline PWA', 'No app store, no accounts, no ads, no data collection. Install from a link; works with zero signal.'],
];
feats.forEach((f,i)=>{
  const col=i%2, row=(i-col)/2;
  const x=0.55+col*6.35, y=1.45+row*1.62;
  s.addShape('ellipse',{x:x,y:y+0.06,w:0.42,h:0.42,fill:{color:i===2?PINK:GRN}});
  s.addText(String(i+1),{x:x,y:y+0.06,w:0.42,h:0.42,align:'center',fontFace:BF,fontSize:14,bold:true,color:WHT,margin:0});
  s.addText(f[0],{x:x+0.6,y:y,w:5.6,h:0.36,fontFace:BF,fontSize:16,bold:true,color:INK,margin:0});
  s.addText(f[1],{x:x+0.6,y:y+0.36,w:5.55,h:1.05,fontFace:BF,fontSize:12.5,color:'33463C',margin:0});
});
s.addShape('roundRect',{x:0.55,y:6.35,w:12.23,h:0.62,rectRadius:0.12,fill:{color:GRNL}});
s.addText([
  {text:'Zero member data leaves the phone. ',options:{bold:true,color:INK}},
  {text:'No tracking, no vendor lock-in, no per-member fees — the opposite of every commercial golf app.',options:{color:'33463C'}},
],{x:0.85,y:6.42,w:11.7,h:0.48,fontFace:BF,fontSize:13,margin:0});
s.addNotes('If "too much detail" comes up: the home screen is three big numbers, like the sprinkler heads. Everything else is opt-in taps. It passes the grandparent test on the first tee.');
foot(s,'02');

// ---------- S3 PROVENANCE ----------
s = pres.addSlide();
s.background = {color:GRNXL};
s.addText('Craftsmanship you can audit', {x:0.55,y:0.42,w:10,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
s.addText('Every yardage in the app traces to an official or public source — nothing is guessed.',
  {x:0.57,y:1.18,w:9.5,h:0.4,fontFace:BF,fontSize:15,italic:true,color:DIM,margin:0});
const rows = [
  [{text:'Source',options:{bold:true,color:WHT,fill:GRN}},{text:'What it provides',options:{bold:true,color:WHT,fill:GRN}},{text:'Pedigree',options:{bold:true,color:WHT,fill:GRN}}],
  ['Official WBYC scorecard','Par, handicap and yardage for all 4 tee sets, men’s & women’s','Club-published'],
  ['OpenStreetMap survey','Green polygons, centerlines, 69 bunkers, 5 water hazards','ODbL, attribution kept'],
  ['USGS 3DEP lidar','Elevation grid + 1,839 contour lines at 2-ft intervals; 3-m detail on every green','U.S. public domain'],
  ['USGS NAIP imagery','18 aerial photos, ~1 m/pixel, geo-aligned under every hole','U.S. public domain'],
];
s.addTable(rows.map(r=>r.map(c=>typeof c==='string'?{text:c,options:{color:INK}}:c)),
  {x:0.55,y:1.75,w:12.23,colW:[3.3,5.93,3.0],fontFace:BF,fontSize:13.5,rowH:0.62,valign:'middle',
   border:{type:'solid',color:'D5E8DC',pt:1},fill:{color:WHT},margin:0.09});
s.addShape('roundRect',{x:0.55,y:5.15,w:5.9,h:1.55,rectRadius:0.12,fill:{color:WHT},line:{color:'D5E8DC',width:1}});
s.addText([{text:'±16 yds',options:{fontSize:34,bold:true,color:GRN,breakLine:true}},
  {text:'measured vs. the printed card, on every tee of every hole',options:{fontSize:12.5,color:DIM}}],
  {x:0.85,y:5.32,w:5.4,h:1.25,fontFace:BF,margin:0});
s.addShape('roundRect',{x:6.88,y:5.15,w:5.9,h:1.55,rectRadius:0.12,fill:{color:WHT},line:{color:'D5E8DC',width:1}});
s.addText([{text:'2 ft',options:{fontSize:34,bold:true,color:PINK,breakLine:true}},
  {text:'contour interval on the greens — finer than the printed pin sheets',options:{fontSize:12.5,color:DIM}}],
  {x:7.18,y:5.32,w:5.4,h:1.25,fontFace:BF,margin:0});
foot(s,'03');

// ---------- S4 THE EXPERIENCE ----------
s = pres.addSlide();
s.background = {color:WHT};
s.addText('One shot, three ways to see it', {x:0.55,y:0.42,w:11,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
s.addImage({path:P+'views.png', x:0.55, y:1.5, w:12.23, h:3.88});
const caps=[['Overhead','Flight arc over the hole map, with carries, wind and club rings'],
  ['Profile','Terrain cross-section that shows why a shot plays long or short'],
  ['3D tracer','Broadcast-style flyover with yardage stats pinned at the apex']];
caps.forEach((c,i)=>{
  const x=0.55+i*4.18;
  s.addText(c[0],{x:x,y:5.55,w:3.9,h:0.35,fontFace:BF,fontSize:16,bold:true,color:i===2?PINK:GRN,margin:0});
  s.addText(c[1],{x:x,y:5.9,w:3.9,h:0.75,fontFace:BF,fontSize:12.5,color:'33463C',margin:0});
});
foot(s,'04');

// ---------- S5 THE 19TH HOLE (review at home) ----------
s = pres.addSlide();
s.background = {color:INK};
s.addText('The 19th hole: take the round home', {x:0.55,y:0.42,w:11.5,h:0.75,fontFace:HF,fontSize:36,bold:true,color:WHT,margin:0});
s.addText('No profile, no sign-up: score a hole or mark a shot and the round saves itself — then reviews best on the big screen at home. The replay is the reward that keeps the app in the round.',
  {x:0.57,y:1.18,w:11.6,h:0.62,fontFace:BF,fontSize:14.5,italic:true,color:PALE,margin:0});
const home=[
  ['Replay every hole','The 3D flyover, tracer and flight stats work from the couch exactly as they did on the tee — spin the terrain, argue the club choice.'],
  ['Walk the card','Strokes, putts, fairways and GIR hole by hole; tap any row to jump back to that hole’s map and relive it.'],
  ['Watch the season build','Vs-par trend, personal bests, last-five averages, and club distances that keep learning from every marked shot.'],
  ['Any screen, no fuss','It’s a web app — phone on the course, iPad on the sofa, laptop in the den. Same link, no installs, no accounts.'],
];
home.forEach((f,i)=>{
  const col=i%2, row=(i-col)/2;
  const x=0.55+col*6.35, y=1.85+row*1.95;
  s.addShape('ellipse',{x:x,y:y+0.05,w:0.42,h:0.42,fill:{color:i===3?PINK:'2FBF71'}});
  s.addText('⌂',{x:x,y:y+0.05,w:0.42,h:0.42,align:'center',fontFace:BF,fontSize:15,bold:true,color:WHT,margin:0});
  s.addText(f[0],{x:x+0.6,y:y,w:5.6,h:0.36,fontFace:BF,fontSize:16,bold:true,color:WHT,margin:0});
  s.addText(f[1],{x:x+0.6,y:y+0.38,w:5.55,h:1.35,fontFace:BF,fontSize:12.5,color:PALE,margin:0});
});
s.addImage({path:P+'motif.png', x:9.4, y:0.18, w:3.5, h:1.28, transparency:20});
s.addText('Rounds are banked on the device that recorded them — that’s the privacy promise. Household sync between phone and iPad is on the roadmap.',
  {x:0.57,y:6.5,w:12,h:0.35,fontFace:BF,fontSize:11,italic:true,color:'9FB8A9',margin:0});
s.addText('WBYC Rangefinder · a member-built proposal · 05',{x:0.55,y:7.08,w:6,h:0.3,fontFace:BF,fontSize:9,color:'7E958A',margin:0});

// ---------- S6 WHAT MEMBERS PAY ELSEWHERE ----------
s = pres.addSlide();
s.background = {color:GRNXL};
s.addText('What members already pay for less', {x:0.55,y:0.42,w:11,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
const apps=[['Golfshot Pro','$60–100 / yr'],['18Birdies Premium','$50–96 / yr'],['GolfLogix','$50 / yr'],['Arccos Caddie','$99+ / yr']];
apps.forEach((a,i)=>{
  const x=0.55+i*3.12;
  s.addShape('roundRect',{x:x,y:1.55,w:2.9,h:1.5,rectRadius:0.12,fill:{color:WHT},line:{color:'D5E8DC',width:1}});
  s.addText([{text:a[1],options:{fontSize:22,bold:true,color:INK,breakLine:true}},
    {text:a[0],options:{fontSize:12.5,color:DIM}}],{x:x+0.25,y:1.75,w:2.5,h:1.1,fontFace:BF,margin:0});
});
s.addText('… for generic maps of 40,000 courses they don’t play, behind accounts, ads and upsells.',
  {x:0.57,y:3.3,w:11.5,h:0.4,fontFace:BF,fontSize:14,italic:true,color:DIM,margin:0});
s.addShape('roundRect',{x:0.55,y:4.0,w:12.23,h:2.15,rectRadius:0.14,fill:{color:INK}});
s.addText([{text:'WBYC Rangefinder: $0 to every member.',options:{fontSize:26,bold:true,color:WHT,breakLine:true}},
  {text:'One course, drawn from lidar and the club’s own card — sharper than any of them on the only 18 holes that matter here. ~300 golfing members × $60/yr equivalent ≈ $18,000/yr of member value.',
   options:{fontSize:14.5,color:PALE}}],
  {x:0.95,y:4.3,w:11.4,h:1.6,fontFace:BF,margin:0});
s.addText('Consumer pricing: ScoringZone & Birvix app-pricing surveys, 2026. Member count is an assumption — replace with the club’s roster.',
  {x:0.55,y:6.55,w:12,h:0.3,fontFace:BF,fontSize:9,color:DIM,margin:0});
s.addNotes('The "who cares" answer lives here: members are already using outside golf apps on our fairways — paying for them, and feeding them location data. The question is not whether an app is used at WBYC; it is whose.');
foot(s,'06');

// ---------- S6 REPLACEMENT COST ----------
s = pres.addSlide();
s.background = {color:WHT};
s.addText('What it would cost to commission', {x:0.55,y:0.42,w:11,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
s.addText([{text:'$45K–$75K',options:{fontSize:64,bold:true,color:GRN,breakLine:true}},
  {text:'typical agency quote for a custom GPS / location app of this scope, single platform',options:{fontSize:15,color:DIM}}],
  {x:0.55,y:1.6,w:6.2,h:2.4,fontFace:BF,margin:0});
const tiers=[['Simple app (forms + content)','$15K – $30K'],['Mid-complexity, GPS & sensors','$30K – $80K'],['Location-tracking app, one platform','$45K – $60K']];
tiers.forEach((t,i)=>{
  const y=1.75+i*0.78;
  s.addShape('roundRect',{x:7.2,y:y,w:5.55,h:0.62,rectRadius:0.1,fill:{color:GRNL}});
  s.addText(t[0],{x:7.45,y:y+0.05,w:3.7,h:0.5,fontFace:BF,fontSize:12.5,color:INK,valign:'middle',margin:0});
  s.addText(t[1],{x:11.0,y:y+0.05,w:1.7,h:0.5,fontFace:BF,fontSize:13,bold:true,color:GRN,valign:'middle',margin:0});
});
s.addShape('roundRect',{x:0.55,y:4.45,w:12.23,h:1.85,rectRadius:0.14,fill:{color:GRNXL},line:{color:'D5E8DC',width:1}});
s.addText([{text:'And the quotes above don’t include the hard part. ',options:{bold:true,color:INK}},
  {text:'Survey-grade course geometry, lidar terrain processing, per-green 3-m elevation patches, offline packaging and a season of on-course tuning are specialist work no template shop delivers. The club would be buying the finished, validated article — not a statement of work.',options:{color:'33463C'}}],
  {x:0.9,y:4.72,w:11.5,h:1.35,fontFace:BF,fontSize:14,margin:0});
s.addText('Dev-cost ranges: Business of Apps, TopFlight Apps & USM Systems 2025–26 pricing guides.',
  {x:0.55,y:6.55,w:12,h:0.3,fontFace:BF,fontSize:9,color:DIM,margin:0});
foot(s,'07');

// ---------- S7 VALUE, THREE WAYS ----------
s = pres.addSlide();
s.background = {color:GRNXL};
s.addText('A fair value, three ways', {x:0.55,y:0.42,w:11,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
const lenses=[
  ['Replacement cost','$45K–$75K','one-time build, before data work',GRN],
  ['Member value','≈ $18K / yr','300 golfers × $60/yr app-subscription equivalent',GRN],
  ['Club-software lens','$3K–$10K / yr','white-label club apps & GPS licensing (quote-based)',GRN],
];
lenses.forEach((l,i)=>{
  const x=0.55+i*4.18;
  s.addShape('roundRect',{x:x,y:1.5,w:3.9,h:2.3,rectRadius:0.14,fill:{color:WHT},line:{color:'D5E8DC',width:1}});
  s.addText([{text:l[0],options:{fontSize:14,bold:true,color:DIM,breakLine:true}},
    {text:l[1],options:{fontSize:30,bold:true,color:l[3],breakLine:true}},
    {text:l[2],options:{fontSize:11.5,color:DIM}}],
    {x:x+0.28,y:1.72,w:3.4,h:1.9,fontFace:BF,margin:0});
});
s.addShape('roundRect',{x:0.55,y:4.15,w:12.23,h:2.1,rectRadius:0.14,fill:{color:INK}});
s.addText([{text:'THE ASK',options:{fontSize:13,bold:true,color:'FFA5EB',charSpacing:2,breakLine:true}},
  {text:'Annual dues in trade  —  est. $8K–$12K / yr',options:{fontSize:28,bold:true,color:WHT,breakLine:true}},
  {text:'Below the member-value lens, inside the club-software lens, and a fraction of replacement cost. Cash outlay for the club: $0.',options:{fontSize:14,color:PALE}}],
  {x:0.95,y:4.4,w:11.4,h:1.7,fontFace:BF,margin:0});
s.addText('Dues estimate from public reporting (2020 tiers $374–$960/mo; initiation raised to $65K in 2025 — MSPBJ). Substitute the actual figure.',
  {x:0.55,y:6.55,w:12.2,h:0.3,fontFace:BF,fontSize:9,color:DIM,margin:0});
foot(s,'08');

// ---------- S8 THE PROPOSAL ----------
s = pres.addSlide();
s.background = {color:WHT};
s.addText('The proposal', {x:0.55,y:0.42,w:9,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
s.addShape('roundRect',{x:0.55,y:1.5,w:5.95,h:4.6,rectRadius:0.14,fill:{color:GRNXL},line:{color:'D5E8DC',width:1}});
s.addText('THE CLUB RECEIVES',{x:0.95,y:1.8,w:5.2,h:0.4,fontFace:BF,fontSize:13,bold:true,charSpacing:2,color:GRN,margin:0});
s.addText([
  {text:'Exclusive club license to WBYC Rangefinder for members and guests',options:{bullet:true,breakLine:true,paraSpaceAfter:10}},
  {text:'Hosting, maintenance and OS/browser updates — handled',options:{bullet:true,breakLine:true,paraSpaceAfter:10}},
  {text:'Reasonable revisions and update services, free (details next slide)',options:{bullet:true,breakLine:true,paraSpaceAfter:10}},
  {text:'A member-built story for the club’s 106th season — and a recruiting talking point',options:{bullet:true}},
],{x:0.95,y:2.3,w:5.25,h:3.5,fontFace:BF,fontSize:14.5,color:'22352B',margin:0});
s.addShape('roundRect',{x:6.83,y:1.5,w:5.95,h:4.6,rectRadius:0.14,fill:{color:INK}});
s.addText('IN EXCHANGE',{x:7.23,y:1.8,w:5.2,h:0.4,fontFace:BF,fontSize:13,bold:true,charSpacing:2,color:'FFA5EB',margin:0});
s.addText([
  {text:'Annual dues credited in trade for the license + services',options:{bullet:true,color:WHT,breakLine:true,paraSpaceAfter:10}},
  {text:'Author retains the underlying code and tooling (the club’s data stays the club’s)',options:{bullet:true,color:WHT,breakLine:true,paraSpaceAfter:10}},
  {text:'Renewal is annual and either side can walk — low ceremony, low risk',options:{bullet:true,color:WHT,breakLine:true,paraSpaceAfter:10}},
  {text:'Scorekeeper’s honorific optional, but welcomed',options:{bullet:true,color:PALE,italic:true}},
],{x:7.23,y:2.3,w:5.25,h:3.5,fontFace:BF,fontSize:14.5,margin:0});
s.addText('Structured as a barter of services — both sides should confirm tax treatment with their accountants.',
  {x:0.57,y:6.45,w:11.5,h:0.35,fontFace:BF,fontSize:11,italic:true,color:DIM,margin:0});
s.addNotes('If asked "why not one-time?": a one-time sale hands the club a depreciating asset; the annual trade buys a living service — seasonal re-survey, fixes, roadmap — and the ask sits below the $18K/yr member-value ceiling. Either side can walk at renewal.');
foot(s,'09');

// ---------- S9 INCLUDED SERVICES ----------
s = pres.addSlide();
s.background = {color:GRNXL};
s.addText('Included free: revisions & updates', {x:0.55,y:0.42,w:11.5,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
const svcs=[
  ['Seasonal data refresh','Tee, pin-area, bunker and hazard changes re-surveyed and shipped each spring'],
  ['Reasonable revisions','UI polish, palette requests, new stats — the same responsiveness that built this app'],
  ['Fixes & compatibility','Bug fixes, new-phone and browser updates, within days not quarters'],
  ['On-course validation','A walked verification round every season, every tee'],
  ['Feature roadmap','New capabilities keep landing (see next slide) at no added cost'],
  ['Member support','A named human who plays here, not a ticket queue'],
];
svcs.forEach((v,i)=>{
  const col=i%3, row=(i-col)/3;
  const x=0.55+col*4.18, y=1.55+row*2.5;
  s.addShape('roundRect',{x:x,y:y,w:3.9,h:2.2,rectRadius:0.14,fill:{color:WHT},line:{color:'D5E8DC',width:1}});
  s.addShape('ellipse',{x:x+0.3,y:y+0.28,w:0.4,h:0.4,fill:{color:i===4?PINK:GRN}});
  s.addText('✓',{x:x+0.3,y:y+0.28,w:0.4,h:0.4,align:'center',fontFace:BF,fontSize:14,bold:true,color:WHT,margin:0});
  s.addText(v[0],{x:x+0.3,y:y+0.85,w:3.35,h:0.4,fontFace:BF,fontSize:15,bold:true,color:INK,margin:0});
  s.addText(v[1],{x:x+0.3,y:y+1.25,w:3.35,h:0.85,fontFace:BF,fontSize:11.5,color:'33463C',margin:0});
});
s.addText('“Reasonable” means the good-faith standard we’d expect of any member trade — scoped in the one-page agreement.',
  {x:0.57,y:6.62,w:11.8,h:0.35,fontFace:BF,fontSize:11,italic:true,color:DIM,margin:0});
foot(s,'10');

// ---------- S10 ROADMAP ----------
s = pres.addSlide();
s.background = {color:WHT};
s.addText('Already moving: the roadmap', {x:0.55,y:0.42,w:11,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
s.addImage({path:P+'motif.png', x:8.6, y:0.25, w:4.2, h:1.54, transparency:12});
const phases=[
  ['NOW — shipping','Shot tracer with flight stats, pin-sheet mode, plays-like profile view, green fall-lines, club-distance learning, all five tee sets incl. the new Greens, scorecard + GHIN helper, offline install',GRN],
  ['FALL 2026','Member beta round, GPS capture of the one unmapped tee (Hole 5 Red), back-tee refinements, feedback sweep',GRN],
  ['2027','AI-illustrated hole art, cinematic hole flyovers, phone-to-iPad round sync, practice-round mode — club input steers the order',PINK],
];
phases.forEach((p2,i)=>{
  const y=1.9+i*1.55;
  s.addShape('ellipse',{x:0.8,y:y+0.12,w:0.5,h:0.5,fill:{color:p2[2]}});
  if(i<phases.length-1) s.addShape('rect',{x:1.02,y:y+0.62,w:0.06,h:1.05,fill:{color:'D5E8DC'}});
  s.addText(p2[0],{x:1.6,y:y,w:3.1,h:0.45,fontFace:BF,fontSize:16,bold:true,color:INK,margin:0});
  s.addText(p2[1],{x:4.8,y:y,w:7.9,h:1.3,fontFace:BF,fontSize:13.5,color:'33463C',margin:0});
});
foot(s,'11');

// ---------- S12 ANTICIPATED QUESTIONS ----------
s = pres.addSlide();
s.background = {color:GRNXL};
s.addText('Anticipated questions', {x:0.55,y:0.42,w:10,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
s.addText('This is a stewardship project — the Ross course documented to two feet. A yardage book that happens to fit in a pocket.',
  {x:0.57,y:1.18,w:11.6,h:0.4,fontFace:BF,fontSize:14.5,italic:true,color:DIM,margin:0});
const qa=[
  ['“Isn’t this too much detail for a traditional club?”',
   'The front page is three big numbers — front, center, back — same as the sprinkler heads. Every layer beyond that is optional and waits for a tap. Clubs commission yardage books and course portraits without blinking; this is both.'],
  ['“Who cares? Will anyone actually use it?”',
   'Members already do — on our fairways, today, paying $60–100/yr to outside apps for fuzzy generic maps that harvest their location. The club can’t stop that. The only open question is whether the default app at WBYC is a stranger’s or the club’s own.'],
  ['“What about member data?”',
   'There is none. No accounts, no sign-up, no analytics; rounds live on the member’s own phone and nothing leaves it. That is less data liability than any vendor app the club could buy.'],
  ['“Why annual, not one-time?”',
   'Because it’s a living service, not a purchase: greens re-surveyed each season, fixes within days, a roadmap the club steers. Renewal is annual and either side can walk — the club never holds a depreciating asset.'],
];
qa.forEach((q,i)=>{
  const col=i%2, row=(i-col)/2;
  const x=0.55+col*6.35, y=1.85+row*2.35;
  s.addShape('roundRect',{x:x,y:y,w:5.88,h:2.1,rectRadius:0.14,fill:{color:WHT},line:{color:'D5E8DC',width:1}});
  s.addText(q[0],{x:x+0.3,y:y+0.2,w:5.3,h:0.55,fontFace:HF,fontSize:14.5,bold:true,italic:true,color:i===1?PINK:GRN,margin:0});
  s.addText(q[1],{x:x+0.3,y:y+0.78,w:5.3,h:1.2,fontFace:BF,fontSize:11,color:'33463C',margin:0});
});
s.addNotes('Lead with the stewardship line before taking questions. The data answer is a shield, not the pitch — use it only when liability comes up.');
s.addText('WBYC Rangefinder · a member-built proposal · 12',{x:0.55,y:7.08,w:6,h:0.3,fontFace:BF,fontSize:9,color:DIM,margin:0});

// ---------- S13 FULL FEATURE INVENTORY ----------
s = pres.addSlide();
s.background = {color:WHT};
s.addText('Appendix: the full inventory', {x:0.55,y:0.42,w:10,h:0.75,fontFace:HF,fontSize:36,bold:true,color:INK,margin:0});
s.addText('Everything in the box today — the breadth a commissioned build would be quoted on.',
  {x:0.57,y:1.18,w:11,h:0.4,fontFace:BF,fontSize:14.5,italic:true,color:DIM,margin:0});
const inv=[
  ['ON THE COURSE',[
    'Live GPS front / center / back, 5-fix smoothing',
    '“Plays like” — elevation + live or manual wind',
    'Per-hole wind arrow, oriented to the shot',
    'Hazards & targets: reach/carry to every bunker, water, dogleg',
    'Carry arcs for the selected club ± neighbors',
    'Auto hole detection as you walk',
    'Ball-flight tracer: map arc, side profile, 3D flyover + stats',
    'Pin sheet: tap today’s pin — every number re-keys to it',
    'Tournament switch: one tap to legal raw yardages']],
  ['SCORING & YOUR GAME',[
    'Running strokes / putts / fairways strip',
    'Full 18-hole card with OUT/IN/total & GIR',
    'Round history: trend line, bests, last-5 averages',
    'Club distances learned from marked shots',
    'Club hints inside the plays-like readout',
    'Shot map: numbered dots + trail per hole',
    'One-tap GHIN posting helper',
    'Women’s par handled automatically from the Red tees']],
  ['CRAFT & PLATFORM',[
    '2-ft contours; fall-line arrows on every green',
    'Hypsometric terrain tint with hillshading',
    'NAIP aerial layer (SAT), geo-aligned',
    '3D terrain with adjustable exaggeration',
    'Three themes, incl. a bright-sunlight mode',
    'Offline PWA: home-screen install, wake lock',
    'No accounts, ads, or data collection',
    'A little hidden whimsy for those who explore']],
];
inv.forEach((c2,ci)=>{
  const x=0.55+ci*4.18;
  s.addText(c2[0],{x:x,y:1.8,w:3.9,h:0.35,fontFace:BF,fontSize:12,bold:true,charSpacing:2,color:ci===2?PINK:GRN,margin:0});
  s.addText(c2[1].map((t,i)=>({text:t,options:{bullet:{code:'2022',indent:10},breakLine:i<c2[1].length-1,paraSpaceAfter:7}})),
    {x:x,y:2.25,w:3.95,h:4.4,fontFace:BF,fontSize:10.5,color:'33463C',margin:0,valign:'top'});
});
s.addText('Full walkthrough: wbyc-user-guide.md ships with the app.',
  {x:0.57,y:6.72,w:11,h:0.3,fontFace:BF,fontSize:10,italic:true,color:DIM,margin:0});
s.addText('WBYC Rangefinder · a member-built proposal · 13',{x:0.55,y:7.08,w:6,h:0.3,fontFace:BF,fontSize:9,color:DIM,margin:0});

// ---------- S14 CLOSE ----------
s = pres.addSlide();
s.background = {path: P+'hero.png'};
s.addShape('rect',{x:0,y:0,w:13.33,h:7.5,fill:{color:'071F13',transparency:35}});
s.addText('The club in every member’s pocket.', {x:0.7,y:2.7,w:11.9,h:1.1,fontFace:HF,fontSize:44,bold:true,color:WHT,margin:0});
s.addText('One walkthrough on the first tee will make the case better than any slide. Shall we book it?',
  {x:0.72,y:3.9,w:9.8,h:0.7,fontFace:BF,fontSize:18,italic:true,color:PALE,margin:0});
s.addText([{text:'Kit Artig',options:{bold:true,color:WHT}},{text:'   ·   kit@kitartig.com',options:{color:PALE}}],
  {x:0.72,y:6.4,w:8,h:0.4,fontFace:BF,fontSize:15,margin:0});
s.addNotes('Close by offering a live demo round with the membership committee.');

pres.writeFile({fileName: P+'WBYC-Rangefinder-Pitch.pptx'}).then(()=>console.log('deck written'));
