import {spawnSync} from 'node:child_process';
import {pptxgen,python} from './runtime.mjs';
const result={node:process.version,engine:null,python:null,imageGeneration:'Check the actual connected tool catalog. This script cannot verify a model connection.',scope:'Read-only dependency check; does not install packages or call image APIs.'};
try{const P=pptxgen();result.engine={available:true,version:new P().version};}catch(e){result.engine={available:false,error:e.message};}
const check=spawnSync(python,['-c',`import importlib.metadata as m, importlib.util, json, os, shutil, sys
modules={'lxml':'lxml','PIL':'Pillow','pdfplumber':'pdfplumber'}
deps={name: {'available':importlib.util.find_spec(name) is not None} for name in modules}
for name, package in modules.items():
 if deps[name]['available']:
  try: deps[name]['version']=m.version(package)
  except m.PackageNotFoundError: pass
wrapper=os.environ.get('FIGURE_SOFFICE_WRAPPER')
print(json.dumps({'executable':sys.executable,'dependencies':deps,'sofficeWrapper':wrapper,'soffice':os.environ.get('FIGURE_SOFFICE') or shutil.which('soffice') or shutil.which('libreoffice'),'pdftoppm':os.environ.get('FIGURE_PDFTOPPM') or shutil.which('pdftoppm')}))`],{encoding:'utf8'});
if(check.status===0){result.python=JSON.parse(check.stdout);}else{result.python={error:check.error?.message||check.stderr||'Python failed'};}
console.log(JSON.stringify(result,null,2));
if(!result.engine.available||!result.python.dependencies?.lxml.available||!result.python.dependencies?.PIL.available)process.exitCode=1;
