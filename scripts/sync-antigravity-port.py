#!/usr/bin/env python3
"""Build Antigravity's host-specific guidance around the shared portable engine."""
import json
from pathlib import Path
from skill_package import skill_files

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'ports/claude/paper-figure'
target = ROOT / 'ports/antigravity/plugin/skills/paper-figure'
host_mode = (ROOT / 'ports/antigravity/image-mode.md').read_text().strip()
host_options = (ROOT / 'ports/antigravity/image-options-intro.md').read_text()
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
            text = text.replace('**Explicitly selected image-provider mode only:**', '**Built-in or explicitly selected image-provider mode:**')
        elif relative == Path('package.json'):
            data = json.loads(text)
            data.update(name='paper-figure-antigravity', description='Portable editable paper-figure engine for Antigravity CLI')
            text = json.dumps(data, indent=2) + '\n'
        elif relative == Path('references/antigravity-environment.md'):
            text = text.replace('# Claude environment and image tools', '# Antigravity CLI environment and image tools')
            text = text.replace('Default to direct native authoring without provider onboarding.', 'Default to the session’s available built-in image tool without provider onboarding.')
            text = text.replace('2. Reuse an existing explicit image-provider choice; otherwise follow the default image workflow.', '2. Reuse an existing explicit image-provider choice; otherwise use the current session’s available `generate_image` tool with host authentication. A local dependency check cannot establish native tool access.')
            text = text.replace('## Apply the selected mode\n', '## Apply the selected mode\n\nFor the default built-in path, save and inspect the full composition draft before native authoring, retain the actual prompt and transfer decisions, and compare it with the saved-PPTX render. If the host tool fails, explain that failure and discuss retry/supplied-image/direct-native paths as appropriate; do not introduce an unrequested API integration.\n')
            start = text.index('Claude API skill containers may prohibit')
            end = text.index('\n## Evidence', start)
            text = text[:start] + 'Install the containing plugin with `agy plugin install /path/to/plugin`. Its bundled skill is staged under `~/.gemini/antigravity-cli/plugins/paper-figure/skills/paper-figure/`. Use `agy plugin list`, or `/plugin` and `/skills` in the TUI, to inspect discovery; invoke `/paper-figure`. Antigravity also reads workspace `.agents/skills/`, which Codex shares. Avoid loading the Codex edition there in an Antigravity project; it requires a different runtime. Check the loaded entry point when both editions are present. This package targets Antigravity CLI, not the Gemini web app.\n' + text[end:]
            text = text.replace('a Claude-host run', 'an Antigravity CLI agent run')
            end = text.index('Installation guidance and capability limits were checked')
            text = text[:end] + 'Host guidance: [Antigravity plugins](https://www.antigravity.google/docs/plugins?tab=cli) and [Agent Skills](https://www.antigravity.google/docs/skills). Follow the CLI’s actual activation and execution permissions.\n'
        elif relative == Path('references/image-options.md'):
            text = host_options
        elif relative == Path('references/image-first.md'):
            text = text.replace('when the user explicitly selects an available image provider', 'when using the built-in Antigravity image tool or an explicitly selected image provider')
            text = text.replace('2. Use the actual provider explicitly selected by the user', '2. Use the current session’s built-in `generate_image` by default, or the actual provider explicitly selected by the user')
        text = text.replace('or assume Claude Code includes cloud document tools.', 'or assume a CLI login includes cloud document tools.')
        text = text.replace('Claude setup', 'host setup').replace('Claude environment setup', 'portable environment setup')
        text = text.replace('Do not assume Claude has a built-in bitmap-generation tool.', 'Resolve the current session’s actual image-generation tool.')
        dest.write_text(text)
    else:
        dest.write_bytes(file.read_bytes())
print(f'Synchronized {len(skill_files(target))} Antigravity CLI skill files.')
