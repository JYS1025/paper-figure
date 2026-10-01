import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
export function pptxgen() {
  try { const lib=require('pptxgenjs'); return lib.default||lib; }
  catch (error) { throw new Error('PptxGenJS is unavailable. Use existing host packages, or install this skill package locally where permitted. See references/claude-environment.md.', {cause:error}); }
}
export const python=process.env.FIGURE_PYTHON||'python3';
