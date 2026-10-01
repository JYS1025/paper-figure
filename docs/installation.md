# Install Paper Figure

The [skills CLI](https://github.com/vercel-labs/skills) installs the skill directly from GitHub. Use Node.js **22.20 or newer** and Git. Commands below pin the installer to `skills@1.7.0`; this is the installer version, not a Paper Figure release.

## Authenticate for the private repository

Your account must have access to `JYS1025/paper-figure`. Install [GitHub CLI](https://cli.github.com/), then run:

```sh
gh auth login
gh auth setup-git
gh repo view JYS1025/paper-figure
```

`gh auth setup-git` configures Git to use GitHub CLI credentials. An existing working HTTPS credential helper also works. Do not put a token in a command URL or README. Authentication is unnecessary for public read access if the repository is made public later.

## Choose one edition

From the project where you want to use Paper Figure:

```sh
# Codex
npx --yes skills@1.7.0 add https://github.com/JYS1025/paper-figure/tree/main/skills/paper-figure --agent codex --copy

# Claude Code
npx --yes skills@1.7.0 add https://github.com/JYS1025/paper-figure/tree/main/ports/claude/paper-figure --agent claude-code --copy
```

Run both commands if you use both agents. The exact subdirectory and `--copy` matter: both editions are called `paper-figure`, but their authoring engines differ. A shared canonical symlink can replace the other edition. A repository-root install or a single command targeting both agents does not select the correct engine for each agent.

By default, the Codex copy goes in `.agents/skills/paper-figure`, and the Claude copy in `.claude/skills/paper-figure`. Add `--global` for the corresponding personal directories, `~/.agents/skills/paper-figure` and `~/.claude/skills/paper-figure`. The `--yes` immediately after `npx` accepts downloading the CLI; a second `--yes` at the end skips the skill installation confirmation.

The CLI supports `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1`. For example, in macOS/Linux/WSL:

```sh
export DISABLE_TELEMETRY=1
```

See the official [Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [Claude Code skill locations](https://code.claude.com/docs/en/skills#where-skills-live).

## Verify and update

Confirm the installed `paper-figure/SKILL.md` exists in the directory for your selected scope, then invoke `paper-figure` in Codex or `/paper-figure` in Claude Code. Start a new session if it is not visible.

For updates, first back up edits you made inside the installed skill, then rerun its exact edition-specific `add` command with the same scope and `--copy`. This replaces that copy. Avoid name-only bulk updates when both editions are installed; they share the same skill name.

The install command fetches `main`. For a repeatable installation, replace `main` in the source URL with a full commit SHA or a published tag.

The [installation verification record](cli-install-validation.json) checks remote installation of both editions into the same isolated project and compares every installed source file.

## Runtime setup

Installation places the skill files; it does not install the authoring engine's packages, configure image generation, or add rendering tools. Follow the [README tool requirements](../README.md#2-check-the-required-tools) and [Claude environment guide](../ports/claude/paper-figure/references/claude-environment.md).

The Codex engine still requires the host's bundled authoring runtime. The Claude engine uses public dependencies. The installer requires Node.js 22.20+, even though the Claude authoring engine itself accepts Node.js 20+.

## Troubleshooting

| Symptom | Next step |
|---|---|
| Repository not found or authentication failed | Confirm access with `gh repo view JYS1025/paper-figure`, then check `gh auth status` and `gh auth setup-git`. |
| Clone times out | Check the network and Git authentication. You can clone once with `gh repo clone JYS1025/paper-figure`, then use the local skill path as shown below. |
| Wrong authoring engine | Reinstall from the correct edition subdirectory with `--copy`. |
| Old edits disappear after update | Restore your backup; the CLI replaces the selected skill directory. |
| Skill is missing in claude.ai | Local CLI installation does not upload a cloud account skill. Use the [Claude ZIP](../output/paper-figure-claude-skill.zip) in claude.ai. |

If you already have a checkout, run from your target project and substitute its absolute path:

```sh
npx --yes skills@1.7.0 add /path/to/paper-figure/skills/paper-figure --agent codex --copy
npx --yes skills@1.7.0 add /path/to/paper-figure/ports/claude/paper-figure --agent claude-code --copy
```
