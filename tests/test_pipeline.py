import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/paper-figure/scripts'))
import pptx as P

ROOT=Path(__file__).resolve().parents[1]
SAMPLE=ROOT/'output/final/09-capabilities.pptx'
class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.dir=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def target(self,source,name,action='replace_text',**kw):
        r=P.inspect(source);n=next(s for s in r['slides'][0]['objects'] if s['name']==name)
        return {'sourceSha256':r['sha256'],'operations':[{'slide':1,'id':n['id'],'name':name,'fingerprint':n['fingerprint'],'action':action,**kw}]}
    def mutate(self,name,fn):
        parts=P.load(SAMPLE);root=P.xml(parts['ppt/slides/slide1.xml']);fn(root);parts['ppt/slides/slide1.xml']=P.serial(root);f=self.dir/name;P.save(parts,f);return f
    def contract(self):return json.loads(SAMPLE.with_suffix('.contract.json').read_text())
    def test_all_nine_content_contracts(self):
        files=sorted((ROOT/'output/final').glob('*.pptx'));self.assertEqual(len(files),9)
        for f in files:
            r=P.inspect(f,json.loads(f.with_suffix('.contract.json').read_text()));self.assertTrue(r['passed'],r['errors'])
            self.assertEqual(r['slides'][0]['counts']['pic'],0)
    def test_raw_export_bug_is_detected(self):
        r=P.inspect(ROOT/'tests/fixtures/raw-export-bug.pptx');self.assertFalse(r['passed']);self.assertTrue(any('dangling' in e for e in r['errors']))
    def test_missing_required_edge_fails(self):
        def change(r):s=P.lookup(r,'input-encoder');s.getparent().remove(s)
        f=self.mutate('missing.pptx',change);self.assertFalse(P.inspect(f,self.contract())['passed'])
    def test_reverse_arrow_fails(self):
        def change(r):s=P.lookup(r,'input-encoder').find('p:spPr/a:ln/a:tailEnd',P.NS);s.tag=P.q('a:headEnd')
        f=self.mutate('reverse.pptx',change);self.assertFalse(P.inspect(f,self.contract())['passed'])
    def test_dangling_reference_fails(self):
        f=self.mutate('dangling.pptx',lambda r:P.lookup(r,'input-encoder').find('.//a:stCxn',P.NS).set('id','9999'))
        self.assertFalse(P.inspect(f)['passed'])
    def test_duplicate_ids_fail(self):
        f=self.mutate('duplicate.pptx',lambda r:P.props(P.lookup(r,'encoder')).set('id',P.ident(P.lookup(r,'input'))))
        self.assertFalse(P.inspect(f)['passed'])
    def test_text_contract_failure(self):
        f=self.mutate('wrongtext.pptx',lambda r:setattr(P.lookup(r,'encoder').find('.//a:t',P.NS),'text','Wrong model'))
        self.assertFalse(P.inspect(f,self.contract())['passed'])
    def test_text_patch_preserves_every_other_object_and_part(self):
        plan=self.target(SAMPLE,'encoder',old='Encoder',new='New encoder');out=self.dir/'edit.pptx';receipt=P.patch(SAMPLE,out,plan)
        before=P.load(SAMPLE);after=P.load(out);self.assertEqual(receipt['changedParts'],['ppt/slides/slide1.xml'])
        for part in before:
            if part!='ppt/slides/slide1.xml':self.assertEqual(before[part],after[part])
        a=P.xml(before['ppt/slides/slide1.xml']);b=P.xml(after['ppt/slides/slide1.xml'])
        for s in P.shapes(a):
            if P.name(s)!='encoder':self.assertEqual(P.node_record(s),P.node_record(P.lookup(b,P.name(s))))
        self.assertEqual(P.text(P.lookup(b,'encoder')),'New encoder')
    def test_source_hash_rejects_stale_edit(self):
        plan=self.target(SAMPLE,'encoder',old='Encoder',new='Changed');plan['sourceSha256']='stale'
        with self.assertRaisesRegex(ValueError,'Source changed'):P.patch(SAMPLE,self.dir/'out.pptx',plan)
    def test_target_fingerprint_rejects_stale_object(self):
        plan=self.target(SAMPLE,'encoder',old='Encoder',new='Changed');plan['operations'][0]['fingerprint']='stale'
        with self.assertRaisesRegex(ValueError,'fingerprint'):P.patch(SAMPLE,self.dir/'out.pptx',plan)
    def test_refuses_overwrite(self):
        plan=self.target(SAMPLE,'encoder',old='Encoder',new='Changed')
        with self.assertRaises(FileExistsError):P.patch(SAMPLE,SAMPLE,plan)
    def test_straight_connector_follows_local_move(self):
        plan=self.target(SAMPLE,'encoder',action='move',dx=12,dy=20);out=self.dir/'move.pptx';P.patch(SAMPLE,out,plan)
        r=P.inspect(out,self.contract());self.assertTrue(r['passed']);d={s['name']:s for s in r['slides'][0]['objects']}
        self.assertEqual(d['encoder']['boundsPx'][:2],[273,120]);self.assertEqual(d['input-encoder']['boundsPx'][3],20)
    def test_native_group_translation(self):
        plan=self.target(SAMPLE,'token-group',action='move',dx=25,dy=-5);out=self.dir/'group.pptx';P.patch(SAMPLE,out,plan)
        d={s['name']:s for s in P.inspect(out)['slides'][0]['objects']};self.assertEqual(d['token-group']['boundsPx'][:2],[61,243]);self.assertEqual(d['token-group.0']['text'],'1')
    def test_routed_move_is_rejected(self):
        f=ROOT/'output/final/02-branch.pptx';plan=self.target(f,'local',action='move',dx=10,dy=10)
        with self.assertRaisesRegex(ValueError,'routed'):P.patch(f,self.dir/'out.pptx',plan)
    def test_actual_powerpoint_edit_survives_patch(self):
        f=ROOT/'output/powerpoint-source-snapshot.pptx';r=P.inspect(f);d={s['name']:s for s in r['slides'][0]['objects']}
        self.assertEqual(d['encoder']['text'],'Encoder edited');self.assertNotEqual(d['encoder']['boundsPx'][1],100)
        plan=self.target(f,'output',old='Output y',new='Result y');out=self.dir/'preserved.pptx';P.patch(f,out,plan)
        e={s['name']:s for s in P.inspect(out)['slides'][0]['objects']}
        self.assertEqual(d['encoder'],e['encoder']);self.assertEqual(d['token-group'],e['token-group']);self.assertEqual(e['output']['text'],'Result y')
    def test_refined_examples_preserve_content_contracts(self):
        files=sorted((ROOT/'output/refined').glob('*.pptx'));self.assertEqual(len(files),8)
        for f in files:
            r=P.inspect(f,json.loads(f.with_suffix('.contract.json').read_text()))
            self.assertTrue(r['passed'],r['errors'])
            self.assertEqual(r['slides'][0]['counts']['pic'],3 if f.stem=='02-branch' else 0)
    def test_photo_crop_survives_export_as_editable_metadata(self):
        parts=P.load(ROOT/'output/refined/02-branch.pptx');r=P.xml(parts['ppt/slides/slide1.xml'])
        pic=P.lookup(r,'detail-photo');crop=pic.find('p:blipFill/a:srcRect',P.NS)
        self.assertEqual(dict(crop.attrib),{'l':'29000','t':'2500','r':'38000','b':'63000'})
        self.assertEqual(P.lookup(r,'local-roi').tag,P.q('p:sp'))
        self.assertEqual(P.lookup(r,'local').tag,P.q('p:sp'))
        original=(ROOT/'skills/paper-figure/assets/astronaut.png').read_bytes()
        self.assertIn(original,[b for n,b in parts.items() if n.startswith('ppt/media/')])
    def test_hybrid_figure_patch_preserves_photos_and_crops(self):
        f=ROOT/'output/refined/02-branch.pptx';out=self.dir/'hybrid.pptx'
        plan=self.target(f,'local',old='Local encoder',new='Detail encoder');P.patch(f,out,plan)
        a=P.load(f);b=P.load(out)
        for n in a:
            if n!='ppt/slides/slide1.xml':self.assertEqual(a[n],b[n])
        ar=P.xml(a['ppt/slides/slide1.xml']);br=P.xml(b['ppt/slides/slide1.xml'])
        for name in ['input-photo','detail-photo','context-photo','local-roi']:
            self.assertEqual(P.node_record(P.lookup(ar,name)),P.node_record(P.lookup(br,name)))
    def test_crop_manifest_rejects_wrong_picture_order(self):
        f=ROOT/'output/refined/02-branch.pptx';r=P.inspect(f)
        items=[{'name':s['name'],'bounds':s['boundsPx']} for s in r['slides'][0]['objects'] if s['kind']=='pic']
        items[0],items[1]=items[1],items[0]
        with self.assertRaisesRegex(ValueError,'Image order/bounds mismatch'):
            P.prepare(f,self.dir/'wrong-crop.pptx',{'slides':[{'images':items}]})
    def test_arrow_styling_preserves_direction_geometry_and_other_objects(self):
        plan=self.target(SAMPLE,'input-encoder',action='style_connector',widthPx=2.6,arrowWidth='med',arrowLength='med')
        out=self.dir/'styled.pptx';P.patch(SAMPLE,out,plan)
        a=P.load(SAMPLE);b=P.load(out);ar=P.xml(a['ppt/slides/slide1.xml']);br=P.xml(b['ppt/slides/slide1.xml'])
        self.assertEqual(P.inspect(SAMPLE)['slides'][0]['edges'],P.inspect(out)['slides'][0]['edges'])
        for s in P.shapes(ar):
            t=P.lookup(br,P.name(s))
            if P.name(s)!='input-encoder':self.assertEqual(P.node_record(s),P.node_record(t))
            else:
                self.assertEqual(P.bounds(s),P.bounds(t));self.assertEqual(P.serial(s.find('p:nvCxnSpPr',P.NS)),P.serial(t.find('p:nvCxnSpPr',P.NS)))
                self.assertEqual(t.find('p:spPr/a:ln',P.NS).get('w'),str(round(2.6*P.EMU)))
        for name in a:
            if name!='ppt/slides/slide1.xml':self.assertEqual(a[name],b[name])
    def test_arrow_styling_rejects_bad_target_and_width(self):
        for name,width in [('encoder',2.6),('input-encoder',float('nan')),('input-encoder',0)]:
            plan=self.target(SAMPLE,name,action='style_connector',widthPx=width,arrowWidth='med',arrowLength='med')
            with self.assertRaises(ValueError):P.patch(SAMPLE,self.dir/'invalid.pptx',plan)
            self.assertFalse((self.dir/'invalid.pptx').exists())

if __name__=='__main__':unittest.main(verbosity=2)
