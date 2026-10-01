# Install Paper Figure

Codex and Claude use the [skills CLI](https://github.com/vercel-labs/skills), requiring Node.js **22.20+** and Git. Antigravity CLI uses its native plugin installer. The commands fetch files from GitHub without a manual ZIP download.

## Public installation

[Paper Figure](https://github.com/JYS1025/paper-figure) is a public repository. The installation commands below work without a GitHub account, access token or GitHub CLI. Install Git and the prerequisites for your chosen edition first. Your agent’s own account and runtime requirements still apply.

## Choose an edition

### Codex and Claude Code

Run from the project where you want to use the skill:

```sh
# Codex
npx --yes skills@1.7.0 add https://github.com/JYS1025/paper-figure/tree/main/skills/paper-figure --agent codex --copy

# Claude Code
npx --yes skills@1.7.0 add https://github.com/JYS1025/paper-figure/tree/main/ports/claude/paper-figure --agent claude-code --copy
```

`skills@1.7.0` is the installer version, not a Paper Figure release. The exact subdirectory and `--copy` matter: both editions are called `paper-figure`, but their authoring engines differ. A shared canonical symlink can replace the other edition. A repository-root install does not select the correct engine for each agent.

By default, Codex installs in `.agents/skills/paper-figure` and Claude in `.claude/skills/paper-figure`. Add `--global` for `~/.agents/skills/paper-figure` or `~/.claude/skills/paper-figure`. The `--yes` immediately after `npx` accepts downloading the CLI; a second `--yes` at the end skips the skill installation confirmation. The installer supports `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1`.

See the official [Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [Claude skill locations](https://code.claude.com/docs/en/skills#where-skills-live).

### Antigravity CLI

Google announced the [transition from Gemini CLI to Antigravity CLI](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) in May 2026. Gemini CLI retains some enterprise and paid-API access; the Google host targeted by this project is **Antigravity CLI (`agy`)**. Antigravity’s built-in image tool is the default when available.

Install [Antigravity CLI](https://antigravity.google/docs/cli/install), then:

```sh
git clone https://github.com/JYS1025/paper-figure.git paper-figure
agy plugin install ./paper-figure/ports/antigravity/plugin
agy plugin list
```

If you already have a checkout, skip cloning and pass its actual `ports/antigravity/plugin` directory. This uses the documented [local plugin installation](https://www.antigravity.google/docs/plugins?tab=cli). It does not assume that an installed `agy` version can select a repository subdirectory from a Git URL.

The plugin contains `plugin.json` and `skills/paper-figure/SKILL.md`. Its user-level destination is `~/.gemini/antigravity-cli/plugins/paper-figure/`. In a new session, inspect `/plugin` or `/skills`, then invoke `/paper-figure`.

Antigravity also discovers workspace `.agents/skills/`, which Codex shares. If a project already has the Codex edition of `paper-figure` there, check the loaded skill path and avoid loading that edition in Antigravity; its authoring engine requires Codex's runtime. Use the portable Antigravity plugin in a workspace without that conflicting entry. The repository's existing `.agents/skills` link is for Codex development.

## Verify and update

Confirm the installed entry point matches your edition. Invoke `paper-figure` in Codex or `/paper-figure` in Claude Code and Antigravity. Start a new session if it is not visible.

For **Codex/Claude**, back up edits made inside the installed skill, then rerun its exact edition-specific `add` command with the same scope and `--copy`. This replaces the copy. Avoid name-only bulk updates when different editions share the skill name.

For **Antigravity**, back up changes made inside the installed plugin, update your checkout, then reinstall:

```sh
git -C paper-figure pull --ff-only
agy plugin uninstall paper-figure
agy plugin install ./paper-figure/ports/antigravity/plugin
```

The commands follow `main`. For a repeatable Codex/Claude install, replace `main` in the source URL with a commit SHA or tag. For Antigravity, check out the desired revision before installing the local plugin.

The earlier [installation verification record](cli-install-validation.json) checks remote installation of Codex and Claude into an isolated project. The [portable-mode validation record](portable-image-validation.json) separately records Antigravity manifest/skill validation, packaged-engine execution and optional image-client tests. These checks do not establish an end-to-end agent figure run.

## Runtime and image setup

Installation places files; it does not install authoring dependencies or add a renderer. Codex and Antigravity use their available host image tools by default. Claude uses direct native authoring. No external-service menu or credential check appears during ordinary setup. See [host workflows](claude-image-generation.md).

The portable engine uses Node.js 20+, Python 3.10+ and public dependencies. The Codex engine uses its host's bundled runtime. See the [README requirements](../README.md#2-check-the-required-tools), [Claude environment](../ports/claude/paper-figure/references/claude-environment.md) and [Antigravity environment](../ports/antigravity/plugin/skills/paper-figure/references/antigravity-environment.md).

## ZIP installation

[Codex](../output/paper-figure-skill.zip) and [Claude](../output/paper-figure-claude-skill.zip) ZIPs contain `paper-figure/SKILL.md`. Extract into the selected skill directory. In claude.ai, upload the Claude ZIP in an environment that supports custom skills, code execution and file creation.

The [Antigravity plugin ZIP](../output/paper-figure-antigravity-plugin.zip) contains `paper-figure/plugin.json` and `paper-figure/skills/paper-figure/`. Extract it and run:

```sh
agy plugin install /path/to/extracted/paper-figure
```

## Troubleshooting

| Symptom | Next step |
|---|---|
| Repository not found or authentication failed | Open the [public repository](https://github.com/JYS1025/paper-figure) and check the source URL, network/proxy settings and Git URL rewrites. Public read access does not require a token. |
| Clone times out | Check network/proxy settings; use an existing checkout when available. |
| Wrong authoring engine | Check the loaded entry-point path. Install the edition-specific directory; check for an existing `.agents/skills/paper-figure` collision in Antigravity. |
| Old edits disappear after update | Restore your backup; installation replaces the selected copy. |
| Skill is missing in claude.ai | Local CLI installation does not upload a cloud account skill; use the Claude ZIP. |
| Host image tool is unavailable | Report the actual limitation and discuss retrying that tool, using a supplied image, or an appropriate direct-native route. |

For an existing checkout, Codex/Claude also accept local source paths:

```sh
npx --yes skills@1.7.0 add /path/to/paper-figure/skills/paper-figure --agent codex --copy
npx --yes skills@1.7.0 add /path/to/paper-figure/ports/claude/paper-figure --agent claude-code --copy
```
