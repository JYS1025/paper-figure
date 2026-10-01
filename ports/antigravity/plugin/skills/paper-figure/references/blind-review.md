# Blind source comparison and quality critique

Use when the user requests a blind comparison or verifier. For ordinary production use the local rendered review; do not create an extra evaluation project automatically.

## Prepare and separate the inputs

1. Select reference/generation pairs by relevant explanatory task before seeing verdicts. Prefer comparable content and abstraction levels. State differences in method, panel count, aspect ratio or crop. Do not add modules merely to match the reference.
2. Remove provenance labels, captions naming the source, filenames and metadata that reveal class. Use neutral pair IDs and randomized A/B positions. Preserve aspect ratio and use comparable presentation sizes. Save the answer key separately.
3. Keep internal labels for a typography/full-figure comparison. Mask them only when requested or when explicitly testing graphical structure alone. Apply the same masking policy to both sides and do not retouch or restyle their graphical content. Mask density can itself become a cue; acknowledge that limitation.
4. Give the evaluator only flattened comparison images and the prompt below. Do not provide raw PPTX/PDF layers that reveal covered content. Keep source names, answer keys, earlier verdicts and proposed fixes outside the evaluator context. Use a fresh context when an authorized callable evaluator is available; otherwise provide the prepared inputs and state that the model test was not run.
5. Save the unedited response before comparing it with the key. Record evaluator identity/settings when available, whether it shares the generator's model, the inputs, recognition from memory and any omitted evaluation. Do not claim a different model or service merely because the context is fresh.

## Evaluator prompt

Use the text below, replacing the masking sentence with the actual treatment. Do not include suggested flaws or desired answers.

> You are reviewing anonymized pairs of research figures. Each pair contains one published-paper figure and one generated figure, labeled A and B in randomized positions. You have no answer key or previous conversation.
>
> Provenance has been hidden. [State whether internal text is visible or masked.] Ignore masks, wrapper labels and file artifacts as evidence. Inspect only the supplied images; do not search for sources or inspect other files/metadata. If you recognize a composition from memory, explicitly record that separately from visual quality.
>
> For each pair, first commit to A or B as the probable published source and give subjective confidence. Then, independently, choose A, B, similar or insufficient evidence for visual quality. Published provenance does not imply superior quality.
>
> Identify up to three meaningful weaknesses in the side you infer is generated, if any. Do not invent criticisms to fill a quota. For each give location, visible evidence and its effect on interpretation. Say when a figure works adequately as an overview or when no strong defect is visible. Do not use “looks AI-generated,” complexity, number of shapes or the presence of a photograph as a standalone reason.
>
> Propose prioritized changes, each with a location, concrete edit, purpose and completion criterion. Distinguish a structural defect from a conditional explanation improvement or a finishing change. Condition any added merge operation, spatial correspondence, state change or value on the actual method; do not invent them. Preserve parts that already work.
>
> Trace main flow, branch/merge endpoints, collection scope, overview/detail relations, persistent item identity, and branch-to-matrix-axis correspondence where applicable. Distinguish one sample from a vector component. Assess whether changing arrow thickness alone would address an observed problem; inspect endpoints, routing, head size and role distinctions before recommending more weight. Essential emphasis should not depend only on hue.
>
> Do not infer a method error merely because masked labels prevent semantic interpretation. Do not force different methods to have the same complexity. Report a verdict table, pair-specific observations and actionable improvements, then limitations. State how recognition from memory, masking, scale or different content affects the interpretation of your judgments.

## Use the result

Treat source accuracy and quality preference as separate results. A correctly recognized famous architecture is not a quality measurement. For a useful follow-up, include less familiar references or compare different drawings of the same supplied content, using only authorized evaluation runs.

Convert justified observations into reusable generation/review decisions. Avoid a universal prescription such as “all arrows must be thick,” “always use photographs,” “add three panels,” or “all generated figures are deficient.” In a skill-development task, update the skill and its checks; do not make revised exhibit figures the deliverable unless requested.
