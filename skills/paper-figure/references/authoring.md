# Authoring and runtime

## Runtime

Use the runtime and libraries returned by `load_workspace_dependencies`; no package installation is needed in the validated environment. For the examples below, replace the placeholder paths with the returned Node/Python paths, the installed Paper Figure skill folder and the installed Presentations skill folder containing `container_tools/artifact_tool_utils.mjs`. Run from a writable task workspace; keep final output and private build files in separate directories, and choose fresh directories for each run.

The repository-root shortcuts `run-examples.sh`, `run-refined-examples.sh` and `run-feedback-examples.sh` are **repository-only and not included in the installed skill or ZIP**. Use the bundled builders directly after this one-time setup in the current shell:

```sh
FIGURE_SKILL_DIR="/absolute/path/to/installed/paper-figure"
FIGURE_TASK_DIR="/absolute/path/to/writable/task-workspace"
export ARTIFACT_NODE_MODULES="/absolute/path/to/bundled/node_modules"
export FIGURE_PYTHON="/absolute/path/to/bundled/python3"
export RUNTIME_NODE="/absolute/path/to/bundled/node"
export RUNTIME_NODE_MODULES="$ARTIFACT_NODE_MODULES"
export RUNTIME_PYTHON="$FIGURE_PYTHON"
export PRESENTATIONS_SKILL_DIR="/absolute/path/to/installed/presentations"
cd "$FIGURE_TASK_DIR"

"$RUNTIME_NODE" "$FIGURE_SKILL_DIR/examples/build-examples.mjs" \
  "$FIGURE_TASK_DIR/output/baseline-01" \
  "$FIGURE_TASK_DIR/.build/baseline-01"
```

This runs the simple structural baseline from either a CLI-installed or extracted skill. Its builders refuse existing output files.

For a new figure or substantial composition redesign, complete [the full image-model draft and transfer plan](image-first.md) before using this engine to author the PPTX. The helpers and example builders implement native reconstruction; they do not generate, inspect or enforce that earlier stage. Running an example builder alone is not the complete production workflow.

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

This writes an editable candidate. Apply the installed Presentations finalizer, semantic contract inspection and actual-file rendering before delivery. Examples demonstrate that complete path.

| Helper | Purpose and author control |
|---|---|
| `module(id,text,x,y,w,h,opts)` | Rectangular native shape with native text. Choose dimensions, fill, stroke, size, bold, padding. |
| `label(id,text,x,y,w,h,opts)` | Native textbox; choose alignment and deliberate line breaks. |
| `add(...)` | Lower-level native geometry; `valign` controls text position inside a representation's boundary. |
| `path(id,points,opts)` | Editable native custom path for curves, contours, dividers or feature geometry. These are not attached semantic connectors. |
| `image(id,bytes,x,y,w,h,opts)` | Independent picture object for a source sample or generated illustrative asset/icon; optional normalized `crop`. Preserve alpha/aspect ratio. Keep explanation objects native. Do not use pictures as connector endpoints. |
| `panel(id,title,x,y,w,h,opts)` | Native enclosure and label; the enclosure is not an editing group. |
| `tokens(id,labels,x,y,opts)` | Individually editable cells grouped together; states can be masked with `masked:[indices]`. |
| `matrix(id,rows,x,y,opts)` | Individually editable native cells; the author chooses highlight semantics. Not a statistical heatmap engine. |
| `group(id,children)` | One level of disjoint native PPT groups; the original child text remains editable. |
| `connect(id,from,to,opts)` | Native connector attached to rectangular endpoints. Choose sides, kind, color, `width` in px, dash, `arrowWidth` and `arrowLength` (`sm`, `med`, `lg`). Default: 2.6 px, medium triangle, round cap/join. Override by visual role. |

Names must be unique during creation. Groups may contain multiple existing top-level objects, and cannot overlap. Connector endpoints currently require rect/roundRect/textbox in the compatibility adapter. Use `fromSide`/`toSide` explicitly when ambiguity affects meaning. `tailEnd` points toward the destination in OOXML. Never infer direction merely from a connector's name.

`figure.mjs` leaves design decisions in the authoring code. It does not equalize every box, apply fixed palettes by index or infer scientific content. Panels, notes and repeated structures should be introduced only when they convey meaning. Long labels can wrap across intentional lines or use a wider module before reducing font size.

Before calling `connect`, decide whether its endpoint represents one item or a set and identify the visible boundary. Use the actual plane/module rectangle, or a logical port coincident with a visible set bracket/frame; do not attach to a remote caption textbox merely because it has the right semantic name. Keep dataflow connectors separate from non-data expansion guides. After export, run `scripts/flow_audit.py latest.pptx --output flow-audit.json` and inspect flagged locations in the saved render. See [relationship review](relationship-review.md) for scope and limits.

## Why a compatibility pass exists

In the validated runtime, raw export sometimes changed a shape's numerical ID without updating the connector endpoint reference. It also dropped an explicitly requested image crop. `pptx.py prepare` resolves actual IDs by unique names, fixes references, removes grouping locks, builds native groups, and writes verified picture names/crop metadata. Picture order is checked against declared bounds before applying crops. It only operates on newly generated candidates and refuses ambiguous matches. Never run this generation manifest over a file a person has edited. Package inspection validates the actual output independently.

For richer examples, use the same shell setup and the included builder:

```sh
"$RUNTIME_NODE" "$FIGURE_SKILL_DIR/examples/build-rich-examples.mjs" \
  "$FIGURE_TASK_DIR/output/rich-01" \
  "$FIGURE_TASK_DIR/.build/rich-01"
```

The builder uses native paths, editable pattern cells, feature planes, signals and a public NASA sample photo. Its figures are 672×400 px (177.8×105.8 mm). These demonstrate choices, not a required layout.

`examples/build-feedback-examples.mjs` revises four cases after the blind visual review: visible connector anchors, overview/detail correspondence, consistent token identities and branch-to-matrix axis flows. With the same shell setup, run:

```sh
"$RUNTIME_NODE" "$FIGURE_SKILL_DIR/examples/build-feedback-examples.mjs" \
  "$FIGURE_TASK_DIR/output/feedback-01" \
  "$FIGURE_TASK_DIR/.build/feedback-01"
```

It creates demonstration revisions; it is not a substitute for preserving an arbitrary human-edited source PPTX.

For formulas and indices, use [editable mathematical typography](math-typography.md). `label()` styles a whole textbox; it is not a math parser and does not expose mixed-script formatting. Treat `a_ci` or `t_now` in a brief as source notation, not finished typography. Literal underscores remain appropriate for actual identifiers. Use a verified native formatting/equation path, consistent script construction and actual-output font/size checks. Advanced mathematical layout is outside this helper's tested scope; do not silently rasterize it or describe text runs as OMML.
