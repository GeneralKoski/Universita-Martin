#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

CLANG_TIDY="$(command -v clang-tidy || echo "$HOME/llvm-project/build/bin/clang-tidy")"
CHECK="-checks=-*,misc-no-printf"
FLAGS=(-std=c++23 -isysroot "$(xcrun --show-sdk-path)")

snippet_for() {
  case "$1" in
    1) echo 01_basic.cpp ;;
    2) echo 02_namespace_collision.cpp ;;
    3) echo 03_macro_indirection.cpp ;;
    4) echo 04_template.cpp ;;
    5) echo 05_method_collision.cpp ;;
    6) echo 06_using_template_alias.cpp ;;
    *) echo "" ;;
  esac
}

run() {
  local file="$1"
  echo "=============================================="
  echo ">>> $file"
  echo "=============================================="
  "$CLANG_TIDY" "$CHECK" "snippets/$file" -- "${FLAGS[@]}"
  echo
}

choice="${1:-}"
if [[ -z "$choice" ]]; then
  echo "Quale snippet vuoi lanciare?"
  for i in 1 2 3 4 5 6; do
    echo "  $i) $(snippet_for "$i")"
  done
  read -rp "Scelta (1-6): " choice
fi

file="$(snippet_for "$choice")"
if [[ -n "$file" ]]; then
  run "$file"
else
  echo "Scelta non valida: '$choice' (usa 1-6)" >&2
  exit 1
fi
