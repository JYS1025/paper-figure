import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Figure,palette as C} from '../scripts/figure.mjs';
import {artifact,python} from '../scripts/runtime.mjs';
const {PresentationFile,FileBlob}=await artifact();
const base=path.dirname(fileURLToPath(import.meta.url));
const dest=path.resolve(process.argv[2]||'output/examples');
const work=path.resolve(process.argv[3]||'.build/examples');
await fs.mkdir(dest,{recursive:true});await fs.mkdir(work,{recursive:true});
const tasks=JSON.parse(await fs.readFile(path.join(base,'tasks.json'),'utf8'));
const fig=title=>new Figure({title,notes:'Original synthetic methodology example; no empirical result is asserted. Canvas: 177.8 × 95.25 mm. Layout choices are illustrative.'});
const tag=(f,t)=>f.label('caption',t,24,13,624,25,{align:'left',size:16,bold:true});
const note=(f,id,t,x,y,w=200)=>f.label(id,t,x,y,w,25,{size:12,color:C.muted});
const builders={
  '01-process':()=>{
    const f=fig('Confidence-aware retrieval');tag(f,'Confidence-aware retrieval');
    f.module('query','Query',24,135,80,54,{fill:C.gray,stroke:C.grayLine});
    f.module('retrieve','Retrieve',143,135,105,54);
    f.module('rerank','Rerank',288,125,125,74,{fill:C.green,stroke:C.greenLine,bold:true});
    f.module('answer','Answer',454,135,91,54,{fill:C.orange,stroke:C.orangeLine});
    f.module('evidence','Evidence',579,135,74,54,{size:12,fill:C.gray,stroke:C.grayLine});
    [['query','retrieve'],['retrieve','rerank'],['rerank','answer'],['answer','evidence']].forEach(([a,b],i)=>f.connect('e'+i,a,b));
    note(f,'retrieved-note','k candidates',126,198,140);note(f,'ranked-note','confidence-weighted score',266,211,166);
    f.label('formula','s = αr + (1 − α)c',251,248,199,35,{size:17});
    return f;
  },
  '02-branch':()=>{
    const f=fig('Two-view feature fusion');tag(f,'Two-view feature fusion');
    f.module('input','Input',24,156,85,52,{fill:C.gray,stroke:C.grayLine});
    f.module('local','Local encoder',185,86,145,55);
    f.module('global','Global encoder',185,222,145,55,{fill:C.purple,stroke:C.purpleLine});
    f.module('fuse','Fuse',414,156,96,52,{fill:C.green,stroke:C.greenLine,bold:true});
    f.module('prediction','Prediction',565,156,88,52,{fill:C.orange,stroke:C.orangeLine,size:12});
    f.connect('e0','input','local',{kind:'elbow',toSide:'left'});f.connect('e1','input','global',{kind:'elbow'});
    f.connect('e2','local','fuse',{kind:'elbow'});f.connect('e3','global','fuse',{kind:'elbow'});f.connect('e4','fuse','prediction');
    note(f,'local-note','fine detail',186,59,144);note(f,'global-note','scene context',186,282,144);
    return f;
  },
  '03-repeat':()=>{
    const f=fig('Residual refinement');tag(f,'Residual refinement');
    f.panel('block','Refinement block  × 4',177,70,323,243,{fill:'#F8FAFC'});
    f.module('input','h₀',29,172,69,54,{fill:C.gray,stroke:C.grayLine});
    f.module('norm','Norm',211,210,88,50);
    f.module('mix','Mix',333,210,87,50,{fill:C.green,stroke:C.greenLine});
    f.module('add','+',445,120,38,38,{fill:C.white,stroke:C.ink,size:20});
    f.module('output','h₄',568,112,72,54,{fill:C.orange,stroke:C.orangeLine});
    f.connect('e0','input','norm',{kind:'elbow'});f.connect('e1','norm','mix');f.connect('e2','mix','add',{kind:'elbow',toSide:'bottom'});f.connect('e3','add','output');
    f.connect('residual','input','add',{kind:'elbow',fromSide:'top',toSide:'left',color:C.muted,dashed:true});
    note(f,'identity','identity',89,107,80);note(f,'share-note','Same block structure; separate parameters',186,278,304);
    return f;
  },
  '04-skip':()=>{
    const f=fig('Multi-scale restoration');tag(f,'Multi-scale restoration');
    f.module('e1','Encode 1',33,77,106,51);f.module('e2','Encode 2',165,164,103,51);f.module('core','Bottleneck',287,253,108,48,{fill:C.purple,stroke:C.purpleLine});
    f.module('d2','Decode 2',416,164,103,51,{fill:C.green,stroke:C.greenLine});f.module('d1','Decode 1',548,77,100,51,{fill:C.green,stroke:C.greenLine});
    f.connect('down1','e1','e2',{kind:'elbow',fromSide:'bottom',toSide:'left'});f.connect('down2','e2','core',{kind:'elbow',fromSide:'bottom',toSide:'left'});
    f.connect('up2','core','d2',{kind:'elbow',fromSide:'right',toSide:'bottom'});f.connect('up1','d2','d1',{kind:'elbow',fromSide:'right',toSide:'bottom'});
    f.connect('skip1','e1','d1',{color:C.orangeLine,dashed:true});f.connect('skip2','e2','d2',{color:C.orangeLine,dashed:true});
    note(f,'skip-label1','skip · high resolution',221,73,233);note(f,'skip-label2','skip',310,163,63);
    note(f,'scale1','H × W',8,141,68);note(f,'scale2','H/2 × W/2',109,224,99);note(f,'scale3','H/4 × W/4',290,307,104);
    return f;
  },
  '05-panels':()=>{
    const f=fig('Cross-modal correspondence');
    f.panel('a','(a) Representations',20,28,294,309,{stroke:'#C6CED4'});
    f.panel('b','(b) Pairwise matching',333,28,319,309,{stroke:'#C6CED4'});
    f.module('image','Image',42,98,78,44);f.module('image-encoder','Vision\nencoder',166,90,124,60);
    f.module('text','Text',42,228,78,44,{fill:C.orange,stroke:C.orangeLine});f.module('text-encoder','Text\nencoder',166,220,124,60,{fill:C.orange,stroke:C.orangeLine});
    f.connect('vision','image','image-encoder');f.connect('language','text','text-encoder');
    f.label('x-label','Text embeddings',421,78,160,24,{color:C.orangeLine,size:13});
    f.label('y-label','Image\nembeddings',342,144,78,60,{color:C.blueLine,size:12});
    f.matrix('scores',[['•','','',''],['','•','',''],['','','•',''],['','','','•']],426,116,{cell:35,gap:3,size:17});
    note(f,'matching-note','Aligned pairs lie on the diagonal',359,288,272);
    return f;
  },
  '06-tokens':()=>{
    const f=fig('Selective token aggregation');tag(f,'Selective token aggregation');
    f.tokens('tokens',['1','2','3','4','5','6'],27,99,{cell:25,gap:4,masked:[1,4]});
    f.module('select','Select',239,87,105,51,{fill:C.green,stroke:C.greenLine});
    f.tokens('kept',['1','3','4','6'],404,99,{cell:25,gap:4});
    f.label('token-port','',27,87,171,51);f.label('kept-port','',404,87,112,51);
    f.connect('selection','token-port','select');f.connect('retained','select','kept-port');
    f.module('aggregate','Aggregate',404,232,112,49,{fill:C.purple,stroke:C.purpleLine});
    f.matrix('weights',[['.5','.2','.2','.1']],46,242,{cell:31,gap:3,size:12});
    f.label('weight-port','',45,232,134,49);f.connect('weights-edge','weight-port','aggregate');f.connect('token-edge','kept-port','aggregate',{fromSide:'bottom',toSide:'top'});
    f.module('summary','z',583,232,49,49,{fill:C.orange,stroke:C.orangeLine,size:19});f.connect('summary-edge','aggregate','summary');
    note(f,'all-label','Token positions',27,64,171);note(f,'kept-label','Retained tokens',394,64,133);note(f,'weights-label','Normalized weights',28,203,172);note(f,'mask-label','Gray: omitted tokens',27,140,175);
    return f;
  },
  '07-long-label':()=>{
    const f=fig('Conditioned temporal alignment');tag(f,'Conditioned temporal alignment');
    f.module('observations','Irregularly sampled\nobservations',26,126,163,71,{fill:C.gray,stroke:C.grayLine,size:14});
    f.module('alignment','Uncertainty-conditioned\ntemporal alignment',251,108,217,106,{fill:C.green,stroke:C.greenLine,size:15,bold:true});
    f.module('representation','Aligned\nrepresentation',530,126,120,71,{size:13});
    f.connect('e0','observations','alignment');f.connect('e1','alignment','representation');
    f.module('metadata','Sampling intervals + confidence',243,277,233,40,{fill:C.orange,stroke:C.orangeLine,size:12});
    f.connect('context','metadata','alignment',{fromSide:'top',toSide:'bottom',color:C.orangeLine});
    note(f,'notation','Δt and confidence remain separate inputs',220,322,278);
    return f;
  },
  '08-train-infer':()=>{
    const f=fig('Training and inference');
    f.panel('train','(a) Training',19,24,634,153,{fill:'#FAFBFC',stroke:'#C6CED4'});
    f.panel('infer','(b) Inference',19,194,634,142,{stroke:'#C6CED4'});
    f.module('train-x','Sample x',41,79,100,44,{fill:C.gray,stroke:C.grayLine});
    f.module('train-model','Model fθ',191,75,129,52);f.module('loss','Loss',379,119,88,44,{fill:C.orange,stroke:C.orangeLine});
    f.module('target','Target y',522,119,100,44,{fill:C.gray,stroke:C.grayLine});
    f.connect('train-forward','train-x','train-model');f.connect('objective','train-model','loss',{kind:'elbow',toSide:'top'});f.connect('supervision','target','loss',{fromSide:'left',toSide:'right'});
    f.connect('gradient','loss','train-model',{fromSide:'left',toSide:'bottom',kind:'elbow',color:C.orangeLine,dashed:true});
    f.label('update-label','update θ',282,146,83,19,{size:11,color:C.orangeLine});
    f.module('infer-x','New x',41,257,100,44,{fill:C.gray,stroke:C.grayLine});
    f.module('infer-model','Model fθ',191,251,129,56);f.module('prediction','Prediction ŷ',423,257,144,44,{fill:C.green,stroke:C.greenLine});
    f.connect('infer-forward','infer-x','infer-model');f.connect('infer-output','infer-model','prediction');
    note(f,'fixed','fixed parameters',182,309,148);
    return f;
  },
  '09-capabilities':()=>{
    const f=fig('Native editing probe');tag(f,'Native editing probe');
    f.module('input','Input x',32,100,112,52);f.module('encoder','Encoder',261,100,143,52);f.module('output','Output y',522,100,112,52);
    f.connect('input-encoder','input','encoder');f.connect('encoder-output','encoder','output');
    f.tokens('token-group',['1','2','3','4'],36,248,{cell:30,gap:5});
    f.label('equation','hₜ₊₁ = hₜ + fθ(hₜ)',269,241,259,45,{size:19});
    note(f,'editable-note','Select individual cells or move the group',28,292,246);
    return f;
  }
};
const skill=process.env.PRESENTATIONS_SKILL_DIR;
if(!skill)throw new Error('Set PRESENTATIONS_SKILL_DIR for export finalization');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
for(const [id,build] of Object.entries(builders)){
  const f=build();const candidate=path.join(work,id+'.pptx');const final=path.join(dest,id+'.pptx');
  await f.export(candidate);
  await finalizePresentation({workspaceDir:path.resolve('.'),candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu',`${672*9525},${360*9525}`],explicitTotalSlideCount:1,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:path.join(work,id+'.validation.json')});
  const p=await PresentationFile.importPptx(await FileBlob.load(final));
  await fs.writeFile(path.join(dest,id+'.png'),new Uint8Array(await (await p.export({slide:p.slides.items[0],format:'png',scale:2})).arrayBuffer()));
  await fs.writeFile(path.join(dest,id+'.contract.json'),JSON.stringify({slides:[tasks[id].contract]},null,2));
  console.log(id+' exported, finalized, reimported and rendered');
}
