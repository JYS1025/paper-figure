// Port regression fixtures. These exercise geometry, not the image-first workflow.
import fs from 'node:fs/promises';
import path from 'node:path';
import {Figure} from '../../ports/claude/paper-figure/scripts/figure.mjs';
const out=path.resolve(process.argv[2]);await fs.mkdir(out,{recursive:true});
const f=new Figure({width:1200,height:650,title:'Port geometry regression'});
const cases=[
 ['right','left',[40,40],[220,110]],['left','right',[220,40],[40,110]],
 ['bottom','top',[40,40],[220,110]],['top','bottom',[40,110],[220,40]],
 ['right','top',[40,40],[220,110]],['bottom','left',[40,40],[220,110]],
 ['left','bottom',[220,110],[40,40]],['top','right',[220,110],[40,40]],
];
const edges=[];
cases.forEach(([fromSide,toSide,a,b],i)=>{
 const dx=i%4*300,dy=Math.floor(i/4)*220;
 f.module(`a${i}`,fromSide,a[0]+dx,a[1]+dy,55,32);
 f.module(`b${i}`,toSide,b[0]+dx,b[1]+dy,55,32);
 f.connect(`edge${i}`,`a${i}`,`b${i}`,{kind:'elbow',fromSide,toSide});edges.push([`a${i}`,`b${i}`]);
});
f.module('a8','Source',280,460,55,32);f.module('b8','Target',40,535,55,32);
f.connect('edge8','a8','b8',{fromSide:'left',toSide:'right'});edges.push(['a8','b8']);
const bytes=await fs.readFile(new URL('../../ports/claude/paper-figure/assets/astronaut.png',import.meta.url));
f.image('contain',bytes,390,480,100,50);
f.image('cover',bytes,540,480,100,50,{fit:'cover'});
f.image('crop',bytes,690,480,100,50,{fit:'stretch',crop:{left:.1,right:.2,top:.15,bottom:.25}});
await f.export(path.join(out,'geometry.pptx'),{contract:{slides:[{nodes:{a8:'Source',b8:'Target'},edges,exactEdges:true,nativeOnly:false}]}});
const checks=[];
for(const [name,fn] of [
 ['duplicate name',()=>f.label('a8','Duplicate',0,0,20,20)],
 ['group collision',()=>{f.group('g',['a0','b0']);f.label('g','Duplicate',0,0,20,20);}],
 ['overlapping group',()=>f.group('other',['a0','b1'])],
 ['duplicate group member',()=>f.group('dup',['a1','a1'])],
 ['bad crop',()=>f.image('bad',bytes,0,0,10,10,{crop:{left:.6,right:.6,top:0,bottom:0}})],
 ['picture endpoint',()=>f.connect('bad','contain','a8')],
 ['unsupported route',()=>f.connect('bad','a8','b8',{kind:'elbow',fromSide:'right',toSide:'left'})],
]){let rejected=false;try{fn();}catch{rejected=true;}if(!rejected)throw new Error(`Negative control failed: ${name}`);checks.push(name);}
try{await f.export(path.join(out,'geometry.pptx'));throw new Error('Overwrite was allowed');}catch(e){if(!e.message.startsWith('Output exists:'))throw e;checks.push('overwrite');}
await fs.writeFile(path.join(out,'creation-negatives.json'),JSON.stringify(checks,null,2));
console.log(JSON.stringify({fixture:path.join(out,'geometry.pptx'),negativeChecks:checks.length}));
