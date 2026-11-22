#!/bin/bash
# agent-skills session start hook
# Injects the using-agent-skills meta-skill into a new session.
#
# Upstream does not wire this script: hosts that already route skills from
# their descriptions (Claude Code, Codex CLI) would run a second router on top
# of the native one — see docs/getting-started.md.
# This fork deliberately keeps hooks/hooks.json, which wires it into the
# Claude Code SessionStart hook, so on native-routing hosts the meta-skill is
# injected on top of native routing (about 3.5k tokens per session). See
# docs/DECISIONS.md, 2026-11-02 "Hook 保留決定".
#
# Every output path must emit the standard SessionStart envelope
#   {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}
# Hosts that validate hook output (Codex CLI, Claude Code) reject other shapes.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")/skills"
META_SKILL="$SKILLS_DIR/using-agent-skills/SKILL.md"

if ! command -v jq >/dev/null 2>&1; then
  echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "agent-skills: jq is required for the session-start hook but was not found on PATH. Install jq (e.g. `brew install jq` or `apt-get install jq`) to enable meta-skill injection. Skills remain available individually."}}'
  exit 0
fi

if [ -f "$META_SKILL" ]; then
  CONTENT=$(cat "$META_SKILL")
  # Use jq to properly escape and construct valid JSON
  jq -cn \
    --arg context "agent-skills loaded. Use the skill discovery flowchart to find the right skill for your task.

$CONTENT" \
    '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $context}}'
else
  echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "agent-skills: using-agent-skills meta-skill not found. Skills may still be available individually."}}'
fi
