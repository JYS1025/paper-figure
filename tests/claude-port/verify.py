#!/usr/bin/env python3
"""Read saved port fixtures and exercise preservation/negative controls."""
import argparse,copy,hashlib,json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'ports/claude/paper-figure/scripts'))
import pptx as P
import flow_audit as F

def main():
    parser=argparse.ArgumentParser();parser.add_argument('work');args=parser.parse_args()
    work=Path(args.work).resolve();source=work/'geometry/geometry.pptx'
    contract=json.loads(source.with_suffix('.contract.json').read_text())
    checks=[]
    def check(name,condition):
        if not condition:raise AssertionError(name)
        checks.append(name)
    def rejects(name,call):
        try:call()
        except (ValueError,FileExistsError):checks.append(name)
        else:raise AssertionError(name)
    original=source.read_bytes();r=P.inspect(source,contract);check('fixture content contract',r['passed'])
    flow=F.audit(source);check('nine attached connector geometries',flow['summary']=={'connectors':9,'requiringRenderedReview':0,'geometryUnchecked':0})
    parts=P.load(source);root=P.xml(parts['ppt/slides/slide1.xml'])
    contained=P.bounds(P.lookup(root,'contain'));check('contain preserves square aspect',contained==[round(v*P.EMU) for v in [415,480,50,50]])
    cover=P.lookup(root,'cover').find('p:blipFill/a:srcRect',P.NS)
    check('cover uses editable crop',cover.get('t')=='25000' and cover.get('b')=='25000')
    crop=P.lookup(root,'crop').find('p:blipFill/a:srcRect',P.NS)
    check('explicit crop preserved',dict(crop.attrib)=={'l':'10000','t':'15000','r':'20000','b':'25000'})
    check('picture media byte identity',all(value==(ROOT/'ports/claude/paper-figure/assets/astronaut.png').read_bytes() for name,value in parts.items() if name.startswith('ppt/media/') and not name.endswith('/')))
    for mutation,name in [('remove','missing edge rejected'),('reverse','reversed edge rejected')]:
        bad=copy.deepcopy(root);edge=P.lookup(bad,'edge8')
        if mutation=='remove':edge.getparent().remove(edge)
        else:
            a=edge.find('.//a:stCxn',P.NS);b=edge.find('.//a:endCxn',P.NS)
            a.attrib.update({'id':b.get('id'),'idx':b.get('idx')});b.attrib.update({'id':P.ident(P.lookup(bad,'a8')),'idx':'1'})
        with tempfile.TemporaryDirectory() as td:
            altered=parts.copy();altered['ppt/slides/slide1.xml']=P.serial(bad);f=Path(td)/'bad.pptx';P.save(altered,f)
            check(name,not P.inspect(f,contract)['passed'])
    bad=copy.deepcopy(root);cx=P.lookup(bad,'edge0').find('p:spPr/a:custGeom/a:pathLst/a:path/a:moveTo/a:pt',P.NS);cx.set('x',str(int(cx.get('x'))+100000))
    check('custom elbow coordinate defect detected',any('from:endpoint_offset' in row['reviewReasons'] for row in F.audit_tree(bad)))
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);latest=td/'human-saved.pptx';saved=parts.copy()
        saved['customXml/untouched.xml']=b'<private-note>preserve me</private-note>'
        P.save(saved,latest);inspection=P.inspect(latest);target=next(o for o in inspection['slides'][0]['objects'] if o['name']=='a8')
        plan={'sourceSha256':inspection['sha256'],'operations':[{'slide':1,**{k:target[k] for k in ('id','name','fingerprint')},'action':'replace_text','old':'Source','new':'Changed source'}]}
        revised=td/'edited.pptx';receipt=P.patch(latest,revised,plan);after=P.load(revised)
        check('requested label edited',P.text(P.lookup(P.xml(after['ppt/slides/slide1.xml']),'a8'))=='Changed source')
        check('all untouched package payloads identical',all(after[k]==v for k,v in saved.items() if k!='ppt/slides/slide1.xml'))
        before_root=P.xml(saved['ppt/slides/slide1.xml']);after_root=P.xml(after['ppt/slides/slide1.xml'])
        check('all untargeted slide objects preserved',all(P.node_record(P.lookup(before_root,P.name(s)))['fingerprint']==P.node_record(s)['fingerprint'] for s in P.shapes(after_root) if P.name(s)!='a8'))
        rejects('stale source rejected',lambda:P.patch(revised,td/'stale.pptx',plan))
        badplan=copy.deepcopy(plan);badplan['operations'][0]['fingerprint']='0'*64
        rejects('wrong fingerprint rejected',lambda:P.patch(latest,td/'wrong.pptx',badplan))
        rejects('existing output rejected',lambda:P.patch(latest,revised,plan))
        move=copy.deepcopy(plan);move['operations'][0].update(action='move',dx=10,dy=-5)
        moved=td/'moved.pptx';P.patch(latest,moved,move)
        check('straight connector rerouted after move',F.audit(moved)['summary']['requiringRenderedReview']==0)
        routed=next(o for o in inspection['slides'][0]['objects'] if o['name']=='a0')
        move['operations']=[{'slide':1,**{k:routed[k] for k in ('id','name','fingerprint')},'action':'move','dx':10,'dy':10}]
        rejects('routed endpoint move requires native editor',lambda:P.patch(latest,td/'routed.pptx',move))
        edge=next(o for o in inspection['slides'][0]['objects'] if o['name']=='edge0')
        style={'sourceSha256':inspection['sha256'],'operations':[{'slide':1,**{k:edge[k] for k in ('id','name','fingerprint')},'action':'style_connector','widthPx':3.2,'arrowWidth':'lg','arrowLength':'med'}]}
        styled=td/'styled.pptx';P.patch(latest,styled,style)
        check('connector style retains endpoints',P.inspect(styled,contract)['passed'] and F.audit(styled)['summary']['requiringRenderedReview']==0)
    check('input file unchanged',source.read_bytes()==original)
    replay=json.loads((work/'replay-inspect.json').read_text());check('complex replay contract',replay['passed'])
    check('complex replay native objects',replay['slides'][0]['counts']=={'sp':196,'cxnSp':10,'grpSp':16,'pic':1,'graphicFrame':0})
    check('complex replay connector attachment',json.loads((work/'replay-flow.json').read_text())['summary']['requiringRenderedReview']==0)
    typography=json.loads((work/'typography-audit.json').read_text());check('fourteen rendered math regions',typography['summary']=={'regions':14,'requiringReview':0,'unmeasuredRegions':0})
    shared=ROOT/'skills/paper-figure';port=ROOT/'ports/claude/paper-figure'
    asset_files=[p for p in (shared/'assets').rglob('*') if p.is_file() and p.name!='SOURCES.md']
    check('all palette/media assets match canonical skill',all((port/p.relative_to(shared)).read_bytes()==p.read_bytes() for p in asset_files))
    check('sixteen color books',len(json.loads((port/'assets/color-books.json').read_text())['books'])==16)
    creation=json.loads((work/'geometry/creation-negatives.json').read_text())
    result={'passed':True,'checks':checks,'creationNegativeChecks':creation,'totalChecks':len(checks)+len(creation),'scope':'Local portable-engine and saved-file checks. Not a Claude-host run, native PowerPoint edit test, new image-model generation or independent quality comparison.'}
    (work/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({'passed':True,'totalChecks':result['totalChecks']}))
if __name__=='__main__':main()
