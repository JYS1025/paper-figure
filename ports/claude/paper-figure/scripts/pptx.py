#!/usr/bin/env python3
"""Small OOXML compatibility, inspection and conservative local-patch tool.

Never re-exports an existing deck through a lossy model. Untargeted ZIP entries
keep byte-identical payloads. Requires lxml; does not use python-pptx.
"""
import argparse, copy, hashlib, json, math, os, posixpath, sys, zipfile
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import unquote, urlsplit
from lxml import etree as E

NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
EMU=9525
SIDE={'top':0,'left':1,'bottom':2,'right':3} # rect / roundRect / textbox
REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PACKAGE_REL='http://schemas.openxmlformats.org/package/2006/relationships'
PRESENTATION_ORDER=('sldMasterIdLst','notesMasterIdLst','handoutMasterIdLst','sldIdLst',
    'sldSz','notesSz','smartTags','embeddedFontLst','custShowLst','photoAlbum',
    'custDataLst','kinsoku','defaultTextStyle','modifyVerifier','extLst')
SCHEMA_DIR=Path(__file__).resolve().parents[1]/'assets/ooxml-xsd'
def q(n):
    p,l=n.split(':'); return '{'+NS[p]+'}'+l
def sub(parent,n,**attrs): return E.SubElement(parent,q(n),{k:str(v) for k,v in attrs.items()})
def sha(data): return hashlib.sha256(data).hexdigest()
def xml(data): return E.fromstring(data,E.XMLParser(resolve_entities=False,no_network=True))
def serial(root): return E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
def load(file):
    with zipfile.ZipFile(file) as z:
        if len(z.namelist())!=len(set(z.namelist())): raise ValueError('Duplicate ZIP entries')
        if sum(i.file_size for i in z.infolist())>200_000_000: raise ValueError('Package exceeds 200 MB limit')
        return {i.filename:z.read(i) for i in z.infolist()}
def save(parts,file,canonical=False):
    file=Path(file); file.parent.mkdir(parents=True,exist_ok=True)
    names=list(parts)
    if canonical:
        if '[Content_Types].xml' not in parts:raise ValueError('Missing [Content_Types].xml')
        names=['[Content_Types].xml']+[n for n in names if n!='[Content_Types].xml' and not n.endswith('/')]
    with file.open('xb') as out:
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
            for n in names:z.writestr(n,parts[n])

def presentation_sequence(data):
    root=xml(data)
    if root.tag!=q('p:presentation'):raise ValueError('Expected a Transitional presentation root')
    order={q('p:'+n):i for i,n in enumerate(PRESENTATION_ORDER)}
    children=[c for c in root if isinstance(c.tag,str)]
    if any(c.tag not in order for c in children):
        raise ValueError('Unsupported presentation child; normalization cannot reorder extensions or AlternateContent')
    tags=[c.tag for c in children]
    if len(tags)!=len(set(tags)):raise ValueError('Duplicate presentation child')
    return root,children,order

def normalized_parts(parts):
    """Only change presentation child order. All other part payloads stay exact."""
    result=parts.copy()
    root,children,order=presentation_sequence(parts['ppt/presentation.xml'])
    expected=sorted(children,key=lambda c:order[c.tag])
    if children!=expected:
        # Comments/PIs keep their slots; move only known element children.
        slots=[i for i,c in enumerate(root) if isinstance(c.tag,str)]
        for child in children:root.remove(child)
        for index,child in zip(slots,expected):root.insert(index,child)
        result['ppt/presentation.xml']=serial(root)
    return result

def normalize(source,destination):
    original=load(source);parts=normalized_parts(original)
    changed=[n for n in parts if parts[n]!=original[n]]
    dropped=[n for n in parts if n.endswith('/')]
    save(parts,destination,canonical=True)
    return {'sourceSha256':sha(Path(source).read_bytes()),'outputSha256':sha(Path(destination).read_bytes()),
        'changedParts':changed,'droppedDirectoryEntries':dropped,'contentTypesFirst':True,
        'untouchedPartsByteIdentical':sum(n not in changed and n not in dropped for n in parts),
        'powerPointOpenVerified':False}

def validate_parts(parts):
    """Offline XSD check, with explicit incomplete coverage for unrecognized XML.

    This is not an OPC semantic validator or a Microsoft PowerPoint open test.
    Microsoft extensions/Markup Compatibility are not stripped or preprocessed.
    """
    class LocalSchemas(E.Resolver):
        def resolve(self,url,pubid,context):
            target=SCHEMA_DIR/Path(urlsplit(url).path).name
            if target.suffix!='.xsd' or not target.is_file():
                raise OSError('Schema dependency is not bundled: '+url)
            return self.resolve_filename(str(target),context)
    parser=E.XMLParser(resolve_entities=False,no_network=True,load_dtd=False)
    parser.resolvers.add(LocalSchemas())
    files=sorted(SCHEMA_DIR.glob('*.xsd'))
    if not files:raise ValueError('Bundled OOXML schemas are missing; reinstall this skill')
    schemas={E.parse(str(f),parser).getroot().get('targetNamespace'):f for f in files}
    compiled={};checked=[];unchecked=[];extensions=[];errors=[]
    defaults={};overrides={}
    try:
        types=xml(parts['[Content_Types].xml'])
        defaults={c.get('Extension','').lower():c.get('ContentType','') for c in types if isinstance(c.tag,str) and E.QName(c).localname=='Default'}
        overrides={unquote(c.get('PartName','')).lstrip('/'):c.get('ContentType','') for c in types if isinstance(c.tag,str) and E.QName(c).localname=='Override'}
    except (KeyError,E.XMLSyntaxError,ValueError) as error:
        errors.append({'part':'[Content_Types].xml','message':str(error)})
    for name,data in parts.items():
        if name.endswith('/'):continue
        ext=name.rsplit('.',1)[-1].lower();mime=overrides.get(name,defaults.get(ext,'')).lower()
        if ext not in ('xml','rels','vml','svg') and not (mime.endswith('+xml') or mime in ('application/xml','text/xml')):continue
        try:
            root=xml(data)
            if root.getroottree().docinfo.doctype:raise ValueError('DOCTYPE is unsupported in OOXML parts')
            namespace=E.QName(root).namespace;schema_file=schemas.get(namespace)
            if schema_file is None:
                unchecked.append({'part':name,'namespace':namespace,'reason':'No bundled schema for this XML namespace'})
                continue
            foreign=sorted({E.QName(c).namespace or '' for c in root.iter() if isinstance(c.tag,str)}-schemas.keys())
            if foreign:
                extensions.append({'part':name,'namespaces':foreign,'reason':'XSD wildcards may allow extensions without validating their internals'})
            if namespace not in compiled:compiled[namespace]=E.XMLSchema(E.parse(str(schema_file),parser))
            schema=compiled[namespace];valid=schema.validate(root)
            checked.append({'part':name,'schema':schema_file.name,'valid':valid})
            if not valid:
                errors.extend({'part':name,'line':e.line,'message':e.message} for e in schema.error_log)
        except (E.XMLSyntaxError,E.XMLSchemaParseError,E.XMLSchemaValidateError,ValueError,OSError) as error:
            errors.append({'part':name,'message':str(error)})
    return {'passed':bool(checked) and not errors and not unchecked,'complete':not unchecked,
        'checkedParts':checked,'uncheckedParts':unchecked,'unvalidatedExtensions':extensions,'errors':errors,
        'scope':'ECMA-376 Transitional XML + OPC XSDs; no Markup Compatibility preprocessing, embedded-package recursion or PowerPoint open test',
        'powerPointOpenVerified':False}

def validate(file):
    return {'file':str(Path(file).resolve()),'sha256':sha(Path(file).read_bytes()),**validate_parts(load(file))}
def slides(parts):
    """Resolve displayed slide order; storage filenames are not slide numbers."""
    try:
        presentation=xml(parts['ppt/presentation.xml'])
        relationships=xml(parts['ppt/_rels/presentation.xml.rels'])
    except KeyError as error:
        raise ValueError('Missing presentation or presentation relationships') from error
    by_id={}
    for relationship in relationships.findall('{'+PACKAGE_REL+'}Relationship'):
        rid=relationship.get('Id')
        if not rid or rid in by_id:raise ValueError('Missing or duplicate presentation relationship ID')
        by_id[rid]=relationship
    ordered=[];slide_ids=set()
    for slide in presentation.findall('p:sldIdLst/p:sldId',NS):
        sid=slide.get('id');relationship=by_id.get(slide.get('{'+REL+'}id'))
        if not sid or sid in slide_ids:raise ValueError('Missing or duplicate presentation slide ID')
        slide_ids.add(sid)
        if relationship is None or relationship.get('Type')!=REL+'/slide':
            raise ValueError('Missing or invalid slide relationship')
        if relationship.get('TargetMode','Internal')!='Internal':raise ValueError('External slide relationships are unsupported')
        target=relationship.get('Target','');uri=urlsplit(target)
        if not target or uri.scheme or uri.netloc or uri.query or uri.fragment:
            raise ValueError('Invalid slide relationship target')
        decoded=unquote(uri.path,errors='strict')
        if '\\' in decoded or any(ord(c)<32 for c in decoded) or decoded.startswith('//'):
            raise ValueError('Invalid slide relationship target')
        part=posixpath.normpath(decoded.lstrip('/') if decoded.startswith('/') else posixpath.join('ppt',decoded))
        if part in ('.','..') or part.startswith('../') or part not in parts:
            raise ValueError('Missing or out-of-package slide target')
        if part in ordered:raise ValueError('Duplicate slide relationship target')
        if xml(parts[part]).tag!=q('p:sld'):raise ValueError('Slide relationship does not target a slide')
        ordered.append(part)
    return ordered

@contextmanager
def report_output(destination,protected=()):
    """Reserve a new report before patching; never overwrite a deck or report."""
    if destination is None:
        yield None
        return
    path=Path(destination)
    if any(path.resolve()==Path(other).resolve() for other in protected if other is not None):
        raise ValueError('Report path collides with an input or PPTX output; choose a new report path')
    with path.open('x',encoding='utf8') as stream:
        created=os.fstat(stream.fileno())
        try:
            yield stream
            stream.flush()
        except BaseException:
            stream.close()
            # Remove only the empty/partial report this invocation reserved.
            try:
                current=path.lstat()
            except FileNotFoundError:
                pass
            else:
                if (current.st_dev,current.st_ino)==(created.st_dev,created.st_ino):path.unlink()
            raise
def props(el): return el.find('.//p:cNvPr',NS)
def name(el): return props(el).get('name')
def ident(el): return props(el).get('id')
def shapes(root): return root.xpath('.//p:sp | .//p:cxnSp | .//p:grpSp | .//p:pic | .//p:graphicFrame',namespaces=NS)
def lookup(root,n):
    found=[s for s in shapes(root) if name(s)==n]
    if len(found)!=1: raise ValueError(f'Expected one object named {n!r}; found {len(found)}')
    return found[0]
def text(el):
    return '\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=NS)) for p in el.findall('p:txBody/a:p',NS))
def xfrm(el): return el.find('p:grpSpPr/a:xfrm',NS) if el.tag==q('p:grpSp') else el.find('p:spPr/a:xfrm',NS)
def bounds(el):
    tr=xfrm(el)
    if tr is None: return None
    off,ext=tr.find('a:off',NS),tr.find('a:ext',NS)
    if off is None or ext is None:return None
    return [int(off.get('x')),int(off.get('y')),int(ext.get('cx')),int(ext.get('cy'))]
def node_record(el):
    b=bounds(el)
    return {'id':ident(el),'name':name(el),'kind':E.QName(el).localname,'text':text(el),'boundsPx':[round(v/EMU,4) for v in b] if b else None,'fingerprint':sha(E.tostring(el,method='c14n')),'fontPt':sorted(set(int(v)/100 for v in el.xpath('./p:txBody//a:rPr/@sz',namespaces=NS)))}
def prepare(source,destination,manifest):
    parts=load(source); specs=manifest['slides'];ordered=slides(parts)
    if len(specs)!=len(ordered):raise ValueError('Manifest slide count mismatch')
    for part,spec in zip(ordered,specs):
        root=xml(parts[part]); tree=root.find('p:cSld/p:spTree',NS)
        image_specs=spec.get('images',[])
        if image_specs:
            pictures=root.findall('.//p:pic',NS)
            if len(pictures)!=len(image_specs):raise ValueError('Image manifest count mismatch')
            for pic,item in zip(pictures,image_specs):
                if any(abs(a-b*EMU)>EMU for a,b in zip(bounds(pic),item['bounds'])):raise ValueError('Image order/bounds mismatch')
                props(pic).set('name',item['name']);props(pic).set('descr',item.get('alt',item['name']))
                if 'crop' in item:
                    crop=item['crop']
                    if any(not isinstance(crop.get(k),(int,float)) or not 0<=crop[k]<1 for k in ['left','top','right','bottom']) or crop['left']+crop['right']>=1 or crop['top']+crop['bottom']>=1:raise ValueError('Invalid image crop')
                    fill=pic.find('p:blipFill',NS);rect=fill.find('a:srcRect',NS)
                    if rect is None:
                        rect=E.Element(q('a:srcRect'));fill.insert(1,rect)
                    for key,side in [('l','left'),('t','top'),('r','right'),('b','bottom')]:rect.set(key,str(round(crop[side]*100000)))
        for lock in root.findall('.//a:spLocks',NS):lock.attrib.pop('noGrp',None)
        for edge in spec.get('edges',[]):
            conn=lookup(root,edge['name']); nv=conn.find('p:nvCxnSpPr/p:cNvCxnSpPr',NS)
            for tag,which,side in [('a:stCxn','from','fromSide'),('a:endCxn','to','toSide')]:
                target=lookup(root,edge[which]); geom=target.find('p:spPr/a:prstGeom',NS)
                if geom is None or geom.get('prst') not in ['rect','roundRect']:
                    raise ValueError('Compatibility adapter only supports rectangular connector endpoints')
                el=nv.find(tag,NS)
                if el is None:el=sub(nv,tag)
                el.set('id',ident(target));el.set('idx',str(SIDE[edge[side]]))
            line=conn.find('p:spPr/a:ln',NS)
            for end in list(line):
                if end.tag in [q('a:headEnd'),q('a:tailEnd')]:line.remove(end)
            arrow_width=edge.get('arrowWidth','sm');arrow_length=edge.get('arrowLength','sm')
            if arrow_width not in ['sm','med','lg'] or arrow_length not in ['sm','med','lg']:raise ValueError('Invalid arrow size')
            sub(line,'a:tailEnd',type='triangle',w=arrow_width,len=arrow_length)
        next_id=max(int(n.get('id')) for n in root.findall('.//p:cNvPr',NS))+1
        for group in spec.get('groups',[]):
            members=[lookup(root,n) for n in group['children']]
            if any(s.getparent() is not tree for s in members):raise ValueError('Groups must contain top-level objects')
            boxes=[bounds(s) for s in members]
            if any(b is None for b in boxes):raise ValueError('Missing group bounds')
            x=min(b[0] for b in boxes);y=min(b[1] for b in boxes)
            w=max(b[0]+b[2] for b in boxes)-x;h=max(b[1]+b[3] for b in boxes)-y
            grp=E.Element(q('p:grpSp'));nv=sub(grp,'p:nvGrpSpPr');sub(nv,'p:cNvPr',id=next_id,name=group['name']);next_id+=1
            sub(nv,'p:cNvGrpSpPr');sub(nv,'p:nvPr');pr=sub(grp,'p:grpSpPr');tr=sub(pr,'a:xfrm')
            sub(tr,'a:off',x=x,y=y);sub(tr,'a:ext',cx=w,cy=h);sub(tr,'a:chOff',x=x,y=y);sub(tr,'a:chExt',cx=w,cy=h)
            index=min(tree.index(s) for s in members)
            for s in sorted(members,key=lambda s:tree.index(s)):grp.append(s)
            tree.insert(index,grp)
        parts[part]=serial(root)
    parts=normalized_parts(parts)
    validation=validate_parts(parts)
    if not validation['passed']:
        details=validation['errors']+validation['uncheckedParts']
        raise ValueError('Generated package failed XSD validation: '+json.dumps(details,ensure_ascii=False))
    save(parts,destination,canonical=True)

def inspect(file,contract=None):
    parts=load(file);pres=xml(parts['ppt/presentation.xml']);size=pres.find('p:sldSz',NS)
    result={'file':str(Path(file).resolve()),'sha256':sha(Path(file).read_bytes()),'sizePx':[int(size.get(k))/EMU for k in ['cx','cy']],'slides':[],'errors':[],'warnings':[]}
    try:
        _,children,order=presentation_sequence(parts['ppt/presentation.xml'])
        if children!=sorted(children,key=lambda c:order[c.tag]):
            result['errors'].append('ppt/presentation.xml: children violate ECMA-376 schema order; normalize to a new file')
    except ValueError as error:result['errors'].append('ppt/presentation.xml: '+str(error))
    contracts=(contract or {}).get('slides',[]);ordered=slides(parts)
    if contract and len(contracts)!=len(ordered): result['errors'].append('contract slide count mismatch')
    for i,part in enumerate(ordered):
        root=xml(parts[part]);objects=shapes(root);records=[node_record(s) for s in objects]
        ids={ident(s):s for s in objects}; names=[name(s) for s in objects]
        errs=[];warn=[];edges=[]
        if len(ids)!=len(objects):errs.append('duplicate object IDs')
        if len(names)!=len(set(names)):warn.append('duplicate names: resolve by current IDs + fingerprint; never guess')
        for s in objects:
            if s.tag!=q('p:cxnSp'):continue
            start=s.find('.//a:stCxn',NS);end=s.find('.//a:endCxn',NS)
            if start is None or end is None or start.get('id') not in ids or end.get('id') not in ids:
                errs.append(f'{name(s)}: dangling connector');continue
            ln=s.find('p:spPr/a:ln',NS);head=ln.find('a:headEnd',NS);tail=ln.find('a:tailEnd',NS)
            edge={'name':name(s),'from':name(ids[start.get('id')]),'to':name(ids[end.get('id')]),'fromIdx':start.get('idx'),'toIdx':end.get('idx'),'directed':tail is not None and tail.get('type') not in ['none',None] and (head is None or head.get('type')=='none')};edges.append(edge)
        for s in objects:
            if s.getparent().tag!=q('p:spTree'):continue
            b=bounds(s)
            if b and (b[0]<-EMU or b[1]<-EMU or b[0]+b[2]>(result['sizePx'][0]+1)*EMU or b[1]+b[3]>(result['sizePx'][1]+1)*EMU):errs.append(f'{name(s)} outside canvas')
        if i<len(contracts):
            c=contracts[i]
            for n,t in c.get('nodes',{}).items():
                found=[r for r in records if r['name']==n]
                if len(found)!=1 or found[0]['text']!=t:errs.append(f'content mismatch: {n}: expected {t!r}')
            actual={(e['from'],e['to']) for e in edges if e['directed']}
            expected={tuple(e) for e in c.get('edges',[])}
            for edge in expected-actual:errs.append(f'missing directed edge: {edge}')
            if c.get('exactEdges',True):
                for edge in actual-expected:errs.append(f'unexpected directed edge: {edge}')
                if len(edges)!=len(expected):errs.append('edge count or direction mismatch')
            for n in c.get('groups',[]):
                if not any(r['name']==n and r['kind']=='grpSp' for r in records):errs.append(f'missing native group: {n}')
            if c.get('nativeOnly',True) and any(r['kind'] in ['pic','graphicFrame'] for r in records):errs.append('unexpected image or graphic frame')
        result['slides'].append({'slide':i+1,'part':part,'objects':records,'edges':edges,'counts':{k:sum(r['kind']==k for r in records) for k in ['sp','cxnSp','grpSp','pic','graphicFrame']},'errors':errs,'warnings':warn})
        result['errors'] += [f'slide {i+1}: {e}' for e in errs];result['warnings'] += [f'slide {i+1}: {e}' for e in warn]
    result['passed']=not result['errors'];return result

def anchor(b,idx):
    x,y,w,h=b
    return [(x+w//2,y),(x,y+h//2),(x+w//2,y+h),(x+w,y+h//2)][int(idx)]
def unrotated(node):
    tr=xfrm(node)
    return tr is not None and int(tr.get('rot','0'))==0 and all(tr.get(k,'false') in ('0','false') for k in ('flipH','flipV'))

def movable_endpoint(node,site):
    geom=node.find('p:spPr/a:prstGeom',NS)
    return (node.tag==q('p:sp') and node.getparent().tag==q('p:spTree')
            and geom is not None and geom.get('prst') in ('rect','roundRect')
            and site in ('0','1','2','3') and bounds(node) is not None and unrotated(node))

def patch(source,destination,plan):
    raw=Path(source).read_bytes()
    if sha(raw)!=plan['sourceSha256']:raise ValueError('Source changed since inspection; inspect latest file again')
    parts=load(source);original=parts.copy();roots={};changed=[];ordered=slides(parts)
    for op in plan['operations']:
        number=op['slide']
        if isinstance(number,bool) or not isinstance(number,int) or not 1<=number<=len(ordered):
            raise ValueError('Slide must be a one-based presentation-order integer')
        part=ordered[number-1]
        if op.get('part',part)!=part:raise ValueError('Slide part changed; inspect the current presentation order')
        if part not in roots:roots[part]=xml(parts[part])
        root=roots[part];matches=[s for s in shapes(root) if ident(s)==str(op['id']) and name(s)==op['name']]
        if len(matches)!=1:raise ValueError('Target no longer uniquely matches')
        target=matches[0]
        if node_record(target)['fingerprint']!=op['fingerprint']:raise ValueError('Target fingerprint changed')
        # One operation per object per plan; the inspected hash is consumed.
        if op['action']=='replace_text':
            old=op['old'];new=op['new']
            if not old:raise ValueError('Empty old text is unsupported')
            runs=[n for n in target.findall('p:txBody/a:p/a:r/a:t',NS) if old in (n.text or '')]
            if len(runs)!=1 or (runs[0].text or '').count(old)!=1:raise ValueError('Text spans runs or is ambiguous; use the native editor')
            runs[0].text=runs[0].text.replace(old,new,1)
        elif op['action']=='style_connector':
            if target.tag!=q('p:cxnSp'):raise ValueError('Connector styling requires a native connector')
            ln=target.find('p:spPr/a:ln',NS)
            if ln is None:raise ValueError('Connector has no line properties')
            width=op.get('widthPx')
            if not isinstance(width,(int,float)) or not math.isfinite(width) or not 0<width<=12:raise ValueError('Invalid connector width')
            for key in ['arrowWidth','arrowLength']:
                if op.get(key) not in ['sm','med','lg']:raise ValueError('Invalid arrow size')
            tail=ln.find('a:tailEnd',NS)
            if tail is None or tail.get('type') not in ['triangle','stealth','arrow']:raise ValueError('Expected an existing directional arrowhead')
            ln.set('w',str(round(width*EMU)));ln.set('cap','rnd')
            for join in list(ln):
                if join.tag in [q('a:round'),q('a:bevel'),q('a:miter')]:ln.remove(join)
            # Join precedes line ends in DrawingML's sequence.
            end_index=next((i for i,e in enumerate(ln) if e.tag in [q('a:headEnd'),q('a:tailEnd')]),len(ln))
            ln.insert(end_index,E.Element(q('a:round')))
            tail.set('w',op['arrowWidth']);tail.set('len',op['arrowLength'])
        elif op['action']=='move':
            if target.getparent().tag!=q('p:spTree') or target.tag not in [q('p:sp'),q('p:grpSp')]:raise ValueError('Move supports only top-level shapes/groups')
            tr=xfrm(target)
            if not unrotated(target):raise ValueError('Rotated/flipped move unsupported')
            affected={ident(target)}|{ident(s) for s in shapes(target)}
            linked=[s for s in shapes(root) if s.tag==q('p:cxnSp') and any(n.get('id') in affected for n in s.findall('.//a:stCxn',NS)+s.findall('.//a:endCxn',NS))]
            if target.tag==q('p:grpSp') and linked:raise ValueError('Moving connected groups requires native PowerPoint rerouting')
            if any(s.find('p:spPr/a:prstGeom',NS) is None or s.find('p:spPr/a:prstGeom',NS).get('prst')!='straightConnector1' for s in linked):raise ValueError('Move with routed connectors requires native PowerPoint')
            ids={ident(s):s for s in shapes(root)};endpoints=[]
            for conn in linked:
                ct=xfrm(conn)
                if conn.getparent().tag!=q('p:spTree') or ct is None or int(ct.get('rot','0'))!=0:
                    raise ValueError('Transformed/grouped connector move requires native PowerPoint')
                refs=[conn.find('.//'+tag,NS) for tag in ('a:stCxn','a:endCxn')]
                if any(ref is None or ref.get('id') not in ids for ref in refs):raise ValueError('Unresolved connected endpoint')
                a,b=[ids[ref.get('id')] for ref in refs]
                if not all(movable_endpoint(node,ref.get('idx')) for node,ref in zip((a,b),refs)):
                    raise ValueError('Rotated/flipped/grouped or unsupported connected endpoint requires native PowerPoint')
                endpoints.append((conn,a,b,refs))
            dx,dy=float(op['dx']),float(op['dy'])
            if not math.isfinite(dx+dy):raise ValueError('Nonfinite movement')
            off=tr.find('a:off',NS);off.set('x',str(int(off.get('x'))+round(dx*EMU)));off.set('y',str(int(off.get('y'))+round(dy*EMU)))
            for conn,a,b,(st,en) in endpoints:
                x1,y1=anchor(bounds(a),st.get('idx'));x2,y2=anchor(bounds(b),en.get('idx'))
                t=xfrm(conn);o=t.find('a:off',NS);ext=t.find('a:ext',NS)
                o.set('x',str(min(x1,x2)));o.set('y',str(min(y1,y2)));ext.set('cx',str(abs(x2-x1)));ext.set('cy',str(abs(y2-y1)))
                for key,val in [('flipH',x2<x1),('flipV',y2<y1)]:
                    t.attrib.pop(key,None)
                    if val:t.set(key,'1')
        else:raise ValueError(f"Unsupported action {op['action']}")
        changed.append({'slide':number,'part':part,'id':op['id'],'name':op['name'],'action':op['action']})
    for p,r in roots.items():parts[p]=serial(r)
    untouched=[p for p in parts if p not in roots]
    assert all(original[p]==parts[p] for p in untouched)
    save(parts,destination)
    return {'sourceSha256':sha(raw),'outputSha256':sha(Path(destination).read_bytes()),'changed':changed,'changedParts':list(roots),'untouchedPartsByteIdentical':len(untouched)}

def main():
    p=argparse.ArgumentParser(description=__doc__);subs=p.add_subparsers(dest='cmd',required=True)
    a=subs.add_parser('prepare');a.add_argument('source');a.add_argument('output');a.add_argument('--manifest',required=True)
    a=subs.add_parser('inspect');a.add_argument('source');a.add_argument('--contract');a.add_argument('--output')
    a=subs.add_parser('validate');a.add_argument('source');a.add_argument('--output')
    a=subs.add_parser('normalize');a.add_argument('source');a.add_argument('output');a.add_argument('--receipt')
    a=subs.add_parser('patch');a.add_argument('source');a.add_argument('output');a.add_argument('--plan',required=True);a.add_argument('--receipt')
    args=p.parse_args()
    if args.cmd=='prepare':prepare(args.source,args.output,json.loads(Path(args.manifest).read_text()));return
    dest=args.output if args.cmd in ('inspect','validate') else args.receipt
    protected=[args.source,getattr(args,'contract',None),getattr(args,'plan',None)]
    if args.cmd in ('patch','normalize'):protected.append(args.output)
    with report_output(dest,protected) as report:
        if args.cmd=='inspect':r=inspect(args.source,json.loads(Path(args.contract).read_text()) if args.contract else None)
        elif args.cmd=='validate':r=validate(args.source)
        elif args.cmd=='normalize':r=normalize(args.source,args.output)
        else:r=patch(args.source,args.output,json.loads(Path(args.plan).read_text()))
        out=json.dumps(r,ensure_ascii=False,indent=2)
        if report is not None:report.write(out)
        else:print(out)
    if args.cmd in ('inspect','validate') and not r['passed']:sys.exit(1)
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError) as e:sys.exit(str(e))
