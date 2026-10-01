import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Figure} from '../scripts/figure.mjs';
import {artifact,python} from '../scripts/runtime.mjs';
const {PresentationFile,FileBlob}=await artifact();
const base=path.dirname(fileURLToPath(import.meta.url));
const dest=path.resolve(process.argv[2]||'output/refined');
const work=path.resolve(process.argv[3]||'.build/refined');
await fs.mkdir(dest,{recursive:true});await fs.mkdir(work,{recursive:true});
const tasks=JSON.parse(await fs.readFile(path.join(base,'tasks.json'),'utf8'));
const photo=new Uint8Array(await fs.readFile(path.join(base,'../assets/astronaut.png')));
const C={ink:'#253540',muted:'#66737B',line:'#C6CED1',blue:'#487F98',pale:'#E6F0F4',green:'#497665',greenPale:'#E8F0EB',warm:'#BD7854',warmPale:'#F6ECE4',gray:'#EFF2F3',white:'#FFFFFF'};
const refs='Design study: MAE https://arxiv.org/abs/2111.06377; CLIP https://arxiv.org/abs/2103.00020; U-Net https://arxiv.org/abs/1505.04597; Transformer https://arxiv.org/abs/1706.03762. Original examples, not reproductions.';
const make=title=>new Figure({width:672,height:400,title,notes:refs+'\nOriginal schematic demonstration. Values, signals and patterns are illustrative, not measured results. Publication width 177.8 mm. NASA astronaut photo via scikit-image, public domain: https://scikit-image.org/docs/stable/api/skimage.data#skimage.data.astronaut'});
const label=(f,id,t,x,y,w,h=21,o={})=>f.label(id,t,x,y,w,h,{size:12,color:C.ink,...o});
const title=(f,t)=>label(f,'heading',t,18,9,638,23,{size:15,bold:true,align:'left'});
const line=(f,id,p,o={})=>f.path(id,p,{color:C.line,width:.8,...o});
const box=(f,id,t,x,y,w,h,o={})=>f.module(id,t,x,y,w,h,{fill:C.white,stroke:C.blue,size:13,strokeWidth:1,...o});
const data=(f,id,t,x,y,w,h,o={})=>f.add(id,t,x,y,w,h,{fill:'none',stroke:'none',size:12,valign:'bottom',padY:0,...o});
const footer=(f,t)=>label(f,'disclosure',t,18,375,636,18,{size:11,color:C.muted,align:'left'});
function vector(f,id,x,y,vals,{cell=10,gap=2,height=37,color=C.blue}={}){
 const ids=[];vals.forEach((v,i)=>{const n=id+'.'+i;f.add(n,null,x+i*(cell+gap),y,cell,height,{fill:C.gray,stroke:'none'});f.add(n+'.value',null,x+i*(cell+gap),y+height*(1-v),cell,Math.max(1,height*v),{fill:color,stroke:'none'});ids.push(n,n+'.value');});f.group(id,ids);
}
function doc(f,id,x,y,w=52,h=68,{fill=C.white,accent=C.blue,tag=''}={}){
 const ids=[];const put=(s,...args)=>{f.add(id+s,...args);ids.push(id+s);};
 put('.sheet',null,x,y,w,h,{fill,stroke:C.line,strokeWidth:.8});
 Array.from({length:Math.min(4,Math.floor((h-18)/8))},(_,i)=>i).forEach(i=>put('.line'+i,null,x+7,y+15+i*8,w-14-(i%2)*7,2,{fill:i===1?accent:'#C9D1D5',stroke:'none'}));
 if(tag){label(f,id+'.tag',tag,x+4,y+1,w-8,14,{size:10,bold:true});ids.push(id+'.tag');}f.group(id,ids);
}
function plane(f,id,x,y,w,h,{layers=3,color=C.blue,fill=C.pale,grid=0}={}){
 const ids=[];for(let i=layers-1;i>=0;i--){const n=id+'.plane'+i;f.add(n,null,x+i*5,y-i*4,w,h,{fill,stroke:color,strokeWidth:.8});ids.push(n);}
 if(grid){for(let i=1;i<grid;i++){line(f,id+'.v'+i,[[x+w*i/grid,y],[x+w*i/grid,y+h]],{color,width:.4});line(f,id+'.h'+i,[[x,y+h*i/grid],[x+w,y+h*i/grid]],{color,width:.4});ids.push(id+'.v'+i,id+'.h'+i);}}
 f.group(id,ids);
}
function pattern(f,id,x,y,size,kind,{color=C.blue,n=5}={}){
 const ids=[];for(let r=0;r<n;r++)for(let c=0;c<n;c++){
 const on=kind===0?r===2:kind===1?c===2:kind===2?(r===2||c===2):((r===0||r===n-1)&&(c>0&&c<n-1))||((c===0||c===n-1)&&(r>0&&r<n-1));
 const k=id+'.'+r+'.'+c;f.add(k,null,x+c*size/n,y+r*size/n,size/n-.5,size/n-.5,{fill:on?color:'#EDF1F2',stroke:'none'});ids.push(k);}
 f.group(id,ids);
}
function signal(f,id,x,y,w,h,{irregular=false,color=C.blue,band=false}={}){
 line(f,id+'.axis',[[x,y+h],[x+w,y+h]],{color:C.line});
 const ys=[.58,.47,.25,.31,.67,.82,.60,.29,.19,.37,.54];const ts=irregular?[0,.07,.16,.21,.38,.43,.58,.73,.79,.92,1]:ys.map((_,i)=>i/(ys.length-1));
 const pts=ys.map((v,i)=>[x+w*ts[i],y+h*v]);
 if(band){f.path(id+'.band',[...pts.map(p=>[p[0],p[1]-6]),...pts.toReversed().map(p=>[p[0],p[1]+6])],{fill:C.pale,color:'none',width:0,closed:true});}
 if(!irregular)line(f,id+'.curve',pts,{color,width:1.5});
 pts.forEach((p,i)=>{if(irregular)line(f,id+'.err'+i,[[p[0],p[1]-5-(i%3)*2],[p[0],p[1]+5+(i%3)*2]],{color:'#BBCBD2',width:1});f.add(id+'.p'+i,null,p[0]-2,p[1]-2,4,4,{geometry:'ellipse',fill:color,stroke:'none'});});
}
const builders={
'01-process':()=>{
 const f=make('Confidence-aware retrieval');title(f,'Confidence-aware retrieval');
 f.add('rerank-focus',null,281,54,171,285,{fill:'#F5F8F7',stroke:'none'});
 data(f,'query','Query',18,99,86,78,{bold:true});label(f,'query-example','Which evidence\nsupports the claim?',18,91,86,52,{size:12});
 box(f,'retrieve','Retrieve',131,117,112,43);box(f,'rerank','Rerank',295,111,143,55,{fill:C.greenPale,stroke:C.green,bold:true});
 data(f,'answer','Answer',474,99,91,78,{bold:true});label(f,'answer-snippet','Claim … [d₂]',474,113,91,28,{size:12});
 data(f,'evidence','Evidence',592,99,64,78,{bold:true});
 [['query','retrieve'],['retrieve','rerank'],['rerank','answer'],['answer','evidence']].forEach(([a,b],i)=>f.connect('e'+i,a,b,{width:2.6}));
 doc(f,'candidate-back',159,195,54,70,{tag:'dₖ'});doc(f,'candidate-mid',149,201,54,70,{tag:'d₂'});doc(f,'candidate-front',139,207,54,70,{tag:'d₁'});
 label(f,'candidate-label','k candidates',131,283,112,23,{color:C.muted});
 label(f,'score-cols','relevance r   confidence c',291,179,151,23,{size:11,color:C.muted});
 ['d₁','d₂','dₖ'].forEach((d,i)=>{label(f,'rank-row'+i,d,300,207+i*27,24,22,{size:12});f.add('r'+i,null,332,214+i*27,[27,38,16][i],7,{fill:C.blue,stroke:'none'});f.add('c'+i,null,389,214+i*27,[34,23,15][i],7,{fill:C.warm,stroke:'none'});});
 label(f,'formula','s = αr + (1 − α)c',292,302,149,25,{size:13});
 doc(f,'answer-sheet',489,206,62,80,{accent:C.green,tag:'answer'});doc(f,'evidence-sheet',598,109,48,36,{tag:'d₂'});
 label(f,'evidence-tag','linked\nsource',589,206,68,40,{color:C.muted});
 footer(f,'Schematic candidate features and document snippets; bar lengths are illustrative.');return f;
},
'02-branch':()=>{
 const f=make('Local detail and global context');title(f,'Local detail and global context');
 data(f,'input','Input',18,118,118,146,{bold:true});f.image('input-photo',photo,18,118,118,118);
 f.add('local-roi',null,52,123,38,41,{fill:'none',stroke:C.warm,strokeWidth:1.7});
 box(f,'local','Local encoder',254,114,132,43,{fill:C.warmPale,stroke:C.warm});box(f,'global','Global encoder',254,279,132,43,{fill:C.pale});
 f.image('detail-photo',photo,272,49,60,60,{crop:{left:.29,top:.025,right:.38,bottom:.63},fit:'cover'});
 f.image('context-photo',photo,272,214,60,60);
 label(f,'detail-label','fine detail',336,68,68,21,{size:11,color:C.warm});label(f,'context-label','scene context',336,233,85,21,{size:11,color:C.blue});
 f.connect('e0','input','local',{kind:'elbow',toSide:'left',color:C.warm});f.connect('e1','input','global',{kind:'elbow',color:C.blue});

 box(f,'fuse','Fuse',492,161,60,54,{fill:C.greenPale,stroke:C.green,bold:true});
 data(f,'prediction','Prediction',588,145,68,92);vector(f,'output-vector',598,158,[.3,.8,.5,.6],{cell:10,height:48,color:C.green});
 f.connect('e2','local','fuse',{kind:'elbow',color:C.warm});f.connect('e3','global','fuse',{kind:'elbow',color:C.blue});f.connect('e4','fuse','prediction');
 label(f,'fusion-note','complementary\nrepresentations',448,244,112,40,{size:11,color:C.muted});
 footer(f,'Illustrative features. Photo: NASA / scikit-image, public domain.');return f;
},
'03-repeat':()=>{
 const f=make('Residual refinement');title(f,'Residual refinement: state sequence and one block');
 ['h₀','h₁','h₂','h₃','h₄'].forEach((t,i)=>{vector(f,'state'+i,28+i*133,53,[.35+i*.08,.75-i*.04,.4+i*.06,.6],{cell:13,height:39,color:i===4?C.green:C.blue});label(f,'state-name'+i,t,34+i*133,99,49,21);if(i<4){line(f,'stage-line'+i,[[94+i*133,75],[147+i*133,75]],{color:C.muted,width:1});f.path('stage-arrow'+i,[[147+i*133,75],[141+i*133,72],[141+i*133,78]],{fill:C.muted,color:'none',closed:true});label(f,'theta'+i,'θ'+['₁','₂','₃','₄'][i],104+i*133,78,35,18,{size:11,color:C.muted});}});
 f.panel('block','Refinement block  × 4',153,150,365,200,{fill:'#F7F9FA',stroke:C.line});
 data(f,'input','h₀',22,247,66,75);vector(f,'input-state',24,252,[.4,.8,.5,.6],{cell:12,height:36});
 box(f,'norm','Norm',187,264,86,42);box(f,'mix','Mix',309,264,88,42,{fill:C.greenPale,stroke:C.green});
 box(f,'add','+',449,215,34,34,{size:22,stroke:C.ink});
 data(f,'output','h₄',582,207,67,75);vector(f,'output-state',585,212,[.7,.65,.72,.68],{cell:12,height:36,color:C.green});
 f.connect('e0','input','norm',{kind:'elbow'});f.connect('e1','norm','mix');f.connect('e2','mix','add',{kind:'elbow',toSide:'bottom'});f.connect('e3','add','output');f.connect('residual','input','add',{width:1.7,kind:'elbow',fromSide:'top',toSide:'left',color:C.muted,dashed:true});
 label(f,'identity','identity',82,183,64,22,{size:11,color:C.muted});label(f,'recurrence','hₜ₊₁ = hₜ + Mixθₜ(Norm(hₜ))',198,319,288,22,{size:13});
 footer(f,'Same block structure; separate parameters. State glyphs are schematic.');return f;
},
'04-skip':()=>{
 const f=make('Multi-scale restoration');title(f,'Multi-scale restoration');
 data(f,'e1','Encode 1',35,57,106,137,{bold:true});plane(f,'e1-features',39,72,80,100,{grid:4});
 data(f,'e2','Encode 2',175,204,86,88,{bold:true});plane(f,'e2-features',194,215,40,50,{grid:3});
 data(f,'core','Bottleneck',288,288,108,65,{bold:true});plane(f,'core-features',325,297,20,25,{layers:4,color:C.muted,fill:'#E9ECEE'});
 data(f,'d2','Decode 2',416,204,86,88,{bold:true});plane(f,'d2-features',434,215,40,50,{grid:3,color:C.green,fill:C.greenPale});
 data(f,'d1','Decode 1',548,57,106,137,{bold:true});plane(f,'d1-features',552,72,80,100,{grid:4,color:C.green,fill:C.greenPale});
 f.connect('down1','e1','e2',{kind:'elbow',fromSide:'bottom',toSide:'left',color:C.blue});f.connect('down2','e2','core',{kind:'elbow',fromSide:'bottom',toSide:'left',color:C.blue});f.connect('up2','core','d2',{kind:'elbow',toSide:'bottom',color:C.green});f.connect('up1','d2','d1',{kind:'elbow',toSide:'bottom',color:C.green});
 f.connect('skip1','e1','d1',{width:1.7,color:C.warm,dashed:true});f.connect('skip2','e2','d2',{width:1.7,color:C.warm,dashed:true});
 label(f,'scale1','H × W',38,38,92,21,{color:C.muted});label(f,'scale2','H/2 × W/2',168,179,105,22,{color:C.muted});label(f,'scale3','H/4 × W/4',285,351,113,21,{color:C.muted});
 label(f,'skip1-label','high-resolution skip',241,101,179,22,{color:C.warm});label(f,'skip2-label','coarse skip',280,224,124,21,{color:C.warm});
 label(f,'stack-key','Stacked planes: feature channels\nPlane size: spatial resolution',263,51,210,42,{size:12,color:C.muted});
 footer(f,'Channel counts are unspecified; repeated planes indicate a feature stack, not a count.');return f;
},
'05-panels':()=>{
 const f=make('Cross-modal correspondence');
 label(f,'a-title','(a) Paired visual and text representations',18,10,345,23,{size:13,bold:true,align:'left'});label(f,'b-title','(b) Pairwise correspondence',386,10,269,23,{size:14,bold:true,align:'left'});line(f,'divider',[[369,45],[369,348]]);
 data(f,'image','Image',20,57,116,111,{bold:true});[0,1,2,3].forEach(i=>pattern(f,'sample'+i,23+(i%2)*53,60+Math.floor(i/2)*42,35,i));
 data(f,'text','Text',20,232,116,115,{bold:true});['horizontal','vertical','cross','ring'].forEach((t,i)=>label(f,'caption'+i,t,22,231+i*22,112,20,{size:12,align:'left',color:C.warm}));
 box(f,'image-encoder','Vision\nencoder',172,83,100,60,{fill:C.pale});box(f,'text-encoder','Text\nencoder',172,253,100,60,{fill:C.warmPale,stroke:C.warm});f.connect('vision','image','image-encoder');f.connect('language','text','text-encoder',{color:C.warm});
 vector(f,'vision-embedding',302,84,[.8,.3,.7,.5],{cell:9,height:56});vector(f,'text-embedding',302,254,[.6,.7,.3,.8],{cell:9,height:56,color:C.warm});
 label(f,'image-notation','I₁ … I₄',290,149,61,22);label(f,'text-notation','T₁ … T₄',289,319,66,22,{color:C.warm});
 label(f,'x-label','Text embeddings',442,56,192,24,{color:C.warm});label(f,'y-label','Image\nembeddings',373,179,65,50,{size:11,color:C.blue});
 const ids=[];for(let r=0;r<4;r++)for(let c=0;c<4;c++){const n='scores.'+r+'.'+c;f.add(n,r===c?'I'+['₁','₂','₃','₄'][r]+'·T'+['₁','₂','₃','₄'][c]:'I'+['₁','₂','₃','₄'][r]+'·T'+['₁','₂','₃','₄'][c],455+c*45,119+r*45,43,43,{fill:r===c?'#DDECF2':'#F2F4F4',stroke:'none',size:11.5,color:r===c?C.blue:C.muted});ids.push(n);}f.group('scores',ids);
 for(let i=0;i<4;i++){label(f,'row'+i,'I'+['₁','₂','₃','₄'][i],433,129+i*45,20,22,{color:C.blue});label(f,'col'+i,'T'+['₁','₂','₃','₄'][i],464+i*45,92,28,22,{color:C.warm});}
 label(f,'matching-note','Sᵢⱼ = Iᵢ · Tⱼ  ·  matched pairs on the diagonal',390,316,264,33,{size:12});footer(f,'Illustrative pattern–text pairs; the matrix encodes correspondence, not measured similarity.');return f;
},
'06-tokens':()=>{
 const f=make('Selective token aggregation');title(f,'Selective token aggregation');
 label(f,'selection-heading','(a) Preserve token identity through selection',18,40,636,24,{bold:true,size:13,align:'left'});
 const tokens=[];for(let i=0;i<6;i++){let x=25+i*31,y=91;const n='tokens.'+i;f.add(n,String(i+1),x,y,26,53,{fill:[1,4].includes(i)?'#E7E9EA':C.pale,stroke:[1,4].includes(i)?'#B8C0C4':C.blue,size:12,valign:'bottom'});tokens.push(n);for(let j=0;j<3;j++){f.add(n+'.v'+j,null,x+4+j*6,y+8,4,[11,18,13][(j+i)%3],{fill:[1,4].includes(i)?'#C1C8CC':C.blue,stroke:'none'});tokens.push(n+'.v'+j);}}f.group('tokens',tokens);
 data(f,'token-port','',23,91,187,53);box(f,'select','Select',262,92,107,51,{fill:C.greenPale,stroke:C.green});f.connect('selection','token-port','select');
 label(f,'mask-note','2 and 5 omitted',25,151,182,24,{color:C.muted});
 const kept=[];[1,3,4,6].forEach((t,i)=>{const n='kept.'+i;f.add(n,String(t),424+i*53,91,43,53,{fill:C.pale,stroke:C.blue,size:12,valign:'bottom'});kept.push(n);for(let j=0;j<3;j++){f.add(n+'.v'+j,null,432+i*53+j*8,99,5,[11,18,13][(j+t-1)%3],{fill:C.blue,stroke:'none'});kept.push(n+'.v'+j);}});f.group('kept',kept);
 data(f,'kept-port','',422,91,207,53);f.connect('retained','select','kept-port');
 line(f,'detail-divider',[[18,188],[654,188]]);label(f,'weighted-title','(b) Form a weighted summary',18,204,345,23,{bold:true,size:13,align:'left'});
 const weights=[];['.5','.2','.2','.1'].forEach((v,i)=>{const n='weights.0.'+i;f.add(n,v,48+i*81,310,46,30,{fill:C.warmPale,stroke:'none',size:13});weights.push(n);vector(f,'weighted-vector'+i,47+i*81,258,[.35+.1*i,.8-.1*i,.5,.65],{cell:9,height:34});label(f,'selected-name'+i,'v'+['₁','₃','₄','₆'][i],52+i*81,235,38,20,{size:12,color:C.blue});});f.group('weights',weights);
 data(f,'weight-port','',40,247,340,96);box(f,'aggregate','Aggregate',446,268,112,54,{fill:C.greenPale,stroke:C.green});
 f.connect('token-edge','kept-port','aggregate',{fromSide:'bottom',toSide:'top',kind:'straight',color:C.blue});f.connect('weights-edge','weight-port','aggregate',{width:1.7,color:C.warm});
 box(f,'summary','z',605,271,48,48,{fill:C.pale,size:20});f.connect('summary-edge','aggregate','summary');
 label(f,'aggregation-equation','z = Σᵢ wᵢvᵢ',437,336,135,23,{size:14});label(f,'normalization','Σᵢ wᵢ = 1',165,344,119,23,{size:13,color:C.warm});footer(f,'Vector glyphs are schematic. Retained positions and normalized weights are specified by the brief.');return f;
},
'07-long-label':()=>{
 const f=make('Uncertainty-conditioned temporal alignment');title(f,'Uncertainty-conditioned temporal alignment');
 data(f,'observations','Irregularly sampled\nobservations',18,62,168,139,{bold:true});signal(f,'observed',28,70,149,77,{irregular:true});
 box(f,'alignment','Uncertainty-conditioned\ntemporal alignment',235,101,218,67,{fill:C.greenPale,stroke:C.green,bold:true,size:13});
 data(f,'representation','Aligned\nrepresentation',504,62,150,139,{bold:true});signal(f,'aligned',513,72,132,74,{band:true});
 f.connect('e0','observations','alignment');f.connect('e1','alignment','representation');
 box(f,'metadata','Sampling intervals + confidence',222,289,245,39,{fill:C.warmPale,stroke:C.warm,size:12});f.connect('context','metadata','alignment',{width:1.7,fromSide:'top',toSide:'bottom',color:C.warm});
 label(f,'source-grid','irregular time support',21,219,162,21,{size:11,color:C.muted});label(f,'target-grid','common time support',500,219,155,21,{size:11,color:C.muted});
 const from=[27,39,69,78,108,146,179],to=[509,531,553,575,597,619,641];from.forEach((x,i)=>{line(f,'input-tick'+i,[[x,247],[x,255]],{color:C.blue,width:1});line(f,'output-tick'+i,[[to[i],247],[to[i],255]],{color:C.blue,width:1});});
 label(f,'dt','Δt₁   Δt₂       Δt₃',28,270,157,21,{size:11,color:C.warm});label(f,'confidence','confidence cᵢ',36,315,132,21,{size:11,color:C.warm});
 [14,26,20,32,16].forEach((v,i)=>f.add('confidence-bar'+i,null,55+i*18,311-v,10,v,{fill:'#DBB49B',stroke:'none'}));
 label(f,'support-caption','alignment depends on both timing and confidence',482,283,173,58,{size:12,color:C.muted});footer(f,'Illustrative observations and uncertainty; no measured reconstruction performance is shown.');return f;
},
'08-train-infer':()=>{
 const f=make('Training and inference');
 label(f,'train-heading','(a) Training · supervision updates the parameters',18,10,639,24,{bold:true,size:14,align:'left'});line(f,'phase-divider',[[18,218],[654,218]]);
 data(f,'train-x','Sample x',21,61,114,95,{bold:true});signal(f,'training-sample',27,63,100,54,{irregular:true});
 box(f,'train-model','Model fθ',189,75,132,63,{fill:C.pale,bold:true});
 box(f,'loss','Loss',405,151,77,46,{fill:C.warmPale,stroke:C.warm,bold:true});
 data(f,'target','Target y',529,104,124,98,{bold:true});signal(f,'target-values',537,110,108,51,{color:C.warm});
 f.connect('train-forward','train-x','train-model');f.connect('objective','train-model','loss',{kind:'elbow',toSide:'top'});f.connect('supervision','target','loss',{width:1.7,fromSide:'left',toSide:'right',color:C.warm});
 f.connect('gradient','loss','train-model',{width:1.9,fromSide:'left',toSide:'bottom',kind:'elbow',color:C.warm,dashed:true});label(f,'update-label','update θ',306,195,88,20,{size:12,color:C.warm});
 label(f,'infer-heading','(b) Inference · apply the learned mapping',18,230,639,23,{bold:true,size:14,align:'left'});
 data(f,'infer-x','New x',21,270,114,87,{bold:true});signal(f,'new-sample',27,271,100,47,{irregular:true});box(f,'infer-model','Model fθ',189,281,132,57,{fill:C.pale,bold:true});
 data(f,'prediction','Prediction ŷ',481,267,173,91,{bold:true});signal(f,'inference-pred',495,268,144,51,{band:true,color:C.green});
 f.connect('infer-forward','infer-x','infer-model');f.connect('infer-output','infer-model','prediction');label(f,'fixed','fixed parameters',184,341,146,24,{size:12,color:C.muted});
 footer(f,'Illustrative signals, not model outputs. Inference uses no target or parameter-update path.');return f;
}
};
const skill=process.env.PRESENTATIONS_SKILL_DIR;if(!skill)throw new Error('Set PRESENTATIONS_SKILL_DIR');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const only=process.env.FIGURE_ONLY;
for(const [id,build] of Object.entries(builders)){
 if(only&&!only.split(',').includes(id))continue;
 const f=build(),candidate=path.join(work,id+'.pptx'),final=path.join(dest,id+'.pptx');await f.export(candidate);
 await finalizePresentation({workspaceDir:path.resolve('.'),candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu',`${672*9525},${400*9525}`],explicitTotalSlideCount:1,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:path.join(work,id+'.validation.json')});
 const p=await PresentationFile.importPptx(await FileBlob.load(final));await fs.writeFile(path.join(dest,id+'.png'),new Uint8Array(await (await p.export({slide:p.slides.items[0],format:'png',scale:2})).arrayBuffer()));
 const contract=structuredClone(tasks[id].contract);if(id==='02-branch')contract.nativeOnly=false;
 await fs.writeFile(path.join(dest,id+'.contract.json'),JSON.stringify({slides:[contract]},null,2));console.log(id+' refined and finalized');
}
