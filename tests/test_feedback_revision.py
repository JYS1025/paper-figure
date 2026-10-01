import hashlib,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/paper-figure/scripts'))
import pptx as P
OUT=ROOT/'output/feedback-revision'

def root_of(stem): return P.xml(P.load(OUT/(stem+'.pptx'))['ppt/slides/slide1.xml'])
def marker(root,prefix):
    colors=[P.lookup(root,f'{prefix}.{r}.{c}').find('p:spPr/a:solidFill/a:srgbClr',P.NS).get('val') for r in range(5) for c in range(5)]
    return tuple(c.upper()!='EFF2F3' for c in colors)

class FeedbackRevision(unittest.TestCase):
    def test_four_native_content_contracts(self):
        files=sorted(OUT.glob('*.pptx'));self.assertEqual(len(files),4)
        for p in files:
            r=P.inspect(p,json.loads(p.with_suffix('.contract.json').read_text()))
            self.assertTrue(r['passed'],r['errors'])
            self.assertEqual(r['slides'][0]['counts']['pic'],0)
    def test_saved_connector_geometry_meets_visible_anchors(self):
        for p in OUT.glob('*.pptx'):
            root=root_of(p.stem);byid={P.ident(s):s for s in P.shapes(root)}
            for s in P.shapes(root):
                if s.tag!=P.q('p:cxnSp'):continue
                x,y,w,h=P.bounds(s);tr=P.xfrm(s)
                flipx,flipy=tr.get('flipH')=='1',tr.get('flipV')=='1'
                ends=[(x+(w if flipx else 0),y+(h if flipy else 0)),(x+(0 if flipx else w),y+(0 if flipy else h))]
                for tag,actual in zip(['a:stCxn','a:endCxn'],ends):
                    ref=s.find('.//'+tag,P.NS);target=byid[ref.get('id')]
                    expected=P.anchor(P.bounds(target),ref.get('idx'))
                    self.assertLessEqual(max(abs(a-b) for a,b in zip(actual,expected)),2,(p.name,P.name(s),tag))
                    visible_fill=target.find('p:spPr/a:solidFill',P.NS) is not None
                    visible_stroke=target.find('p:spPr/a:ln/a:solidFill',P.NS) is not None
                    self.assertTrue(visible_fill or visible_stroke,(p.name,P.name(target)))
    def test_token_identity_survives_selection_and_weight_pairing(self):
        r=root_of('06-tokens')
        patterns=[marker(r,f'tokens.{i}.key') for i in range(6)]
        self.assertEqual(len(set(patterns)),6)
        for i,t in enumerate([1,3,4,6]):
            self.assertEqual(patterns[t-1],marker(r,f'kept.{i}.key'))
            self.assertEqual(patterns[t-1],marker(r,f'selected-key{i}'))
        self.assertAlmostEqual(sum(float(P.text(P.lookup(r,f'weights.0.{i}'))) for i in range(4)),1)
    def test_correspondence_axes_keep_item_units_and_noncolor_diagonal(self):
        r=root_of('05-panels');sub=['₁','₂','₃','₄']
        for i in range(4):
            m=marker(r,f'sample{i}')
            for prefix in [f'caption-key{i}',f'col-key{i}',f'row-key{i}']:self.assertEqual(m,marker(r,prefix))
        for i in range(4):
            for j in range(4):
                s=P.lookup(r,f'scores.{i}.{j}')
                self.assertEqual(P.text(s),f'I{sub[i]}·T{sub[j]}')
                width=int(s.find('p:spPr/a:ln',P.NS).get('w'))/P.EMU
                self.assertAlmostEqual(width,1.3 if i==j else .4,places=3)
    def test_feature_dimensions_follow_stated_resolution_ratios(self):
        r=root_of('04-skip')
        dims=[P.bounds(P.lookup(r,n))[2:] for n in ['e1','e2','core','d2','d1']]
        self.assertEqual(dims,[[v*P.EMU,v*P.EMU] for v in [80,40,20,40,80]])
        for n in ['e1','e2','core','d2','d1']:self.assertEqual(P.text(P.lookup(r,n)),'')
    def test_single_step_is_distinct_from_full_sequence(self):
        r=root_of('03-repeat')
        self.assertEqual(P.text(P.lookup(r,'input-name')),'hₜ')
        self.assertEqual(P.text(P.lookup(r,'output-name')),'hₜ₊₁')
        self.assertEqual(P.text(P.lookup(r,'state-name0')),'h₀')
        self.assertEqual(P.text(P.lookup(r,'state-name4')),'h₄')
        self.assertIn('× 4',P.text(P.lookup(r,'block.title')))
        sources={P.lookup(r,n).find('.//a:stCxn',P.NS).get('id') for n in ['residual','e0']}
        self.assertEqual(sources,{P.ident(P.lookup(r,'fork'))})
    def test_previous_review_sources_remain_unchanged(self):
        key=json.loads((ROOT/'docs/validation/blind-evaluation/answer-key.json').read_text())
        for p in key['pairs']:
            source=ROOT/f"output/arrows/{p['generated']}.pptx"
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),p['generated_pptx_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)
