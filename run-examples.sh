#!/bin/sh
set -eu
# Local Codex bundled runtime. Override these paths when moving the project.
TASK_RUNTIME="${TASK_RUNTIME:-/Users/odysseus/.cache/codex-runtimes/codex-primary-runtime/dependencies}"
export ARTIFACT_NODE_MODULES="${ARTIFACT_NODE_MODULES:-$TASK_RUNTIME/node/node_modules}"
export FIGURE_PYTHON="${FIGURE_PYTHON:-$TASK_RUNTIME/python/bin/python3}"
export RUNTIME_NODE_MODULES="$ARTIFACT_NODE_MODULES"
export RUNTIME_NODE="$TASK_RUNTIME/node/bin/node"
export RUNTIME_PYTHON="$FIGURE_PYTHON"
export PRESENTATIONS_SKILL_DIR="${PRESENTATIONS_SKILL_DIR:-/Users/odysseus/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations}"
exec "$TASK_RUNTIME/node/bin/node" skills/paper-figure/examples/build-examples.mjs "${1:-output/examples}" "${2:-.build/examples-$(date +%Y%m%d-%H%M%S)}"
