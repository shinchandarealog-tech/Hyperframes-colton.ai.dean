#!/bin/bash
# SessionStart hook: prepares the /watch skill in Claude Code cloud sessions.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# yt-dlp is the only /watch dependency missing from the base image (ffmpeg ships with it).
if ! command -v yt-dlp >/dev/null 2>&1; then
  pip install -q yt-dlp
fi

# Pre-seed /watch preferences so it skips its first-run questions: balanced detail, no Whisper key.
CONFIG_DIR="$HOME/.config/watch"
CONFIG_FILE="$CONFIG_DIR/.env"
if [ ! -f "$CONFIG_FILE" ]; then
  mkdir -p "$CONFIG_DIR"
  printf 'GROQ_API_KEY=\nOPENAI_API_KEY=\nWATCH_DETAIL=balanced\nSETUP_COMPLETE=true\n' > "$CONFIG_FILE"
  chmod 600 "$CONFIG_FILE"
fi
