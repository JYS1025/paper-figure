# Claude environment and image tools

The public PptxGenJS engine creates native editable figures. Default to direct native authoring without provider onboarding. Keep content contracts, original-reference review, color roles and saved-file validation. See [image workflow](image-options.md); a requested integration is read only when its user-request condition applies.

## Check the actual host

1. Locate this skill folder; resolve relative paths from it. Confirm code execution, file reading/writing and image inspection are available. Do not assume a particular `/mnt` path, terminal tool name or document skill exists.
2. Reuse an existing explicit image-provider choice; otherwise follow the default image workflow. Do not offer external API setup or inspect credentials as part of ordinary onboarding or after a tool failure.
3. Run `node scripts/preflight.mjs` from this folder. By default it checks local authoring dependencies only; it does not inspect image credentials, discover agent tools or verify provider access. Node.js 20+ and Python 3.10+ are suitable. The engine needs `pptxgenjs`, `lxml` and `Pillow`; PDF typography checks also need `pdfplumber`.
4. Locate an actual saved-PPTX renderer. The included `render.py` supports LibreOffice plus Poppler (`pdftoppm`). A host-provided PPTX renderer or PowerPoint can be used instead if it reads the saved candidate. Record its name and inspect the actual result. Missing renderer means visual verification is incomplete, not passed.

If a host supplies a PPTX skill, read its environment and renderer instructions. Do not copy its proprietary implementation into this skill or assume Claude Code includes cloud document tools. Follow the host's actual image-viewing and file-delivery conventions.

## Apply the selected mode

In direct native mode, proceed after content, reference and palette preparation. This is a complete supported route; do not claim that an image-model draft exists. Use supplied imagery and native pictograms as appropriate. Exact reconstruction of a supplied raster and local PPTX edits need no new draft.

When an image provider was explicitly selected, resolve its actual tool or client and complete [image-first.md](image-first.md). If the requested integration is Gemini API, read [its setup guide](gemini-image-api.md) only then. Keep that integration absent from ordinary user-facing choices and fallback suggestions. A failed provider call is a failure, not permission to switch providers or omit a required stage. Explain the actual limitation and continue independent preparation.

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

Deliver the editable PPTX, saved-file preview and concise validation note naming the selected mode. In image-draft mode, also deliver the selected draft and keep its prompt, transfer plan and side-by-side comparison. No-API mode does not require those nonexistent artifacts. Keep asset inventories and saved-file inspection reports in both modes as applicable. A full draft must never be embedded in the final PPTX, even hidden. Local engine checks do not establish a Claude-host run; XML inspection does not establish native PowerPoint edit behavior. Blind review remains conditional on a user request.

Installation guidance and capability limits were checked against [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude custom-skill upload](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [Claude image capability](https://support.claude.com/en/articles/9002504-can-claude-produce-images), and [Agent Skills environments](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Check current host capabilities rather than relying on this document as a permanent tool catalog.
