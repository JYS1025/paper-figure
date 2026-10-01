"""Skill checks use existing saved artifacts; no figures are created or edited."""
import hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/paper-figure/scripts'))
import pptx as P
import flow_audit as A

class FlowAudit(unittest.TestCase):
    def tree(self):return P.xml(P.load(ROOT/'output/feedback-revision/04-skip.pptx')['ppt/slides/slide1.xml'])
    def test_valid_references_can_still_attach_to_invisible_label_boxes(self):
        source=ROOT/'output/arrows/04-skip.pptx'
        self.assertTrue(P.inspect(source)['passed'])
        r=A.audit(source)
        self.assertEqual(r['summary']['connectors'],6)
        self.assertEqual(r['summary']['requiringRenderedReview'],6)
        self.assertTrue(all('from:transparent_boundary' in c['reviewReasons'] for c in r['connectors']))
        self.assertNotIn('passed',r)  # Diagnostic flags are not a quality verdict.
    def test_visible_feature_plane_anchors_are_not_false_positives(self):
        r=A.audit(ROOT/'output/feedback-revision/04-skip.pptx')
        self.assertEqual(r['summary'],{'connectors':6,'requiringRenderedReview':0,'geometryUnchecked':0})
    def test_displaced_connector_is_detected_in_memory(self):
        r=self.tree();off=P.xfrm(P.lookup(r,'down1')).find('a:off',P.NS)
        off.set('x',str(int(off.get('x'))+5*P.EMU))
        result=next(x for x in A.audit_tree(r) if x['name']=='down1')
        self.assertIn('from:endpoint_offset',result['reviewReasons'])
        self.assertAlmostEqual(result['endpointOffsetsPx']['from'],5)
    def test_group_transform_is_reported_as_unchecked(self):
        r=self.tree();group=P.lookup(r,'e1.features');off=P.xfrm(group).find('a:off',P.NS)
        off.set('x',str(int(off.get('x'))+12*P.EMU))
        result=next(x for x in A.audit_tree(r) if x['name']=='down1')
        self.assertEqual(result['geometryStatus'],'not_checked')
        self.assertIn('geometry:manual_check_required',result['reviewReasons'])
        self.assertNotIn('endpointOffsetsPx',result)
    def test_unresolved_target_is_reported_without_inventing_a_location(self):
        r=self.tree();P.lookup(r,'down1').find('.//a:endCxn',P.NS).set('id','999999')
        result=next(x for x in A.audit_tree(r) if x['name']=='down1')
        self.assertEqual(result['to']['status'],'missing_or_ambiguous_reference')
        self.assertEqual(result['geometryStatus'],'not_checked')
    def test_audit_preserves_saved_file_bytes(self):
        p=ROOT/'output/arrows/06-tokens.pptx';before=p.read_bytes();r=A.audit(p)
        self.assertEqual(p.read_bytes(),before)
        self.assertEqual(r['sourceSha256'],hashlib.sha256(before).hexdigest())
    def test_inherited_boundary_style_stays_unresolved(self):
        r=self.tree();node=P.lookup(r,'e1');sp=node.find('p:spPr',P.NS)
        for tag in ['a:solidFill','a:noFill','a:ln']:
            for element in sp.findall(tag,P.NS):sp.remove(element)
        self.assertEqual(A.boundary_state(node),'unspecified')

if __name__=='__main__':unittest.main(verbosity=2)
