# PPTX compatibility and recovery

Keep four kinds of evidence separate: content/connector inspection, XML schema
validation, rendering, and opening the saved file in desktop PowerPoint.
LibreOffice rendering is **not proof that PowerPoint can open the file**. Passing
XSDs also does not establish rendering, editing behavior or all OPC constraints.
Record the application, version and OS for any actual desktop open test; otherwise
state that PowerPoint opening is unverified.

## New figures

`Figure.export()` uses `pptx.py prepare` to finalize generated files. This step
orders `ppt/presentation.xml` children according to ECMA-376, writes
`[Content_Types].xml` first, omits ZIP directory entries and checks XML against
the bundled Transitional and OPC schemas before writing the destination. A
schema error or incomplete XML coverage stops the export. Do not bypass this
failure by delivering the raw temporary PptxGenJS output.

Run the checks again on the final saved file and retain their reports:

```sh
python scripts/pptx.py inspect figure.pptx --contract figure.contract.json --output inspect.json
python scripts/pptx.py validate figure.pptx --output xsd.json
python scripts/flow_audit.py figure.pptx
```

The schema check runs offline with `lxml`. Its report lists checked XML parts,
schema errors and XML with no applicable bundled schema. XML is identified by
content types and `.xml`, `.rels`, `.vml` and `.svg` suffixes. XML parts with
unknown root namespaces make coverage incomplete and return a nonzero exit status.
Schema-permitted extension elements are inventoried in `unvalidatedExtensions`:
an XSD pass can allow those through wildcards without validating their internals.
Markup Compatibility is not preprocessed; Microsoft extensions and Strict OOXML
may therefore be unsupported. Such a result is a validation limit, not proof
that a human-authored PowerPoint file is corrupt. Never strip those elements to
obtain a passing result. Embedded packages are not recursively validated.

Schemas are unmodified official files; sources, hashes and third-party notices
are bundled in `assets/ooxml-xsd/`.

## Previously generated files

PptxGenJS 4.0.1 was reproduced writing `notesMasterIdLst` after `sldIdLst`, even
without an explicit `addNotes()` call. The Transitional schema requires the notes
master list before the slide list. Default `inspect` now detects this order
violation. It is a confirmed schema defect; its role in a reported desktop
PowerPoint open failure still requires testing that original file and app.

For that specific defect, normalize to a **new** file, then validate and test it:

```sh
python scripts/pptx.py normalize original.pptx normalized.pptx --receipt normalization.json
python scripts/pptx.py validate normalized.pptx --output normalized-xsd.json
```

This operation only reorders known presentation children and canonicalizes ZIP
layout. Every other part payload, including slides, connectors, groups, notes
and media, stays byte-identical. It refuses duplicate or unknown presentation
children rather than guessing their order. It leaves an already ordered
presentation part byte-identical. The receipt records changed parts and removed
directory entries; the original file and existing output/report paths are never
overwritten. ZIP directory entries and content-types placement are compatibility
conventions here, not independently confirmed causes of PowerPoint failure.

Routine `patch` deliberately does **not** normalize a human-edited file. Keep
that preservation operation separate from explicit package recovery. Neither
normalization nor XSD validation is a general PowerPoint repair service.

## If PowerPoint still refuses to open it

Keep the original, normalized candidate and exact error message. Record the OS,
PowerPoint version, and whether each candidate opens. Compare a minimal
`examples/engine-smoke.mjs` export where the portable engine is available. If
only a LibreOffice re-save opens, retain that as a separate diagnostic candidate;
it can rewrite many parts and must not be described as a lossless repair.
Reduce connectors, custom geometry, groups and pictures one at a time only as
diagnostic copies, never by replacing the user's original figure.
