# Claude environment and image tools

The public PptxGenJS engine supports two image modes: Gemini API drafting followed by native reconstruction, or direct native authoring without an image API. Both retain content contracts, original-reference review, color roles, editable explanations and saved-file validation. Choose using [image options and key registration](image-options.md).

## Check the actual host

1. Locate this skill folder; resolve relative paths from it. Confirm code execution, file reading/writing and image inspection are available. Do not assume a particular `/mnt` path, terminal tool name or document skill exists.
2. Offer Gemini API or no-API mode unless already selected. The included `scripts/gemini_image.py` implements the optional Google image API connection. Its human-terminal `setup` command registers a key privately; its `status` command is offline. Do not request secrets in chat. No-API mode requires neither a key nor an image-model draft.
3. Run `node scripts/preflight.mjs` from this folder. It checks local dependencies and optional credential presence; it does not make an API request, detect MCP connections or certify model access. Node.js 20+ and Python 3.10+ are suitable. The engine needs `pptxgenjs`, `lxml` and `Pillow`; PDF typography checks also need `pdfplumber`. The image client uses Python's standard library plus Pillow, with no extra SDK.
4. Locate an actual saved-PPTX renderer. The included `render.py` supports LibreOffice plus Poppler (`pdftoppm`). A host-provided PPTX renderer or PowerPoint can be used instead if it reads the saved candidate. Record its name and inspect the actual result. Missing renderer means visual verification is incomplete, not passed.

If a host supplies a PPTX skill, read its environment and renderer instructions. Do not copy its proprietary implementation into this skill or assume Claude Code includes cloud document tools. Follow the host's actual image-viewing and file-delivery conventions.

## Apply the selected mode

In Gemini API mode, generate the full composition before native construction. Save the actual prompt, output image and generation record; inspect it and write transfer decisions. Follow [image-first.md](image-first.md) and generate final pictorial assets separately as needed. The client calls the documented Google HTTPS endpoint using a header credential and does not silently retry. It handles image and text-only responses distinctly.

For another provider explicitly chosen by the user, resolve its actual tool or configured integration. Never print credentials or put them in prompts, output records or the skill package. Installing the skill does not create a Google account, enable billing, or register a key; those remain user-controlled setup actions. Some claude.ai/API environments restrict outbound network access, so key registration alone may not enable direct API calls there.

In no-API mode, proceed to native authoring after content, reference and palette preparation. This is a complete supported route, not a blocked task or a waiver requiring further confirmation. Do not describe native geometry as an image-model draft. If an API-mode request fails or cannot access the network, explain the failure and offer setup/retry or no-API mode. Exact reconstruction of a supplied raster and local edits to an existing PPTX have their own routes and need no new draft.

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

Deliver the editable PPTX, saved-file preview and concise validation note naming the selected mode. In API mode, also deliver the selected draft and keep its prompt, transfer plan and side-by-side comparison. No-API mode does not require those nonexistent artifacts. Keep asset inventories and saved-file inspection reports in both modes as applicable. A full draft must never be embedded in the final PPTX, even hidden. Local engine checks do not establish a Claude-host run; credential presence does not establish model access; XML inspection does not establish native PowerPoint edit behavior. Blind review remains conditional on a user request.

Installation guidance and capability limits were checked against [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude custom-skill upload](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [Claude image capability](https://support.claude.com/en/articles/9002504-can-claude-produce-images), and [Agent Skills environments](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Check current host capabilities rather than relying on this document as a permanent tool catalog.
