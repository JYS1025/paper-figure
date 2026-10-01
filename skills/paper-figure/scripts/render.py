#!/usr/bin/env python3
"""Render a saved PPTX via the explicitly selected bundled LibreOffice.

No deck rewrite is performed. Output: PDF for QA, full PNG, publication PNG.
"""
import argparse,json,os,subprocess,tempfile
from pathlib import Path
from PIL import Image
from pptx import inspect

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source');p.add_argument('output_dir')
    p.add_argument('--soffice',default=os.environ.get('FIGURE_SOFFICE'))
    p.add_argument('--pdftoppm',default=os.environ.get('FIGURE_PDFTOPPM'))
    a=p.parse_args()
    if not a.soffice or not a.pdftoppm:p.error('Supply absolute bundled --soffice and --pdftoppm paths from load_workspace_dependencies')
    if not Path(a.soffice).is_absolute() or not Path(a.pdftoppm).is_absolute():p.error('Use absolute runtime paths')
    source=Path(a.source).resolve();out=Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=False)
    report=inspect(source)
    with tempfile.TemporaryDirectory(prefix='figure-render-',dir=out) as td:
        env=os.environ.copy();env['XDG_CACHE_HOME']=td
        proc=subprocess.run([a.soffice,'--headless','--convert-to','pdf','--outdir',str(out),str(source)],capture_output=True,text=True,env=env,timeout=90)
        (out/'renderer.log').write_text(proc.stdout+proc.stderr)
        pdf=out/(source.stem+'.pdf')
        if proc.returncode or not pdf.exists():raise RuntimeError('LibreOffice conversion failed; see renderer.log')
        subprocess.run([a.pdftoppm,'-png','-r','192',str(pdf),str(out/'slide')],check=True,capture_output=True,timeout=90)
    for i in range(1,len(report['slides'])+1):
        # Poppler zero-pads only for sufficiently long decks.
        matches=list(out.glob(f'slide-{i}.png')) or list(out.glob(f'slide-{i:02d}.png'))
        if len(matches)!=1:raise RuntimeError('Missing rendered slide')
        with Image.open(matches[0]) as im:
            im.resize(tuple(round(v) for v in report['sizePx']),Image.Resampling.LANCZOS).save(out/f'publication-{i}.png')
    (out/'render.json').write_text(json.dumps({'sourceSha256':report['sha256'],'renderer':'bundled LibreOffice → PDF → Poppler','canvasMm':[round(v*25.4/96,3) for v in report['sizePx']],'publicationPreviewDpi':96,'physicalSizeNote':'Screen pixels do not establish physical size; print at 100% or calibrate the display.'},indent=2))
    print(out)
if __name__=='__main__':main()
