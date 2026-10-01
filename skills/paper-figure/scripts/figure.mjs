import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {artifact,python} from './runtime.mjs';
const {Presentation,PresentationFile}=await artifact();
const here=path.dirname(fileURLToPath(import.meta.url));
export const palette={ink:'#233947',muted:'#526572',blue:'#E4EEF7',blueLine:'#436D91',green:'#E2F0E9',greenLine:'#427462',orange:'#FAECD7',orangeLine:'#A36E26',purple:'#EEE7F6',purpleLine:'#785896',gray:'#F1F3F5',grayLine:'#84929C',white:'#FFFFFF'};

/** Thin drawing helpers; positions, sizing, color and emphasis are author decisions. CSS px. */
export class Figure {
  constructor({width=672,height=360,font='Arial',title='',notes=''}={}) {
    this.presentation=Presentation.create({slideSize:{width,height}});
    this.slide=this.presentation.slides.add();this.slide.background.fill='#FFFFFF';
    this.width=width;this.height=height;this.font=font;
    this.objects=new Map();this.edges=[];this.groups=[];this.images=[];
    this.slide.speakerNotes.textFrame.setText(`${title}\n${notes}`);
  }
  add(id,text,x,y,w,h,opts={}) {
    if(this.objects.has(id))throw new Error(`Duplicate object name: ${id}`);
    if(![x,y,w,h].every(Number.isFinite)||w<=0||h<=0)throw new Error(`Invalid bounds: ${id}`);
    const sh=this.slide.shapes.add({name:id,geometry:opts.geometry||'rect',position:{left:x,top:y,width:w,height:h},fill:opts.fill||palette.white,line:{fill:opts.stroke??palette.ink,width:opts.strokeWidth??1,style:opts.dashed?'dashed':'solid'}});
    if(text!==null){sh.text=text;sh.text.style={typeface:this.font,fontSize:opts.size??14,color:opts.color||palette.ink,bold:opts.bold??false,alignment:opts.align||'center',verticalAlignment:opts.valign||'middle',autoFit:'none',wrap:'square',insets:{left:opts.pad??5,right:opts.pad??5,top:opts.padY??2,bottom:opts.padY??2}};}
    this.objects.set(id,sh);return sh;
  }
  module(id,text,x,y,w,h,opts={}) {return this.add(id,text,x,y,w,h,{fill:palette.blue,stroke:palette.blueLine,...opts});}
  label(id,text,x,y,w,h,opts={}) {return this.add(id,text,x,y,w,h,{geometry:'textbox',fill:'none',stroke:'none',strokeWidth:0,pad:0,...opts});}
  path(id,points,{fill='none',color=palette.ink,width=1,closed=false,dashed=false}={}) {
    if(this.objects.has(id)||points.length<2||points.some(p=>p.length!==2||!p.every(Number.isFinite)))throw new Error(`Invalid path: ${id}`);
    const x=Math.min(...points.map(p=>p[0])),y=Math.min(...points.map(p=>p[1]));
    const w=Math.max(.01,Math.max(...points.map(p=>p[0]))-x),h=Math.max(.01,Math.max(...points.map(p=>p[1]))-y);
    const commands=points.map((p,i)=>({[i?'lineTo':'moveTo']:{x:p[0]-x,y:p[1]-y}}));if(closed)commands.push({close:{}});
    const sh=this.slide.shapes.add({name:id,geometry:'custom',position:{left:x,top:y,width:w,height:h},fill,line:{fill:color,width,style:dashed?'dashed':'solid'},customPaths:[{width:w,height:h,commands}]});
    this.objects.set(id,sh);return sh;
  }
  image(id,bytes,x,y,w,h,{alt=id,crop,contentType='image/png',fit='contain'}={}) {
    if(this.objects.has(id))throw new Error(`Duplicate image: ${id}`);
    if(crop&&(!['left','top','right','bottom'].every(k=>Number.isFinite(crop[k])&&crop[k]>=0&&crop[k]<1)||crop.left+crop.right>=1||crop.top+crop.bottom>=1))throw new Error(`Invalid image crop: ${id}`);
    const im=this.slide.images.add({blob:bytes,contentType,alt,fit,position:{left:x,top:y,width:w,height:h},...(crop?{crop}:{})});
    // Images are independent media objects; diagram labels and arrows remain native.
    this.objects.set(id,im);this.images.push({name:id,alt,bounds:[x,y,w,h],...(crop?{crop}:{})});return im;
  }
  panel(id,title,x,y,w,h,{fill='none',stroke=palette.grayLine,...opts}={}) {
    const box=this.add(id,null,x,y,w,h,{fill,stroke,strokeWidth:.7,...opts});
    this.label(`${id}.title`,title,x+8,y+5,w-16,22,{align:'left',bold:true,size:14});return box;
  }
  tokens(id,labels,x,y,{cell=24,gap=5,fill=palette.blue,stroke=palette.blueLine,masked=[],size=12}={}) {
    const ids=labels.map((text,i)=>{const name=`${id}.${i}`;this.add(name,text,x+i*(cell+gap),y,cell,cell,{fill:masked.includes(i)?palette.gray:fill,stroke:masked.includes(i)?palette.grayLine:stroke,size,pad:0});return name;});
    this.group(id,ids);return ids;
  }
  matrix(id,rows,x,y,{cell=24,gap=2,highlight=(r,c)=>r===c,size=12}={}) {
    const ids=[];rows.forEach((row,r)=>row.forEach((text,c)=>{const n=`${id}.${r}.${c}`;this.add(n,String(text),x+c*(cell+gap),y+r*(cell+gap),cell,cell,{fill:highlight(r,c)?palette.blue:palette.gray,stroke:'none',strokeWidth:0,size,pad:0});ids.push(n);}));this.group(id,ids);return ids;
  }
  group(id,children) {
    if(this.objects.has(id)||this.groups.some(g=>g.name===id))throw new Error(`Duplicate group ${id}`);
    if(children.length<2||children.some(n=>!this.objects.has(n)))throw new Error('Groups need at least two existing shapes');
    if(this.groups.some(g=>g.children.some(n=>children.includes(n))))throw new Error('Overlapping groups are unsupported');
    this.groups.push({name:id,children});
  }
  connect(id,from,to,{fromSide='right',toSide='left',kind='straight',color=palette.ink,width=2.6,dashed=false,arrowWidth='med',arrowLength='med'}={}) {
    if(this.objects.has(id))throw new Error(`Duplicate edge ${id}`);
    if(!Number.isFinite(width)||width<=0||!['sm','med','lg'].includes(arrowWidth)||!['sm','med','lg'].includes(arrowLength))throw new Error(`Invalid connector styling: ${id}`);
    const a=this.objects.get(from),b=this.objects.get(to);if(!a||!b)throw new Error(`Unknown endpoints ${from}, ${to}`);
    // OOXML tailEnd is the destination. headEnd points back to the source.
    const sh=this.slide.shapes.connect(a,b,{kind,fromSide,toSide,line:{fill:color,width,style:dashed?'dashed':'solid'},tail:{type:'triangle',width:arrowWidth,length:arrowLength},cap:'round',join:'round'});
    sh.name=id;this.objects.set(id,sh);this.edges.push({name:id,from,to,fromSide,toSide,kind,arrowWidth,arrowLength});return sh;
  }
  async export(file,{contract}={}) {
    file=path.resolve(file);await fs.mkdir(path.dirname(file),{recursive:true});
    const dir=await fs.mkdtemp(path.join(path.dirname(file),'.figure-'));
    const raw=path.join(dir,'raw.pptx'), manifest=path.join(dir,'manifest.json');
    await (await PresentationFile.exportPptx(this.presentation)).save(raw);
    await fs.writeFile(manifest,JSON.stringify({slides:[{edges:this.edges,groups:this.groups,images:this.images}]}));
    const result=spawnSync(python,[path.join(here,'pptx.py'),'prepare',raw,file,'--manifest',manifest],{encoding:'utf8'});
    if(result.status!==0)throw new Error(result.stderr||result.stdout);
    if(contract)await fs.writeFile(file.replace(/\.pptx$/,'.contract.json'),JSON.stringify(contract,null,2));
    return file;
  }
}
