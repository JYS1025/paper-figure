#!/usr/bin/env python3
"""Read-only native-connector diagnostics; never a visual-quality score.

Requires the same lxml runtime as pptx.py. Transparent anchors are review
flags, since a separate visible bracket/image may correctly delimit a proxy.
Unsupported transforms and inherited boundary styles are reported explicitly.
"""
import argparse
import json
from pathlib import Path
import pptx as P

PRESETS={'straightConnector1','bentConnector2','bentConnector3','bentConnector4','bentConnector5'}

def identity_group_space(node):
    for parent in node.iterancestors():
        if parent.tag!=P.q('p:grpSp'):continue
        tr=P.xfrm(parent)
        if tr is None or float(tr.get('rot','0'))!=0 or any(tr.get(k) in ('1','true') for k in ('flipH','flipV')):return False
        off,ext,ch_off,ch_ext=[tr.find(k,P.NS) for k in ('a:off','a:ext','a:chOff','a:chExt')]
        if any(x is None for x in (off,ext,ch_off,ch_ext)):return False
        if any(off.get(k)!=ch_off.get(k) for k in ('x','y')):return False
        if any(ext.get(k)!=ch_ext.get(k) for k in ('cx','cy')):return False
    return True

def paint_state(parent):
    if parent is None:return 'unspecified'
    if parent.find('a:noFill',P.NS) is not None:return 'transparent'
    solid=parent.find('a:solidFill',P.NS)
    if solid is not None:
        alpha=solid.find('.//a:alpha',P.NS)
        return 'transparent' if alpha is not None and alpha.get('val')=='0' else 'visible'
    # Non-solid paint needs visual inspection rather than an opacity guess.
    return 'unspecified'

def boundary_state(node):
    sp=node.find('p:spPr',P.NS);fill=paint_state(sp)
    ln=sp.find('a:ln',P.NS) if sp is not None else None
    stroke='transparent' if ln is not None and ln.get('w')=='0' else paint_state(ln)
    if 'visible' in (fill,stroke):return 'visible'
    return 'transparent' if fill==stroke=='transparent' else 'unspecified'

def supported_endpoint(node,site):
    if node.tag!=P.q('p:sp') or site not in ('0','1','2','3'):return False
    tr=P.xfrm(node);geom=node.find('p:spPr/a:prstGeom',P.NS)
    return (tr is not None and P.bounds(node) is not None and geom is not None
            and geom.get('prst') in ('rect','roundRect')
            and float(tr.get('rot','0'))==0
            and not any(tr.get(k) in ('1','true') for k in ('flipH','flipV'))
            and identity_group_space(node))

def audit_tree(root,slide_number=1,tolerance_px=.5):
    nodes=P.shapes(root);by_id={}
    for n in nodes:by_id.setdefault(P.ident(n),[]).append(n)
    rows=[]
    for edge in nodes:
        if edge.tag!=P.q('p:cxnSp'):continue
        row={'slide':slide_number,'name':P.name(edge),'geometryStatus':'not_checked','reviewReasons':[]}
        resolved=[]
        for label,tag in [('from','a:stCxn'),('to','a:endCxn')]:
            ref=edge.find('.//'+tag,P.NS)
            candidates=by_id.get(ref.get('id'),[]) if ref is not None else []
            if len(candidates)!=1:
                row[label]={'status':'missing_or_ambiguous_reference'}
                row['reviewReasons'].append(label+':missing_or_ambiguous_reference');continue
            node=candidates[0];state=boundary_state(node);site=ref.get('idx')
            row[label]={'name':P.name(node),'site':site,'boundary':state}
            resolved.append((node,site))
            if state!='visible':row['reviewReasons'].append(label+':'+state+'_boundary')
        tr=P.xfrm(edge);geom=edge.find('p:spPr/a:prstGeom',P.NS)
        supported=(len(resolved)==2 and tr is not None and P.bounds(edge) is not None
                   and geom is not None and geom.get('prst') in PRESETS
                   and float(tr.get('rot','0'))==0 and identity_group_space(edge)
                   and all(supported_endpoint(n,site) for n,site in resolved))
        if supported:
            x,y,w,h=P.bounds(edge);fx=tr.get('flipH') in ('1','true');fy=tr.get('flipV') in ('1','true')
            actual=[(x+(w if fx else 0),y+(h if fy else 0)),(x+(0 if fx else w),y+(0 if fy else h))]
            row['geometryStatus']='checked';row['endpointOffsetsPx']={}
            for label,(node,site),pt in zip(('from','to'),resolved,actual):
                expected=P.anchor(P.bounds(node),site)
                delta=max(abs(a-b) for a,b in zip(pt,expected))/P.EMU
                row['endpointOffsetsPx'][label]=round(delta,5)
                if delta>tolerance_px:row['reviewReasons'].append(label+':endpoint_offset')
        else:row['reviewReasons'].append('geometry:manual_check_required')
        rows.append(row)
    return rows

def audit(source):
    source=Path(source);parts=P.load(source);rows=[]
    for i,part in enumerate(P.slides(parts),1):
        for row in audit_tree(P.xml(parts[part]),i):
            row['part']=part;rows.append(row)
    return {
        'source':str(source.resolve()),'sourceSha256':P.sha(source.read_bytes()),
        'readOnly':True,'scope':'Native connector attachment diagnostics; inspect the rendered figure for meaning and quality.',
        'summary':{'connectors':len(rows),'requiringRenderedReview':sum(bool(r['reviewReasons']) for r in rows),
                   'geometryUnchecked':sum(r['geometryStatus']=='not_checked' for r in rows)},
        'connectors':rows,
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source');parser.add_argument('--output')
    args=parser.parse_args();result=audit(args.source)
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        # Never overwrite a deck, an existing diagnostic, or any other file.
        with Path(args.output).open('x') as stream:stream.write(text)
    else:print(text,end='')

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError) as error:raise SystemExit(str(error))
