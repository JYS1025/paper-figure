# Corrections from the independent skill review

Reviewed base: `1380c83f3b38ffe8154b26f647bf926cbc62b3dd`. Corrective validation: 2026-10-01. The current source and rebuilt Codex, Claude and Antigravity packages were tested locally. Source hashes, ZIP hashes and evidence hashes are in the [validation record](preservation-fixes-validation.json).

## Findings and changes

| Review finding | Correction | Verification |
|---|---|---|
| P1: inspection reports and patch receipts could replace a PPTX with JSON. | Reserve a new report exclusively before patching. Reject input/output collisions, existing reports, hard links and symbolic links. Remove the newly reserved receipt if patching fails. | CLI tests check nonzero failure, unchanged source bytes and no revised deck on rejection. Successful receipts match the saved PPTX hash. |
| P2: reordered slides could patch the wrong visible page. | Resolve `presentation.xml` slide IDs through presentation relationships. Inspection, patching, preparation, materialization and flow audits share that order. Receipts include the actual part; plans can verify it. | Reordered and nonnumeric slide-part fixtures run in all three editions. Missing/external/duplicate relationships fail before saving. A saved PDF confirms the first visible page changed and the second did not. |
| P2: whole-document equality checks conflicted with the intentional API/no-API modes. | Remove five prose-equality assertions. Keep engine, asset, content and preservation checks; add tests of actual behavior across editions. | 124 unit tests pass, including 54 new preservation cases and four packaging checks. The revised portable runner passes 33 checks on freshly built fixtures. |
| P3: Antigravity's missing-renderer error linked to the absent Claude guide. | Synchronize guide names in Python as well as documentation. Package validation checks script-embedded guide paths against files actually shipped. | A renderer-unavailable subprocess produces an existing guide path; a deliberately missing guide fails packaging validation. |
| Bounded risk: moving a shape connected to a rotated peer used unsupported geometry. | Reject moves involving rotated/flipped/grouped/nonrectangular endpoints, invalid sites, or transformed/routed connectors before saving. Document the native-editor boundary. | Negative cases preserve the source and create no output. Supported rectangular straight-connector moves still pass attachment checks. |

The rotation finding concerned unsupported cached geometry; the original review observed LibreOffice repairing the attachment. It was not evidence of confirmed visual corruption in every application.

## Guidance improvements

Revision instructions now define slide numbers as displayed positions, explain exclusive report paths and include the optional inspected part in the plan example. The portable reference cards no longer point to unshipped example names. All editions include a small grouped native-text subscript recipe with explicit limits; it is not an equation parser. The portable package version is 1.1.1.

The Codex image-draft requirement and the portable API/no-API selection remain distinct. Speculative API response changes and a broad rewrite of working visual guidance were not made. Live model access and agent behavior need their own execution evidence.

## Saved-output evidence

- Reordered deck: [source](validation/review-fixes/reordered-source.pptx), [patched PPTX](validation/review-fixes/reordered-fixed.pptx), [receipt](validation/review-fixes/reordered-receipt.json), [PDF](validation/review-fixes/reordered-fixed.pdf), [first page](validation/review-fixes/reordered-page-1.png), [second page](validation/review-fixes/reordered-page-2.png). Both previews were inspected; PDF text independently locates the patched label on page 1 only.
- Fresh complex replay: [PPTX](validation/review-fixes/replay.pptx), [PDF](validation/review-fixes/replay.pdf), [preview](validation/review-fixes/replay.png). It retains 196 native shapes, 10 connectors, 16 groups and one independent picture. Fourteen math regions pass the recorded size, character and font checks.
- [Unit-test log](validation/review-fixes/unit-tests.log), [33 portable checks](validation/review-fixes/portable-regression.json), [extracted-package execution](validation/review-fixes/packaged-checks.json), [math plan](validation/review-fixes/typography-plan.json) and [math results](validation/review-fixes/typography-audit.json).

The initial replay requested Times New Roman, but the current renderer substituted Liberation Serif. The [diagnostic](validation/review-fixes/font-substitution-diagnostic.json) correctly flagged all 14 regions. The technical fixture was then reauthored with Liberation Serif explicitly selected and reviewed; character and size thresholds were unchanged. Historical figures and earlier validation records were preserved. The replacement font was not silently added to a pass list for the original artifact.

## Reproduction and limits

Run `python3 -m unittest discover -s tests -v` with the project's test dependencies. `tests/test_preservation_guards.py` exercises 18 scenarios per edition against temporary copies of a saved fixture. `tests/test_skill_package.py` checks shipped references and the missing-renderer recovery path. These tests do not require live image credentials.

After shared portable edits, synchronize and package:

```sh
python3 scripts/sync-antigravity-port.py
python3 scripts/package-claude-skill.py --edition codex
python3 scripts/package-claude-skill.py --edition claude
python3 scripts/package-claude-skill.py --edition antigravity
```

The packaging command retains its historical filename and now handles all three editions. It checks each ZIP payload against source and excludes dependencies, caches and credential files. All three extracted packages generated a technical fixture and passed content/connector checks; their patchers also passed the original reordered-deck and report-collision reproductions. The extracted Antigravity plugin passed CLI validation without installation or activation.

The render evidence uses LibreOffice → PDF → Poppler. It is not a native PowerPoint screenshot or manual edit test. Real Claude/Antigravity agent execution, paid Gemini image generation, model-account access and Windows behavior remain unverified. No new image-model draft or comparative visual-quality result is claimed by this corrective test run.
