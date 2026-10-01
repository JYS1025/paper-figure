#!/usr/bin/env python3
"""Build the Antigravity CLI edition from the maintained portable Claude engine."""
import json
from pathlib import Path
from skill_package import skill_files

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'ports/claude/paper-figure'
target = ROOT / 'ports/antigravity/plugin/skills/paper-figure'
host_mode = (ROOT / 'ports/antigravity/image-mode.md').read_text().strip()
host_options = (ROOT / 'ports/antigravity/image-options-intro.md').read_text().rstrip() + '\n\n'
for file in skill_files(source):
    relative = file.relative_to(source)
    if str(relative) == 'references/claude-environment.md':
        relative = Path('references/antigravity-environment.md')
    dest = target / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    if file.suffix in ('.md', '.py', '.mjs', '.json', '.txt', '.html', '.svg'):
        text = file.read_text().replace('claude-environment.md', 'antigravity-environment.md')
        if relative == Path('SKILL.md'):
            text = text.replace('(Claude)', '(Antigravity CLI)').replace('Claude environment and image-tool setup', 'Antigravity CLI environment and image-tool setup')
            text = text.replace('This package works with Claude Code and Claude environments that expose code execution and file output.', 'This package targets Antigravity CLI with shell execution, file output and image inspection. It does not install a custom skill into the Gemini web app.')
            start = text.index('## Choose the image mode')
            end = text.index('## Create', start)
            text = text[:start] + '## Choose the image mode\n\n' + host_mode + '\n\n' + text[end:]
            text = text.replace('**Gemini API / chosen image-provider mode only:**', '**Built-in / selected image-provider mode only:**')
        elif relative == Path('package.json'):
            data = json.loads(text)
            data.update(name='paper-figure-antigravity', version='1.1.2', description='Portable editable paper-figure engine for Antigravity CLI')
            text = json.dumps(data, indent=2) + '\n'
        elif relative == Path('references/antigravity-environment.md'):
            text = text.replace('# Claude environment and image tools', '# Antigravity CLI environment and image tools')
            text = text.replace('The public PptxGenJS engine supports two image modes: Gemini API drafting followed by native reconstruction, or direct native authoring without an image API. Both retain', 'Use the built-in Antigravity image tool when available, an explicitly selected optional Gemini API client, or direct native authoring without image generation. All routes use the public PptxGenJS engine and retain')
            text = text.replace('Choose using [image options and key registration]', 'Choose using [image workflow options]')
            start = text.index('2. Offer Gemini API')
            end = text.index('\n3.', start)
            text = text[:start] + '2. Check the current agent session for the built-in `generate_image` tool. Use it by default when available and no other route was selected. Do not require a separate Gemini API key for this host path. If unavailable, offer the optional Gemini API client or direct native authoring. Key setup applies only to an explicitly selected external API route; see [image options](image-options.md).' + text[end:]
            text = text.replace('## Apply the selected mode\n', '## Apply the selected mode\n\nIn built-in mode, use the host’s callable image tool with its actual schema and authentication. Save and inspect the full draft before native construction, retain its prompt and transfer plan, and compare it with the saved PPTX render. Do not read host credentials or require `gemini_image.py setup` for this route.\n')
            text = text.replace('Some claude.ai/API environments restrict outbound network access, so key registration alone may not enable direct API calls there.', 'An Antigravity CLI login does not configure the separate image API key. Network restrictions in your CLI sandbox can still prevent API access.')
            start = text.index('Claude API skill containers may prohibit')
            end = text.index('\n## Evidence', start)
            text = text[:start] + 'Install the containing plugin with `agy plugin install /path/to/plugin`. Its bundled skill is staged under `~/.gemini/antigravity-cli/plugins/paper-figure/skills/paper-figure/`. Use `agy plugin list`, or `/plugin` and `/skills` in the TUI, to inspect discovery; invoke `/paper-figure`. Antigravity also reads workspace `.agents/skills/`, which Codex shares. Avoid loading the Codex edition there in an Antigravity project; it requires a different runtime. Check the loaded entry point when both editions are present. This package targets Antigravity CLI, not the Gemini web app.\n' + text[end:]
            text = text.replace('a Claude-host run', 'an Antigravity CLI agent run')
            end = text.index('Installation guidance and capability limits were checked')
            text = text[:end] + 'Host guidance: [Antigravity plugins](https://www.antigravity.google/docs/plugins?tab=cli) and [Agent Skills](https://www.antigravity.google/docs/skills). Image credentials and route selection: [image options](image-options.md). Follow the CLI\'s actual activation and execution permissions.\n'
        elif relative == Path('references/image-options.md'):
            text = host_options + text[text.index('## Gemini API mode'):]
            text = text.replace('## No-API mode', '## Direct native authoring without image generation (`no-api`)')
        elif relative == Path('references/image-first.md'):
            text = text.replace('when the user selects Gemini API or another available image provider', 'when using the built-in Antigravity image tool or another selected available image provider')
            text = text.replace('2. Use the bundled `scripts/gemini_image.py` client for Gemini API mode, or the actual provider already selected by the user', '2. Use the callable built-in `generate_image` tool for `antigravity-native`, the bundled `scripts/gemini_image.py` client only for selected Gemini API mode, or another explicitly selected provider')
        elif relative == Path('scripts/preflight.mjs'):
            text = text.replace("modes:['gemini-api','no-api']", "modes:['antigravity-native','gemini-api','no-api'],hostToolAvailability:'check-in-agent-session',credentialStatusAppliesTo:'gemini-api only'")
        if relative in [Path(n) for n in ('SKILL.md', 'references/review-and-editing.md', 'references/visual-assets.md', 'references/visual-design.md', 'references/authoring.md', 'references/image-first.md', 'references/antigravity-environment.md')]:
            text = text.replace('In API mode', 'In image-draft mode').replace('in API mode', 'in image-draft mode').replace('in both modes', 'in all modes')
        text = text.replace('or assume Claude Code includes cloud document tools.', 'or assume a CLI login includes cloud document tools.')
        text = text.replace('Claude setup', 'host setup').replace('Claude environment setup', 'portable environment setup')
        text = text.replace('Do not assume Claude has a built-in bitmap-generation tool.', 'Do not assume the host exposes a built-in bitmap-generation tool.')
        dest.write_text(text)
    else:
        dest.write_bytes(file.read_bytes())
print(f'Synchronized {len(skill_files(target))} Antigravity CLI skill files.')
