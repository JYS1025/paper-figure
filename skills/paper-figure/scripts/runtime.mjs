import path from 'node:path';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs';
// Resolve bundled dependencies without installing or redistributing them.
export async function artifact() {
  try { return await import('@oai/artifact-tool'); }
  catch (e) {
    const root=process.env.ARTIFACT_NODE_MODULES;
    if (!root) throw new Error('Set ARTIFACT_NODE_MODULES to Node.js packages from load_workspace_dependencies. '+e.message);
    const dir=path.join(root,'@oai/artifact-tool');
    const pkg=JSON.parse(fs.readFileSync(path.join(dir,'package.json'),'utf8'));
    return import(pathToFileURL(path.join(dir,pkg.module||pkg.main||'dist/artifact_tool.mjs')).href);
  }
}
export const python=process.env.FIGURE_PYTHON||'python3';
