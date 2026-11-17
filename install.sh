#!/usr/bin/env bash
# minions installer: copies the kit's template into a project without overwriting anything.
#
#   ./install.sh <project-dir>                  install the core kit
#   ./install.sh <project-dir> --add <agent>... add optional agents from library/agents/
#   ./install.sh --list                         list optional library agents
set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="$(tr -d '[:space:]' < "$KIT_DIR/VERSION")"

usage() {
  sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
}

list_library() {
  echo "Optional library agents (see library/README.md for when to use each):"
  for f in "$KIT_DIR"/library/agents/*.md; do
    echo "  - $(basename "$f" .md)"
  done
}

[ $# -ge 1 ] || usage
if [ "$1" = "--list" ]; then list_library; exit 0; fi
case "$1" in -*) usage ;; esac

TARGET="$1"; shift
[ -d "$TARGET" ] || { echo "error: directory not found: $TARGET" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"
[ "$TARGET" != "$KIT_DIR" ] || { echo "error: target is the kit itself" >&2; exit 1; }

# --- add library agents -------------------------------------------------------
if [ "${1:-}" = "--add" ]; then
  shift
  [ $# -ge 1 ] || { list_library; exit 1; }
  mkdir -p "$TARGET/.claude/agents"
  for agent in "$@"; do
    src="$KIT_DIR/library/agents/$agent.md"
    dest="$TARGET/.claude/agents/$agent.md"
    if [ ! -f "$src" ]; then echo "  unknown agent: $agent"; continue; fi
    if [ -e "$dest" ]; then echo "  skip (exists): .claude/agents/$agent.md"; continue; fi
    cp "$src" "$dest"
    echo "  added: .claude/agents/$agent.md"
  done
  echo
  echo "Record these under 'Library agents added' in docs/ai/MINIONS.md."
  exit 0
fi
[ $# -eq 0 ] || usage

# --- install core kit ---------------------------------------------------------
echo "Installing minions v$VERSION into $TARGET"
echo
copied=0; skipped=0
cd "$KIT_DIR/template"
while IFS= read -r rel; do
  rel="${rel#./}"
  dest="$TARGET/$rel"
  if [ -e "$dest" ]; then
    echo "  skip (exists): $rel"
    skipped=$((skipped + 1))
    continue
  fi
  mkdir -p "$(dirname "$dest")"
  if [ "$rel" = "docs/ai/MINIONS.md" ]; then
    sed -e "s|{{VERSION}}|$VERSION|" \
        -e "s|{{DATE}}|$(date +%Y-%m-%d)|" \
        -e "s|{{SOURCE}}|$KIT_DIR|" "$rel" > "$dest"
  else
    cp "$rel" "$dest"
  fi
  echo "  copied: $rel"
  copied=$((copied + 1))
done < <(find . -type f ! -name '.DS_Store' | sort)

echo
echo "Done: $copied copied, $skipped skipped."
if [ "$skipped" -gt 0 ]; then
  echo
  echo "Skipped files already existed and were left untouched. To merge, compare:"
  echo "  diff -ru \"$KIT_DIR/template\" \"$TARGET\" | less"
  echo "or ask Claude to merge the kit's version of a specific file into yours."
  if [ -f "$TARGET/CLAUDE.md" ] && ! grep -q '@AGENTS.md' "$TARGET/CLAUDE.md"; then
    echo
    echo "IMPORTANT: your existing CLAUDE.md does not import AGENTS.md. Add this as its first line:"
    echo "  @AGENTS.md"
    echo "and merge in the 'Claude Code: lead engineer' section from template/CLAUDE.md."
  fi
fi
cat <<EOF

Next steps:
  1. cd "$TARGET" && claude
  2. Run /project-setup to fill in AGENTS.md and docs/project/.
  3. Check that /agents lists the core agents.
EOF
