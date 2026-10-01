# Reference cards

These are our interpretations of published figures. They are not rules endorsed by the paper authors. Use the original for visual study; generate original native elements for the user's content. No source images are redistributed with this skill.

## State changes: MAE

- Original: [MAE architecture](https://arxiv.org/html/2111.06377v3/arch.png).
- Meaning: visible/masked patch states and the transformations from input through representation to reconstruction.
- Layout principle: align consecutive states and make the encoder/decoder asymmetry visible. Preserve the identity of recurring tokens.
- Color/shape: colors distinguish token state; varying module scale can distinguish their roles. Decorative color cycling would destroy that meaning.
- Suitable: masking, selection, compression, reconstruction, staged transformations.
- Misuse: coloring unrelated modules like patch states, implying a state change that the method does not have, or copying original module proportions when they are irrelevant.
- Native elements: `tokens()` with a named group and separately editable cells; rectangular modules. See `06-tokens`.

## Semantic consistency across panels: CLIP

- Original: [CLIP diagrams](https://arxiv.org/html/2103.00020v1/main-diagrams.png).
- Meaning: image and text branches and their pairwise correspondence.
- Layout principle: separate views of a method into readable panels while keeping roles consistent; label matrix axes and the reading order.
- Color/shape: modality color remains stable across panels; the matrix highlights correspondence rather than embellishment.
- Suitable: paired inputs, matching, contrastive objectives, training/application views.
- Misuse: reusing the same color for a different role in the next panel; dropping negative pairs or objective details that are essential to the supplied method.
- Native elements: `panel()`, `matrix()`, labeled modules. See `05-panels`.

## Relationships expressed spatially: U-Net

- Original: [U-Net architecture](https://lmbweb.informatik.uni-freiburg.de/people/ronneber/u-net/u-net-architecture.png).
- Meaning: encoder/decoder symmetry, resolution changes and matching skip levels.
- Layout principle: pair related levels and align skip endpoints. Reserve a lane for each connection; module size can encode scale if explicitly labeled.
- Color/shape: consistent operation roles; shape size expresses a quantity only when the reader is told what it means.
- Suitable: multiscale encoders, decoders, hierarchical processing, paired routes.
- Misuse: symmetric layout suggesting a nonexistent symmetry; blindly reproducing tiny original numeric labels at an unreadable publication size.
- Native elements: rectangles of chosen sizes, connectors with selected sides, level annotations. See `04-skip`.

## Hierarchy and repetition: Transformer

- Original: [Transformer architecture](https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png).
- Meaning: nested modules, repetition and residual pathways.
- Layout principle: one readable representative block plus a repeat count; separate main path from bypass lanes. Enclosure means containment, not automatically shared weights.
- Color/shape: operation colors remain consistent; connector style differentiates role when a legend or label makes the meaning clear.
- Suitable: repeated blocks, nested submodules, residual or conditioning paths.
- Misuse: turning repetition into a feedback loop; implying weight sharing merely by drawing one block; connecting a bypass to the wrong addition.
- Native elements: `panel()` with repeat label, `group()` for objects edited together, native connected arrows. See `03-repeat`.

## Related color strengths: RLDX-1

- Original: [Figure 2 overview](https://arxiv.org/html/2605.03269v2/fig2_overview_rldx.png), [Figure 3 architecture](https://arxiv.org/html/2605.03269v2/fig3_overview_architecture.png), visually inspected 2026-09-30.
- Meaning: nested model structure, recurring token families and supporting motion/memory modules.
- Color/shape: pale mint enclosures, lavender supporting regions, stronger teal blocks and purple/mint/blue tokens. Figure 2 gives all three stream modules the same lavender, grouping their structural role.
- Suitable: maintaining a related palette across a broad overview and a denser detail view.
- Misuse: giving every modality a new hue automatically; importing the memory/stream structure into a method without it; claiming that the adapted HEX values are author-specified.
- Reuse: [color books](color-books.md), especially `sage-lavender`, provide original palette values and application guidance rather than a copied diagram.

## Icon role and mathematical typography

The following originals were visually inspected on 2026-09-30. They are selected examples, not a survey of how often a style occurs across publications.

- [BLIP-2, Figures 1–2](https://arxiv.org/html/2301.12597v3): small flat snowflakes mark frozen modules while photographs supply image content. The state symbol and the observed scene have different visual roles.
- [Flamingo, Figure 3](https://arxiv.org/html/2204.14198v2): repeated snowflakes and a legend identify frozen modules; photographic inputs remain concrete examples. A status pictogram need not become a detailed object illustration.
- [RLDX-1, Figures 2–3](https://arxiv.org/html/2605.03269v2): video frames supply observations; tokens, blocks and operation marks express internal structure. This reference does not imply that hardware icons are required.
- [CLIP, Figure 1](https://arxiv.org/html/2103.00020v1/main-diagrams.png): photographs, text examples and indexed correspondence entries serve distinct roles. Its small indices form a consistent notation system; matching the font style alone is not enough.
- [DiT, Figure 3](https://arxiv.org/html/2212.09748v2#S1.F3): ordinary module labels are distinct from the mathematical alpha/gamma/beta labels and their indices. Compare mathematical roles, script proportions and spacing, not just font family.

Apply these observations through [visual assets](visual-assets.md) and [mathematical typography](math-typography.md). Do not infer a mandatory serif font, pictogram quota or ban on richer scientific illustrations.

## Choosing instead of copying

Start from the content contract. Choose a reading path and one primary emphasis. Mix useful principles when the content needs it. A linear pipeline with no state information does not benefit from adding tokens merely to resemble MAE. A matrix is not required for every two-branch method. The reference cards guide judgment; they do not define four fixed templates.

## Direct visual observations from the revision review

The original images were opened and inspected on 2026-09-29. MAE shows photographic patches as well as abstract tokens; CLIP combines example media, text, embeddings and a fully indexed matrix. U-Net encodes spatial scale in feature-map geometry, while the Transformer gets detail from internal operations and exact joins. These differences were missing from the first all-box examples.

Use `examples/build-rich-examples.mjs` for revised demonstrations: 02 photograph/crop with native region marks, 04 scaled feature planes, 05 concrete paired patterns and a correspondence matrix, 06 stable token identities and weighted vectors, 07 irregular samples and aligned support. The original builder is a structural baseline, not a target for publication quality. See [visual design](visual-design.md) for representation choices and honest illustrative-data handling.
