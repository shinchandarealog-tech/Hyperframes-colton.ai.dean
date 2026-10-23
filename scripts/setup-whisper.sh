#!/usr/bin/env bash
# Build whisper.cpp where the HyperFrames CLI looks for it, so
# `npx hyperframes transcribe` works fully offline (no API keys).
# Idempotent: exits early if the binary is already built.
#
# Requires: git, cmake, a C/C++ compiler.
# Usage:    bash scripts/setup-whisper.sh [--with-model]
#   --with-model  also pre-download the default small.en model (~488 MB)
#                 by transcribing whisper.cpp's bundled sample.
set -euo pipefail

WHISPER_TAG="v1.9.5"
DIR="$HOME/.cache/hyperframes/whisper/whisper.cpp"
BIN="$DIR/build/bin/whisper-cli"

if [ -x "$BIN" ]; then
  echo "whisper-cli already built: $BIN"
else
  rm -rf "$DIR"
  mkdir -p "$(dirname "$DIR")"
  git clone --depth 1 --branch "$WHISPER_TAG" https://github.com/ggml-org/whisper.cpp.git "$DIR"
  cmake -S "$DIR" -B "$DIR/build" -DCMAKE_BUILD_TYPE=Release
  cmake --build "$DIR/build" --config Release -j"$(nproc 2>/dev/null || sysctl -n hw.ncpu)"
  echo "Built: $BIN"
fi

if [ "${1:-}" = "--with-model" ]; then
  tmp="$(mktemp -d)"
  cp "$DIR/samples/jfk.wav" "$tmp/"
  (cd "$tmp" && npx --yes hyperframes transcribe jfk.wav --model small.en)
  rm -rf "$tmp"
fi
