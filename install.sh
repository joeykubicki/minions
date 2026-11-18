#!/usr/bin/env bash
# minions installer: copies the kit's template into a project without overwriting anything.
#
#   ./install.sh <project-dir>                  install the core kit
#   ./install.sh <project-dir> --add <name>...  add optional agents or add-ons from library/
#   ./install.sh --list                         list optional agents and add-ons
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
  echo
  echo "Optional add-ons (each has a README in library/addons/<name>/):"
  for d in "$KIT_DIR"/library/addons/*/; do
    echo "  - $(basename "$d")"
  done
}

# Copy an add-on's files/ tree into the project (never overwriting), then merge
# its settings.json hooks into the project's .claude/settings.json.
add_addon() {
  local name="$1" src="$KIT_DIR/library/addons/$1" rel dest
  while IFS= read -r rel; do
    rel="${rel#./}"
    dest="$TARGET/$rel"
    if [ -e "$dest" ]; then echo "  skip (exists): $rel"; continue; fi
    mkdir -p "$(dirname "$dest")"
    cp "$src/files/$rel" "$dest"
    echo "  added: $rel"
  done < <(cd "$src/files" && find . -type f ! -name '.DS_Store' | sort)

  [ -f "$src/settings.json" ] || return 0
  if ! command -v python3 >/dev/null 2>&1; then
    echo "  python3 not found: merge $src/settings.json into .claude/settings.json by hand"
    return 0
  fi
  python3 - "$src/settings.json" "$TARGET/.claude/settings.json" <<'PY'
import json, os, sys
fragment_path, settings_path = sys.argv[1], sys.argv[2]
with open(fragment_path) as f:
    fragment = json.load(f)
settings = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path) as f:
            settings = json.load(f)
    except ValueError:
        print("  could not parse .claude/settings.json; add these hooks by hand:")
        print(json.dumps(fragment, indent=2))
        sys.exit(0)
hooks = settings.setdefault("hooks", {})
for event, groups in fragment.get("hooks", {}).items():
    current = hooks.setdefault(event, [])
    have = {h.get("command") for g in current for h in g.get("hooks", [])}
    for group in groups:
        if all(h.get("command") in have for h in group.get("hooks", [])):
            print(f"  skip (exists): {event} hook in .claude/settings.json")
            continue
        current.append(group)
        print(f"  merged: {event} hook into .claude/settings.json")
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")
PY
  echo "  next: read library/addons/$name/README.md in the kit"
}

[ $# -ge 1 ] || usage
if [ "$1" = "--list" ]; then list_library; exit 0; fi
case "$1" in -*) usage ;; esac

TARGET="$1"; shift
[ -d "$TARGET" ] || { echo "error: directory not found: $TARGET" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"
[ "$TARGET" != "$KIT_DIR" ] || { echo "error: target is the kit itself" >&2; exit 1; }

# --- add library agents and add-ons ---------------------------------------------
if [ "${1:-}" = "--add" ]; then
  shift
  [ $# -ge 1 ] || { list_library; exit 1; }
  for name in "$@"; do
    if [ -d "$KIT_DIR/library/addons/$name" ]; then
      add_addon "$name"
      continue
    fi
    src="$KIT_DIR/library/agents/$name.md"
    dest="$TARGET/.claude/agents/$name.md"
    if [ ! -f "$src" ]; then echo "  unknown agent or add-on: $name (see --list)"; continue; fi
    if [ -e "$dest" ]; then echo "  skip (exists): .claude/agents/$name.md"; continue; fi
    mkdir -p "$TARGET/.claude/agents"
    cp "$src" "$dest"
    echo "  added: .claude/agents/$name.md"
  done
  echo
  echo "Record these under 'Library additions' in docs/ai/MINIONS.md."
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
