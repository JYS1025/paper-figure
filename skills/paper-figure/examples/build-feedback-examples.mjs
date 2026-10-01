import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Figure} from '../scripts/figure.mjs';
import {python} from '../scripts/runtime.mjs';

const dest=path.resolve(process.argv[2]||'output/feedback-revision');
const work=path.resolve(process.argv[3]||'.build/feedback-revision/candidate');
await fs.mkdir(dest,{recursive:true});await fs.mkdir(work,{recursive:true});
const C={ink:'#253540',muted:'#66737B',line:'#C6CED1',blue:'#487F98',pale:'#E6F0F4',green:'#497665',greenPale:'#E8F0EB',warm:'#BD7854',warmPale:'#F6ECE4',gray:'#EFF2F3',white:'#FFFFFF'};
const make=t=>new Figure({width:672,height:400,title:t,notes:'Original schematic examples. The visible grouping, ports and identity markers reflect the supplied review. No empirical results are shown. Publication width 177.8 mm. Input briefs: examples/tasks.json. Reference study: https://arxiv.org/abs/2111.06377 ; https://arxiv.org/abs/2103.00020 ; https://arxiv.org/abs/1505.04597 ; https://arxiv.org/abs/1706.03762 .'});
const label=(f,id,t,x,y,w,h=21,o={})=>f.label(id,t,x,y,w,h,{size:12,color:C.ink,...o});
const title=(f,t)=>label(f,'heading',t,18,9,638,23,{size:15,bold:true,align:'left'});
const line=(f,id,p,o={})=>f.path(id,p,{color:C.line,width:.8,...o});
const box=(f,id,t,x,y,w,h,o={})=>f.module(id,t,x,y,w,h,{fill:C.white,stroke:C.blue,size:13,strokeWidth:1,...o});
const frame=(f,id,x,y,w,h,color=C.line)=>f.add(id,null,x,y,w,h,{fill:'none',stroke:color,strokeWidth:.8});
const footer=(f,t)=>label(f,'disclosure',t,18,375,636,18,{size:10.5,color:C.muted,align:'left'});

function vector(f,id,x,y,vals,{cell=10,gap=2,height=37,color=C.blue}={}){
 const ids=[];vals.forEach((v,i)=>{const n=id+'.'+i;f.add(n,null,x+i*(cell+gap),y,cell,height,{fill:C.gray,stroke:'none'});f.add(n+'.value',null,x+i*(cell+gap),y+height*(1-v),cell,Math.max(1,height*v),{fill:color,stroke:'none'});ids.push(n,n+'.value');});f.group(id,ids);
}
function pattern(f,id,x,y,size,kind,color=C.blue){
 const n=5,ids=[];
 for(let r=0;r<n;r++)for(let c=0;c<n;c++){
  const on=kind===0?r===2:kind===1?c===2:kind===2?(r===2||c===2):kind===3?((r===0||r===4)&&(c>0&&c<4))||((c===0||c===4)&&(r>0&&r<4)):kind===4?r+c===4:Math.abs(r-2)+Math.abs(c-2)===2;
  const k=id+'.'+r+'.'+c;f.add(k,null,x+c*size/n,y+r*size/n,size/n-.35,size/n-.35,{fill:on?color:C.gray,stroke:'none'});ids.push(k);
 }f.group(id,ids);
}
function feature(f,id,x,y,w,h,{color=C.blue,fill=C.pale,layers=3,grid=4}={}){
 const ids=[];
 for(let i=layers-1;i>0;i--){const n=id+'.back'+i;f.add(n,null,x+i*5,y-i*4,w,h,{fill,stroke:color,strokeWidth:.8});ids.push(n);}
 // The connected node is exactly the visible front plane, not a label box.
 f.add(id,null,x,y,w,h,{fill,stroke:color,strokeWidth:1});ids.push(id);
 for(let i=1;i<grid;i++){const a=id+'.v'+i,b=id+'.h'+i;line(f,a,[[x+w*i/grid,y],[x+w*i/grid,y+h]],{color,width:.4});line(f,b,[[x,y+h*i/grid],[x+w,y+h*i/grid]],{color,width:.4});ids.push(a,b);}
 if(ids.length>1)f.group(id+'.features',ids);
}

const builders={
 '03-repeat':()=>{
  const f=make('Residual refinement');title(f,'Residual refinement: state sequence and one block');
  ['h₀','h₁','h₂','h₃','h₄'].forEach((t,i)=>{
   vector(f,'state'+i,28+i*133,53,[.35+i*.08,.75-i*.04,.4+i*.06,.6],{cell:13,height:39,color:i===4?C.green:C.blue});label(f,'state-name'+i,t,34+i*133,99,49,21);
   if(i<4){line(f,'stage-line'+i,[[94+i*133,75],[147+i*133,75]],{color:C.muted,width:1});f.path('stage-arrow'+i,[[147+i*133,75],[141+i*133,72],[141+i*133,78]],{fill:C.muted,color:'none',closed:true});label(f,'theta'+i,'θ'+['₁','₂','₃','₄'][i],104+i*133,78,35,18,{size:11,color:C.muted});}
  });
  frame(f,'detail-target',92,64,59,34,C.blue);
  line(f,'detail-guide',[[121.5,98],[121.5,133],[334,133],[334,150]],{color:C.blue,width:.9,dashed:true});
  f.panel('block','One block, repeated × 4',153,150,365,200,{fill:'#F7F9FA',stroke:C.line});
  frame(f,'input',24,251,56,46,C.blue);vector(f,'input-state',28,256,[.4,.8,.5,.6],{cell:10,height:36});label(f,'input-name','hₜ',26,301,52,22);
  f.add('fork',null,122,272,4,4,{fill:C.ink,stroke:'none'});
  box(f,'norm','Norm',187,253,86,42);box(f,'mix','Mix',309,253,88,42,{fill:C.greenPale,stroke:C.green});
  box(f,'add','+',449,212,34,34,{size:22,stroke:C.ink});
  frame(f,'output',585,206,56,46,C.green);vector(f,'output-state',589,211,[.7,.65,.72,.68],{cell:10,height:36,color:C.green});label(f,'output-name','hₜ₊₁',585,260,56,22);
  f.connect('input-fork','input','fork',{width:1.8,arrowWidth:'sm',arrowLength:'sm'});
  f.connect('e0','fork','norm');f.connect('e1','norm','mix');f.connect('e2','mix','add',{kind:'elbow',toSide:'bottom'});f.connect('e3','add','output');
  f.connect('residual','fork','add',{width:1.7,kind:'elbow',fromSide:'top',toSide:'left',color:C.muted,dashed:true});
  label(f,'identity','identity',192,207,80,20,{size:11,color:C.muted});
  label(f,'recurrence','hₜ₊₁ = hₜ + Mixθₜ(Norm(hₜ))',198,315,288,23,{size:13});
  footer(f,'Four applications, separate parameters θ₁…θ₄. The inset shows one application; states are schematic.');
  return f;
 },
 '04-skip':()=>{
  const f=make('Multi-scale restoration');title(f,'Multi-scale restoration');
  feature(f,'e1',39,99,80,80);feature(f,'e2',194,220,40,40,{grid:3});feature(f,'core',327,310,20,20,{layers:4,grid:0,color:C.muted,fill:'#E9ECEE'});
  feature(f,'d2',434,220,40,40,{grid:3,color:C.green,fill:C.greenPale});feature(f,'d1',552,99,80,80,{color:C.green,fill:C.greenPale});
  for(const [id,t,x,y,w] of [['e1','Encode 1',22,70,116],['e2','Encode 2',163,192,112],['core','Bottleneck',283,279,108],['d2','Decode 2',400,192,112],['d1','Decode 1',531,70,121]])label(f,id+'-label',t,x,y,w,22,{bold:true});
  f.connect('down1','e1','e2',{kind:'elbow',fromSide:'bottom',toSide:'left',color:C.blue});f.connect('down2','e2','core',{kind:'elbow',fromSide:'bottom',toSide:'left',color:C.blue});
  f.connect('up2','core','d2',{kind:'elbow',toSide:'bottom',color:C.green});f.connect('up1','d2','d1',{kind:'elbow',toSide:'bottom',color:C.green});
  f.connect('skip1','e1','d1',{width:1.7,color:C.warm,dashed:true});f.connect('skip2','e2','d2',{width:1.7,color:C.warm,dashed:true});
  // Distinct visible entry sites do not assert an unspecified merge operator.
  for(const [id,x,y,c] of [['d1-skip-port',552,138,C.warm],['d1-main-port',591,177,C.green],['d2-skip-port',434,239,C.warm],['d2-main-port',453,258,C.green]])f.add(id,null,x,y,2,2,{fill:c,stroke:'none'});
  label(f,'scale1','H × W',38,45,92,21,{color:C.muted});label(f,'scale2','H/2 × W/2',167,168,105,22,{color:C.muted});label(f,'scale3','H/4 × W/4',284,340,113,21,{color:C.muted});
  label(f,'skip1-label','high-resolution skip',239,112,179,22,{color:C.warm});label(f,'skip2-label','coarse skip',271,213,124,21,{color:C.warm});
  label(f,'stack-key','Plane size: spatial resolution\nStacking: feature channels',230,45,244,44,{size:12,color:C.muted});
  footer(f,'Two decoder inputs are shown separately. Merge operator and channel counts are unspecified.');return f;
 },
 '05-panels':()=>{
  const f=make('Cross-modal correspondence');
  label(f,'a-title','(a) Paired representations',18,10,328,23,{size:14,bold:true,align:'left'});label(f,'b-title','(b) Pairwise correspondence',371,10,283,23,{size:14,bold:true,align:'left'});
  frame(f,'text',18,70,120,86,C.warm);label(f,'text-label','Text',22,158,112,21,{bold:true});
  ['horizontal','vertical','cross','ring'].forEach((t,i)=>{pattern(f,'caption-key'+i,24,77+i*18,12,i,C.warm);label(f,'caption'+i,t,42,72+i*18,93,21,{size:11.5,align:'left',color:C.warm});});
  frame(f,'image',18,218,120,96,C.blue);label(f,'image-label','Image',22,319,112,21,{bold:true});
  [0,1,2,3].forEach(i=>pattern(f,'sample'+i,34+(i%2)*49,225+Math.floor(i/2)*43,34,i));
  box(f,'text-encoder','Text\nencoder',168,86,100,54,{fill:C.warmPale,stroke:C.warm});box(f,'image-encoder','Vision\nencoder',168,239,100,54,{fill:C.pale});
  f.connect('language','text','text-encoder',{color:C.warm});f.connect('vision','image','image-encoder',{color:C.blue});
  label(f,'x-label','Text embeddings',438,63,208,23,{color:C.warm});label(f,'y-label','Image\nembeddings',283,210,98,42,{size:11,color:C.blue});
  frame(f,'text-axis',438,94,208,38,C.warm);frame(f,'image-axis',391,164,40,192,C.blue);
  f.connect('text-axis-flow','text-encoder','text-axis',{color:C.warm});f.connect('image-axis-flow','image-encoder','image-axis',{color:C.blue,kind:'elbow'});
  const rows=[],cols=[],scores=[];
  for(let i=0;i<4;i++){
   const sub=['₁','₂','₃','₄'][i];
   f.add('col'+i,'T'+sub,438+i*52,94,51,38,{fill:C.warmPale,stroke:C.warm,strokeWidth:.5,size:12,pad:0});cols.push('col'+i);
   pattern(f,'col-key'+i,442+i*52,105,11,i,C.warm);
   f.add('row'+i,'I'+sub,391,164+i*48,40,46,{fill:C.pale,stroke:C.blue,strokeWidth:.5,size:11.5,pad:0,valign:'bottom'});rows.push('row'+i);
   pattern(f,'row-key'+i,405,169+i*48,12,i,C.blue);
   // Header-to-column correspondence is alignment, not a new computation.
   line(f,'column-guide'+i,[[464+i*52,134],[464+i*52,160]],{color:C.warm,width:.7});
  }
  f.group('row-embeddings',rows);f.group('column-embeddings',cols);
  for(let r=0;r<4;r++)for(let c=0;c<4;c++){
   const n='scores.'+r+'.'+c,diag=r===c;
   f.add(n,'I'+['₁','₂','₃','₄'][r]+'·T'+['₁','₂','₃','₄'][c],438+c*52,164+r*48,50,46,{fill:diag?'#DDECF2':'#F5F6F6',stroke:diag?C.ink:'#D9E0E2',strokeWidth:diag?1.3:.4,size:11.5,color:diag?C.ink:C.muted,pad:0,bold:diag});scores.push(n);
  }f.group('scores',scores);
  label(f,'matching-note','Sᵢⱼ = Iᵢ · Tⱼ',176,325,144,24,{size:13});
  footer(f,'Illustrative item patterns. Outlined diagonal cells mark paired items, not measured similarity.');return f;
 },
 '06-tokens':()=>{
  const f=make('Selective token aggregation');title(f,'Selective token aggregation');
  label(f,'selection-heading','(a) Preserve token identity through selection',18,40,636,24,{bold:true,size:13,align:'left'});
  frame(f,'token-port',23,87,188,61,C.line);
  const tokens=[];
  for(let i=0;i<6;i++){
   const x=25+i*31,n='tokens.'+i,masked=[1,4].includes(i);
   f.add(n,String(i+1),x,91,26,53,{fill:masked?'#E7E9EA':C.pale,stroke:masked?'#B8C0C4':C.blue,size:12,valign:'bottom'});tokens.push(n);
   pattern(f,n+'.key',x+4,99,18,i,masked?'#B4BFC5':C.blue);
  }f.group('tokens',tokens);
  box(f,'select','Select',262,92,107,51,{fill:C.greenPale,stroke:C.green});f.connect('selection','token-port','select');
  label(f,'mask-note','2 and 5 omitted',25,151,182,24,{color:C.muted});
  frame(f,'kept-port',418,80,218,75,C.blue);const kept=[];
  [1,3,4,6].forEach((t,i)=>{const n='kept.'+i,x=424+i*53;f.add(n,String(t),x,91,43,53,{fill:C.pale,stroke:C.blue,size:12,valign:'bottom'});kept.push(n);pattern(f,n+'.key',x+12,99,18,t-1);});f.group('kept',kept);
  f.connect('retained','select','kept-port');
  line(f,'detail-divider',[[18,188],[654,188]]);label(f,'weighted-title','(b) Form a weighted summary',18,204,345,23,{bold:true,size:13,align:'left'});
  frame(f,'weight-port',28,236,370,112,C.warm);const weights=[];
  ['.5','.2','.2','.1'].forEach((v,i)=>{
   const x=40+i*86,t=[1,3,4,6][i],n='weights.0.'+i;
   frame(f,'weighted-pair'+i,x,245,62,94,C.line);
   pattern(f,'selected-key'+i,x+10,248,12,t-1);label(f,'selected-name'+i,'v'+['₁','₃','₄','₆'][i],x+26,241,29,22,{size:12,color:C.blue});
   vector(f,'weighted-vector'+i,x+9,268,[.35+.1*i,.8-.1*i,.5,.65],{cell:9,height:31});
   f.add(n,v,x+8,307,46,27,{fill:C.warmPale,stroke:'none',size:13});weights.push(n);
  });f.group('weights',weights);
  box(f,'aggregate','Aggregate',471,265,112,54,{fill:C.greenPale,stroke:C.green});
  f.connect('token-edge','kept-port','aggregate',{fromSide:'bottom',toSide:'top',color:C.blue});
  f.connect('weights-edge','weight-port','aggregate',{width:1.7,color:C.warm});
  box(f,'summary','z',613,268,40,48,{fill:C.pale,size:20});f.connect('summary-edge','aggregate','summary');
  label(f,'aggregation-equation','z = Σᵢ wᵢvᵢ',460,337,135,23,{size:14});label(f,'normalization','Σᵢ wᵢ = 1',154,348,119,23,{size:13,color:C.warm});
  footer(f,'Patterns identify tokens. Each lower frame pairs vᵢ with wᵢ; feature bars are schematic.');return f;
 }
};

// Requirements are authored from the supplied brief/review, before drawing.
const contracts={
 '03-repeat':{nodes:{'state-name0':'h₀','state-name4':'h₄','input-name':'hₜ','output-name':'hₜ₊₁',norm:'Norm',mix:'Mix',add:'+', 'block.title':'One block, repeated × 4'},edges:[['input','fork'],['fork','norm'],['norm','mix'],['mix','add'],['add','output'],['fork','add']]},
 '04-skip':{nodes:{'e1-label':'Encode 1','e2-label':'Encode 2','core-label':'Bottleneck','d2-label':'Decode 2','d1-label':'Decode 1',scale1:'H × W',scale2:'H/2 × W/2',scale3:'H/4 × W/4'},edges:[['e1','e2'],['e2','core'],['core','d2'],['d2','d1'],['e1','d1'],['e2','d2']]},
 '05-panels':{nodes:{'image-label':'Image','text-label':'Text','image-encoder':'Vision\nencoder','text-encoder':'Text\nencoder','x-label':'Text embeddings','y-label':'Image\nembeddings'},edges:[['image','image-encoder'],['text','text-encoder'],['image-encoder','image-axis'],['text-encoder','text-axis']],groups:['scores','row-embeddings','column-embeddings']},
 '06-tokens':{nodes:{select:'Select',aggregate:'Aggregate',summary:'z','tokens.1':'2','tokens.4':'5','kept.0':'1','kept.1':'3','kept.2':'4','kept.3':'6','weights.0.0':'.5','weights.0.1':'.2','weights.0.2':'.2','weights.0.3':'.1'},edges:[['token-port','select'],['select','kept-port'],['kept-port','aggregate'],['weight-port','aggregate'],['aggregate','summary']],groups:['tokens','kept','weights']}
};
const skill=process.env.PRESENTATIONS_SKILL_DIR;if(!skill)throw new Error('Set PRESENTATIONS_SKILL_DIR');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
for(const [id,build] of Object.entries(builders)){
 if(process.env.FIGURE_ONLY&&!process.env.FIGURE_ONLY.split(',').includes(id))continue;
 const contract={slides:[contracts[id]]};await fs.writeFile(path.join(work,id+'.contract.json'),JSON.stringify(contract,null,2));
 const f=build(),candidate=path.join(work,id+'.pptx'),final=path.join(dest,id+'.pptx');await f.export(candidate);
 await finalizePresentation({workspaceDir:path.resolve('.'),candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','6400800,3810000'],explicitTotalSlideCount:1,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:path.join(work,id+'.validation.json')});
 await fs.copyFile(path.join(work,id+'.contract.json'),path.join(dest,id+'.contract.json'));console.log(id+' finalized');
}
