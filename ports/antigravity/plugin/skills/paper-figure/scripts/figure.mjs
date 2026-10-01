import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {pptxgen,python} from './runtime.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
export const palette={ink:'#233947',muted:'#526572',blue:'#E4EEF7',blueLine:'#436D91',green:'#E2F0E9',greenLine:'#427462',orange:'#FAECD7',orangeLine:'#A36E26',purple:'#EEE7F6',purpleLine:'#785896',gray:'#F1F3F5',grayLine:'#84929C',white:'#FFFFFF'};
const color=v=>{if(!/^#?[0-9a-f]{6}$/i.test(v))throw new Error(`Use a six-digit RGB color: ${v}`);return v.replace('#','');};
const fill=v=>v==='none'?{color:'FFFFFF',transparency:100}:{color:color(v)};
const line=o=>o.stroke==='none'||o.strokeWidth===0?{color:'FFFFFF',transparency:100,width:0}:{color:color(o.stroke),width:o.strokeWidth*.75,...(o.dashed?{dashType:'dash'}:{})};
const pos=b=>({x:b[0]/96,y:b[1]/96,w:b[2]/96,h:b[3]/96});
const sidePoint=(b,s)=>({left:[b[0],b[1]+b[3]/2],right:[b[0]+b[2],b[1]+b[3]/2],top:[b[0]+b[2]/2,b[1]],bottom:[b[0]+b[2]/2,b[1]+b[3]]})[s];
const sideVector={left:[-1,0],right:[1,0],top:[0,-1],bottom:[0,1]};
function route(a,b,fromSide,toSide,kind) {
  if(kind==='straight')return [a,b];
  if(kind!=='elbow')throw new Error(`Unsupported connector kind: ${kind}`);
  const v=sideVector[fromSide],z=sideVector[toSide],dx=b[0]-a[0],dy=b[1]-a[1];
  if(v[0]*dx+v[1]*dy<=0||z[0]*(-dx)+z[1]*(-dy)<=0)throw new Error('Elbow requires facing sides and a monotone route. Use visible intermediate ports or native PowerPoint for return paths.');
  if(v[0]&&z[0])return [a,[(a[0]+b[0])/2,a[1]],[(a[0]+b[0])/2,b[1]],b];
  if(v[1]&&z[1])return [a,[a[0],(a[1]+b[1])/2],[b[0],(a[1]+b[1])/2],b];
  return [a,v[0]?[b[0],a[1]]:[a[0],b[1]],b];
}

/** Native PowerPoint drawing helper. Coordinates and font sizes are CSS px at 96 dpi. */
export class Figure {
  constructor({width=672,height=360,font='Arial',title='',notes=''}={}) {
    if(![width,height].every(v=>Number.isFinite(v)&&v>0))throw new Error('Invalid canvas');
    Object.assign(this,{width,height,font,title,notes,objects:new Map(),edges:[],groups:[],images:[]});
  }
  register(id,item) {
    if(typeof id!=='string'||!id||this.objects.has(id)||this.groups.some(g=>g.name===id))throw new Error(`Duplicate or invalid object name: ${id}`);
    if(!item.bounds.every(Number.isFinite)||item.bounds[2]<=0||item.bounds[3]<=0)throw new Error(`Invalid bounds: ${id}`);
    item.name=id;this.objects.set(id,item);return item;
  }
  add(id,text,x,y,w,h,opts={}) {
    const style={typeface:this.font,fontSize:opts.size??14,color:opts.color||palette.ink,bold:opts.bold??false,italic:opts.italic??false,alignment:opts.align||'center',verticalAlignment:opts.valign||'middle',wrap:'square',insets:{left:opts.pad??5,right:opts.pad??5,top:opts.padY??2,bottom:opts.padY??2}};
    return this.register(id,{kind:'shape',bounds:[x,y,w,h],geometry:opts.geometry||'rect',fill:opts.fill||palette.white,stroke:opts.stroke??palette.ink,strokeWidth:opts.strokeWidth??1,dashed:!!opts.dashed,text:text===null?null:{value:String(text),style}});
  }
  module(id,text,x,y,w,h,opts={}) {return this.add(id,text,x,y,w,h,{fill:palette.blue,stroke:palette.blueLine,...opts});}
  label(id,text,x,y,w,h,opts={}) {return this.add(id,text,x,y,w,h,{geometry:'textbox',fill:'none',stroke:'none',strokeWidth:0,pad:0,...opts});}
  path(id,points,{fill='none',color=palette.ink,width=1,closed=false,dashed=false}={}) {
    if(points.length<2||points.some(p=>p.length!==2||!p.every(Number.isFinite)))throw new Error(`Invalid path: ${id}`);
    const x=Math.min(...points.map(p=>p[0])),y=Math.min(...points.map(p=>p[1]));
    return this.register(id,{kind:'path',bounds:[x,y,Math.max(.01,Math.max(...points.map(p=>p[0]))-x),Math.max(.01,Math.max(...points.map(p=>p[1]))-y)],points,closed,fill,stroke:color,strokeWidth:width,dashed});
  }
  image(id,bytes,x,y,w,h,{alt=id,crop,contentType='image/png',fit='contain'}={}) {
    if(!['contain','cover','stretch'].includes(fit))throw new Error(`Unsupported picture fit: ${fit}`);
    if(crop&&(!['left','top','right','bottom'].every(k=>Number.isFinite(crop[k])&&crop[k]>=0&&crop[k]<1)||crop.left+crop.right>=1||crop.top+crop.bottom>=1))throw new Error(`Invalid image crop: ${id}`);
    if(!['image/png','image/jpeg'].includes(contentType))throw new Error('Use PNG or JPEG picture assets');
    const im=this.register(id,{kind:'image',bounds:[x,y,w,h],bytes:Buffer.from(bytes),alt,crop,contentType,fit});
    this.images.push({name:id,alt,bounds:[x,y,w,h],fit,...(crop?{crop}:{})});return im;
  }
  panel(id,title,x,y,w,h,{fill='none',stroke=palette.grayLine,...opts}={}) {
    const box=this.add(id,null,x,y,w,h,{fill,stroke,strokeWidth:.7,...opts});
    this.label(`${id}.title`,title,x+8,y+5,w-16,22,{align:'left',bold:true,size:14});return box;
  }
  tokens(id,labels,x,y,{cell=24,gap=5,fill=palette.blue,stroke=palette.blueLine,masked=[],size=12}={}) {
    const ids=labels.map((t,i)=>{const n=`${id}.${i}`;this.add(n,t,x+i*(cell+gap),y,cell,cell,{fill:masked.includes(i)?palette.gray:fill,stroke:masked.includes(i)?palette.grayLine:stroke,size,pad:0});return n;});
    this.group(id,ids);return ids;
  }
  matrix(id,rows,x,y,{cell=24,gap=2,highlight=(r,c)=>r===c,size=12}={}) {
    const ids=[];rows.forEach((row,r)=>row.forEach((t,c)=>{const n=`${id}.${r}.${c}`;this.add(n,String(t),x+c*(cell+gap),y+r*(cell+gap),cell,cell,{fill:highlight(r,c)?palette.blue:palette.gray,stroke:'none',strokeWidth:0,size,pad:0});ids.push(n);}));this.group(id,ids);return ids;
  }
  group(id,children) {
    if(!id||this.objects.has(id)||this.groups.some(g=>g.name===id))throw new Error(`Duplicate group: ${id}`);
    if(children.length<2||new Set(children).size!==children.length||children.some(n=>!this.objects.has(n)))throw new Error('Groups need at least two distinct existing objects');
    if(this.groups.some(g=>g.children.some(n=>children.includes(n))))throw new Error('Overlapping groups are unsupported');
    this.groups.push({name:id,children});
  }
  connect(id,from,to,{fromSide='right',toSide='left',kind='straight',color=palette.ink,width=2.6,dashed=false,arrowWidth='med',arrowLength='med'}={}) {
    if(!sideVector[fromSide]||!sideVector[toSide])throw new Error('Unknown connector side');
    if(!Number.isFinite(width)||width<=0||!['sm','med','lg'].includes(arrowWidth)||!['sm','med','lg'].includes(arrowLength))throw new Error(`Invalid connector styling: ${id}`);
    const a=this.objects.get(from),b=this.objects.get(to);
    if(!a||!b||[a,b].some(o=>o.kind!=='shape'||!['rect','roundRect','textbox'].includes(o.geometry)))throw new Error('Connector endpoints must be existing native rectangles');
    const points=route(sidePoint(a.bounds,fromSide),sidePoint(b.bounds,toSide),fromSide,toSide,kind);
    if(points[0].every((v,i)=>v===points.at(-1)[i]))throw new Error('Zero-length connector');
    const sh=this.path(id,points,{color,width,dashed});sh.kind='connector';sh.connectorKind=kind;
    this.edges.push({name:id,from,to,fromSide,toSide,kind,arrowWidth,arrowLength});return sh;
  }
  async export(file,{contract}={}) {
    file=path.resolve(file);
    if(!file.endsWith('.pptx'))throw new Error('Use a .pptx output filename');
    try{await fs.access(file);throw new Error(`Output exists: ${file}`);}catch(e){if(e.code!=='ENOENT')throw e;}
    const PptxGenJS=pptxgen(),pptx=new PptxGenJS();
    pptx.defineLayout({name:'FIGURE',width:this.width/96,height:this.height/96});pptx.layout='FIGURE';pptx.title=this.title;pptx.subject='Editable research figure';pptx.author='';pptx.company='';pptx.lang='en-US';
    const slide=pptx.addSlide();slide.background={color:'FFFFFF'};slide.addNotes(`${this.title}\n${this.notes}`);
    for(const [id,o] of this.objects){
      if(o.kind==='image'){
        slide.addImage({...pos(o.bounds),data:`data:${o.contentType};base64,${o.bytes.toString('base64')}`,objectName:id,altText:o.alt});continue;
      }
      const geometry=o.geometry==='textbox'?'rect':o.geometry||'rect';
      if(!pptx.ShapeType[geometry])throw new Error(`Unsupported native shape: ${geometry}`);
      const options={...pos(o.bounds),objectName:id,fill:fill(o.fill),line:line(o)};
      if(o.text){
        const t=o.text.style,p=t.insets||{};
        slide.addText(o.text.value,{...options,shape:pptx.ShapeType[geometry],fontFace:t.typeface||this.font,fontSize:(t.fontSize??14)*.75,color:color(t.color||palette.ink),bold:!!t.bold,italic:!!t.italic,align:t.alignment||'center',valign:t.verticalAlignment==='middle'?'mid':t.verticalAlignment||'mid',margin:[p.top??2,p.right??5,p.bottom??2,p.left??5].map(v=>v*.75),wrap:t.wrap!=='none',breakLine:false,paraSpaceAfterPt:0,charSpacing:0});
      }else slide.addShape(pptx.ShapeType[geometry],options);
    }
    await fs.mkdir(path.dirname(file),{recursive:true});
    const dir=await fs.mkdtemp(path.join(path.dirname(file),'.figure-'));
    try{
      const raw=path.join(dir,'raw.pptx'),manifest=path.join(dir,'manifest.json');
      await pptx.writeFile({fileName:raw});
      await fs.writeFile(manifest,JSON.stringify({slides:[{edges:this.edges,groups:this.groups,images:this.images,paths:[...this.objects.values()].filter(o=>['path','connector'].includes(o.kind))}]}));
      const result=spawnSync(python,[path.join(here,'materialize.py'),raw,file,'--manifest',manifest],{encoding:'utf8'});
      if(result.status!==0)throw new Error(result.error?.message||result.stderr||result.stdout);
      if(contract)await fs.writeFile(file.replace(/\.pptx$/,'.contract.json'),JSON.stringify(contract,null,2),{flag:'wx'});
    }finally{await fs.rm(dir,{recursive:true,force:true});}
    return file;
  }
}
