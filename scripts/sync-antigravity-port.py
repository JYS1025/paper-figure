#!/usr/bin/env python3
"""Build the Antigravity CLI edition from the maintained portable Claude engine."""
import json
from pathlib import Path
from skill_package import skill_files

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'ports/claude/paper-figure'
target = ROOT / 'ports/antigravity/plugin/skills/paper-figure'
for file in skill_files(source):
    relative = file.relative_to(source)
    if str(relative) == 'references/claude-environment.md':
        relative = Path('references/antigravity-environment.md')
    dest = target / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    if file.suffix in ('.md', '.mjs', '.json'):
        text = file.read_text().replace('claude-environment.md', 'antigravity-environment.md')
        if relative == Path('SKILL.md'):
            text = text.replace('(Claude)', '(Antigravity CLI)').replace('Claude environment and image-tool setup', 'Antigravity CLI environment and image-tool setup')
            text = text.replace('This package works with Claude Code and Claude environments that expose code execution and file output.', 'This package targets Antigravity CLI with shell execution, file output and image inspection. It does not install a custom skill into the Gemini web app.')
        elif relative == Path('package.json'):
            data = json.loads(text)
            data.update(name='paper-figure-antigravity', description='Portable editable paper-figure engine for Antigravity CLI')
            text = json.dumps(data, indent=2) + '\n'
        elif relative == Path('references/antigravity-environment.md'):
            text = text.replace('# Claude environment and image tools', '# Antigravity CLI environment and image tools')
            text = text.replace('Some claude.ai/API environments restrict outbound network access, so key registration alone may not enable direct API calls there.', 'An Antigravity CLI login does not configure the separate image API key. Network restrictions in your CLI sandbox can still prevent API access.')
            start = text.index('Claude API skill containers may prohibit')
            end = text.index('\n## Evidence', start)
            text = text[:start] + 'Install the containing plugin with `agy plugin install /path/to/plugin`. Its bundled skill is staged under `~/.gemini/antigravity-cli/plugins/paper-figure/skills/paper-figure/`. Use `agy plugin list`, or `/plugin` and `/skills` in the TUI, to inspect discovery; invoke `/paper-figure`. Antigravity also reads workspace `.agents/skills/`, which Codex shares. Avoid loading the Codex edition there in an Antigravity project; it requires a different runtime. Check the loaded entry point when both editions are present. This package targets Antigravity CLI, not the Gemini web app.\n' + text[end:]
            text = text.replace('a Claude-host run', 'an Antigravity CLI agent run')
            end = text.index('Installation guidance and capability limits were checked')
            text = text[:end] + 'Host guidance: [Antigravity plugins](https://www.antigravity.google/docs/plugins?tab=cli) and [Agent Skills](https://www.antigravity.google/docs/skills). Image credentials and route selection: [image options](image-options.md). Follow the CLI\'s actual activation and execution permissions.\n'
        text = text.replace('or assume Claude Code includes cloud document tools.', 'or assume a CLI login includes cloud document tools.')
        text = text.replace('Claude setup', 'host setup').replace('Claude environment setup', 'portable environment setup')
        text = text.replace('Do not assume Claude has a built-in bitmap-generation tool.', 'Do not assume the host exposes a built-in bitmap-generation tool.')
        dest.write_text(text)
    else:
        dest.write_bytes(file.read_bytes())
print(f'Synchronized {len(skill_files(target))} Antigravity CLI skill files.')
