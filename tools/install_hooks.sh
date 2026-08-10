#!/usr/bin/env bash
# tools/install_hooks.sh — install the imp19c pre-commit gate.
# Run once per clone (it is NOT auto-installed — git hooks are per-clone, not versioned).
#   bash tools/install_hooks.sh
# Installs a .git/hooks/pre-commit that runs tools/precommit_checks.py on the staged diff and
# blocks the commit on mechanical defects (brace imbalance, BOM/EOL churn, macro/# in LOG strings).
# Bypass a specific commit with `git commit --no-verify` (leaves a record).
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
HOOK="$REPO/.git/hooks/pre-commit"
cat > "$HOOK" <<'EOF'
#!/usr/bin/env bash
# imp19c pre-commit gate — calls the versioned checker. See tools/precommit_checks.py.
REPO="$(git rev-parse --show-toplevel)"
exec python3 "$REPO/tools/precommit_checks.py"
EOF
chmod +x "$HOOK"
echo "installed $HOOK -> tools/precommit_checks.py"
