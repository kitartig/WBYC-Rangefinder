// Assertions for wbyc-rangefinder (run: node run.js from tests/)
setTimeout(()=>{
  const A=(name,cond)=>{ if(!cond){ console.error('FAIL:',name); process.exitCode=1; } else console.log('ok:',name); };
  try{
    setDemo(true); render();
    const map=()=>elems['map'].innerHTML;
    // flat-map flight arc + stats
    A('flat arc rendered', map().includes('class="flight"'));
    A('arc gradient present', map().includes('arcgrad'));
    A('arc stats rendered', map().includes('class="fstat"') && map().includes(' yds</text>'));
    A('arc apex stat present', map().includes('apex '));
    A('apex dot + leader', map().includes('flight-apex'));
    A('ground shadow kept', map().includes('stroke="var(--accent)"'));
    // profile inset
    const prof=elems['profile'];
    A('profile visible', prof.classList.contains('on'));
    A('profile terrain', prof.innerHTML.includes('pterr'));
    A('profile trajectory', prof.innerHTML.includes('parc'));
    A('profile yardage label', / yds/.test(prof.innerHTML));
    elems['.dist .box.center'].onclick();
    A('profile toggles off', !elems['profile'].classList.contains('on'));
    elems['.dist .box.center'].onclick();
    A('profile toggles back on', elems['profile'].classList.contains('on'));
    // green view: fine contours, small arrows, no arc
    elems['grnBtn'].onclick();
    A('1-ft fine contours render in green view', map().includes('ctrf'));
    A('fall arrows present', map().includes('class="fall"'));
    A('no arc in green view', !map().includes('class="flight"'));
    elems['grnBtn'].onclick();
    // SAT
    elems['satBtn'].onclick();
    A('vib filter defined', map().includes('id="vib"'));
    elems['grnBtn'].onclick();
    A('gclip in SAT green view', map().includes('gclip'));
    elems['grnBtn'].onclick(); elems['satBtn'].onclick();
    // green tees (4/2026 card)
    A('5 tee sets loaded', course.tees.length===5 && course.tees[4].name==='Green' && course.tees[4].total_yardage===4779);
    A('every hole has a Green box', course.holes.every(h2=>h2.tee_boxes.some(tb2=>tb2.name==='Green')));
    A('estimates flagged', course.holes.filter(h2=>h2.tee_boxes.find(tb2=>tb2.name==='Green').estimated).length===15);
    A('h5 red re-pinned to card 290', (()=>{const h5=course.holes[4],rd=h5.tee_boxes.find(t=>t.name==='Red');return rd.estimated===true && Math.abs(yds({lat:rd.lat,lng:rd.lng},h5.green.center)-290)<3;})());
    A('red h10 updated', course.holes[9].tee_boxes.find(tb2=>tb2.name==='Red').yardage===260);
    (()=>{ const t0=tee; tee='Green'; holeIdx=0; render();
      A('green tee: womens par', elems['holeMeta'].innerHTML.includes('Par 5'));
      A('green tee: green hcp', elems['holeMeta'].innerHTML.includes('Hcp 1'));
      A('green tee: card yardage', elems['holeMeta'].innerHTML.includes('360 yds'));
      tee=t0; render(); })();
    // player name
    globalThis.prompt=()=>' Kit ';
    elems['pname'].onclick();
    A('name saves trimmed', pname==='Kit');
    A('scorecard signed', elems['scTitle'].textContent==='KIT — SCORECARD');
    globalThis.prompt=()=>null;
    // export/import + no-plus-strokes
    A('CARD shows gross not vs-par', (()=>{ const h=hole(); card.holes[holeIdx]={s:6,p:2,f:true}; renderScore(); return elems['scTotV'].textContent===6 || elems['scTotV'].textContent==='6'; })());
    A('export wired', typeof elems['scExport'].onclick==='function');
    A('import wired', typeof elems['scImport'].onclick==='function');
    (()=>{ let dl=''; const oCreate=document.createElement;
      document.createElement=t2=>{ const el=oCreate(t2); if(t2==='a'){ el.click=()=>{dl='clicked';}; } return el; };
      globalThis.Blob=class{constructor(a){this.a=a;}}; globalThis.URL={createObjectURL:()=>'blob:x',revokeObjectURL(){}};
      elems['scExport'].onclick(); document.createElement=oCreate;
      A('export produces a download', dl==='clicked'); })();
    // live-GPS tap immunity
    (()=>{ demo=false; pos={lat:course.holes[0].green.center.lat+0.001,lng:course.holes[0].green.center.lng}; render();
      const svg=mapTransform.svg; svg.getBoundingClientRect=()=>({left:0,top:0,width:300,height:400});
      mapTap({clientX:150,clientY:200});
      A('live GPS tap does not enter demo', demo===false);
      pos=null; })();
    // waiting ball when GPS on, no fix
    (()=>{ demo=false; pos=null; render();
      A('waiting ball shown (GPS on, no fix)', elems['map'].innerHTML.includes('you-search'));
      A('no FW button in strip', !elems['map'] || document.getElementById('fwBtn').innerHTML===''); })();
    // far-fix shows centered marker not off-screen ball
    (()=>{ demo=false; pos={lat:0,lng:0}; render(); // 0,0 is nowhere near WBYC
      A('far GPS shows searching marker', elems['map'].innerHTML.includes('patiently waiting for you!') && elems['map'].innerHTML.includes('you-search'));
      A('no off-screen gold ball when far', !elems['map'].innerHTML.includes('you-glow'));
      pos=null; })();
    // weather flourish
    (()=>{ weather={code:61,day:true}; demo=true; render();
      A('weather flourish (rain) renders', elems['map'].innerHTML.includes('wx-rain'));
      weather={code:0,day:true}; render();
      A('weather flourish (sun) renders', elems['map'].innerHTML.includes('sunglint'));
      weather={code:null,day:true}; render(); })();
    // far fix blanks distances (no 4-digit couch readout)
    (()=>{ demo=false; pos={lat:0,lng:0}; render();
      A('far fix blanks CENTER distance', elems['dCenter'].textContent==='–');
      pos=null; })();
    // demo ball snaps to the selected tee (so Red reads the Red yardage)
    (()=>{ setDemo(true); holeIdx=4; const t0=tee;
      tee='Blue'; snapDemo(); render(); const blue=+elems['dCenter'].textContent;
      tee='Red'; snapDemo(); render(); const red=+elems['dCenter'].textContent;
      A('demo: Red tee reads ~290 (card), not Blue distance', Math.abs(red-290)<6 && blue>red+80);
      tee=t0; holeIdx=0; render(); })();
    // GPS toggle label
    setDemo(false); A('GPS toggle reads ON when live', elems['demoBtn'].textContent==='GPS ON');
    setDemo(true); A('GPS toggle reads OFF in manual', elems['demoBtn'].textContent==='GPS OFF');
    setDemo(true); // leave in demo for remaining tests
    // pin sheet
    (()=>{ const h=hole(), gf=h.green.front;
      freshPins(); pins.p[h.hole_number]={lat:gf.lat,lng:gf.lng}; savePins(); render();
      A('pin sheet: label flips to PIN', elems['dCLbl'].textContent==='PIN');
      A('pin flag drawn', map().includes('pinflag'));
      A('center dist re-keys to pin', elems['dCenter'].textContent===elems['dFront'].textContent);
      open3D();
      const fw=D3.flagWorld, pw=D3.mesh.toWorld(gf);
      A('3D flag moves to pin', Math.hypot(fw[0]-pw[0],fw[1]-pw[1])<1);
      close3D();
      delete pins.p[h.hole_number]; savePins(); render();
      A('pin clears back to CENTER', elems['dCLbl'].textContent==='CENTER');
    })();
    // pinch zoom
    A('map base exported', Array.isArray(mapTransform.base) && mapTransform.base.length===4);
    (()=>{ const bw=mapTransform.base[2];
      mapZoom={k:2, cx:mapTransform.base[0]+bw/2, cy:mapTransform.base[1]+mapTransform.base[3]/2};
      applyMapZoom();
      A('pinch halves the viewBox', Math.abs(parseFloat(elems['map'].attrs['viewBox'].split(' ')[2])-bw/2)<0.2);
      mapZoom={k:1.0}; applyMapZoom();
      A('snap-back restores full hole', Math.abs(parseFloat(elems['map'].attrs['viewBox'].split(' ')[2])-bw)<0.2 && mapZoom===null);
    })();
    // 3D tracer + mesh
    open3D();
    A('tracer built', !!D3.tracer && D3.tracer.pts.length===49);
    (()=>{ const p0=D3.tracer.pts[0], p1=D3.tracer.pts[48], mid=D3.tracer.pts[24];
      A('tracer apex above chord', mid[2] > (p0[2]+p1[2])/2 + 3);
      A('tracer spans tee to green', Math.hypot(p1[0]-p0[0],p1[1]-p0[1]) > 100); })();
    A('tracer stats computed', !!D3.tracer.stats && D3.tracer.stats.yds>50 && D3.tracer.stats.apexFt>10);
    A('tracer apexI sane', D3.tracer.apexI>20 && D3.tracer.apexI<40);
    A('mesh has no NaN gaps', !Array.from(D3.mesh.zs).some(isNaN));
    A('filled mask exported', !!D3.mesh.filled);
    A('edge map built', !!D3.mesh.edge && Object.keys(D3.mesh.edge).length>50);
    A('draped outlines built', Array.isArray(D3.mesh.outlines) && D3.mesh.outlines.length>1);
    A('toWorld exposed', typeof D3.mesh.toWorld==='function');
    draw3D();
    A('draw3D with tracer ok', true);
    A('d3Trace wired', typeof elems['d3Trace'].onclick==='function');
    elems['d3Trace'].onclick();
    A('replay restarts tracer', !!D3.tracer);
    close3D();
    A('close clears tracer', D3.tracer===null);
    // The Bear's Log keepsake generates from real round data
    (()=>{ card.holes[0]={s:3,p:1,f:true}; card.holes[6]={s:2,p:1,f:null}; card.holes[1]={s:5,p:2,f:false};
      const r=blBuild();
      A('bearlog builds from a round', !r.empty && r.html.includes("The Bear's Log") && r.html.includes('The Score') && r.html.includes('bl-strip'));
      A('bearlog notes a birdie', r.html.includes('Birdie on the'));
      openBearLog();
      A('bearlog opens', elems['bearlog'].classList.contains('open'));
      A('bearlog has a memento note field', typeof elems['blNote'].onclick==='function');
      elems['blClose'].onclick(); A('bearlog closes', !elems['bearlog'].classList.contains('open'));
    })();
    // self-writing memory line from past rounds
    (()=>{ const save=rounds.slice(); rounds.length=0;
      const p0=course.holes[0].par, p1=course.holes[1].par;
      rounds.push({date:'2026-06-01', tee:'White', holes:Array.from({length:18},(_,i)=>({s:i===0?p0-1:i===1?p1+1:0,p:0,f:null}))});
      holeIdx=0; render();
      A('memory surfaces a past birdie', elems['holeMemory'].classList.contains('on') && /birdied/i.test(elems['holeMemory'].textContent));
      A('memory marked good', elems['holeMemory'].classList.contains('good'));
      holeIdx=1; render();
      A('memory shows last-time on a played hole', /Last time here/.test(elems['holeMemory'].textContent));
      holeIdx=5; render();
      A('memory hidden with no history', !elems['holeMemory'].classList.contains('on'));
      rounds.length=0; save.forEach(r=>rounds.push(r)); holeIdx=0; render();
    })();
    // map-pinned memories: arm, place via a tap, render a star, remove via a tap
    (()=>{ setDemo(true); holeIdx=0; memories.length=0; render();
      const h0=course.holes[0], spot={lat:h0.green.center.lat+0.0002, lng:h0.green.center.lng};
      const svg=mapTransform.svg; svg.getBoundingClientRect=()=>({left:0,top:0,width:300,height:400});
      // place: arm, then a scripted prompt supplies the note
      memArm=true;
      // tap somewhere on the map — unrot maps client point to a lat/lng near the hole
      mapTap({clientX:150,clientY:150});
      // the note is now captured by an in-app sheet, not window.prompt()
      // the star once armed silently: a white ring on a white border, so the button
    // looked dead. Assert the class the CSS hangs the armed look on, not just the flag.
    A('star button arms, and says so in a class the CSS can see', (()=>{
      memArm=false; elems['memBtn'].classList.remove('on');
      elems['memBtn'].onclick();
      return memArm===true && elems['memBtn'].classList.contains('on');
    })());
    A('star button disarms on a second tap', (()=>{
      elems['memBtn'].onclick();
      return memArm===false && !elems['memBtn'].classList.contains('on');
    })());
    // a card left open from an earlier day used to keep claiming that date
    A('an untouched card from an earlier day re-dates itself', (()=>{
      staleAsked=false; card=blankCard(); card.start='2020-01-01';
      const r=staleCardChecked();
      return r===true && card.start===today();
    })());
    A('a scored card from an earlier day banks when confirmed', (()=>{
      staleAsked=false; const before=rounds.length;
      card=blankCard(); card.start='2020-01-01'; card.holes[0]={s:5,p:2,f:null};
      globalThis.confirm=()=>true;
      staleCardChecked();
      return rounds.length===before+1 && card.start===today() && !card.holes.some(e=>e.s>0);
    })());
    A('declining keeps the old card exactly as it was', (()=>{
      staleAsked=false; const before=rounds.length;
      card=blankCard(); card.start='2020-01-01'; card.holes[0]={s:5,p:2,f:null};
      globalThis.confirm=()=>false;
      staleCardChecked();
      const kept = rounds.length===before && card.start==='2020-01-01' && card.holes[0].s===5;
      globalThis.confirm=()=>true; card=blankCard();
      return kept;
    })());
    A('today() is the LOCAL date, not UTC', (()=>{
      const d=new Date();
      const local=`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
      return today()===local;
    })());
    A('a new card is stamped with the local date', blankCard().start===today());
    A('tap opens the memory sheet', elems['rfMemSheet'].classList.contains('open'));
      A('nothing written before the sheet is confirmed', memories.length===0);
      A('memory disarms after placing', memArm===false);
      elems['rfMemText'].value='chip-in from the fringe';
      rfCommitMemory();
      A('memory placed on commit', memories.length===1 && memories[0].h===h0.hole_number && /chip-in/.test(memories[0].note));
      A('sheet closes after commit', !elems['rfMemSheet'].classList.contains('open'));
      // cancelling discards
      memArm=true; mapTap({clientX:150,clientY:150});
      elems['rfMemText'].value='discard me'; rfCloseMemorySheet();
      A('cancel writes nothing', memories.length===1);
      // it renders as a star on this hole
      render(); A('memory star drawn on its hole', elems['map'].innerHTML.includes('mem-star'));
      // not shown on a different hole
      holeIdx=2; render(); A('memory hidden on other holes', !elems['map'].innerHTML.includes('mem-star'));
      // remove: tap near it with confirm=true
      holeIdx=0; render();
      const q=mapTransform, before=memories.length;
      // place a second one at a known spot then tap it to remove
      globalThis.confirm=()=>true;
      memories.push({h:1,lat:spot.lat,lng:spot.lng,note:'x',date:'2026-07-20'});
      // tap AT that memory: find its screen coords via rot is internal — instead assert removal path by proximity using its own latlng
      const m=memories[memories.length-1]; mapTransform.unrot=()=>({lat:m.lat,lng:m.lng});
      mapTap({clientX:10,clientY:10});
      A('memory removed on tap+confirm', memories.length===before);
      memories.length=0; globalThis.prompt=()=>null; render();
    })();
    // keepsake photographs: add, cap, remove, and a quota failure that must not be silent
    (()=>{ const day='2026-07-27';
      localStorage.removeItem(RF_PHOTO_KEY);
      A('photo added', rfAddPhoto('data:image/jpeg;base64,AAA', day)==='ok');
      A('photo stored against the round', (rfLoadPhotos()[day]||[]).length===1);
      while((rfLoadPhotos()[day]||[]).length < RF_CAP) rfAddPhoto('data:,x', day);
      A('per-round cap enforced', (rfLoadPhotos()[day]||[]).length===RF_CAP);
      A('cap refuses further photos', rfAddPhoto('data:,y', day)==='cap');
      rfRemovePhoto(0, day);
      A('photo removed', (rfLoadPhotos()[day]||[]).length===RF_CAP-1);
      const realSet=localStorage.setItem;
      localStorage.setItem=()=>{ throw new Error('QuotaExceededError'); };
      A('quota failure is reported, never silent', rfAddPhoto('data:,z', day)==='full');
      localStorage.setItem=realSet;
      localStorage.removeItem(RF_PHOTO_KEY);
    })();
  }catch(e){ console.error('THROW:', e); process.exitCode=1; }
  process.exit();
}, 80);
