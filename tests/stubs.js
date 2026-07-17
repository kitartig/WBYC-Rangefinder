// DOM-stub harness for wbyc-rangefinder — concatenate: stubs.js + <extracted app js> + tests.js
const CTX=new Proxy(function(){},{get:(t,k)=>k===Symbol.toPrimitive?()=>'':CTX,apply:()=>CTX,set:()=>true});
const elems={};
function mkEl(id){
  const cls=new Set();
  return {id,style:{},dataset:{},attrs:{},innerHTML:'',textContent:'',value:'',title:'',
    classList:{add:c=>cls.add(c),remove:c=>cls.delete(c),toggle:(c,f)=>{(f===undefined?!cls.has(c):f)?cls.add(c):cls.delete(c);},contains:c=>cls.has(c)},
    setAttribute(k,v){this.attrs[k]=v;},getAttribute(k){return this.attrs[k];},
    getBoundingClientRect:()=>({left:0,top:0,width:300,height:400}),
    addEventListener(){},setPointerCapture(){},appendChild(){},remove(){},focus(){},
    querySelectorAll:()=>[],getContext:()=>CTX,toDataURL:()=>'data:,',
    viewBox:{baseVal:{x:0,y:0,width:100,height:100}},clientWidth:300,clientHeight:400,width:0,height:0};
}
globalThis.document={
  getElementById:id=>elems[id]||(elems[id]=mkEl(id)),
  querySelector:sel=>elems[sel]||(elems[sel]=mkEl(sel)),
  querySelectorAll:()=>[],
  createElement:tag=>mkEl(tag+'_'+Math.random()),
  body:{className:'',style:{},classList:{add(){},remove(){},toggle(){},contains:()=>false},appendChild(){}},
  addEventListener(){},
};
globalThis.elems=elems;
const store={wbyc_prof:'on'};
globalThis.localStorage={getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=String(v);},removeItem:k=>{delete store[k];}};
globalThis.location={protocol:'file:',href:'file:///x'};
globalThis.navigator={geolocation:{watchPosition:()=>1,clearWatch(){}},clipboard:{writeText:async()=>{}},wakeLock:{request:async()=>({release:async()=>{}})}};
globalThis.window=globalThis;
globalThis.addEventListener=()=>{};
globalThis.requestAnimationFrame=()=>0;
globalThis.getComputedStyle=()=>({getPropertyValue:()=>'#000'});
globalThis.confirm=()=>true; globalThis.prompt=()=>null; globalThis.open=()=>{};
globalThis.devicePixelRatio=1;
