# Authoring and runtime

## Runtime

Read [portable environment setup](antigravity-environment.md), then run `node scripts/preflight.mjs` from the skill directory. Prefer already installed public `pptxgenjs`, Python `lxml`, `Pillow` and `pdfplumber`; use the included dependency manifests only when needed and installation is available. `FIGURE_PYTHON` can select the actual Python executable. Node uses normal module resolution and honors `NODE_PATH` for existing shared packages. Do not assume a private runtime or a fixed installation path. Outputs must use new filenames/directories.

Choose a mode with [image options](image-options.md). In image-draft mode, complete [the full image-model draft and transfer plan](image-first.md) before using this engine. In no-API mode, proceed directly from the content contract, references and color roles. The helpers and example builders implement native reconstruction; they do not generate, inspect or enforce that earlier stage. Running an example builder alone does not establish that the reference review, selected mode or saved-file review was completed.

The engine is a small JS helper, not a layout language. Import `Figure` and `palette` from `scripts/figure.mjs`. Use CSS px at 96dpi: 1 px = 0.75 pt; 96 px = 25.4 mm. For a target width W mm use `W*96/25.4` px. A 672px canvas is 177.8mm wide; 12px text is 9pt at that size. Shrinking that whole figure to 88.9mm also halves the text. Do not assume a slide that looks readable when zoomed in will fit a single column.

## Choose colors explicitly

For generated pictures/icons plus native explanations, read [visual assets](visual-assets.md). Follow the reviewed [draft and transfer plan](image-first.md) when reconstructing the full composition. The content contract remains the source of scientific meaning, and explanatory text and diagram geometry must retain native editability.

The exported `palette` in `figure.mjs` is a compatibility default for older examples, not the required design palette. For new figures, read [color books](color-books.md) and load the selected recipe from the bundled JSON. Assign families to the current method's roles explicitly; do not index-cycle the colors through modules.

```js
const catalog = JSON.parse(await fs.readFile(
  new URL('../assets/color-books.json', figureModuleUrl), 'utf8'));
// figureModuleUrl is the file URL of scripts/figure.mjs in the installed skill.
const book = catalog.books.find(b => b.id === 'sage-lavender');
if (!book) throw new Error('Unknown color book');
const roles = { sharedModel: book.colors.sage, conditioning: book.colors.lavender };
f.module('model', 'Model', 220, 90, 150, 70, {
  fill: roles.sharedModel.fill, stroke: roles.sharedModel.stroke,
  color: book.neutral.ink
});
f.connect('encode', 'input', 'model', { color: book.neutral.connector });
```

Apply the chosen styles to all relevant labels, tokens, matrices and paths as well as modules; helpers otherwise retain their older defaults. If a convenience helper does not expose the needed colors (for example `matrix()`), create its native cells with `add()` using explicit styles. Use accents selectively on small marks. The catalog previews are color-use examples, not architecture templates.

## Small API

```js
const f = new Figure({width:672,height:280,font:'Arial',title:'Feature pipeline'});
f.module('input','Input',25,100,100,50,{fill:palette.gray});
f.module('encoder','Encoder',220,90,150,70,{bold:true});
f.module('output','Representation',465,100,175,50);
f.connect('encode','input','encoder');
f.connect('represent','encoder','output');
await f.export('/absolute/private-build/candidate.pptx');
```

This writes an editable candidate. Export automatically materializes native paths, connectors, groups and picture crop metadata. Then apply semantic contract inspection, flow audit and actual-file rendering before delivery. `examples/engine-smoke.mjs` tests the portable engine only; it is not a complete image-first figure workflow.

| Helper | Purpose and author control |
|---|---|
| `module(id,text,x,y,w,h,opts)` | Rectangular native shape with native text. Choose dimensions, fill, stroke, size, bold, padding. |
| `label(id,text,x,y,w,h,opts)` | Native textbox; choose alignment and deliberate line breaks. |
| `add(...)` | Lower-level native geometry; `valign` controls text position inside a representation's boundary. |
| `path(id,points,opts)` | Editable native custom path for curves, contours, dividers or feature geometry. These are not attached semantic connectors. |
| `image(id,bytes,x,y,w,h,opts)` | Independent picture object for a source sample or generated illustrative asset/icon; optional normalized `crop`, with `fit` set to `contain` (default), `cover` or `stretch`. Use PNG for alpha; PNG/JPEG are supported. Preserve aspect ratio unless deliberately stretching. Keep explanation objects native. Do not use pictures as connector endpoints. |
| `panel(id,title,x,y,w,h,opts)` | Native enclosure and label; the enclosure is not an editing group. |
| `tokens(id,labels,x,y,opts)` | Individually editable cells grouped together; states can be masked with `masked:[indices]`. |
| `matrix(id,rows,x,y,opts)` | Individually editable native cells; the author chooses highlight semantics. Not a statistical heatmap engine. |
| `group(id,children)` | One level of disjoint native PPT groups; the original child text remains editable. |
| `connect(id,from,to,opts)` | Native connector attached to rectangular endpoints. Choose sides, kind, color, `width` in px, dash, `arrowWidth` and `arrowLength` (`sm`, `med`, `lg`). Default: 2.6 px, medium triangle, round cap/join. Override by visual role. |

Names must be unique during creation. Groups may contain multiple existing top-level objects, and cannot overlap. Connector endpoints require rect/roundRect/textbox. `kind` accepts `straight` or `elbow`; elbows use attached native custom paths and support monotone routes between facing sides. A return path or complex obstacle route needs explicit visible intermediate ports or native PowerPoint editing; do not silently reverse or approximate it. Groups are disjoint and one level deep. Use `fromSide`/`toSide` explicitly when ambiguity affects meaning. `tailEnd` points toward the destination in OOXML. Never infer direction merely from a connector's name.

`figure.mjs` leaves design decisions in the authoring code. It does not equalize every box, apply fixed palettes by index or infer scientific content. Panels, notes and repeated structures should be introduced only when they convey meaning. Long labels can wrap across intentional lines or use a wider module before reducing font size.

Before calling `connect`, decide whether its endpoint represents one item or a set and identify the visible boundary. Use the actual plane/module rectangle, or a logical port coincident with a visible set bracket/frame; do not attach to a remote caption textbox merely because it has the right semantic name. Keep dataflow connectors separate from non-data expansion guides. After export, run `scripts/flow_audit.py latest.pptx --output flow-audit.json` and inspect flagged locations in the saved render. See [relationship review](relationship-review.md) for scope and limits.

## Native package materialization

PptxGenJS writes the standard PowerPoint package and native text/shapes/pictures. `materialize.py` creates editable DrawingML custom paths and true `p:cxnSp` connectors, preserves picture aspect ratios/crops, and passes the actual candidate to `pptx.py prepare`. That pass resolves endpoint IDs by unique names and builds native groups. It runs only on a newly generated candidate and refuses ambiguous matches. Never apply a creation manifest to a human-edited deck. The independent inspector and renderer read the saved result.

`scripts/flow_audit.py` also checks endpoint positions on unrotated native polyline connectors. It checks attachment coordinates, not obstacle avoidance, scientific meaning or how PowerPoint will reroute after a manual edit. Routed connector and connected-group moves stay outside the conservative patcher.

## Engine check and saved-file validation

From this skill directory, choose fresh output paths:

```sh
node examples/engine-smoke.mjs /absolute/work/engine-check.pptx
python3 scripts/pptx.py inspect /absolute/work/engine-check.pptx --contract /absolute/work/engine-check.contract.json --output /absolute/work/inspect.json
python3 scripts/flow_audit.py /absolute/work/engine-check.pptx --output /absolute/work/flow.json
python3 scripts/render.py /absolute/work/engine-check.pptx /absolute/work/render
```

Inspect the rendered images using the host's actual image-reading tool. The renderer writes a PDF, full-size PNGs, publication-size PNGs and the tested renderer/source hash. Use `--soffice-wrapper` when the host provides a Python rendering wrapper; see [environment setup](antigravity-environment.md). Rendering reads the saved PPTX without rewriting it. The smoke fixture tests engine features with a public NASA picture; it is not a composition to recycle and does not create an image-model draft. Independent scientific tasks are in `examples/tasks.json`.

For formulas and indices, use [editable mathematical typography](math-typography.md). `label()` styles a whole textbox; it is not a math parser and does not expose mixed-script formatting. Treat `a_ci` or `t_now` in a brief as source notation, not finished typography. Literal underscores remain appropriate for actual identifiers. Use a verified native formatting/equation path, consistent script construction and actual-output font/size checks. Advanced mathematical layout is outside this helper's tested scope; do not silently rasterize it or describe text runs as OMML.
