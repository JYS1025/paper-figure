# Color books for research diagrams

Use this reference when choosing or revising diagram colors. The reusable values are in [color-books.json](../assets/color-books.json); the visual catalog is [color-books.html](../assets/color-books.html). These are author-curated starting combinations, not official journal palettes or exact reproductions of the cited papers.

## Choose a family and assign meaning

Respect an existing manuscript palette and user-assigned meanings first. Otherwise choose a book that fits the diagram's relationships and desired emphasis. Do not choose randomly, cycle books merely for variety, or assign a new hue to each successive box. Pastel is neither a defect nor evidence of AI authorship. Palette choice alone cannot repair a generic composition or an ambiguous relationship.

| Book ID | Character | Useful starting context |
|---|---|---|
| `sage-lavender` | Mint/sage, lavender and steel blue; RLDX-inspired | Nested architecture, streams, memory and conditioning |
| `blue-apricot` | Cool blue against warm apricot, optional teal | Two complementary branches, encoding/decoding |
| `teal-coral` | Teal/coral representation states, neutral operators | Token selection, reconstruction, state changes |
| `plum-sand` | Warm violet, sand and slate | Language, retrieval, evidence and comparison |
| `moss-clay` | Earthy green, clay and blue-gray | Specimens, materials, devices and physical processes |
| `ink-cobalt` | Neutral structure with concentrated blue/orange | Dense figures or one principal contribution |
| `royal-wheat` | Solid royal blue and light cream; BLIP-2 | Existing backbone and a trainable bridge |
| `periwinkle-orchid` | Blue, orchid and rose; Flamingo | Repeated frozen/trainable components |
| `pistachio-rose` | Light green, sky and pink; SAM 2 subset | Recurring functional modules in video/memory |
| `cyan-lilac` | Cyan enclosure, lilac features and cream heads; Mask2Former subset | Overview/detail and multiscale representations |
| `amethyst-honey` | Purple outputs, gold operations and blue input; RT-2 | Token-to-action or heterogeneous outputs |
| `graphite-ochre` | Gray pool, ochre seed and red exclusion; DINOv2 | Curation, retrieval and explicit rejection |
| `celadon-blush` | Green/pink spaces with ice-blue transforms; Latent Diffusion | Distinct representation spaces |
| `sky-leaf` | Blue/green/amber operations, gray outer block; DiT | Repeated operation families and residual blocks |
| `olive-copper` | Olive/copper/blue routes on white; Mamba | State propagation and selection/control paths |
| `graphite-silver` | Gray models and white operations; DINO | Monochrome relational explanations |

These contexts are examples, not domain restrictions. Select only the needed hues, and add a compatible role if the content genuinely needs more categories. There is no three-color quota. Preserve one role's identity across overview/detail panels and before/after states unless a defined state change requires another encoding.

Distinguish books by **allocation**, not just their color names. For colored routes on white, consider `olive-copper`; for mostly neutral machinery with sparse selection/rejection marks, `graphite-ochre`; for a strong filled backbone against a light adapter, `royal-wheat`; for an explanation that needs no hue coding, `graphite-silver`. The ten added books record the directly inspected figure and the visual observation in each JSON `inspiration` entry and in the catalog's reference details. Read the chosen book's evidence before adapting its roles. Publication is not itself a quality score: retain the useful allocation principle and improve weak label/line contrast where needed.

In the private design plan, record the chosen book, a short reason, the role-to-family mapping, and what is neutral. For example: `sage-lavender; shared model=sage, conditioning=lavender, physical signals=steel; generic operations=neutral`. That mapping is authored for the current brief, not implied by the book. Equivalent stream modules may share a color; different inputs do not automatically require different module colors.

## Use the whole recipe, not just a list of HEX values

Each color family has three opaque RGB values:

- `fill`: broad shapes, feature planes and enclosures.
- `stroke`: visible boundaries and small outlines, paired with the fill.
- `accent`: small tokens, indicators and selected paths requiring more emphasis.

The neutral set supplies white canvas, dark `ink`, `secondary_text`, quiet `surface`, `stroke`, and `connector`. Use neutral dark text on light fills. Use the family stroke rather than a pale fill for a thin line. Treat accents as marks by default, not backgrounds for dark text; if text is placed on an accent, choose and verify its contrasting color separately.

An intentionally saturated module can be appropriate: `royal-wheat` demonstrates white text on its strong blue, following the type of contrast used by BLIP-2. Its sample's white/accent pairing is checked separately. The `preview` field controls catalog demonstrations only; it is not a scientific role mapping or an instruction to transplant the sample architecture. For `graphite-ochre`, vermilion is reserved for the explicit rejection example rather than assigned to a successful output merely because it is the third color.

Adjust color strength together with area, boundary weight and arrowheads. A broad pale enclosure can coexist with a strong small token of the same family. Use solid RGB values rather than stacking translucent layers whose appearance changes with overlap. A tinted container does not require all contained objects to repeat that tint. White gaps and neutral operators help the reader separate color roles. No fixed area percentage is required.

Do not transfer categorical diagram palettes to quantitative heatmaps. Select an appropriate sequential/diverging colormap separately when measured values are encoded. Photographic samples retain their meaningful colors; do not recolor evidence to match the book.

## What the RLDX reference actually shows

Visually inspected on 2026-09-30: [Figure 2](https://arxiv.org/html/2605.03269v2/fig2_overview_rldx.png) and [Figure 3](https://arxiv.org/html/2605.03269v2/fig3_overview_architecture.png), from the [RLDX-1 technical report](https://arxiv.org/html/2605.03269v2).

Figure 2 uses pale mint for the major model containers and pale lavender for supporting regions and stream modules. All three stream modules share lavender: color organizes structural role rather than assigning one unrelated hue per modality. Figure 3 extends the same visual vocabulary: a quiet mint enclosure, stronger teal transformer blocks, lavender support modules, blue physical-signal tokens, and purple/mint token families. Dark connectors and text remain legible against these light regions. Some source labels are purple; that is an observation, not a requirement to color all labels.

The transferable principle is consistent hue families at different strengths and scales. The `sage-lavender` book is an adaptation of that principle. Its HEX values were authored, not extracted from the original. It does not copy the architecture, typography, layout or scientific meaning.

## Check the actual use

View the saved figure at publication width. Check label contrast, thin boundaries, small tokens and intersections, not just large swatches. If two roles become hard to distinguish in grayscale, preserve their meaning with labels, lane position, shape or line pattern. When a critical distinction relies on hue, inspect a color-vision simulation of the actual figure or add sufficient non-color encoding. Similar-luminance fills are not necessarily bad when their identity is otherwise explicit.

The catalog's automatic checks cover RGB syntax and contrast of intended text/fill and boundary/fill pairs. They do not certify aesthetics, color-vision accessibility, print fidelity or the readability of a complete figure. State what was actually inspected. Palette-only recoloring should preserve the current file's objects, geometry, content and role identities.

Underlying guidance: [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/), [CUD accent/base colors](https://jfly.uni-koeln.de/colorset/), and [Okabe–Ito on small marks and redundant encoding](https://jfly.uni-koeln.de/color/).

## Maintaining the books

Edit the single JSON source, then run `python3 scripts/build_color_books.py` from the skill root to rebuild the self-contained HTML catalog, full overview, compact index, individual SVG cards and sheets of four books. This helper uses only Python's standard library. Its contrast targets (4.5 for text/fill, 3 for boundary/fill and accent/fill) are local screening heuristics, not general publication rules; it reports failures rather than silently changing colors. If a book is deliberately revised for a different application, review that application's actual pairings and adjust the screening accordingly. For a new paper-inspired book, record the actual inspected figure, observation and transfer decision; do not use a citation as decoration or claim invented HEX values were sampled.
