#!/usr/bin/env python3
"""Finalize newly generated candidates only: native paths, attached connectors,
picture fitting and groups. Never apply a generation manifest to a user's deck.
"""
import argparse, copy, io, json, posixpath, tempfile
from pathlib import Path
from PIL import Image
from lxml import etree as E
import pptx as P

def custom_geometry(pr, item):
    for child in list(pr):
        if child.tag in (P.q('a:prstGeom'),P.q('a:custGeom')):pr.remove(child)
    g=E.Element(P.q('a:custGeom'));pr.insert(1,g)
    for tag in ('a:avLst','a:gdLst','a:ahLst','a:cxnLst'):P.sub(g,tag)
    P.sub(g,'a:rect',l='0',t='0',r='r',b='b');paths=P.sub(g,'a:pathLst')
    x,y,w,h=item['bounds'];unit=10000
    path=P.sub(paths,'a:path',w=round(w*unit),h=round(h*unit),fill='norm' if item['closed'] else 'none',stroke='1')
    for i,(px,py) in enumerate(item['points']):
        command=P.sub(path,'a:moveTo' if i==0 else 'a:lnTo');P.sub(command,'a:pt',x=round((px-x)*unit),y=round((py-y)*unit))
    if item['closed']:P.sub(path,'a:close')

def fit_images(root,parts,part,spec):
    relpath=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
    rels={r.get('Id'):r.get('Target') for r in P.xml(parts[relpath])}
    pictures=root.findall('.//p:pic',P.NS)
    if len(pictures)!=len(spec.get('images',[])):raise ValueError('Picture manifest mismatch')
    for pic,item in zip(pictures,spec.get('images',[])):
        if P.name(pic)!=item['name']:raise ValueError('Picture order mismatch')
        blip=pic.find('p:blipFill/a:blip',P.NS)
        rid=blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        media=posixpath.normpath(posixpath.join(posixpath.dirname(part),rels[rid]))
        with Image.open(io.BytesIO(parts[media])) as im:iw,ih=im.size
        crop=item.get('crop',dict(left=0,top=0,right=0,bottom=0)).copy()
        ew,eh=iw*(1-crop['left']-crop['right']),ih*(1-crop['top']-crop['bottom'])
        x,y,w,h=item['bounds'];fit=item.get('fit','contain')
        if fit=='contain':
            scale=min(w/ew,h/eh);nw,nh=ew*scale,eh*scale;x+=(w-nw)/2;y+=(h-nh)/2;w,h=nw,nh
        elif fit=='cover':
            if ew/eh>w/h:
                trim=(ew-eh*w/h)/iw/2;crop['left']+=trim;crop['right']+=trim
            else:
                trim=(eh-ew*h/w)/ih/2;crop['top']+=trim;crop['bottom']+=trim
        item['bounds']=[x,y,w,h];item['crop']=crop
        tr=P.xfrm(pic);off=tr.find('a:off',P.NS);ext=tr.find('a:ext',P.NS)
        off.set('x',str(round(x*P.EMU)));off.set('y',str(round(y*P.EMU)))
        ext.set('cx',str(round(w*P.EMU)));ext.set('cy',str(round(h*P.EMU)))

def materialize(source,destination,manifest):
    parts=P.load(source)
    if len(P.slides(parts))!=len(manifest['slides']):raise ValueError('Slide count mismatch')
    for part,spec in zip(P.slides(parts),manifest['slides']):
        root=P.xml(parts[part])
        for item in spec.get('paths',[]):
            obj=P.lookup(root,item['name']);pr=obj.find('p:spPr',P.NS)
            if item['kind']=='connector':
                connector=E.Element(P.q('p:cxnSp'));nv=P.sub(connector,'p:nvCxnSpPr');nv.append(copy.deepcopy(P.props(obj)))
                P.sub(nv,'p:cNvCxnSpPr');P.sub(nv,'p:nvPr');connector.append(pr)
                obj.getparent().replace(obj,connector);obj=connector
            if item.get('connectorKind')=='straight':
                g=pr.find('a:prstGeom',P.NS);g.set('prst','straightConnector1')
                a,b=item['points'][0],item['points'][-1];tr=P.xfrm(obj)
                # The connector endpoints use exact zero extents where aligned.
                off=tr.find('a:off',P.NS);ext=tr.find('a:ext',P.NS)
                off.set('x',str(round(min(a[0],b[0])*P.EMU)));off.set('y',str(round(min(a[1],b[1])*P.EMU)))
                ext.set('cx',str(round(abs(b[0]-a[0])*P.EMU)));ext.set('cy',str(round(abs(b[1]-a[1])*P.EMU)))
                if b[0]<a[0]:tr.set('flipH','1')
                if b[1]<a[1]:tr.set('flipV','1')
            else:custom_geometry(pr,item)
            ln=pr.find('a:ln',P.NS)
            if ln is not None:
                ln.set('cap','rnd')
                for child in list(ln):
                    if child.tag in (P.q('a:round'),P.q('a:bevel'),P.q('a:miter')):ln.remove(child)
                P.sub(ln,'a:round')
        if spec.get('images'):fit_images(root,parts,part,spec)
        parts[part]=P.serial(root)
    with tempfile.TemporaryDirectory(prefix='figure-native-',dir=Path(destination).resolve().parent) as td:
        intermediate=Path(td)/'native.pptx';P.save(parts,intermediate)
        P.prepare(intermediate,destination,manifest)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source');parser.add_argument('output');parser.add_argument('--manifest',required=True)
    args=parser.parse_args();materialize(args.source,args.output,json.loads(Path(args.manifest).read_text()))
