# Antigravity CLI environment and image tools

Use the built-in Antigravity image tool when available, an explicitly selected optional Gemini API client, or direct native authoring without image generation. All routes use the public PptxGenJS engine and retain content contracts, original-reference review, color roles, editable explanations and saved-file validation. Choose using [image workflow options](image-options.md).

## Check the actual host

1. Locate this skill folder; resolve relative paths from it. Confirm code execution, file reading/writing and image inspection are available. Do not assume a particular `/mnt` path, terminal tool name or document skill exists.
2. Check the current agent session for the built-in `generate_image` tool. Use it by default when available and no other route was selected. Do not require a separate Gemini API key for this host path. If unavailable, offer the optional Gemini API client or direct native authoring. Key setup applies only to an explicitly selected external API route; see [image options](image-options.md).
3. Run `node scripts/preflight.mjs` from this folder. It checks local dependencies and optional credential presence; it does not make an API request, detect MCP connections or certify model access. Node.js 20+ and Python 3.10+ are suitable. The engine needs `pptxgenjs`, `lxml` and `Pillow`; PDF typography checks also need `pdfplumber`. The image client uses Python's standard library plus Pillow, with no extra SDK.
4. Locate an actual saved-PPTX renderer. The included `render.py` supports LibreOffice plus Poppler (`pdftoppm`). A host-provided PPTX renderer or PowerPoint can be used instead if it reads the saved candidate. Record its name and inspect the actual result. Missing renderer means visual verification is incomplete, not passed.

If a host supplies a PPTX skill, read its environment and renderer instructions. Do not copy its proprietary implementation into this skill or assume a CLI login includes cloud document tools. Follow the host's actual image-viewing and file-delivery conventions.

## Apply the selected mode

In built-in mode, use the host’s callable image tool with its actual schema and authentication. Save and inspect the full draft before native construction, retain its prompt and transfer plan, and compare it with the saved PPTX render. Do not read host credentials or require `gemini_image.py setup` for this route.

In Gemini API mode, generate the full composition before native construction. Save the actual prompt, output image and generation record; inspect it and write transfer decisions. Follow [image-first.md](image-first.md) and generate final pictorial assets separately as needed. The client calls the documented Google HTTPS endpoint using a header credential and does not silently retry. It handles image and text-only responses distinctly.

For another provider explicitly chosen by the user, resolve its actual tool or configured integration. Never print credentials or put them in prompts, output records or the skill package. Installing the skill does not create a Google account, enable billing, or register a key; those remain user-controlled setup actions. An Antigravity CLI login does not configure the separate image API key. Network restrictions in your CLI sandbox can still prevent API access.

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

Install the containing plugin with `agy plugin install /path/to/plugin`. Its bundled skill is staged under `~/.gemini/antigravity-cli/plugins/paper-figure/skills/paper-figure/`. Use `agy plugin list`, or `/plugin` and `/skills` in the TUI, to inspect discovery; invoke `/paper-figure`. Antigravity also reads workspace `.agents/skills/`, which Codex shares. Avoid loading the Codex edition there in an Antigravity project; it requires a different runtime. Check the loaded entry point when both editions are present. This package targets Antigravity CLI, not the Gemini web app.

## Evidence and delivery

Deliver the editable PPTX, saved-file preview and concise validation note naming the selected mode. In image-draft mode, also deliver the selected draft and keep its prompt, transfer plan and side-by-side comparison. No-API mode does not require those nonexistent artifacts. Keep asset inventories and saved-file inspection reports in all modes as applicable. A full draft must never be embedded in the final PPTX, even hidden. Local engine checks do not establish an Antigravity CLI agent run; credential presence does not establish model access; XML inspection does not establish native PowerPoint edit behavior. Blind review remains conditional on a user request.

Host guidance: [Antigravity plugins](https://www.antigravity.google/docs/plugins?tab=cli) and [Agent Skills](https://www.antigravity.google/docs/skills). Image credentials and route selection: [image options](image-options.md). Follow the CLI's actual activation and execution permissions.
