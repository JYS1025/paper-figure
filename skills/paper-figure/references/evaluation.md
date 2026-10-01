# Evaluation protocol

The eight tasks in `../examples/tasks.json` cover process, branching/merging, repetition, symmetry/skips, panels, tokens/matrix, long labels, and training/inference. They are synthetic scientific diagrams, not copies of reference figures. The ninth file is a capability probe.

## Four conditions for a future controlled model comparison

| Condition | Allowed additions to common brief |
|---|---|
| A | Generic PPT tooling only |
| B | A + the reference cards |
| C | B + small paper-figure helpers |
| D | C + render, critique and revise |

Use fresh independent contexts, identical specified model/version/reasoning settings, common content and publication size, same total time/token/tool-call budget, same fonts and rendering environment. Record all prompts and outputs, including failures. Count rendering/critique against D's total budget. Do not allow previous conditions' solutions to leak into later contexts. Randomize order and blind visual reviewers to condition labels. Keep raw scores per task and condition. With eight tasks, avoid population-level or statistical-generalization claims.

Check the current session's authorized evaluator capability before running an experiment. Availability and authorization are runtime facts, not permanent properties of the skill. If a callable evaluator is unavailable, keep the corresponding cells unmeasured and provide the reproducible protocol. Examples produced by one evolving conversation are demonstrations, not independent A/B/C/D observations; do not assign invented scores.

## Measures

- Semantic gate: required nodes, labels, direction and edges; training/inference distinction. Critical missing/reversed connections fail regardless of aesthetics.
- Visual: readability at target size, hierarchy, clear flow, meaningful emphasis, crossings, clipping and the applicable [relationship checks](relationship-review.md). Keep written observations beside ratings; allow similar quality and no major defect as legitimate outcomes.
- Native editing: select text and modify it; move module; move/edit grouped cells; verify connectors; save and reopen in named application/version.
- Preservation: start from a human-edited latest file, make one requested local edit, compare untouched parts and native app rendering.
- Effort: capture generation duration, review rounds and actual manual editing time. Do not infer human effort from code length or from automation action count.

Keep XML evidence, rendering evidence, native-app evidence and blind model evaluation in separate columns. Run failed/missing/reversed-edge and stale-patch negative controls so a broken checker cannot appear to pass everything.

## Published reference vs generated figure

This is a separate qualitative diagnostic, not a substitute for the four-condition experiment. Follow [blind review](blind-review.md) for input separation, masking, randomization, recognition bias and the reusable evaluator prompt. Report source choices, subjective confidence, remembered compositions, quality preferences and concrete feedback separately. Neither source accuracy nor a clean native-object audit is a publication-quality score.
