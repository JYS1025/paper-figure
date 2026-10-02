# PPTX compatibility fix — 1.2.1

## Confirmed defect and remaining uncertainty

A reported Claude-edition file rendered in LibreOffice but failed to open in
desktop PowerPoint. The reported source file is not available in this checkout;
its OS, PowerPoint version, exact error and normalized/re-saved outcomes remain
pending. This release fixes a reproduced standards defect, without claiming to
have established the cause of that user's open failure.

Two minimal PptxGenJS 4.0.1 presentations, with and without an explicit
`addNotes()` call, both placed `notesMasterIdLst` after `sldIdLst`. Both failed
the official Transitional `pml.xsd`. The required sequence places notes masters
before slide IDs. Removing the skill's `addNotes()` call would not fix this
reproduction. Normative source: [ECMA-376 Part 4, Transitional XML schemas](https://ecma-international.org/publications-and-standards/standards/ecma-376/).

Both raw files also contained 19 ZIP directory entries and did not place
`[Content_Types].xml` first. Those layout differences alone have not been shown
to make a package invalid or cause the reported failure.

## Changes

- All three editions normalize new exports at the shared `prepare` stage,
  then validate XML against bundled official Transitional and OPC XSDs before
  writing the destination. No network connection is needed.
- Default `inspect` now detects the presentation child-order defect.
- `validate` reports per-part XSD results and unsupported XML explicitly.
  Schema-permitted extension namespaces are inventoried separately, because
  wildcard acceptance does not validate their internals. XSD success is not
  a complete OPC semantic check or a PowerPoint open test.
- `normalize` repairs the known order in a new file, canonicalizes ZIP layout
  and emits a receipt. Only `ppt/presentation.xml` may have a changed part
  payload. Existing output/report paths and the source are protected.
- Routine human-file `patch` retains its original preservation behavior. It
  does not silently apply package normalization.

The portable package version is 1.2.1; Codex includes the same compatibility
engine and schemas. Source hashes and notices accompany the 34 unmodified XSDs.

## Validation

207 regression tests passed, including 39 new cases across Codex, Claude and
Antigravity. These cover the negative order control, official schema rejection,
normalization idempotence, original-file and untargeted-payload preservation,
automatic export rejection, unknown XML/extension reporting, offline entity
handling and CLI output/report collision guards.

The fresh portable engine smoke fixture passed XSD validation and rendered via
LibreOffice → PDF → Poppler. The rendered preview retained native labels,
mathematical indices, paths, groups, attached arrows and the independent photo.
The local PowerPoint UI control failed to respond, so no native open/edit result
is claimed. Machine-readable results for minimal files and packaged editions
are in [the validation record](pptx-compatibility-validation.json).

## Update and recover a previous output

Update the installed edition using the [installation guide](installation.md#verify-and-update).
From that skill's directory:

```sh
python scripts/pptx.py normalize original.pptx normalized.pptx --receipt normalization.json
python scripts/pptx.py validate normalized.pptx --output normalized-xsd.json
```

Test `normalized.pptx` in the affected PowerPoint installation and retain the
original. If it still fails, record the exact error and compare a separate
LibreOffice re-save; that broader rewrite is a diagnostic candidate, not a
lossless repair. See [compatibility and recovery](../skills/paper-figure/references/pptx-compatibility.md)
for scope and next steps.
