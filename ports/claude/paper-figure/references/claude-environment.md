# Claude environment and image tools

The scientific and design workflow is the same on every host: contract and references → full image-model composition draft → inspected transfer plan → native editable reconstruction → saved-file validation. This port changes runtime integration, not those requirements. It uses public PptxGenJS rather than a private authoring runtime.

## Check the actual host

1. Locate this skill folder; resolve relative paths from it. Confirm code execution, file reading/writing and image inspection are available. Do not assume a particular `/mnt` path, terminal tool name or document skill exists.
2. Identify an actual connected image-generation tool or authorized provider integration. Read its real schema and available capability instructions. The skill cannot add a model service or credentials. Claude's own text, HTML or SVG output is not an image-model draft.
3. Run `node scripts/preflight.mjs` from this folder. It only checks local packages/binaries; it cannot detect MCP connections or certify image generation. Node.js 20+ and Python 3.10+ are suitable. The engine needs `pptxgenjs`, `lxml` and `Pillow`; PDF typography checks also need `pdfplumber`.
4. Locate an actual saved-PPTX renderer. The included `render.py` supports LibreOffice plus Poppler (`pdftoppm`). A host-provided PPTX renderer or PowerPoint can be used instead if it reads the saved candidate. Record its name and inspect the actual result. Missing renderer means visual verification is incomplete, not passed.

If a host supplies a PPTX skill, read its environment and renderer instructions. Do not copy its proprietary implementation into this skill or assume Claude Code includes cloud document tools. Follow the host's actual image-viewing and file-delivery conventions.

## Full composition drafting is still required

Use the discovered image tool to generate the full composition before native construction. Save its actual prompt, output image, provider/tool identity and any returned generation ID; inspect it and write transfer decisions. Do not invent a tool invocation, successful output, generation timestamp or model review. Follow [image-first.md](image-first.md) and generate final pictorial assets separately as needed.

With an existing authorized image API integration, use its configured credentials without printing or copying secrets into prompts, metadata, files or this package. Do not hard-code provider endpoints or guessed tool names. Installing this skill does not install or configure an image server and does not authorize account changes.

If image generation is absent, complete independent preparation (content contract, reference inspection and color-role selection), then report the missing connection before production. Do not make a code-drawn sketch and call it an image-model draft. An explicit user waiver permits direct native authoring; accurately label that exception. A user-supplied raster for exact reconstruction uses the supplied-image route. Neither is evidence of a new image-model generation. Local edits to the latest human-edited PPTX need no new draft.

## Dependencies without host-specific paths

Prefer packages already present. `FIGURE_PYTHON` selects the Python executable. If Node libraries are installed in a shared directory, use that real directory as `NODE_PATH` before starting Node. Do not guess the path.

When dependencies are absent and network/package installation is allowed, work in a writable copy of this skill directory. Use a local Node install and virtual environment:

```sh
npm install --omit=dev
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export FIGURE_PYTHON="$PWD/.venv/bin/python"
node scripts/preflight.mjs
```

These are POSIX examples for macOS/Linux. On Windows use the corresponding virtual-environment executable and environment-variable syntax. Do not overwrite managed skill folders, create global installs by default, or bundle `node_modules`/`.venv` in the skill ZIP. If installation is disallowed, state the missing dependency; do not claim the engine ran.

LibreOffice/Poppler and suitable fonts are system capabilities, not included in the manifests. `render.py` discovers `soffice`/`libreoffice` and `pdftoppm` on PATH, or accepts absolute `--soffice` and `--pdftoppm` paths (`FIGURE_SOFFICE`, `FIGURE_PDFTOPPM`). For a host-supplied Python LibreOffice wrapper use `--soffice-wrapper /actual/path/soffice.py` or `FIGURE_SOFFICE_WRAPPER`; the wrapper takes priority and uses the same Python interpreter as `render.py`. Use the host wrapper when its sandbox requires it. Do not silently install a desktop app. Check actual rendered font names, including substitutes, rather than assuming Arial or Times New Roman is installed.

Claude API skill containers may prohibit network access and runtime dependency installation. This package has not been validated in that container; do not promise the setup commands will run there. Use an environment with the required packages or an explicitly integrated external execution service. The delivered target is Claude Code or claude.ai with suitable tools.

## Evidence and delivery

Deliver the editable PPTX, saved-file preview, selected full draft and concise validation note. Keep the actual draft prompt, transfer plan, side-by-side comparison, asset inventory and inspection reports in the task files. The full draft must never be embedded in the final PPTX, even hidden. Local engine checks do not establish that Claude ran the full workflow; a successful ZIP upload does not establish image-model availability; XML inspection does not establish native PowerPoint edit behavior. Blind review is conditional on a user request and needs an actual independent reviewer, with provenance excluded.

Installation guidance and capability limits were checked against [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude custom-skill upload](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [Claude image capability](https://support.claude.com/en/articles/9002504-can-claude-produce-images), and [Agent Skills environments](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Check current host capabilities rather than relying on this document as a permanent tool catalog.
