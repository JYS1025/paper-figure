# Plan and review the relationships

Use this before laying out a figure and when reviewing its saved render. Apply only rows relevant to the method. A simple overview need not expose every internal operation.

## Before drawing: a compact private plan

Record the following alongside the content contract; it is an authoring aid, not another document the user must approve.

| Question | Decision needed |
|---|---|
| What does one mark mean? | Sample, token, vector, vector component, feature plane, operation or illustrative identity marker. Do not silently change this unit between views. |
| What does each edge carry? | One item, a named collection, a control signal, a gradient or a relationship callout. Distinguish process flow from an expansion guide. |
| Where does it attach? | Visible source and destination boundary, or a port on a visibly delimited set. A transparent textbox used for a caption is not a substitute for the represented object. |
| What stays the same? | Stable item identity or spatial correspondence across states. Use labels, position, patterns or small markers as needed; do not imply a correspondence the brief does not specify. |
| What changes? | Selection, spatial resolution, representation, weighting, repetition or another stated transformation. Show the relevant change; omit decorative changes. |
| What defines the state? | Distinguish a measured property, a classification and an acquisition/processing status. A change of fill after measurement need not mean that the item's physical contents changed. Define decision symbols and state encodings in the figure or its adjacent caption; for standalone use, keep the necessary definitions with the figure. |
| Which detail belongs where? | Link an expanded block to its actual overview region. Separate one-step input/output from whole-sequence input/output. |
| What is unknown? | Record unspecified merge operators, channel counts or measured values. Show known inputs without inventing addition, concatenation or results. Ask only if the missing fact is necessary to complete the requested explanation. |

Then describe the central relationship in one sentence. If the composition would not help a reader understand that relationship, choose a more suitable representation before adding styling.

## Review the saved render

| Applicable structure | Observable acceptance check |
|---|---|
| Main flow or bottleneck | Trace input to output. Every line visibly begins and ends at its intended object; no stage relies on an unexplained gap. Check the actual marks, not only connector IDs. |
| Branch / multiple inputs | A shared input has a clear departure point. Distinct incoming paths have identifiable entry sites. Display the merge operation only when it is defined. |
| Collection input | Point to exactly which items the outgoing arrow includes. A bracket, alignment or common boundary must make that scope unambiguous; a frame is not mandatory. |
| Overview + detail | Identify the expanded region without guessing. Callout style must not imply an extra computational dependency. Repetition and weight sharing remain distinct. |
| Selection / repeated items | Pick one retained output item and trace its identity back to its input. Markers may stand for identity, not invented numerical features. |
| Status / decision encoding | At intended publication size and in grayscale, distinguish every essential state in both marks and legend. In particular, unmeasured/pending must not collapse into negative/empty. If pale versus white fails, adjust lightness or add a defined non-color cue without implying a new material or biological component. |
| Delayed measurement / actuation | When the method explicitly depends on a delayed decision, identify which sample or timestamp the action belongs to. Add timing, buffering or tracking detail only if supplied and relevant to the explanation; a spatially separated detector and actuator alone does not justify inventing a delay module or numeric latency. A functional overview can be adequate without this detail. |
| Pairwise matrix | Pick any cell and trace its row and column to the two source items. Keep sample count distinct from vector dimension. Important diagonal/group structure survives removal of color. |
| Spatial hierarchy | If drawn dimensions claim to encode a ratio, they follow the declared quantity. Otherwise mark the scale as schematic. Stack thickness must not assert an unspecified channel count. |
| Connector styling | At publication size, inspect shaft/head proportions, entry clearance, lanes and role distinctions. Thicken only when visibility is the observed problem; thickness cannot repair missing scope or correspondence. |

Temporarily cover labels when useful to diagnose dependence on text, but perform the final readability review with labels visible. Label-free uncertainty does not prove the fully labeled figure lacks an explanation. Reduced grayscale is a structural check, not proof that all text remains legible at half width.

## Act on findings proportionally

- **Structural defect:** a required relation is missing/reversed, an attachment visibly lands on the wrong object, or the mark's unit changes inconsistently. Repair before delivery.
- **Conditional explanation improvement:** the purpose may benefit from a more explicit merge, spatial correspondence or state detail. Check the method first; do not invent it. An adequate overview may need no such addition.
- **Finishing change:** a slight diagonal, clearance or emphasis issue that does not alter interpretation. Fix locally when useful, preserving clear parts of the figure.

Keep each observation concrete: **location → visible evidence → effect on interpretation → proposed change → completion criterion**. Finding no important defect is a valid result. Do not equate recognizable paper provenance with superior quality or require a simple figure to match a more complex method's module count.

## Reusable artifact check

Run the read-only audit on the latest saved file:

```sh
python scripts/flow_audit.py latest.pptx --output flow-audit.json
```

It reports the saved file hash, each native connector's endpoints, directly declared boundary visibility and endpoint coordinate differences for supported rectangular shapes. It flags transparent anchors even when their native references are valid. A transparent proxy may coincide with a valid visible bracket or image; inspect that case in the render instead of adding a box automatically. Rotated/scaled group spaces and unsupported connector geometry are reported as unchecked. Inherited styles can leave visibility unresolved.

Resolve every relevant flag through a correction or a specific rendered observation. A clean audit does not verify set membership, item identity, matrix meaning, typography or overall aesthetics; those remain part of the review above.
