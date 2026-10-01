// Reproduce the reviewed gallery figures with Codex's bundled Artifact Tool runtime.
// Run from the repository root, with ARTIFACT_NODE_MODULES and FIGURE_PYTHON set.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {Figure} from '../skills/paper-figure/scripts/figure.mjs';
const root=process.cwd(), build=path.join(root,'.build/gallery-14-15');
await fs.mkdir(build,{recursive:true});
const books=JSON.parse(await fs.readFile('skills/paper-figure/assets/color-books.json','utf8')).books;
const version=process.argv[2]||'v1';
function setup(folder,bookId){
 const o=path.join(root,'output',folder),b=path.join(build,folder);
 return {o,b,book:books.find(x=>x.id===bookId)};
}
function primitives(f,n){
 const nodes={};
 const L=(id,t,x,y,w,h,opts={})=>{nodes[id]=t;return f.label(id,t,x,y,w,h,{size:12,color:n.ink,padY:0,...opts});};
 const B=(id,t,x,y,w,h,opts={})=>{if(t!==null)nodes[id]=t;return f.add(id,t,x,y,w,h,{fill:n.canvas,stroke:n.stroke,strokeWidth:.9,size:12,pad:0,padY:0,color:n.ink,...opts});};
 return {nodes,L,B};
}
async function save(f,b,nodes,edges,extra={}){
 await fs.mkdir(b,{recursive:true});
 await fs.writeFile(path.join(b,'contract.json'),JSON.stringify({slides:[{nodes,edges,groups:f.groups.map(g=>g.name),nativeOnly:!f.images.length,exactEdges:true}]},null,2));
 await fs.writeFile(path.join(b,'design.json'),JSON.stringify({width:f.width,height:f.height,images:f.images,...extra},null,2));
 const raw=path.join(b,`export-${version}.pptx`),candidate=path.join(b,`candidate-${version}.pptx`);
 await f.export(raw);
 const dedup=spawnSync(process.env.FIGURE_PYTHON||'python3',[path.join(root,'scripts/deduplicate-pptx-media.py'),raw,candidate],{encoding:'utf8'});
 if(dedup.status!==0)throw new Error(dedup.stderr||dedup.stdout);
 console.log(JSON.stringify({folder:path.basename(b),objects:f.objects.size,images:f.images.length}));
}
{
 const {o,b,book}=setup('gallery-masked-reconstruction-14','teal-coral'),n=book.neutral,c=book.colors;
 const task=JSON.parse(await fs.readFile(path.join(o,'content-contract.json'),'utf8'));
 const f=new Figure({width:672,height:420,title:task.title,notes:'Original illustrative MAE-inspired training schematic. The separately generated red-panda source is not experimental data. Predictions are symbolic native cells, not a reconstruction. Four of sixteen patches are visible. The twelve masked positions contribute to the loss. Full generated composition draft is not embedded. All explanatory text, masks, tokens, borders and arrows are native. Cropped pictures are independently replaceable. Intended width 177.8 mm.'});
 const {nodes,L,B}=primitives(f,n),photo=await fs.readFile(path.join(o,'assets/red-panda.png'));
 L('title',task.title,16,14,640,27,{size:19,bold:true,align:'left'});
 L('input-heading','Masked image',16,71,128,20,{bold:true});
 L('input-sub','4 × 4 patches',16,91,128,18,{color:n.secondary_text});
 L('gather-heading','Visible\npatches',160,72,64,37,{bold:true});
 L('latent-heading','Latents',290,83,45,20,{bold:true});
 L('restore-heading','Restore order',349,73,114,22,{bold:true});
 L('restore-sub','+ mask tokens',349,95,114,20,{size:11.5,color:n.secondary_text});
 L('prediction-heading','Predicted patches',535,75,131,20,{bold:true});
 L('prediction-sub','symbolic',535,97,131,18,{color:n.secondary_text});
 const crop=id=>{const row=Math.floor((id-1)/4),col=(id-1)%4;return {left:col/4,top:row/4,right:(3-col)/4,bottom:(3-row)/4};};
 const visible=new Set(task.visiblePatchIds);
 B('masked-field',null,16,120,128,128,{fill:'none',stroke:n.stroke,strokeWidth:1});
 for(let i=1;i<=16;i++){
  const x=16+((i-1)%4)*32,y=120+Math.floor((i-1)/4)*32;
  if(visible.has(i)){
   f.image(`input-photo-${i}`,photo,x,y,32,32,{crop:crop(i),alt:`Original image patch ${i}; row-major 4 by 4 partition.`});
   B(`input-id-bg-${i}`,null,x+1,y+17,18,14,{fill:'#FFFFFF',stroke:'none'});
   L(`input-id-${i}`,String(i),x+1,y+17,18,14,{size:11.5,bold:true});
  }else B(`input-mask-${i}`,'M',x,y,32,32,{fill:'#E3E5E7',stroke:'#FFFFFF',size:12.5,color:'#62696D'});
  B(`input-border-${i}`,null,x,y,32,32,{fill:'none',stroke:'#FFFFFF',strokeWidth:1.2});
 }
 B('gathered-patches',null,177,117,30,134,{fill:'none',stroke:'none'});
 for(const [j,i] of task.visiblePatchIds.entries()){
  const y=117+j*34.67;
  f.image(`gather-photo-${i}`,photo,177,y,30,30,{crop:crop(i),alt:`Selected image patch ${i}, same source crop as input.`});
  B(`gather-id-bg-${i}`,null,177,y+16,18,14,{fill:'#FFFFFF',stroke:'none'});
  L(`gather-id-${i}`,String(i),177,y+16,18,14,{size:11.5,bold:true});
 }
 B('encoder','Encoder',230,109,49,150,{fill:n.surface,stroke:n.stroke,strokeWidth:1.15,size:11.5});
 B('visible-latents',null,300,122,24,124,{fill:'none',stroke:'none'});
 for(const [j,i] of task.visiblePatchIds.entries())B(`latent-${i}`,String(i),300,122+j*33.33,24,24,{fill:c.teal.fill,stroke:c.teal.stroke,bold:true,color:c.teal.accent});
 B('restored-tokens',null,364,142,84,84,{fill:'none',stroke:n.stroke,strokeWidth:1});
 for(let i=1;i<=16;i++)B(`restore-${i}`,visible.has(i)?String(i):'M',364+((i-1)%4)*21,142+Math.floor((i-1)/4)*21,21,21,{fill:visible.has(i)?c.teal.fill:'#E3E5E7',stroke:'#FFFFFF',strokeWidth:1.1,size:11,color:visible.has(i)?c.teal.accent:'#62696D',bold:visible.has(i)});
 B('decoder','Decoder',474,138,47,92,{fill:n.surface,stroke:n.stroke,strokeWidth:1.15,size:11.3});
 B('predicted-patches',null,548,132,104,104,{fill:'none',stroke:c.coral.stroke,strokeWidth:1});
 for(let i=1;i<=16;i++)B(`prediction-${i}`,String(i),548+((i-1)%4)*26,132+Math.floor((i-1)/4)*26,26,26,{fill:c.coral.fill,stroke:'#FFFFFF',strokeWidth:1.1,size:12.5,color:c.coral.accent});
 const chain=['masked-field','gathered-patches','encoder','visible-latents','restored-tokens','decoder','predicted-patches'],edges=[];
 for(let i=0;i<chain.length-1;i++){f.connect(`forward-${i}`,chain[i],chain[i+1],{width:2.3,color:n.connector});edges.push([chain[i],chain[i+1]]);}
 L('visible-count','4 of 16 visible',16,255,128,18,{size:11.5,color:n.secondary_text});
 L('target-heading','Original target',16,294,96,20,{bold:true});
 B('target-image',null,28,318,72,72,{stroke:n.stroke,fill:'none'});
 f.image('target-photo',photo,28,318,72,72,{alt:'Intact original source image, supplied as the reconstruction target.'});
 B('masked-loss','Masked-patch loss',490,330,162,48,{fill:c.coral.fill,stroke:c.coral.stroke,strokeWidth:1.1,bold:true});
 f.connect('target-to-loss','target-image','masked-loss',{width:2,color:n.connector});edges.push(['target-image','masked-loss']);
 f.connect('prediction-to-loss','predicted-patches','masked-loss',{fromSide:'bottom',toSide:'top',kind:'elbow',width:2.3,color:c.coral.accent});edges.push(['predicted-patches','masked-loss']);
 L('target-route-label','Compare only the 12 masked positions',125,326,335,20,{size:12,color:n.secondary_text});
 L('prediction-route-label','Masked\npositions',454,283,108,34,{size:11.5,color:c.coral.accent,align:'right'});
 L('footer',task.requiredDisclosure,16,398,640,15,{size:10.8,color:n.secondary_text,align:'left'});
 await save(f,b,nodes,edges,{patchIds:task.visiblePatchIds,maskedCount:12});
}
{
 const {o,b,book}=setup('gallery-graph-pooling-15','blue-apricot'),n=book.neutral,c=book.colors;
 const task=JSON.parse(await fs.readFile(path.join(o,'content-contract.json'),'utf8'));
 const f=new Figure({width:672,height:390,title:task.title,notes:'Original illustrative hard-assignment pooling example inspired by DiffPool, which learns soft assignments. Eight nodes, eleven undirected edges, three clusters. Adjacency A has zero diagonal; S is one-hot. A′=SᵀAS has diagonal 6,6,2. Graph renders cross-cluster edges only; diagonal mass retained in matrix. No trained model result. Every visible object is native, including grouped text math (not OMML). Full composition draft not embedded. Intended width 177.8 mm.'});
 const {nodes,L,B}=primitives(f,n),hues=[c.blue,c.apricot,c.teal],letters=['A','B','C'],math=[];
 L('title',task.title,16,14,640,26,{size:19,bold:true,align:'left'});
 L('panel-a','(a) Original graph',12,249,234,21,{bold:true});
 L('panel-b','(b) Assignment S',263,249,150,21,{bold:true});
 L('panel-c','(c) Coarsened graph',447,249,215,21,{bold:true});
 // Irregular native hulls make membership visible without requiring color alone.
 f.path('hull-A',[[13,75],[34,57],[83,54],[110,66],[120,104],[105,134],[74,150],[35,139],[18,115]],{fill:c.blue.fill,color:'none',closed:true});
 f.path('hull-B',[[134,110],[173,90],[218,107],[237,139],[234,178],[208,195],[173,184],[143,168]],{fill:c.apricot.fill,color:'none',closed:true});
 f.path('hull-C',[[54,198],[99,185],[147,186],[173,211],[163,239],[101,246],[59,231]],{fill:c.teal.fill,color:'none',closed:true});
 const pos={1:[38,88],2:[91,88],3:[65,128],4:[169,125],5:[148,164],6:[211,166],7:[144,218],8:[79,218]};
 for(const [a,d] of task.undirectedEdges)f.path(`graph-edge-${a}-${d}`,[pos[a],pos[d]],{color:n.connector,width:1.5});
 for(const [j,letter] of letters.entries())for(const id of task.clusters[letter]){
  const [x,y]=pos[id];B(`node-${id}`,String(id),x-11,y-11,22,22,{geometry:'ellipse',fill:'#FFFFFF',stroke:hues[j].accent,strokeWidth:1.7,size:12.5});
 }
 L('cluster-A','A',58,58,25,21,{size:15,bold:true,color:c.blue.accent});
 L('cluster-B','B',195,100,25,21,{size:15,bold:true,color:c.apricot.accent});
 L('cluster-C','C',102,220,25,21,{size:15,bold:true,color:c.teal.accent});
 const sx=302,sy=69,cw=26,rh=21;
 B('assignment-field',null,sx,sy,cw*3,rh*8,{fill:'none',stroke:n.stroke,strokeWidth:1});
 for(let col=0;col<3;col++)L(`assignment-col-${col}`,letters[col],sx+col*cw,46,cw,20,{bold:true,color:hues[col].accent,size:13});
 for(let row=0;row<8;row++){
  L(`assignment-row-${row}`,String(row+1),278,sy+row*rh,20,rh,{size:12});
  for(let col=0;col<3;col++)B(`assignment-${row}-${col}`,String(task.assignmentMatrix[row][col]),sx+col*cw,sy+row*rh,cw,rh,{fill:task.assignmentMatrix[row][col]?hues[col].fill:'#FFFFFF',stroke:'#ADB3B9',strokeWidth:.6,bold:!!task.assignmentMatrix[row][col],size:12.5});
 }
 // Visible frame-free caption boxes act as process-edge anchors; all graph edges are undirected paths.
 B('input-anchor',null,12,58,227,190,{fill:'none',stroke:'none'});
 B('pool-anchor',null,464,65.5,180,175,{fill:'none',stroke:'none'});
 f.connect('explain-assignments','input-anchor','assignment-field',{width:2.5,color:n.connector});
 f.connect('explain-pooling','assignment-field','pool-anchor',{width:2.5,color:n.connector});
 const pp={A:[496,101],B:[616,101],C:[556,211]};
 for(const [edge,count] of Object.entries(task.pooledEdgeLabels)){
  const [a,d]=edge.split('-');f.path(`pooled-edge-${a}-${d}`,[pp[a],pp[d]],{color:n.connector,width:count===2?2.6:1.8});
 }
 L('pooled-count-AB','2',541,72,30,22,{size:15});
 L('pooled-count-AC','1',507,148,27,22,{size:15});
 L('pooled-count-BC','1',577,148,27,22,{size:15});
 for(const [j,letter] of letters.entries()){
  const [x,y]=pp[letter];B(`pooled-node-${letter}`,letter,x-22,y-22,44,44,{geometry:'ellipse',fill:hues[j].fill,stroke:hues[j].accent,strokeWidth:1.8,size:19,color:hues[j].accent});
 }
 f.path('lower-rule',[[16,282],[656,282]],{color:'#C5C9CE',width:.7});
 L('pooling-heading','Pool features and edges',16,297,220,20,{bold:true,align:'left'});
 // Native mathematical runs: T is placed explicitly as a superscript and remains editable.
 function equation(id,parts,x,y){
  const children=[],start=x;
  for(let i=0;i<parts.length;i++){
   const p=parts[i],z=p.sup?12.5:19,w=p.w,name=`${id}-${i}`;
   const sh=L(name,p.t,x,y+(p.sup?0:5),w+3,29,{align:'left',valign:'top'});
   sh.text.style={typeface:'Times New Roman',fontSize:z,color:n.ink,italic:p.italic??false,bold:false,alignment:'left',verticalAlignment:'top',autoFit:'none',wrap:'none',insets:{left:0,right:0,top:0,bottom:0}};
   x+=w;children.push(name);
  }
  f.group(id,children);math.push({name:id,expectedText:parts.map(p=>p.t).join(''),boundsPx:[start-1,y-1,x-start+5,34]});
 }
 equation('feature-equation',[{t:'X′',w:19,italic:true},{t:' = ',w:21},{t:'S',w:11,italic:true},{t:'T',w:9,sup:true},{t:'Z',w:12,italic:true}],16,322);
 equation('adjacency-equation',[{t:'A′',w:19,italic:true},{t:' = ',w:21},{t:'S',w:11,italic:true},{t:'T',w:9,sup:true},{t:'AS',w:27,italic:true}],128,322);
 L('definitions','A: adjacency   S: assignments   Z: node embeddings',16,358,342,17,{size:10.7,color:n.secondary_text,align:'left'});
 L('pooled-matrix-heading','Pooled adjacency',331,299,134,20,{bold:true,align:'left'});
 L('diagonal-note','Diagonal mass retained;\ngraph shows cross-cluster edges.',331,327,149,40,{size:10.7,color:n.secondary_text,align:'left'});
 const ax=520,ay=305,acw=38,arh=20;
 for(let col=0;col<3;col++)L(`adj-col-${col}`,letters[col],ax+col*acw,285,acw,20,{bold:true,color:hues[col].accent,size:12});
 for(let row=0;row<3;row++){
  L(`adj-row-${row}`,letters[row],ax-25,ay+row*arh,21,arh,{bold:true,color:hues[row].accent,size:12});
  for(let col=0;col<3;col++)B(`pooled-adj-${row}-${col}`,String(task.pooledAdjacency[row][col]),ax+col*acw,ay+row*arh,acw,arh,{fill:row===col?hues[row].fill:'#FFFFFF',stroke:'#ADB3B9',strokeWidth:.7,size:12.5});
 }
 L('footer',task.requiredDisclosure,16,376,640,14,{size:10.7,color:n.secondary_text,align:'left'});
 await save(f,b,nodes,[['input-anchor','assignment-field'],['assignment-field','pool-anchor']],{math,graphPositions:pos,pooledPositions:pp});
}
